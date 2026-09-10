import sys, os, traceback

LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'boottest.log')

def log(m):
    try:
        with open(LOGFILE, 'a') as f:
            f.write(m + "\n")
        print(m, flush=True)
    except Exception:
        pass

log("boottest: python " + sys.version.split()[0])
log("boottest: frozen=" + str(getattr(sys, 'frozen', False)))

try:
    log("importing eventlet")
    import eventlet
    log("eventlet ok")
    log("monkey_patch")
    eventlet.monkey_patch()
    log("monkey_patch ok")
except Exception:
    log("FAIL at eventlet: " + traceback.format_exc())
    sys.exit(3)

try:
    log("importing app")
    from app import app, socketio
    log("app imported ok")
except Exception:
    log("FAIL at app: " + traceback.format_exc())
    sys.exit(4)

try:
    log("importing server_entry")
    import server_entry as se
    log("server_entry imported ok")
except Exception:
    try:
        import importlib.util
        spec = importlib.util.find_spec('server_entry')
        log("server_entry spec None? " + str(spec is None))
    except Exception as e:
        log("server_entry err2 " + repr(e))
    log("FAIL at server_entry: " + traceback.format_exc())
    sys.exit(5)

log("ALL OK")
