import asyncio
import sys
import os
import time

# Load impacket from local source path
_local_impacket_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'impacket_src', 'impacket-0.13.0')
if os.path.isdir(_local_impacket_path) and _local_impacket_path not in sys.path:
    sys.path.insert(0, _local_impacket_path)

from commandcenter import OmniShell

def check_dependencies():
    """Verify core functional dependencies are installed."""
    deps = ['scapy', 'paramiko', 'requests', 'cryptography']
    optional = ['impacket']
    missing = []
    optional_missing = []
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    for dep in optional:
        try:
            __import__(dep)
        except ImportError:
            optional_missing.append(dep)
    
    if missing:
        print(f"[!] MISSING REQUIRED DEPENDENCIES: {', '.join(missing)}")
        print("[*] Install via: pip install -r requirements.txt")
        sys.exit(1)
    
    if optional_missing:
        print(f"[!] OPTIONAL DEPENDENCIES NOT FOUND: {', '.join(optional_missing)}")
        print("[*] Some features (Windows SMB/WMI exploitation) will be disabled.")
        print("[*] To enable full functionality, install: pip install impacket")
        print("[*] Continuing in limited mode...\n")
        time.sleep(2)

async def main():
    # Ensure administrative privileges for Scapy and Raw Sockets
    if os.name == 'nt':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[!] SYSTEM ALERT: Framework requires Administrative privileges for Raw Socket operations.")
    elif os.name == 'posix':
        if os.geteuid() != 0:
            print("[!] SYSTEM ALERT: Framework requires root privileges for Scapy/Raw Socket operations.")

    print("""
    ============================================================  [STABLE]
    ||              OMNISCIENCE ULTRAMAX PRO v7.1             ||
    ||          HIGH-SECURITY CYBER INTERCEPT PLATFORM        ||
    ||      AUTHORIZED FOR GOVERNMENTAL INTEL OPERATIONS      ||
    ============================================================
    [*] Initializing AMMO v2 Asynchronous Engine...
    [*] Loading Cryptographic Modules...
    [*] Loading Command Center...
    """)

    shell = OmniShell()

    # Check if command arguments are provided
    if len(sys.argv) > 1:
        # Non-interactive mode: execute command from arguments
        cmd_input = " ".join(sys.argv[1:])
        print(f"[*] Executing command: {cmd_input}")
        try:
            await shell.handle_command(cmd_input)
        except Exception as e:
            print(f"[CRITICAL] Command execution failed: {e}")
    else:
        # Interactive mode
        try:
            await shell.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down C2 sessions...")
        except Exception as e:
            print(f"[CRITICAL] Kernel Panic: {e}")

if __name__ == "__main__":
    # Check dependencies before starting the event loop
    check_dependencies()
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())