from PyInstaller import __main__

a = Analysis(
    ['Orders.py'],
    pathex=[],
    binaries=[],
    datas=[('./py/static/media/*', './py/static/media'), 
           ('./py/static/style/auth.qss', './py/static/style'), 
           ('./dataBase/secret.key', './py/'), 
           ('./dataBase/shop.db', './dataBase'),
           ('./py/static/media/check_icon.png', './py/static/media'),
           ('./py/static/media/down-chevron.png', './py/static/media'),
           ('./py/static/media/logo.png', './py/static/media')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# قم بتحديد الأيقونة هنا
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Orders',
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
    icon='./py/static/media/icon.ico'  # تأكد من وضع الأيقونة بصيغة .ico
)



# pyinstaller main.spec