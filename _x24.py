import re
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_recovered.py"
data = open(p, encoding="utf-8").read()
lines = data.splitlines()
# 1) mangled route: 'def x(...) = app.route'
m = re.findall(r"def [^)]*\=\s*app\.route", data)
print("mangled-route defs:", len(m))
for x in m: print("   ", x[:100])
# 2) jammed statements (multiple def/if/for/return on one physical line that shouldn't be)
jammed = re.findall(r"[^\n]*\b(?:if|def|for|while)\s+[^\n]*\b(?:if|def|for|while)\s+[^\n]*", data)
print("jammed control-flow lines:", len(jammed))
for x in jammed[:20]: print("   >>", x[:110])
# 3) count def
print("def count:", len(re.findall(r"^\s*def\s+", data, re.M)))
# 4) 'Something TERRIBLE' or dropped
for mk in ["TERRIBLE","pass  # ","(???)","<unknown>","# (missing"]:
    print("marker", mk, "=", data.count(mk))
