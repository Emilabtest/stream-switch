from PyInstaller.archive.readers import CArchiveReader
org = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig\CArchive.toc"
# list extracted entries directory
import os
d = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig"
for root, dirs, files in os.walk(d):
    for f in files:
        rel = os.path.relpath(os.path.join(root,f), d)
        print("ENTRY:", rel)
