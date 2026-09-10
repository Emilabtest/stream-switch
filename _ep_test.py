import sys
print("start", flush=True)
import eventlet
print("eventlet imported", flush=True)
eventlet.monkey_patch()
print("monkey_patch done", flush=True)
