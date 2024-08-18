# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['alien_invasion.py',
    'alien.py',
    'bullet.py',
    'button.py',
    'game_stats.py',
    'scoreboard.py',
    'settings.py',
    'ship.py',
    'star.py',
    'pngdebug.py'],
    pathex=['D:\\GAMEFORME\\alien_invasion'],
    binaries=[],
    datas=[
    ('images\\ALIEN(2).png','images'),
    ('images\\ALIEN.bmp','images'),
    ('images\\SHIP1.bmp','images'),
    ('images\\STAR.png','images'),
    ('images\\SHIP2.bmp','images')],
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
    name='外星人入侵',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='D:\\GAMEFORME\\alien_invasion\\favicon.ico'
)
