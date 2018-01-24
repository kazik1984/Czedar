# -*- mode: python -*-

block_cipher = None


a = Analysis(['CzedarApp.py'],
             pathex=['D:\\Czedar\\src'],
             binaries=None,
             datas=[('D:\Czedar\src\config.txt','.'),('D:\Czedar\src\cdr_pattern.txt','.'),('D:\Czedar\src\RunCzedar.bat','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
		  a.binaries+[('oraociei12.dll','C:\instantclient_12\oraociei12.dll','BINARY'),('ojdbc6.jar','C:\instantclient_12\ojdbc6.jar','BINARY')],
          a.zipfiles,
          a.datas,
          name='CzedarApp',
          debug=True,
          strip=False,
          upx=True,
          console=True , icon='Martin-Berube-Food-Cheese.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='CzedarApp')
