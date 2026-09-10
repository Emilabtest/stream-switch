import sys, importlib.util
import os
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
pyc = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app.pyc"
spec = importlib.util.spec_from_file_location("app", pyc)
m = importlib.util.module_from_spec(spec)
sys.modules["app"] = m
try: spec.loader.exec_module(m)
except SystemExit: pass
app = m.app
rules = sorted(app.url_map.iter_rules(), key=lambda r: r.rule)
print("=== TOTAL routes:", len(rules), "===")
seen=set()
for r in rules:
    if r.rule in seen: continue
    seen.add(r.rule)
    print(sorted(method for method in r.methods if method in ("GET","POST","PUT","DELETE","PATCH")), r.rule)
