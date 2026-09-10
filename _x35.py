import ast, os, glob
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\recovered_src"
for f in sorted(glob.glob(os.path.join(out,"*.py"))):
    name = os.path.basename(f)
    data = open(f, encoding="utf-8").read()
    # null bytes?
    if "\x00" in data:
        print("%s: HAS NULL BYTES (%d)" % (name, data.count("\x00")))
        # strip them and note
        data = data.replace("\x00","")
        open(f,"w",encoding="utf-8",newline="\n").write(data)
        print("   -> stripped nulls")
        try:
            ast.parse(data); print("   -> now OK after null strip")
        except SyntaxError as e:
            print("   -> still ERR line %s: %s"%(e.lineno, e.msg))
        continue
    try:
        ast.parse(data); print("%s: OK"%name)
    except SyntaxError as e:
        lines=data.splitlines()
        ln=e.lineno or 1
        print("%s: ERR line %s: %s"%(name,e.lineno,e.msg))
        for i in range(max(0,ln-3), min(len(lines),ln+2)):
            print("      %d| %s"%(i+1, lines[i]))
