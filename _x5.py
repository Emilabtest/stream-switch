import os, marshal, struct, types, importlib.util as iu
from PyInstaller.archive.readers import ZlibArchiveReader
pyz_path = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\PYZ.pyz"
outdir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
os.makedirs(outdir, exist_ok=True)
z = ZlibArchiveReader(pyz_path)
keys = list(z.toc.keys())
magic = iu.MAGIC_NUMBER
hdr = (magic + b"\x00"*4 + b"\x00"*4 + b"\x00"*4 + b"\x00"*4)[:16]
targets = ["app", "roles", "updater", "licensing", "server_entry"]
found = 0
for name in keys:
    if name in targets:
        try:
            obj = z.extract(name)
            print("extract type for", name, "->", type(obj))
            if isinstance(obj, types.CodeType):
                data = hdr + marshal.dumps(obj)
                fn = os.path.join(outdir, name + ".pyc")
                with open(fn, "wb") as f:
                    f.write(data)
                print("  saved", fn, len(data), "bytes")
                found += 1
        except Exception as e:
            print("  fail", name, repr(e))
print("done found:", found)
