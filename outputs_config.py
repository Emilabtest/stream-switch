"""outputs_config.py — 6-output mapping for 3rd Project (additive).

4× HDMI — user assignable to any of: program, ch1..ch10
USB     — fixed to program, direct via USB cable (no IP, direct display)
Network — fixed to program, reachable via LAN IP http://<server-ip>:5890/program

Storage: data/outputs.json
{
  "hdmi": {"1": "program", "2": "ch1", "3": "ch2", "4": "ch3"},
  "usb": "program",
  "network": "program"
}
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "data", "outputs.json")
VALID_TARGETS = tuple(["program"] + ["ch%d" % i for i in range(1, 11)])
DEFAULTS = {
    "hdmi": {"1": "program", "2": "ch1", "3": "ch2", "4": "ch3"},
    "usb": "program",
    "network": "program",
}

def _load():
    try:
        if os.path.isfile(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                hdmi = data.get("hdmi", {})
                if isinstance(hdmi, dict):
                    out = dict(DEFAULTS)
                    out["hdmi"] = dict(DEFAULTS["hdmi"])
                    for k in ("1", "2", "3", "4"):
                        v = str(hdmi.get(k, "") or "").strip().lower()
                        if v in VALID_TARGETS:
                            out["hdmi"][k] = v
                    return out
    except Exception:
        pass
    return dict(hdmi=dict(DEFAULTS["hdmi"]), usb="program", network="program")

def _save(data):
    from jsonio import atomic_write_json
    atomic_write_json(FILE, data)

def init_app(app):
    from flask import jsonify, request
    try:
        from app import operator_required
    except Exception:
        from flask import session as _sess
        from functools import wraps
        def operator_required(f):
            @wraps(f)
            def _w(*a, **kw):
                if not _sess.get("operator"):
                    return jsonify({"ok": False}), 401
                return f(*a, **kw)
            return _w

    @app.route("/api/outputs", methods=["GET"])
    @operator_required
    def _get():
        c = _load()
        # server IP for network output
        ip = "127.0.0.1"
        try:
            import socket as _sock
            s = _sock.socket(_sock.AF_INET, _sock.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            pass
        port = int(os.environ.get("LEITURGIA_PORT", "5890"))
        base = "http://%s:%d" % (ip, port)
        return jsonify(
            hdmi=c["hdmi"],
            usb=c["usb"],
            network=c["network"],
            valid_targets=list(VALID_TARGETS),
            urls={
                "program": base + "/program",
                "ch1": base + "/ch1", "ch2": base + "/ch2",
                "ch3": base + "/ch3", "ch4": base + "/ch4",
                "usb_program": "USB direct — no IP (push program to USB display)",
                "network_program": base + "/program",
            },
            server_ip=ip, server_port=port,
        )

    @app.route("/api/outputs/hdmi", methods=["POST"])
    @operator_required
    def _post_hdmi():
        body = request.get_json(silent=True) or {}
        port = str(body.get("port", "") or "").strip()
        target = str(body.get("target", "") or "").strip().lower()
        if port not in ("1", "2", "3", "4"):
            return jsonify({"ok": False, "message": "port must be 1-4"}), 400
        if target not in VALID_TARGETS:
            return jsonify({"ok": False, "message": "target must be program or ch1-10"}), 400
        c = _load()
        c["hdmi"][port] = target
        _save(c)
        return jsonify({"ok": True, "hdmi": c["hdmi"]})

    # USB-to-USB program (no IP) — direct COM serial MJPEG
    @app.route("/api/usb/ports", methods=["GET"])
    @operator_required
    def _usb_ports():
        import usb_program
        return jsonify(usb_program.list_ports())

    @app.route("/api/usb/program/status", methods=["GET"])
    @operator_required
    def _usb_status():
        import usb_program
        return jsonify(usb_program.status())

    @app.route("/api/usb/program/start", methods=["POST"])
    @operator_required
    def _usb_start():
        import usb_program
        body = request.get_json(silent=True) or {}
        port = str(body.get("port", "") or "").strip()
        ok, msg = usb_program.start(port)
        return jsonify({"ok": ok, "message": msg}), (200 if ok else 400)

    @app.route("/api/usb/program/stop", methods=["POST"])
    @operator_required
    def _usb_stop():
        import usb_program
        ok, msg = usb_program.stop()
        return jsonify({"ok": ok, "message": msg})

    # Dedicated program endpoints for USB / Network (same content, distinct URLs for clarity)
    @app.route("/program", methods=["GET"])
    def _program():
        # Program is the active service item rendered on ch1's projection state,
        # but we expose it as a stable URL for USB/network clients.
        # Reuse the existing projection view without requiring operator auth.
        from flask import redirect
        return redirect("/ch1?output=1", code=302)

    # ── MACRO state: active macro overrides HDMI output ──────────────────────
    _macro_state = {"active": None}  # None or "1"-"10"

    @app.route("/api/macro/active", methods=["GET"])
    @operator_required
    def _macro_get():
        return jsonify(active=_macro_state["active"])

    @app.route("/api/macro/set", methods=["POST"])
    @operator_required
    def _macro_set():
        body = request.get_json(silent=True) or {}
        ch = str(body.get("channel", "") or "").strip()
        if ch and ch not in [str(i) for i in range(1, 11)]:
            return jsonify({"ok": False, "message": "channel must be 1-10"}), 400
        _macro_state["active"] = ch or None
        return jsonify({"ok": True, "active": _macro_state["active"]})

    # Keep devices / output push wiring if available — try to import screen_config
    try:
        import screen_config_routes
        screen_config_routes.init_app(app)
    except Exception:
        pass
