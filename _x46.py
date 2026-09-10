import os, sys
# do a lightweight check: can the Analysis find app via SourcelessFileLoader through pathex?
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\recovery_build\pymod")
try:
    import app as appmod
    print("app importable via pymod on path: YES, routes:", len(list(appmod.app.url_map.iter_rules())))
except Exception as e:
    print("FAIL", e)
