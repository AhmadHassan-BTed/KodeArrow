# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['QTT.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas', 'numpy', 'matplotlib', 'scipy', 'PIL', 'cv2', 'tensorflow', 'torch', 'jupyter', 'IPython', 'sqlite3', 'xml', 'html', 'http', 'email', 'unittest', 'multiprocessing', 'concurrent', 'asyncio', 'logging', 'doctest', 'pdb', 'profile', 'cProfile', 'trace', 'decimal', 'fractions', 'statistics', 'wave', 'audioop', 'chunk', 'sunau', 'aifc', 'sndhdr', 'ossaudiodev', 'winsound'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='TypingTest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
