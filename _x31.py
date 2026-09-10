import os, sys
sys.argv = ["probe"]
# Simulate: put pymod on path, does importlib find app.pyc as a module via pathex?
import importlib.util, importlib.machinery
pymod = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\leiturgia-work\recovery_build\pymod"
finder = importlib.machinery.PathFinder.find_spec("app", [pymod])
print("PathFinder.find_spec('app', [pymod]):", finder)
print("loader type:", type(finder.loader).__name__ if finder else None)
