import sys
import ctypes
from ctypes import wintypes

pid = int(sys.argv[1])
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010


class UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ("Length", wintypes.USHORT),
        ("MaximumLength", wintypes.USHORT),
        ("Buffer", wintypes.LPVOID),
    ]


class RTL_USER_PROCESS_PARAMETERS(ctypes.Structure):
    _fields_ = [
        ("Reserved1", ctypes.c_byte * 16),
        ("Reserved2", ctypes.c_byte * 40),
        ("ImagePathName", UNICODE_STRING),
        ("CommandLine", UNICODE_STRING),
        ("Environment", UNICODE_STRING),
    ]


class PEB(ctypes.Structure):
    _fields_ = [
        ("Reserved1", ctypes.c_byte * 2),
        ("BeingDebugged", ctypes.c_byte),
        ("Reserved2", ctypes.c_byte * 1),
        ("Reserved3", ctypes.c_byte * 4),
        ("Ldr", ctypes.c_void_p),
        ("ProcessParameters", ctypes.c_void_p),
        ("Reserved4", ctypes.c_byte * 104),
        ("Reserved5", ctypes.c_void_p * 52),
        ("PostProcessInitRoutine", ctypes.c_void_p),
        ("Reserved6", ctypes.c_byte * 128),
        ("Reserved7", ctypes.c_void_p),
        ("SessionId", wintypes.ULONG),
    ]


class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("Reserved1", ctypes.c_void_p),
        ("PebBaseAddress", ctypes.c_void_p),
        ("Reserved2", ctypes.c_void_p * 2),
        ("UniqueProcessId", ctypes.c_void_p),
        ("Reserved3", ctypes.c_void_p),
    ]


PROCESS_BASIC_INFORMATION_SIZE = ctypes.sizeof(PROCESS_BASIC_INFORMATION)


def read_mem(h, addr, size):
    buf = ctypes.create_string_buffer(size)
    read = ctypes.c_size_t(0)
    if ctypes.windll.kernel32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, size, ctypes.byref(read)):
        return buf.raw
    return None


def read_mem_chunked(h, addr, size):
    out = bytearray()
    chunk = 0x1000
    pos = 0
    while pos < size:
        n = min(chunk, size - pos)
        data = read_mem(h, addr + pos, n)
        if data is None:
            break
        if b"\x00\x00" in data[: n - 1]:
            pass
        out.extend(data)
        pos += n
    return bytes(out)


def read_ustr(h, ustr):
    if not ustr.Buffer:
        return None
    data = read_mem(h, ustr.Buffer, ustr.Length)
    if data is None:
        return None
    return data.decode("utf-16-le", errors="replace")


h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
if not h:
    print("OpenProcess failed", ctypes.windll.kernel32.GetLastError())
    sys.exit(1)

pbi = PROCESS_BASIC_INFORMATION()
size = ctypes.c_ulong(0)
status = ctypes.windll.ntdll.NtQueryInformationProcess(
    h, 0, ctypes.byref(pbi), PROCESS_BASIC_INFORMATION_SIZE, ctypes.byref(size)
)
if status != 0:
    print("NtQuery failed", hex(status & 0xFFFFFFFF))
    sys.exit(1)

peb_data = read_mem(h, pbi.PebBaseAddress, ctypes.sizeof(PEB))
if not peb_data:
    print("read PEB failed")
    sys.exit(1)

peb = PEB.from_buffer_copy(peb_data)
ptr = peb.ProcessParameters
print("ProcessParameters ptr =", hex(ptr))
params_data = read_mem(h, ptr, ctypes.sizeof(RTL_USER_PROCESS_PARAMETERS))
if not params_data:
    print("read params failed")
    sys.exit(1)

params = RTL_USER_PROCESS_PARAMETERS.from_buffer_copy(params_data)
env_size = params.Environment.Length
print("Environment Length =", env_size, "Buffer =", hex(params.Environment.Buffer or 0))
env_data = read_mem_chunked(h, params.Environment.Buffer, env_size)
if env_data:
    envs = env_data.decode("utf-16-le", errors="replace").split("\x00")
    target = sys.argv[2] if len(sys.argv) > 2 else "_MEIPASS"
    found = False
    for e in envs:
        if e.startswith(target) or e.startswith("MEIPASS"):
            print(e)
            found = True
    if not found:
        print("(no matching env vars found; total env bytes=%d)" % env_size)
else:
    print("read env failed")