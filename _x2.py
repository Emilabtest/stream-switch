import os
from PyInstaller.archive.readers import CArchiveReader
exe = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\LeiturgiaServer.original.exe"
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig"
os.makedirs(out, exist_ok=True)
a = CArchiveReader(exe)
n=0
for name, entry in a.toc.items():
    data = a.extract(name)
    rel = name.replace("\\", os.sep)
    dest = os.path.join(out, rel)
    d = os.path.dirname(dest)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    n += 1
print("CArchive extracted:", n, "entries")
