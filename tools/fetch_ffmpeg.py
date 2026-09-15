"""fetch_ffmpeg.py — fetch portable ffmpeg for this project (run once per PC).

Prefers the small PyPI wheel (imageio-ffmpeg, ~30MB); falls back to the
full gyan.dev essentials zip (~70MB). Result: tools/ffmpeg/ffmpeg.exe,
which broadcast_push.py prefers over any system install.

Usage:  .venv\\Scripts\\python.exe tools\\fetch_ffmpeg.py
"""
import os
import subprocess
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_DIR = os.path.join(HERE, "tools", "ffmpeg")
DEST_EXE = os.path.join(DEST_DIR, "ffmpeg.exe")
GYAN_ZIP = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def via_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
        import imageio_ffmpeg
        src = imageio_ffmpeg.get_ffmpeg_exe()
        os.makedirs(DEST_DIR, exist_ok=True)
        with open(src, "rb") as f, open(DEST_EXE, "wb") as o:
            o.write(f.read())
        return True
    except Exception as e:
        print("pip path failed:", e)
        return False


def via_zip():
    import tempfile
    zf = os.path.join(tempfile.gettempdir(), "ffmpeg-ess.zip")
    print("downloading", GYAN_ZIP)
    urllib.request.urlretrieve(GYAN_ZIP, zf)
    with zipfile.ZipFile(zf) as z:
        for n in z.namelist():
            if n.endswith("/bin/ffmpeg.exe"):
                os.makedirs(DEST_DIR, exist_ok=True)
                with z.open(n) as f, open(DEST_EXE, "wb") as o:
                    o.write(f.read())
                return True
    return False


if __name__ == "__main__":
    if os.path.isfile(DEST_EXE):
        print("already present:", DEST_EXE)
    elif via_pip() or via_zip():
        print("ok:", DEST_EXE)
    else:
        sys.exit("FAILED to fetch ffmpeg")
