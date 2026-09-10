import ast, os, re
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\recovered_src"
lines = open(out+"\\app.py", encoding="utf-8").read().splitlines()
# Find all jammed lines: lines whose content has >=3 top-level statement appearers
# and marker comments
for i,ln in enumerate(lines,1):
    s=ln.strip()
    if not s or s.startswith("#"): continue
    # jammed indicator: 'Decompyle incomplete' or multiple '=' with keywords, or ')()()'
    suspicious = False
    if "Decompyle incomplete" in ln: suspicious=True
    if ln.strip().endswith(")()()"): suspicious=True
    if re.search(r"continue\w+ = |^\w+ = \w+ = ", ln): suspicious=True
    if suspicious or ln.count(")")>=4 and ln.count("(")>=2 and "jsonify" in ln:
        print("%4d| %s"%(i, ln[:110]))
