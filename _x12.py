import os, marshal, types, importlib.util as iu
from PyInstaller.archive.readers import ZlibArchiveReader
pyz_path = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\PYZ.pyz"
outdir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
os.makedirs(outdir, exist_ok=True)
z = ZlibArchiveReader(pyz_path)
targets = ["app","cloud_agent","hymnal","jsonio","licensing","media_manager","order_of_service","projection","roles","timer","updater","version"]
magic = iu.MAGIC_NUMBER
hdr = (magic + b"\x00"*4 + b"\x00"*4 + b"\x00"*4 + b"\x00"*4)[:16]
for name in targets:
    try:
        obj = z.extract(name)
        if isinstance(obj, types.CodeType):
            data = hdr + marshal.dumps(obj)
            fn = os.path.join(outdir, name + ".pyc")
            with open(fn, "wb") as f:
                f.write(data)
            print("saved", name, ".pyc", len(data))
        else:
            print("NOT code:", name, type(obj))
    except Exception as e:
        print("FAIL", name, repr(e))
print("done")
