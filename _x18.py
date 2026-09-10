import ast, re
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_rapid.py"
data = open(p, encoding="utf-8", errors="replace").read()
nulls = data.count("\x00")
clean = data.replace("\x00","")
open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_rapid_clean.py","w",encoding="utf-8").write(clean)
out=[]
out.append("nulls=%d clean_len=%d"%(nulls,len(clean)))
try:
    tree=ast.parse(clean)
    funcs=[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]
    out.append("PARSE OK. funcs=%d"%len(funcs))
    if len(funcs)<260: out.append("FUNCS: "+str(sorted(funcs)))
except SyntaxError as e:
    out.append("SYNTAX ERROR line %s: %s"%(e.lineno,e.msg))
routes=sorted(set(re.findall(r"['\"](/(?:api|media|login|logout|ch|remote|settings)[^'\"]*)['\"]", clean)))
out.append("ROUTES (%d):"%len(routes)); out.extend(routes)
open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\rapid_report2.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
