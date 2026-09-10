import marshal, types, importlib.util as iu
from PyInstaller.archive.readers import ZlibArchiveReader
pyz_path = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\PYZ.pyz"
z = ZlibArchiveReader(pyz_path)
keys = list(z.toc.keys())
# find app-level / project modules (not third-party)
import re
thirdparty = {"flask","flask_socketio","eventlet","greenlet","engineio","socketio","werkzeug","jinja2","markupsafe","itsdangerous","click","limiter","flask_limiter","limits","certifi","charset_normalizer","requests","dns","idna","urllib3","setuptools","websockets","wrapt","dateutil","jwt","argon2","bcrypt","cryptography","OpenSSL","ruamel","yaml","PyInstaller","win32","pywin32","appdirs"}
proj = []
for k in keys:
    top = k.split(".")[0]
    base = k.split(".")[0].split("_")[0]
    if not k.startswith("_") and top not in thirdparty and not k.startswith(("flask","dns","eventlet","engineio","socketio","setuptools","win32")):
        proj.append(k)
proj.sort()
print("App-level-ish modules in PYZ (filtered):")
for p in proj:
    print("  ", p)
print("total filtered:", len(proj))
