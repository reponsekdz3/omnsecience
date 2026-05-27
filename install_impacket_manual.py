#!/usr/bin/env python3
"""
OmniSec Dependency Installer — Installs impacket even behind restrictive firewalls.
Uses multiple fallback strategies: pip (with retries), direct download with SSL bypass, manual copy.
"""

import sys
import os
import subprocess
import ssl
import time

def run_pip(args):
    return subprocess.run([sys.executable, "-m", "pip"] + args, capture_output=True, text=True)

def install_via_pip():
    print("[*] Method 1: pip install with extended timeout...")
    r = run_pip(["install", "impacket", "--retries", "20", "--timeout", "120", "--default-timeout=100"])
    if r.returncode == 0:
        print("[+] impacket installed via pip")
        return True
    print(f"    pip failed: {r.stderr[:200]}")
    return False

def install_via_direct_download():
    print("[*] Method 2: Direct download with SSL bypass...")
    try:
        import urllib.request
        import tarfile
        import io
        import tempfile
        import shutil
        import site
        
        url = "https://files.pythonhosted.org/packages/impacket-0.13.0.tar.gz"
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
                    data = resp.read()
                    print(f"[+] Downloaded {len(data)} bytes")
                    
                    # Extract to temp
                    tmpdir = tempfile.mkdtemp()
                    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
                        tar.extractall(tmpdir)
                    
                    src_dir = os.path.join(tmpdir, "impacket-0.13.0", "impacket")
                    if not os.path.isdir(src_dir):
                        print(f"[!] Extracted structure unexpected: {os.listdir(tmpdir)}")
                        return False
                    
                    # Copy impacket folder to site-packages
                    sp = site.getsitepackages()[0] if site.getsitepackages() else site.getusersitepackages()
                    dest = os.path.join(sp, "impacket")
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    shutil.copytree(src_dir, dest)
                    print(f"[+] impacket copied to {dest}")
                    return True
            except Exception as e:
                print(f"    Attempt {attempt+1} failed: {e}")
                time.sleep(3)
        return False
    except Exception as e:
        print(f"[!] Direct download error: {e}")
        return False

def main():
    print("=" * 70)
    print(" OMNISEC — IMPACKET INSTALLER")
    print("=" * 70)
    print()
    
    # Check if already importable
    try:
        import impacket
        print("[+] impacket already available")
        return 0
    except ImportError:
        print("[*] impacket not found — installing...")
    
    # Try pip
    if install_via_pip():
        return 0
    
    print("[!] pip method failed, trying direct download...")
    if install_via_direct_download():
        return 0
    
    print("\n[!] AUTOMATIC INSTALL FAILED")
    print("    Please install impacket manually:")
    print("    1. Download from: https://github.com/fortra/impacket/releases")
    print("       (look for impacket-0.13.0.tar.gz or .whl)")
    print("    2. Then run: pip install <downloaded_file>")
    print("\n    Or use a machine with internet to download and copy here.")
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Cancelled")
        sys.exit(1)
