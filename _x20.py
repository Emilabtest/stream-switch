import ast, re
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_rapid.py"
data = open(p,"rb").read().decode("utf-16le")
out=[]
out.append("decoded len: %d"%len(data))
try:
    tree=ast.parse(data)
    funcs=[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]
    out.append("PARSE OK. funcs=%d"%len(funcs))
    out.append("FUNCS: "+str(sorted(funcs)[:120]))
except SyntaxError as e:
    out.append("SYNTAX ERROR line %s: %s"%(e.lineno,e.msg))
    lines=data.splitlines()
    ln=e.lineno
    if ln is not None:
        for i in range(max(0,ln-4),min(len(lines),ln+3)):
            out.append("%d: %s"%(i+1,lines[i]))
routes=sorted(set(re.findall(r"['\"](/(?:api|media|login|logout|ch|remote|settings)[^'\"]*)['\"]", data)))
out.append("ROUTES (%d):"%len(routes)); out.extend(routes)
open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\rapid_report3.txt","w",encoding="utf-8").write("\n".join(out))
# save clean utf-8 version
open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_rapid.py","w",encoding="utf-8").write(data) if False else None
print("done")
