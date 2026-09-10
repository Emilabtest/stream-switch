import ast, re
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_rapid.py"
data = open(p, encoding="utf-8", errors="replace").read()
out=[]
try:
    tree=ast.parse(data)
    funcs=[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]
    out.append("PARSE OK. top-level funcs=%d"%len(funcs))
    if len(funcs)<250: out.append("FUNCS: "+str(sorted(funcs)))
except SyntaxError as e:
    out.append("SYNTAX ERROR line %s: %s"%(e.lineno,e.msg))
    lines=data.splitlines()
    ln=e.lineno
    if ln is not None:
        for i in range(max(0,ln-4),min(len(lines),ln+3)):
            out.append("%d: %s"%(i+1,lines[i]))
routes=sorted(set(re.findall(r"['\"](/(?:api|media|static|login|logout|ch|remote|settings)[^'\"]*)['\"]", data)))
out.append("ROUTE STRINGS (%d):"%len(routes))
out.extend(routes)
open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\rapid_report.txt","w",encoding="utf-8").write("\n".join(out))
print("done, wrote rapid_report.txt")
