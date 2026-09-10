# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
a = Analysis(
    ['_app_test.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('app.version', '.')],
    hiddenimports=[
        'eventlet.hubs.epolls', 'eventlet.hubs.kqueue', 'eventlet.hubs.poll', 'eventlet.hubs.selects',
        'eventlet.green.thread', 'eventlet.green.threading', 'eventlet.websocket',
        'engineio.async_drivers.threading', 'engineio.async_drivers.eventlet', 'socketio',
        'licensing', 'updater', 'flask_socketio',
    ] + collect_submodules('dns'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='app_test', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, upx_exclude=[], runtime_tmpdir=None,
    console=True, disable_windowed_traceback=False,
)
