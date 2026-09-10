import re
d = open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_decompiled.py", encoding="utf-8", errors="replace").read()
# route strings present in decompiled output
routes = set(re.findall(r"'(/[^']*)'", d))
api_routes = sorted(r for r in routes if r.startswith("/api/"))
print("=== API routes found in decompiled source ===")
print(len(api_routes))
for r in api_routes: print("  ", r)
print("=== bare 'def ' count ===", len(re.findall(r"^\s*def\s+", d, re.M)))
print("=== mangled 'def x( = app.route' count ===", len(re.findall(r"def [^)]*\= app\.route", d)))
print("=== 'Something TERRIBLE' present ===", "TERRIBLE" in d)
print("=== suspicious markers in source ===")
for mk in ["END_FOR","LOAD_FAST","Unsupported","<error>","???","# (unknown)"]:
    print("  ", mk, d.count(mk))
