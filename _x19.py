p = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\app_rapid.py"
data = open(p,"rb").read()
print("total bytes:", len(data))
print("first 40 bytes:", data[:40])
# check utf-16le BOM
print("BOM utf16le:", data[:2] == b"\xff\xfe")
# check if null at every other byte (ascii utf16le)
sample = data[:40]
ascii_run = all(data[i]==0 for i in range(1,40,2))
print("null at odd positions (utf16le ascii):", ascii_run)
