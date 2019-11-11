# -*- mode: python ; coding: utf-8 -*-
# beta version in one folder

block_cipher = None
APPNAME = 'canda-0.1.2-debug'



a = Analysis(['C:\\Users\\gerolbado\\Desktop\\canda 0.1.x\\canda\\main.py'],
             pathex=['C:\\Users\\gerolbado\\Desktop\\canda 0.1.x'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=APPNAME,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=APPNAME)
