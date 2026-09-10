# Test: uses a .py wrapper that loads a .pyc from same dir, replicating PyInstaller's compile step
import os, sys, importlib.util, importlib.machinery, types, subprocess, textwrap, tempfile

# Build a test package dir: wrapper app.py + app.pyc, roles.pyc, updater.pyc, etc
testdir = tempfile.mkdtemp()
pymod = os.path.join(testdir, "pymod")
os.makedirs(pymod)
src_dir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
for m in ["app","roles","updater","licensing","media_manager","order_of_service","projection","jsonio","hymnal","timer","version","cloud_agent"]:
    shutil = __import__("shutil")
    shutil.copy(os.path.join(src_dir, m+".pyc"), os.path.join(pymod, m+".pyc"))

# Write a loader that registers pymod on path and imports app
py_path = os.path.join(testdir, "__load__.py")
with open(py_path, "w") as f:
    f.write(textwrap.dedent('''
        import os, sys
        _base = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(_base, "pymod"))
        from app import app, socketio
        print("LOADED routes:", len(list(app.url_map.iter_rules())))
        print("socketio:", type(socketio).__name__)
    '''))
sys.path.insert(0, testdir)
import __load__   # runs the loader
print("OK: wrapper-based sourceless import works")
