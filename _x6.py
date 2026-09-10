import sys, importlib.util, os, types
pyc = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app.pyc"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    try:
        spec.loader.exec_module(m)
        return m
    except Exception as e:
        import traceback; traceback.print_exc()
        return None
m = load("app", pyc)
if m is not None and hasattr(m, "app"):
    app = m.app
    print("=== Flask routes ===")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if any(k in rule.rule for k in ["screen","channel","monitor","projection","aspect","output","theme","update"]):
            print(rule.methods, rule.rule)
    print("=== has SocketIO handlers 'aspect:update'? ===")
    print("router keys sample:", [k for k in dir(app) if 'socket' in k.lower()][:5])
else:
    print("app module failed to load fully")
