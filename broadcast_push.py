"""broadcast_push.py — real RTMP push via portable ffmpeg.

The old /api/broadcast/* endpoints only flipped a "live" flag in
data/broadcast.json (simulated). This module manages a REAL ffmpeg
subprocess that pushes video to Facebook / YouTube RTMP:

* ffmpeg resolution order: tools/ffmpeg/ffmpeg.exe (portable, copyable to
  other PCs) -> imageio-ffmpeg wheel binary (.venv) -> system PATH.
* Never logs the full stream key (only last 4 chars).
* Thread-safe start/stop/status; log tail kept in data/broadcast_ffmpeg.log.

Source modes:
  device — DirectShow capture device (HDMI card / webcam) + optional audio
  mjpeg  — re-encode the local MJPEG feed (uses existing live_input pipeline)
  screen — gdigrab desktop capture (closest to "program tile" inc. overlays)
"""
import os
import re
import shutil
import subprocess
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PORTABLE_EXE = os.path.join(HERE, "tools", "ffmpeg", "ffmpeg.exe")
LOG_FILE = os.path.join(HERE, "data", "broadcast_ffmpeg.log")

_lock = threading.Lock()
_proc = None
_info = {"state": "idle", "started_at": None, "pgm": None,
         "mode": None, "target": None, "pid": None, "error": None}


def find_ffmpeg():
    """Return ffmpeg exe path or None (portable first)."""
    if os.path.isfile(PORTABLE_EXE):
        return PORTABLE_EXE
    try:
        import imageio_ffmpeg
        p = imageio_ffmpeg.get_ffmpeg_exe()
        if p and os.path.isfile(p):
            return p
    except Exception:
        pass
    return shutil.which("ffmpeg")


def _tail(s, n=4):
    s = s or ""
    return s[-n:] if len(s) >= n else ("*" * len(s))


def _write_log(line):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
            f.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), line))
    except OSError:
        pass


def _read_log_tail(n=30):
    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        return "".join(lines[-n:])
    except OSError:
        return ""


def list_dshow_devices(timeout=15):
    """Enumerate DirectShow devices via ffmpeg. Returns {video:[], audio:[]}."""
    ff = find_ffmpeg()
    if not ff:
        return {"video": [], "audio": [], "error": "ffmpeg not found"}
    try:
        p = subprocess.run(
            [ff, "-hide_banner", "-list_devices", "true",
             "-f", "dshow", "-i", "dummy"],
            capture_output=True, text=True, timeout=timeout,
            creationflags=0x08000000 if os.name == "nt" else 0)
        out = (p.stderr or "") + (p.stdout or "")
    except Exception as e:
        return {"video": [], "audio": [], "error": str(e)}
    video, audio, section = [], [], None
    for line in out.splitlines():
        if "DirectShow video devices" in line:
            section = "video"
        elif "DirectShow audio devices" in line:
            section = "audio"
        m = re.search(r'"([^"]+)"', line)
        if m and section in ("video", "audio") and "Alternative name" not in line:
            (video if section == "video" else audio).append(m.group(1))
    return {"video": video, "audio": audio}


def _build_cmd(ff, mode, src, rtmp_url, stream_key):
    target = rtmp_url.rstrip("/") + "/" + stream_key
    out = ["-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
           "-b:v", "2500k", "-maxrate", "2500k", "-bufsize", "5000k",
           "-pix_fmt", "yuv420p", "-g", "60",
           "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
           "-f", "flv", target]
    if mode == "device":
        cmd = [ff, "-hide_banner", "-loglevel", "warning",
               "-f", "dshow", "-i", "video=%s" % src["video"]]
        if src.get("audio"):
            cmd += ["-f", "dshow", "-i", "audio=%s" % src["audio"]]
        else:  # silent audio so FB/YT accept the stream
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
        return cmd + out, target
    if mode == "screen":
        cmd = [ff, "-hide_banner", "-loglevel", "warning",
               "-f", "gdigrab", "-framerate", "30", "-i", "desktop",
               "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
        return cmd + out, target
    # mjpeg: re-encode local feed
    cmd = [ff, "-hide_banner", "-loglevel", "warning",
           "-f", "mjpeg", "-use_wallclock_as_timestamps", "1",
           "-i", src["mjpeg_url"],
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    return cmd + out, target


def start(mode, src, rtmp_url, stream_key, pgm=None):
    """Start pushing. Returns (ok, message)."""
    global _proc
    with _lock:
        if _proc is not None and _proc.poll() is None:
            return False, "already live (pid %s)" % _proc.pid
        _proc = None
        ff = find_ffmpeg()
        if not ff:
            _info.update(state="error",
                         error="ffmpeg not found — wait for download or copy tools/ffmpeg/ffmpeg.exe")
            return False, _info["error"]
        if not rtmp_url or not stream_key:
            _info.update(state="error", error="RTMP URL / stream key missing")
            return False, _info["error"]
        try:
            cmd, target = _build_cmd(ff, mode, src, rtmp_url, stream_key)
        except Exception as e:
            _info.update(state="error", error="bad source: %s" % e)
            return False, _info["error"]
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            lf = open(LOG_FILE, "a", encoding="utf-8", errors="replace")
            _proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=lf,
                creationflags=0x08000000 if os.name == "nt" else 0)
        except Exception as e:
            _proc = None
            _info.update(state="error", error="cannot launch ffmpeg: %s" % e)
            return False, _info["error"]
        _write_log("START mode=%s pgm=%s target=...%s pid=%s"
                   % (mode, pgm, _tail(stream_key), _proc.pid))
        _info.update(state="live", started_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                     pgm=pgm, mode=mode, pid=_proc.pid, error=None,
                     target="(hidden key ...%s)" % _tail(stream_key))
        return True, "pushing (pid %s)" % _proc.pid


def stop():
    """Stop pushing. Returns (ok, message)."""
    global _proc
    with _lock:
        p, _proc = _proc, None
        if p is None or p.poll() is not None:
            _info.update(state="idle", started_at=None, pid=None)
            return True, "already stopped"
        try:
            p.terminate()
            try:
                p.wait(timeout=8)
            except subprocess.TimeoutExpired:
                p.kill()
        except Exception as e:
            _info.update(state="error", error="stop failed: %s" % e)
            return False, _info["error"]
        _write_log("STOP pid=%s" % p.pid)
        _info.update(state="idle", started_at=None, pid=None)
        return True, "stopped"


def status():
    """Real status: live only while ffmpeg is actually running."""
    global _proc
    with _lock:
        if _proc is not None and _proc.poll() is not None:
            rc = _proc.poll()
            _write_log("EXIT rc=%s pid=%s" % (rc, _proc.pid))
            _proc = None
            _info.update(state="error", started_at=None, pid=None,
                         error="ffmpeg exited (rc=%s) — check log" % rc)
        return dict(_info, ffmpeg=bool(find_ffmpeg()),
                    log_tail=_read_log_tail())
