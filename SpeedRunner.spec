# -*- mode: python -*-

block_cipher = None


a = Analysis(['SpeedRunner.py'],
             pathex=['/Users/nicluo/Dev/speed-runner'],
             binaries=[],
             datas=[('assets', 'assets')],
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
          exclude_binaries=True,
          name='SpeedRunner',
          debug=False,
          strip=False,
          upx=True,
          icon='icon.ico',
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SpeedRunner')
app = BUNDLE(coll,
          name='SpeedRunner.app',
          bundle_identifier='com.nicluo.speedrunner',
          icon='icon.icns' )
