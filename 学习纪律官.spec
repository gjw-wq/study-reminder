# -*- mode: python ; coding: utf-8 -*-
# 学习纪律官 - PyInstaller 打包配置
# 关键配置说明:
#   upx=False               - 关闭 UPX 压缩，避免 Qt/Python DLL 被压缩损坏
#   collect_all('PyQt6')    - 一次性收集 PyQt6 的二进制、数据文件、隐藏模块
#   console=False           - 无控制台窗口（发布模式），调试时临时改为 True
#
# 注意: 此文件会被 build.bat / build.py 自动修改 upx 和 console 参数
#       不要手动修改以下标记行:
#         [BUILD_MARKER:UPX]     - 由脚本替换
#         [BUILD_MARKER:CONSOLE] - 由脚本替换

import os
import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# collect_all 返回 (binaries, datas, hiddenimports)
_pyqt6_bin, _pyqt6_data, _pyqt6_hidden = collect_all('PyQt6')

hiddenimports = _pyqt6_hidden + ['PyQt6.sip']
binaries = _pyqt6_bin
datas = _pyqt6_data + [('icons', 'icons')]

# 本地图标资源
icon_path = os.path.join(os.getcwd(), 'icons', 'app.ico')
if not os.path.exists(icon_path):
    icon_path = None

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas', 'matplotlib', 'scipy', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='学习纪律官',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                      # [BUILD_MARKER:UPX]
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                   # [BUILD_MARKER:CONSOLE]
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
