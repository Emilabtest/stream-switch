import os, sys, dis
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
sys.path.insert(0, r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc")
import timer as tm
import rolemap
# find Timer class
for name in dir(tm):
    o = getattr(tm, name)
    if isinstance(o, type):
        print("TIMER CLASS:", name)
        for m in dir(o):
            if m in ("timer_state","remaining","in_overtime"):
                fn = getattr(o, m)
                print("--", name, m, "varnames:", fn.__code__.co_varnames, "names:", fn.__code__.co_names, "consts:", fn.__code__.co_consts)
