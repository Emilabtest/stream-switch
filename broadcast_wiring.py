"""broadcast_wiring.py — wire REAL RTMP push onto the running app (additive).

The production server boots from ``pymod/app.pyc`` (frozen), so edits to
``app.py`` alone have no runtime effect. Following the established pattern
(live_input.init_app / bible.init_app / server_version.init_app), this module
is imported from server_entry.py AFTER ``from app import app`` and:

* overrides the 5 simulated broadcast view functions with real ones backed
  by broadcast_push (ffmpeg subprocess),
* adds GET /api/broadcast/devices and POST /api/broadcast/pgm.

``app.pyc`` stays untouched.
"""
import json
import os
import re
import time

import broadcast_push
from jsonio import atomic_write_json

HERE = os.path.dirname(os.path.abspath(__file__))
BROADCAST_FILE = os.path.join(HERE, "data", "broadcast.json")
DEFAULTS = {
    "destination": "facebook",
    "rtmp_url": "",
    "stream_key": "",
    "title": "Saturday Worship Service",
    "state": "idle",
    "started_at": None,
    "pgm_channel": "ch1",
    "source_mode": "screen",
    "video_device": "",
    "audio_device": "",
    "mjpeg_url": "",
}


def _load():
    try:
        if os.path.isfile(BROADCAST_FILE):
            with open(BROADCAST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                merged = dict(DEFAULTS)
                merged.update(data)
                return merged
    except Exception:
        pass
    return dict(DEFAULTS)


def _save(data):
    atomic_write_json(BROADCAST_FILE, data)


def init_app(app):
    """Override simulated broadcast endpoints with real ffmpeg-backed ones."""
    from flask import jsonify, request

    try:
        from app import operator_required
    except Exception:  # fallback: plain session check
        from flask import session as _session

        def operator_required(f):
            from functools import wraps

            @wraps(f)
            def _w(*a, **kw):
                if not _session.get("operator"):
                    return jsonify({"ok": False, "message": "Unauthorized"}), 401
                return f(*a, **kw)

            return _w

    @operator_required
    def _cfg_get():
        c = _load()
        return jsonify({
            "destination": c["destination"],
            "rtmp_url": c["rtmp_url"],
            "title": c["title"],
            "pgm_channel": c.get("pgm_channel", "ch1"),
            "source_mode": c.get("source_mode", "device"),
            "video_device": c.get("video_device", ""),
            "audio_device": c.get("audio_device", ""),
            "mjpeg_url": c.get("mjpeg_url", ""),
            "stream_key_set": bool(c["stream_key"]),
            "key_tail": (c["stream_key"][-4:] if c["stream_key"] else ""),
        })

    @operator_required
    def _cfg_save():
        body = request.get_json(silent=True) or {}
        c = _load()
        if body.get("destination") in ("facebook", "youtube"):
            c["destination"] = body["destination"]
        for k in ("rtmp_url", "stream_key", "title", "video_device",
                  "audio_device", "mjpeg_url"):
            if isinstance(body.get(k), str):
                c[k] = body[k].strip()
        if body.get("source_mode") in ("device", "mjpeg", "screen"):
            c["source_mode"] = body["source_mode"]
        if isinstance(body.get("pgm_channel"), str) and re.match(r"^ch\d+$", body["pgm_channel"]):
            c["pgm_channel"] = body["pgm_channel"]
        _save(c)
        return jsonify({"ok": True})

    @operator_required
    def _start():
        c = _load()
        mode = c.get("source_mode", "device")
        if mode == "mjpeg":
            src = {"mjpeg_url": c.get("mjpeg_url") or
                   "http://127.0.0.1:%d/live/feed/0.mjpeg"
                   % int(os.environ.get("LEITURGIA_STREAM_PORT", "5002"))}
        else:
            src = {"video": c.get("video_device", ""),
                   "audio": c.get("audio_device", "")}
        ok, msg = broadcast_push.start(mode, src, c.get("rtmp_url", ""),
                                       c.get("stream_key", ""),
                                       pgm=c.get("pgm_channel", "ch1"))
        if not ok:
            c["state"] = "error"
            _save(c)
            return jsonify({"ok": False, "state": "error", "message": msg}), 400
        c["state"] = "live"
        c["started_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        _save(c)
        return jsonify({"ok": True, "state": "live", "message": msg})

    @operator_required
    def _stop():
        c = _load()
        ok, msg = broadcast_push.stop()
        c["state"] = "idle"
        c["started_at"] = None
        _save(c)
        return jsonify({"ok": ok, "state": "idle", "message": msg})

    @operator_required
    def _status():
        c = _load()
        real = broadcast_push.status()
        state = real.get("state", "idle")
        shown = c.get("state", "idle")
        if state == "live":
            shown = "live"
            c["state"] = "live"
        elif state == "error":
            shown = "error"
            c["state"] = "error"
        return jsonify({
            "state": shown,
            "destination": c["destination"],
            "started_at": c["started_at"],
            "pgm_channel": c.get("pgm_channel", "ch1"),
            "source_mode": c.get("source_mode", "device"),
            "ffmpeg": real.get("ffmpeg", False),
            "simulated": False,
            "message": real.get("error"),
            "log_tail": real.get("log_tail", ""),
        })

    @operator_required
    def _pgm():
        body = request.get_json(silent=True) or {}
        ch = str(body.get("channel") or "")
        if not re.match(r"^ch\d+$", ch):
            return jsonify({"ok": False, "message": "bad channel"}), 400
        c = _load()
        c["pgm_channel"] = ch
        _save(c)
        return jsonify({"ok": True, "pgm_channel": ch})

    @operator_required
    def _devices():
        return jsonify(broadcast_push.list_dshow_devices())

    vf = app.view_functions
    if "api_broadcast_config" in vf:
        vf["api_broadcast_config"] = _cfg_get
    if "api_broadcast_config_save" in vf:
        vf["api_broadcast_config_save"] = _cfg_save
    if "api_broadcast_start" in vf:
        vf["api_broadcast_start"] = _start
    if "api_broadcast_stop" in vf:
        vf["api_broadcast_stop"] = _stop
    if "api_broadcast_status" in vf:
        vf["api_broadcast_status"] = _status

    app.add_url_rule("/api/broadcast/pgm", view_func=_pgm, methods=["POST"])
    app.add_url_rule("/api/broadcast/devices", view_func=_devices, methods=["GET"])
