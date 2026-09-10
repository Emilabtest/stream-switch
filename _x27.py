import re, ast
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_recovered.py"
data = open(p, encoding="utf-8").read()
# top-level and any import lines
imports = sorted(set(re.findall(r"^(?:from|import)\s+([A-Za-z_][\w.]*)", data, re.M)))
print("=== import roots ===")
for im in imports: print("  ", im)
