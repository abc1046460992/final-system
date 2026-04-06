# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['c:\\Users\\abc10\\Desktop\\\u200f\u200fمدرسة الملك خالد المتوسطة - نسخة\\مدرسة الملك خالد حضور وانصراف وغياب وتواصل مع ولي الامر\\attendance_main.py'],
    pathex=[],
    binaries=[],
    datas=[('شعار_الوزارة.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='نظام_المدرسة',
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
)
