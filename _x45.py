import re, os, glob
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\recovered_src"
# mangled signature patterns seen from pycdc-rapid 3.12 failures:
#  - "Decompyle incomplete"
#  - ")()()"  (empty call chain artifact)
#  - jammed: identifier followed immediately by '=' splitting a lambda/expr
#  - 'continue<ident> = ' etc
pat = re.compile(r"Decompyle incomplete|\)\s*\(\s*\)\s*\(\s*\)\s*\(\s*\)|= \(lambda.*\)|\)\s*\(\s*\)\s*[A-Za-z_]|continue[a-zA-Z_] |\b\w+ = \w+ = ")
for f in sorted(glob.glob(os.path.join(out,"*.py"))):
    data = open(f, encoding="utf-8").read()
    # find count of 'Decompyle incomplete' markers
    inc = data.count("Decompyle incomplete")
    m2 = len(re.findall(r"\)\s*\(\s*\)\s*\(\s*\)\s*\(\s*\)", data))
    lamb = len(re.findall(r"= \(lambda", data))
    jam = len(re.findall(r"continue\w+ = |\b\w+ = \w+ = ", data))
    print("%-22s inc=%d emptycall=%d lambda=%d jam=%d" % (os.path.basename(f), inc, m2, lamb, jam))
