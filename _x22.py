p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_recovered.py"
lines = open(p, encoding="utf-8").read().splitlines()
# Mangled detection: multiple statements jammed without newline, or 'def' inside def line
import re
mangled = []
for i,ln in enumerate(lines,1):
    # contains no space after keyword like 'continu = ' or 'enumerate' jams
    if re.search(r"[a-zA-Z0-9_\]]\s=\s[a-zA-Z_].*?[a-z][a-z]=\s", ln):
        mangled.append((i, "assign-jam"))
    if ln.count("def ") > 1:
        mangled.append((i, "multi-def"))
    if "u = " in ln and ln.count(" = ") > 2:
        mangled.append((i, "multi-assign"))
print("lines:", len(lines))
print("mangled-ish lines:", len(mangled))
for m in mangled[:60]:
    print("  ", m)
