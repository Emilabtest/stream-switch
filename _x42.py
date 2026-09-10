import os, sys
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
sys.path.insert(0, r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc")
import timer as tm
for name in dir(tm):
    o = getattr(tm, name)
    if isinstance(o, type):
        print("TIMER CLASS:", name)
        for m in dir(o):
            if not m.startswith("__"):
                fn = getattr(o, m)
                if callable(fn):
                    print("  med:", m, "varnames:", fn.__code__.co_varnames, "names:", fn.__code__.co_names)
