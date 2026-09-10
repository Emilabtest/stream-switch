import sys, os, importlib.util
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
pyc = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app.pyc"
spec = importlib.util.spec_from_file_location("app", pyc)
m = importlib.util.module_from_spec(spec)
sys.modules["app"] = m
try:
    spec.loader.exec_module(m)
except SystemExit:
    pass
if hasattr(m, "app"):
    from flask import Flask
    app = m.app
    print("=== app loaded OK ===")
    print("routes:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if any(k in rule.rule for k in ["screen","channel","monitor","projection","aspect","update","theme"]):
            print(sorted(rule.methods), rule.rule)
else:
    print("no app attr; module attrs sample:", [a for a in dir(m) if not a.startswith("__")][:20])
