import os, glob
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\recovered_src"
for f in glob.glob(os.path.join(out, "*.py")):
    data = open(f, encoding="utf-8", errors="replace").read()
    # strip BOM and leading whitespace/newlines from the very start
    data = data.lstrip("\ufeff")
    open(f, "w", encoding="utf-8", newline="\n").write(data)
print("stripped BOM from all")
