import sys, traceback
def log(m):
    print(m, flush=True)
log("import eventlet")
import eventlet
eventlet.monkey_patch()
log("monkey_patch ok")
log("try from app import app, socketio")
try:
    from app import app, socketio
    log("app import OK")
except Exception:
    log("FAILED:")
    traceback.print_exc()
    log("ALLDONE")
    sys.exit(1)
log("ALLDONE-OK")
