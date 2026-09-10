# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['_ep_test.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['eventlet.hubs.epolls', 'eventlet.hubs.kqueue', 'eventlet.hubs.poll', 'eventlet.hubs.selects', 'eventlet.green.thread'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='ep_test', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, upx_exclude=[], runtime_tmpdir=None,
    console=True, disable_windowed_traceback=False,
)
