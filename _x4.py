import os, sys
from PyInstaller.archive.readers import CArchiveReader
exe = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\LeiturgiaServer.original.exe"
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig"
os.makedirs(out, exist_ok=True)
a = CArchiveReader(exe)
pyz_path = os.path.join(out, "PYZ.pyz")
with open(pyz_path, "wb") as f:
    f.write(a.extract("PYZ.pyz"))
print("PYZ saved:", os.path.getsize(pyz_path), "bytes")
# load with ZlibArchiveReader using the filename
from PyInstaller.archive.readers import ZlibArchiveReader
z = ZlibArchiveReader(pyz_path)
toc = z.toc
print("PYZ module count:", len(toc))
# show interesting modules
import fnmatch
pats = ["app*","*screen*","server*","roles*","updater*","licensing*"]
for name in toc.keys():
    for p in pats:
        if fnmatch.fnmatch(name, p):
            print("  MODULE:", name)
            break
