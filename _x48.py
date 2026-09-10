import os, sys
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
import logging; logging.disable(logging.WARNING)
repo = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\ecb-backup\leiturgia-windows"
sys.path.insert(0, os.path.join(repo, "pymod"))
import app as appmod
rules = list(appmod.app.url_map.iter_rules())
print("app loaded. routes:", len(rules))
for t in ["/api/channels","/api/output/monitors","/api/settings/projection"]:
    found = any(t == r.rule for r in rules)
    print("  endpoint %s: %s" % (t, "FOUND" if found else "MISSING"))
print("OK")
