"""app_launcher.py — Native window wrapper for LIGHT STREAM SWITCH APP.

Uses pywebview to display the Flask server in a native window
(no browser chrome, no address bar — looks like a real desktop app).

Usage:
  python app_launcher.py          # opens on port 5890
  python app_launcher.py 5891     # custom port
"""
import sys
import time
import threading
import subprocess
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5890
URL = f"http://127.0.0.1:{PORT}"

def start_server():
    """Start the Flask server in a subprocess."""
    bat = os.path.join(HERE, "run5890.bat")
    if PORT != 5890:
        subprocess.Popen(
            ["cmd", "/c", f"set LEITURGIA_PORT={PORT} && .venv\\Scripts\\python.exe -m pymod.app"],
            cwd=HERE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            ["cmd", "/c", bat],
            cwd=HERE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

def wait_for_server(url, timeout=30):
    """Wait until the Flask server is ready."""
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False

def main():
    import webview

    # Start Flask server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    print(f"Starting server on port {PORT}...")
    if not wait_for_server(URL):
        print("Server failed to start.")
        sys.exit(1)
    print("Server ready.")

    # Create native window
    window = webview.create_window(
        title="LIGHT STREAM SWITCH APP",
        url=URL,
        width=1400,
        height=900,
        min_size=(1024, 600),
        resizable=True,
        text_select=True,
    )

    # Start pywebview (blocks until window is closed)
    webview.start(debug=False)

if __name__ == "__main__":
    main()
