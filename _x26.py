import marshal, types, importlib.util as iu, os
# server_entry from CArchive (raw marshal bytes)
data = open(r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\extract_orig\server_entry","rb").read()
try:
    code = marshal.loads(data)
    print("server_entry code OK, type:", type(code))
    # save as proper .pyc
    magic = iu.MAGIC_NUMBER
    hdr = (magic + b"\x00"*4 + b"\x00"*4 + b"\x00"*4 + b"\x00"*4)[:16]
    outf = r"C:\Users\LIFE HOPE CENTER\AppData\Local\Temp\opencode\pyz_orig\pyc\server_entry.pyc"
    open(outf,"wb").write(hdr + data)
    print("saved server_entry.pyc", os.path.getsize(outf))
except Exception as e:
    print("marshal fail:", e)
