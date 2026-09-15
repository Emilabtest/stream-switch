"""usb_receiver.py — run on the OTHER PC to display USB program.

The main PC pushes program frames over a USB-to-USB bridge cable (virtual COM
port) as [4-byte length][JPEG]. This script reads that stream and shows it
in a window, or re-serves it as MJPEG on http://127.0.0.1:5009/usb/program.mjpeg
so any local app can use it as a "USB input".

Usage (other PC, needs pyserial, opencv-python):
  python usb_receiver.py COM4
  python usb_receiver.py --list
  python usb_receiver.py COM4 --serve  # also start MJPEG server on 5009
"""
import argparse
import struct
import sys
import threading

def list_ports():
    try:
        import serial.tools.list_ports as lp
        for p in lp.comports():
            print("%s  %s  %s" % (p.device, p.description, p.hwid))
    except Exception as e:
        print("list failed:", e)

def run_reader(port, serve=False):
    mjpeg_latest = [None]
    lock = threading.Lock()

    def mjpeg_server():
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        class H(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                if "usb/program" not in self.path:
                    self.send_error(404); return
                self.send_response(200)
                self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                last = None
                while True:
                    with lock:
                        data = mjpeg_latest[0]
                    if data and data != last:
                        last = data
                        self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + data + b"\r\n")
                        self.wfile.flush()
                    import time; time.sleep(0.06)
        ThreadingHTTPServer(("127.0.0.1", 5009), H).serve_forever()

    if serve:
        threading.Thread(target=mjpeg_server, daemon=True).start()
        print("Serving http://127.0.0.1:5009/usb/program.mjpeg")

    # Show via OpenCV window as well
    try:
        import serial, cv2, numpy as np
    except Exception as e:
        print("need pyserial opencv-python:", e); sys.exit(1)

    ser = serial.Serial(port, baudrate=1152000, timeout=2)
    print("Reading from", port)
    while True:
        hdr = ser.read(4)
        if len(hdr) < 4:
            continue
        n = struct.unpack(">I", hdr)[0]
        if n <= 0 or n > 10_000_000:
            continue
        data = b""
        while len(data) < n:
            chunk = ser.read(n - len(data))
            if not chunk:
                break
            data += chunk
        if len(data) != n:
            continue
        with lock:
            mjpeg_latest[0] = data
        # Show window
        arr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imshow("USB Program", img)
            if cv2.waitKey(1) == 27:
                break

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("port", nargs="?", help="COM port, e.g. COM4")
    ap.add_argument("--list", action="store_true", help="list ports")
    ap.add_argument("--serve", action="store_true", help="also serve MJPEG on 5009")
    args = ap.parse_args()
    if args.list:
        list_ports()
    elif not args.port:
        ap.print_help()
    else:
        run_reader(args.port, serve=args.serve)
