import re
# dump the mangled regions with generous context for each problem file
files = {
 "app.py": (875, 888),
 "cloud_agent.py": (30, 48),
 "hymnal.py": (36, 55),
 "order_of_service.py": (50, 70),
 "roles.py": (95, 115),
 "timer.py": (55, 72),
 "updater.py": (100, 115),
}
out = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\recovered_src"
for fn,(a,b) in files.items():
    lines = open(out+"\\"+fn, encoding="utf-8").read().splitlines()
    print("========", fn, "========")
    for i in range(a-1, min(b,len(lines))):
        print("%4d| %s"%(i+1, lines[i]))
    print()
