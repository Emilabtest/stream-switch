import os, marshal, types, zlib
from PyInstaller.archive.readers import CArchiveReader
from PyInstaller.archive.readers import ZlibArchiveReader
exe = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\LeiturgiaServer.original.exe"
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig"
os.makedirs(out, exist_ok=True)
a = CArchiveReader(exe)
pyz_data = a.extract("PYZ.pyz")
with open(os.path.join(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig", "PYZ.pyz"), "wb") as f:
    f.write(pyz_data)
z = ZlibArchiveReader(pyz_data)
# get toc
toc = z.toc
print("PYZ total modules:", len(toc))
# Dump code objects to .pyc files
import importlib.util as iu
pyver = (3,12)
out_ext = iu.MAGIC_NUMBER
hdr = out_ext + b"\x00"*4 + struct_pack(b"")
def struct_pack(dummy): from struct import pack; return b""
hdr = out_ext + b"\x00"*4
for name, (ispkg, offset, length) in toc.items():
    code = z.extract(name) if hasattr(z,'extract') else None
print("done toc iteration")
# Better: use _pyz_extract via marshal
