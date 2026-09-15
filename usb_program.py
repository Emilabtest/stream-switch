"""usb_program.py — USB-to-USB program output (no IP).

The "USB" output is fixed to program and goes out a direct USB cable to the
other PC. The other PC's application opens the same USB link as a data input
(virtual COM port) and sees our program frames as MJPEG.

Physical link: USB bridge / data-link cable (appears as COMx on both PCs) or
a USB-serial adapter pair. No network/IP is used.

Protocol (simple, no HTTP):
  [4-byte BE length][JPEG bytes]  repeated at ~ TARGET_FPS

Receiver on the other PC just reads the length, then the JPEG, and displays it.
A sample receiver is tools/usb_receiver.py (run on the other PC).

If no COM port exists (cable not plugged), enumerate returns [] and start
returns an error — no fallback to IP.
"""
import os
import struct
import threading
import time

TARGET_FPS = 15
JPEG_QUALITY = 80
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "usb_program.log")

_lock = threading.Lock()
_thread = None
_stop = threading.Event()
_info = {"state": "idle", "port": None, "started_at": None, "error": None, "frames": 0}

def _log(msg):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
            f.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), msg))
    except Exception:
        pass

def list_ports():
    """List USB/serial ports that could be the USB-to-USB link."""
    ports = []
    try:
        import serial.tools.list_ports as _lp
        for p in _lp.comports():
            # Keep everything that looks like a USB serial / bridge cable
            ports.append({"device": p.device, "description": p.description, "hwid": p.hwid})
    except Exception as e:
        return {"ports": [], "error": "pyserial not installed: %s" % e}
    # Prefer USB-tagged devices first, but return all
    usb = [p for p in ports if "USB" in (p["description"] or "") or "USB" in (p["hwid"] or "")]
    return {"ports": usb if usb else ports}

def _capture_jpeg():
    """Capture one program frame as JPEG bytes.
    Use screen capture (gdigrab via mss) as source for "program" —
    if no display is available, fall back to a tiny placeholder JPEG.
    """
    try:
        import mss, cv2, numpy as np
        with mss.mss() as sct:
            mon = sct.monitors[1]  # primary
            img = np.array(sct.grab(mon))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # Downscale for USB bandwidth
            h, w = img.shape[:2]
            scale = 720 / max(w, h) if max(w, h) > 720 else 1.0
            if scale < 1:
                img = cv2.resize(img, (int(w*scale), int(h*scale)))
            ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
            if ok:
                return buf.tobytes()
    except Exception:
        pass
    # Fallback: 1x1 JPEG placeholder
    try:
        import cv2, numpy as np
        img = np.zeros((240, 320, 3), dtype=np.uint8)
        cv2.putText(img, "PROGRAM", (70, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if ok:
            return buf.tobytes()
    except Exception:
        pass
    return None

def _writer(port_name):
    """Background thread: open COM port and push frames until stopped."""
    ser = None
    try:
        import serial
        ser = serial.Serial(port_name, baudrate=1152000, timeout=1, write_timeout=2)
        # Some bridge cables need DTR/RTS
        try:
            ser.dtr = True; ser.rts = True
        except Exception:
            pass
        _log("USB writer opened %s" % port_name)
    except Exception as e:
        with _lock:
            _info.update(state="error", error="open %s failed: %s" % (port_name, e))
        _log("open failed %s: %s" % (port_name, e))
        return
    period = 1.0 / max(1, TARGET_FPS)
    frames = 0
    while not _stop.is_set():
        t0 = time.time()
        jpg = _capture_jpeg()
        if jpg:
            try:
                ser.write(struct.pack(">I", len(jpg)))
                ser.write(jpg)
                frames += 1
                with _lock:
                    _info["frames"] = frames
            except Exception as e:
                with _lock:
                    _info.update(state="error", error="write failed: %s" % e)
                _log("write failed: %s" % e)
                break
        dt = time.time() - t0
        if dt < period:
            time.sleep(period - dt)
    try:
        ser.close()
    except Exception:
        pass
    _log("USB writer closed %s frames=%d" % (port_name, frames))

def start(port_name):
    global _thread
    with _lock:
        if _thread is not None and _thread.is_alive():
            return False, "already running on %s" % _info.get("port")
        if not port_name or not port_name.strip():
            return False, "no USB port selected"
        _stop.clear()
        _info.update(state="live", port=port_name.strip(), started_at=time.strftime("%Y-%m-%d %H:%M:%S"), error=None, frames=0)
        _thread = threading.Thread(target=_writer, args=(port_name.strip(),), daemon=True, name="usb-program")
        _thread.start()
        _log("START USB program on %s" % port_name)
        return True, "pushing program to %s" % port_name

def stop():
    global _thread
    with _lock:
        t = _thread
        if t is None or not t.is_alive():
            _info.update(state="idle", port=None, started_at=None, error=None)
            return True, "already stopped"
        _stop.set()
    try:
        t.join(timeout=5)
    except Exception:
        pass
    with _lock:
        _thread = None
        _info.update(state="idle", port=None, started_at=None, error=None)
    _log("STOP USB program")
    return True, "stopped"

def status():
    with _lock:
        t = _thread
        alive = t is not None and t.is_alive()
        if not alive and _info.get("state") == "live":
            _info["state"] = "error"
            if not _info.get("error"):
                _info["error"] = "writer died"
        return dict(_info, alive=alive)
