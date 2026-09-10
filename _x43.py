import os, sys, dis
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
sys.path.insert(0, r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc")
import timer as tm
st = tm.TimerState
# dump the mangled timer_state property full
import inspect
# reconstruct via dis on the code object stored as TimerState.timer_state
prop = st.timer_state
print("=== timer_state dis ===")
dis.dis(prop)
print("varnames:", prop.__code__.co_varnames)
print("names:", prop.__code__.co_names)
print("consts:", prop.__code__.co_consts)
