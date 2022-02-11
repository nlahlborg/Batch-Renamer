# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['..\\batch_renamer.py'],
             pathex=['.\\util'],
             binaries=[],
             datas=[('..\\settings\\default_settings.json', 'settings'), ('..\\qss\\stylesheet.qss', 'qss'), ('..\\images\\icon.png', 'images')],
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
          name='Batch_Renamer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='..\\images\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Batch_Renamer')
