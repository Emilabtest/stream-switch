import os, sys, importlib.util, thread
# Simulate the production layout: pymod/ + server_entry logic
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
repo = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\ecb-backup\leiturgia-windows"
pymod = os.path.join(repo, "pymod")
sys.path.insert(0, pymod)
# load app sourceless
import app as appmod
print("app loaded. routes:", len(list(appmod.app.url_map.iter_rules())))
# confirm Screen Config API endpoints present
rules = {tuple(sorted(m for m in r.methods if m in ("GET","POST","DELETE"))): r.rule for r in appmod.app.url_map.iter_rules()}
targets = ["/api/channels","/api/output/monitors","/api/settings/projection"]
for t in targets:
    found = any(t == r.rule for r in appmod.app.url_map.iter_rules())
    print("  endpoint %s: %s" % (t, "FOUND" if found else "MISSING"))
print("ALL DEPENDENCIES LOADED OK")
