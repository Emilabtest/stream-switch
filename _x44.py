import os, sys, dis
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
sys.path.insert(0, r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc")
import timer as tm
st = tm.TimerState
prop = st.timer_state
fn = prop.fget
print("=== timer_state.fget dis ===")
dis.dis(fn)
print("varnames:", fn.__code__.co_varnames)
print("names:", fn.__code__.co_names)
print("consts:", fn.__code__.co_consts)
