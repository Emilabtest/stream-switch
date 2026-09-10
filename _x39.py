import os, sys, importlib.util, dis, types, marshal
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
pyc_dir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
sys.path.insert(0, pyc_dir)

def find_meth(modname, clsname, methname):
    m = importlib.import_module(modname)
    cls = getattr(m, clsname)
    meth = getattr(cls, methname)
    return meth

# roles.to_dict
try:
    meth = find_meth("roles","RoleManager","to_dict")
    print("======== roles.RoleManager.to_dict ========")
    print("varnames:", meth.__code__.co_varnames)
    print("names:", meth.__code__.co_names)
    print("consts:", meth.__code__.co_consts)
    dis.dis(meth)
except Exception as e:
    import traceback; traceback.print_exc()
