from PyInstaller.archive.readers import ZlibArchiveReader
import os
pyz_path = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\PYZ.pyz"
z = ZlibArchiveReader(pyz_path)
keys = set(z.toc.keys())
workdir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work"
proj = []
for f in os.listdir(workdir):
    if f.endswith(".py") and not f.startswith("_"):
        proj.append(f[:-3])
proj += ["app", "server_entry"]
proj = sorted(set(proj))
print("Project modules in PYZ toc:")
for p in proj:
    status = "IN PYZ" if p in keys else "NOT in PYZ"
    print(f"  {p:22s} {status}")
