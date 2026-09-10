import sys, traceback
def log(m):
    print(m, flush=True)

log("step1 import eventlet")
import eventlet
eventlet.monkey_patch()
log("step1 ok")

log("step2 try import engineio.async_drivers.eventlet")
try:
    import importlib
    m = importlib.import_module('engineio.async_drivers.eventlet')
    log("step2 SUCCESS " + str(m))
except Exception:
    log("step2 FAILED:")
    traceback.print_exc()
    log("DONE-FAIL")
    sys.exit(1)
log("ALL OK")
