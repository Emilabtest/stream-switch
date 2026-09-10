p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_recovered.py"
lines = open(p, encoding="utf-8").read().splitlines()
# A jammed line = multiple top-level statements collapsed. Detect: line has >=3 '=' OR brackets balance weirdly, and is NOT a dict literal
import ast
bad=[]
for i,ln in enumerate(lines,1):
    s=ln.strip()
    if not s or s.startswith("#"): continue
    # heuristic: two keywords that signal jammed statements
    if re.search(r"(^|\s)(if|def|for|while|return|continue|break)\s+=|(=\s*)(if|for|while)\s", ln) and s.count("=")>=2:
        bad.append((i,jam("ctrl")))
    # too many '=' with no obvious list/dict
    eqs=s.count("=")-s.count("==")
    if eqs>=3:
        bad.append((i,"eqs=%d"%eqs))
    # consecutive statements with no newline:  '... }{' or '})if' ...
print("total lines:", len(lines))
print("suspicious:", len(bad))
for b in bad[:80]: print("  ", b)
