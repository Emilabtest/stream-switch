import re
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_recovered.py"
data = open(p, encoding="utf-8").read()
lines = data.splitlines()
# Find the jammed lines and print with surrounding 1 line context
jammed_ids=[]
for i,ln in enumerate(lines,1):
    s=ln.strip()
    if re.match(r"^(resp\['title'\]|socketio\.emit|'message': 'Invalid|update/start|_media_budget|filename|return jsonify|safe_names)", ln):
        continue
# Simpler: print lines that look jammed (contain a closing after opening at same indent level)
# We'll just dump lines 870-890 and a few known ones
rng = list(range(869,895)) + list(range(0,0))
for i in rng:
    if 0 < i <= len(lines):
        print("%4d| %s"%(i, lines[i-1]))
