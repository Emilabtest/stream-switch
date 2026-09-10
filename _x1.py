import os
from PyInstaller.archive.readers import CArchiveReader
exe = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\LeiturgiaServer.original.exe"
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig"
os.makedirs(out, exist_ok=True)
a = CArchiveReader(exe)
print("=== CArchive entries (names) ===")
toc = a.toc
for name in toc:
    print(name)
