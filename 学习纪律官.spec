# -*- mode: python ; coding: utf-8 -*-
import os
import glob
import PyQt6
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files, collect_dynamic_libs

datas = [('icons', 'icons')]
binaries = []
hiddenimports = []

tmp_ret = collect_all('PyQt6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt6-Qt6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

qt6_root = os.path.join(os.path.dirname(PyQt6.__file__), 'Qt6')
qt6_bin = os.path.join(qt6_root, 'bin')
qt6_plugins = os.path.join(qt6_root, 'plugins')

existing_binary_names = set(os.path.basename(b[0]) for b in binaries)

for dll in glob.glob(os.path.join(qt6_bin, 'Qt6*.dll')):
    if os.path.basename(dll) not in existing_binary_names:
        binaries.append((dll, '.'))
        existing_binary_names.add(os.path.basename(dll))

for dll in glob.glob(os.path.join(qt6_bin, '*.dll')):
    basename = os.path.basename(dll)
    if basename.startswith(('avcodec', 'avformat', 'avutil', 'swresample', 'swscale')):
        if basename not in existing_binary_names:
            binaries.append((dll, '.'))
            existing_binary_names.add(basename)

if os.path.isdir(qt6_plugins):
    for root, dirs, files in os.walk(qt6_plugins):
        for f in files:
            if f.endswith('.dll'):
                src = os.path.join(root, f)
                rel = os.path.relpath(root, qt6_root)
                datas.append((src, rel))


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas', 'matplotlib', 'scipy', 'tkinter'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='学习纪律官',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons\\app.ico'],
)
