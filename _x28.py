import os, sys, importlib.util, importlib.machinery, types
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
pyc_dir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
sys.path.insert(0, pyc_dir)
# Test sourceless import of 'app'
try:
    import app as appmod
    print("import app via sourceless: OK")
    print("has app attr:", hasattr(appmod,"app"), "has socketio:", hasattr(appmod,"socketio"))
    print("route count:", len(list(appmod.app.url_map.iter_rules())))
except Exception as e:
    import traceback; traceback.print_exc()
