import os
exa = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig"
# app.version
p = os.path.join(exa, "app.version")
print("=== app.version ===")
print(open(p, "rb").read().decode("utf-8", "replace"))
# server_entry - compiled code?
p2 = os.path.join(exa, "server_entry")
data = open(p2, "rb").read()
print("=== server_entry first 200 bytes ===")
print(data[:200])
