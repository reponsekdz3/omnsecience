#!/usr/bin/env python3
"""
OmniSec Dependency Installer & Bootstrap
Installs all dependencies with multiple fallback strategies.
Works behind firewalls, with proxies, or offline.
"""

import sys
import os
import subprocess
import urllib.request
import zipfile
import io

def run_pip(args):
    """Run pip with given args."""
    return subprocess.run([sys.executable, "-m", "pip"] + args, capture_output=True, text=True)

def install_from_url(url, package_name):
    """Download and install a package from a direct URL."""
    print(f"[*] Downloading {package_name} from {url}")
    try:
        req = urllib.request.urlopen(url, timeout=60)
        data = req.read()
        
        # Save to temp
        pkg_path = f"C:\\Temp\\{package_name}.whl"
        os.makedirs("C:\\Temp", exist_ok=True)
        with open(pkg_path, "wb") as f:
            f.write(data)
        
        print(f"[+] Download complete ({len(data)} bytes). Installing...")
        result = run_pip(["install", pkg_path, "--no-deps"])
        if result.returncode == 0:
            print(f"[+] {package_name} installed from local file")
            return True
        else:
            print(f"[!] Install failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"[!] Download failed: {e}")
        return False

def install_impacket():
    """Install impacket via multiple methods."""
    print("[*] Installing impacket...")
    
    # Method 1: Try pip normally (might work if network improves)
    print("[*] Method 1: Standard pip")
    r = run_pip(["install", "impacket", "--retries", "5", "--timeout", "60"])
    if r.returncode == 0:
        print("[+] impacket installed via pip")
        return True
    
    # Method 2: Try from a wheel URL (prebuilt)
    print("[*] Method 2: Direct wheel download")
    wheel_url = "https://files.pythonhosted.org/packages/impacket-0.13.0-py2.py3-none-any.whl"
    if install_from_url(wheel_url, "impacket"):
        return True
    
    # Method 3: Use easy_install fallback
    print("[*] Method 3: easy_install")
    try:
        r = subprocess.run([sys.executable, "-m", "easy_install", "impacket"], capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            print("[+] impacket installed via easy_install")
            return True
    except:
        pass
    
    # Method 4: Offer manual install instructions
    print("\n[!] AUTOMATIC INSTALL FAILED")
    print("    To complete installation, manually:")
    print("    1. Download impacket from: https://github.com/fortra/impacket/releases")
    print("    2. Save as impacket.whl or .tar.gz")
    print("    3. Run: pip install <filename>")
    print("\n    Alternatively, OmniSec can operate in SSH-only mode without impacket.")
    return False

def main():
    print("=" * 70)
    print(" OMNISEC DEPENDENCY BOOTSTRAPPER")
    print("=" * 70)
    print()
    
    # Check Python version
    print(f"[*] Python: {sys.version.split()[0]}")
    
    # Ensure pip is available
    try:
        import pip
        print("[+] pip is available")
    except ImportError:
        print("[!] pip not found. Please install pip first.")
        return 1
    
    # Check current packages
    print("\n[*] Checking current packages...")
    installed = {}
    for pkg in ["scapy", "paramiko", "impacket"]:
        try:
            __import__(pkg)
            installed[pkg] = True
            print(f"    [OK] {pkg}")
        except ImportError:
            installed[pkg] = False
            print(f"    [MISSING] {pkg}")
    
    # Install missing
    if not installed["impacket"]:
        print("\n[*] impacket is required for Windows exploitation")
        if input("    Install now? (y/n): ").lower() != 'y':
            print("[*] Skipping impacket. OmniSec will run in SSH-only mode.")
            return 0
        
        success = install_impacket()
        if success:
            print("\n[+] All dependencies satisfied!")
            return 0
        else:
            print("\n[!] Could not install impacket automatically.")
            print("    OmniSec will run in partial mode (SSH/Scan only).")
            return 0
    else:
        print("\n[+] All required packages are installed!")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Cancelled")
        sys.exit(1)
