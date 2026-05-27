#!/usr/bin/env python3
"""
Omniscience Framework Pro - Cross-Platform Build Script
Creates standalone executables for Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import shutil

# Configuration
APP_NAME = "OmnisciencePro"
VERSION = "5.1"
MAIN_SCRIPT = "kivygui.py"

# Dependencies
DEPS = [
    'colorama',
    'scapy',
    'impacket', 
    'paramiko',
    'Pillow',
    'pyinstaller',
    'pycryptodome'
]

# Platform-specific dependencies
PLATFORM_DEPS = {
    'windows': ['pywin32'],
    'darwin': [],
    'linux': []
}

def get_platform():
    """Get current platform."""
    return platform.system().lower()

def install_dependencies():
    """Install all required dependencies."""
    print("[*] Installing dependencies...")
    
    # Install main deps
    for dep in DEPS:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep, '-q'])
            print(f"  [+] {dep}")
        except:
            print(f"  [!] {dep} failed")
    
    # Install platform-specific deps
    current_platform = get_platform()
    if current_platform in PLATFORM_DEPS:
        for dep in PLATFORM_DEPS[current_platform]:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep, '-q'])
                print(f"  [+] {dep} (platform-specific)")
            except:
                print(f"  [!] {dep} failed (platform-specific)")

def create_spec_file(platform_name):
    """Create PyInstaller spec file for the target platform."""
    
    # Get platform-specific settings
    if platform_name == 'windows':
        console = False  # GUI app
        icon_ext = 'ico'
        exe_name = f"{APP_NAME}.exe"
    elif platform_name == 'darwin':
        console = True
        icon_ext = 'icns'
        exe_name = f"{APP_NAME}.app"
    else:  # linux
        console = True
        icon_ext = ''
        exe_name = APP_NAME
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Collect all Python files
py_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and not file.startswith('.'):
            py_files.append(os.path.join(root, file))

a = Analysis(
    ['{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'colorama',
        'scapy.all',
        'scapy.layers.inet',
        'scapy.layers.l2',
        'impacket',
        'impacket.smbconnection',
        'impacket.dcerpc.v5',
        'impacket.dcerpc.v5.wmi',
        'impacket.dcerpc.v5.dcomrt',
        'impacket.dcerpc.v5.dcom',
        'paramiko',
        'paramiko.transport',
        'PIL',
        'PIL.Image',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['tkinter', 'test'],
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
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    spec_file = f'Omniscience_{platform_name}.spec'
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    
    print(f"[+] Created {spec_file}")
    return spec_file

def build_for_platform(platform_name):
    """Build executable for specific platform."""
    print(f"\\n[*] Building for {platform_name}...")
    
    # Create spec file
    spec_file = create_spec_file(platform_name)
    
    # Build
    output_dir = f"build/{platform_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Clean old builds
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        
        # Run PyInstaller
        cmd = [
            'pyinstaller',
            spec_file,
            '--name', APP_NAME,
            '--onefile',
            '--clean'
        ]
        
        if platform_name == 'windows':
            cmd.append('--windowed')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[+] Build successful for {platform_name}!")
            
            # Move output
            if os.path.exists(f'dist/{APP_NAME}'):
                if platform_name == 'windows':
                    final_name = f'dist/{APP_NAME}.exe'
                else:
                    final_name = f'dist/{APP_NAME}'
                
                if os.path.exists(final_name):
                    shutil.copy(final_name, f'{output_dir}/')
                    print(f"[+] Saved to {output_dir}/")
        else:
            print(f"[!] Build failed: {result.stderr}")
            
    except FileNotFoundError:
        print("[!] PyInstaller not found")
    except Exception as e:
        print(f"[!] Error: {e}")

def build_all():
    """Build for all platforms."""
    print(f"Omniscience Framework Pro v{VERSION} - Build Script")
    print("=" * 50)
    
    # Install dependencies first
    install_dependencies()
    
    current_platform = get_platform()
    print(f"\\n[*] Current platform: {current_platform}")
    
    # Build for current platform
    build_for_platform(current_platform)
    
    print("\\n[*] Build complete!")
    print("[*] Check the build/ directory for executables")

def build_windows():
    """Build specifically for Windows."""
    build_for_platform('windows')

def build_macos():
    """Build specifically for macOS."""
    build_for_platform('darwin')

def build_linux():
    """Build specifically for Linux."""
    build_for_platform('linux')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        if target == 'windows':
            build_windows()
        elif target == 'macos' or target == 'darwin':
            build_macos()
        elif target == 'linux':
            build_linux()
        elif target == 'all':
            build_all()
        else:
            print(f"Unknown target: {target}")
            print("Usage: python installer.py [windows|macos|linux|all]")
    else:
        build_all()
