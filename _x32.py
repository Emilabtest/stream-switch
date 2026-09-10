import os
rb = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\recovery_build"
modules = ["app","roles","updater","licensing","media_manager","order_of_service","projection","jsonio","hymnal","timer","version","cloud_agent"]
for m in modules:
    # remove pymod (keep as data fallback) and create .py wrappers
    wrapper = os.path.join(rb, m + ".py")
    with open(wrapper, "w", encoding="utf-8") as f:
        f.write("import os as _os, sys as _sys, importlib.util as _iu\n")
        f.write("_here = _os.path.dirname(_os.path.abspath(__file__))\n")
        f.write("_pyc = _os.path.join(_here, 'pymod', %r)\n" % (m + ".pyc"))
        f.write("_spec = _iu.spec_from_file_location(%r, _pyc)\n" % m)
        f.write("_mod = _iu.module_from_spec(_spec)\n")
        f.write("_sys.modules[%r] = _mod\n" % m)
        f.write("_spec.loader.exec_module(_mod)\n")
    print("wrote wrapper:", m + ".py")
print("done")
