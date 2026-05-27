#!/usr/bin/env python3
"""
Omniscience Framework v5.1 - Installer
Creates a standalone executable for Windows
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """Install required dependencies."""
    print("[*] Installing dependencies...")
    
    deps = [
        'colorama',
        'scapy', 
        'impacket',
        'paramiko',
        'pywin32',
        'Pillow'
    ]
    
    for dep in deps:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep, '-q'])
            print(f"  [+] {dep} installed")
        except:
            print(f"  [!] {dep} failed (optional)")

def create_spec_file():
    """Create PyInstaller spec file."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['4.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('*.py', '.'),
    ],
    hiddenimports=[
        'colorama',
        'scapy.all',
        'impacket',
        'paramiko',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Omniscience',
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
    icon=None,
)
'''
    with open('omniscience.spec', 'w') as f:
        f.write(spec_content)
    print("[+] Spec file created")

def build_exe():
    """Build the executable."""
    print("[*] Building executable...")
    try:
        subprocess.check_call(['pyinstaller', 'omniscience.spec', '--onefile', '--console'])
        print("[+] Build complete!")
        print("[+] Executable: dist/Omniscience.exe")
    except FileNotFoundError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        build_exe()
    except Exception as e:
        print(f"[!] Build failed: {e}")

def main():
    print("=" * 60)
    print("  OMNISCIENCE FRAMEWORK v5.1 - INSTALLER")
    print("=" * 60)
    print()
    
    # Check if running from source directory
    if not os.path.exists('4.py'):
        print("[!] Run this installer from the heavy directory!")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Create spec file
    create_spec_file()
    
    # Build
    build_exe()
    
    print()
    print("=" * 60)
    print("  INSTALLATION COMPLETE!")
    print("=" * 60)
    print("Run: dist/Omniscience.exe")

if __name__ == "__main__":
    main()
