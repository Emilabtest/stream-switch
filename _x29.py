import os, sys
os.chdir(r"C:\Users\LIFE HOPE CENTER\Documents\Default Project\Leiturgia")
pyc_dir = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc"
sys.path.insert(0, pyc_dir)
# reduce noise
import logging; logging.disable(logging.WARNING)
try:
    import app as appmod
    print("app import OK; routes:", len(list(appmod.app.url_map.iter_rules())))
    # exercise key internal modules
    import roles, updater, licensing, media_manager, order_of_service, projection, jsonio, hymnal, timer, version, cloud_agent
    print("all project modules import OK")
except Exception as e:
    import traceback; traceback.print_exc()
