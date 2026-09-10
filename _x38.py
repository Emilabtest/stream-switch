import os, sys, importlib.util, dis, types
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
sys.path.insert(0, os.path.dirname(__file__))
pyc_dir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
sys.path.insert(0, pyc_dir)
import logging; logging.disable(logging.WARNING)
import roles as roles_mod
# find the RoleMap class
cls = None
for name in dir(roles_mod):
    obj = getattr(roles_mod, name)
    if isinstance(obj, type):
        print("CLASS:", name)
# find to_dict method
for name in dir(roles_mod):
    obj = getattr(roles_mod, name)
    if isinstance(obj, type):
        for mname in dir(obj):
            if mname == "to_dict":
                meth = getattr(obj, mname)
                print("=== to_dict disassembly ===")
                print("source follows; showing dis of code constants")
                print("argcount:", meth.__code__.co_argcount, "varnames:", meth.__code__.co_varnames, "names:", meth.__code__.co_names)
# also dump constant tuple (compiled source line info sometimes present)
