# main.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[
        '.',  # Caminho atual
        'C:\\Users\\david.sousa\\Documents\\scripts\\custom\\rodopar_interface_customtk\\.venv\\Lib\\site-packages',  # Caminho do site-packages
    ],
    binaries=['C:\\Users\\david.sousa\\Documents\\scripts\\custom\\rodopar_interface_customtk\\.venv\\Lib\\site-packages\\pywin32_system32\\*.dll', 'pywin32_system32'],
    datas=[
        ('config/*', 'config'),
        ('imagens/*', 'imagens'),
        ('media/*', 'media'),
        ('ost_dadosfixos/*', 'ost_dadosfixos'),
        ('xml_process/*', 'xml_process'),
    ],
    hiddenimports=['customtkinter', 'pdfplumber', 'pywin32', 'pythoncom', 'pywintypes'],  # Adicione as dependências aqui
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='media/image/icon_main.ico',  # Substitua pelo caminho do seu ícone
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)