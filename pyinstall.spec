# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['main.py'],
    binaries=[],
    datas=[
        *collect_data_files('customtkinter'),  # Inclui arquivos do CTkinter
        ('media/image/clean_icon.png', 'media/image'),  # Imagens
    ],
    hiddenimports=[
        'PIL._tkinter_finder',  # Necessário para o Pillow (PIL)
        'pygame._sdl2'  # Para evitar erros do Pygame
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['api-ms-win-core-path-l1-1-0.dll'],
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
    name='AutoPreenchimento',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Remove o console (⚠️ Certifique-se de tratar erros na GUI!)
    icon='seu_icone.ico'  # Adicione um ícone .ico
)