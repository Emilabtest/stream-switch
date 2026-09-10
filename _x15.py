import ast
p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_decompiled.py"
data = open(p, encoding="utf-8", errors="replace").read()
out=[]
out.append("chars: %d"%len(data))
try:
    tree = ast.parse(data)
    funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    out.append("PARSE OK. funcs: %d"%len(funcs))
    if len(funcs)<250: out.append(str(sorted(funcs)))
except SyntaxError as e:
    out.append("SYNTAX ERROR line %s: %s"%(e.lineno, e.msg))
    lines=data.splitlines()
    ln = e.lineno
    if ln is not None:
        for i in range(max(0,ln-3), min(len(lines),ln+2)):
            out.append("%d: %s"%(i+1, lines[i]))
open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\ast_report.txt","w",encoding="utf-8").write("\n".join(out))
print("written")
