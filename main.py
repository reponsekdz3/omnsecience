import asyncio
import sys
import os
import time
import subprocess
import json
import threading
from datetime import datetime

# Load impacket from local source path (force correct import target)
_repo_root = os.path.dirname(os.path.abspath(__file__))
_local_impacket_parent = os.path.join(_repo_root, 'impacket_src', 'impacket-0.13.0')
if os.path.isdir(_local_impacket_parent) and _local_impacket_parent not in sys.path:
    sys.path.insert(0, _local_impacket_parent)

# If a conflicting top-level namespace package (./impacket/) was already imported,
# remove it so subsequent imports resolve to ./impacket_src/impacket-0.13.0/impacket.
try:
    import impacket as _impacket_mod  # noqa: F401
    _impacket_paths = list(getattr(_impacket_mod, '__path__', []))
    _preferred = os.path.join(_local_impacket_parent, 'impacket') if os.path.isdir(_local_impacket_parent) else None
    if _preferred and _preferred not in _impacket_paths:
        for m in list(sys.modules.keys()):
            if m == 'impacket' or m.startswith('impacket.'):
                sys.modules.pop(m, None)
        import importlib
        importlib.invalidate_caches()
except Exception:
    pass


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


def open_scanner_window():
    """Open a new window for real-time device scanning."""
    scanner_script = '''
import sys
import os
import time
import json
import threading
from datetime import datetime

# Setup paths
sys.path.insert(0, r"{repo_root}")

from colorama import Fore, Style, init
init(autoreset=True)

# Import scanner
from exploit_engine import UniversalNetworkAccess, UniversalDevice
from advanced_scanner import AdvancedNetworkScanner

class RealTimeScanner:
    def __init__(self):
        self.exploiter = UniversalNetworkAccess()
        self.scanner = AdvancedNetworkScanner()
        self.scanning = False
        self.devices = {{}}
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        self.clear_screen()
        print(Fore.CYAN + "=" * 100)
        print(Fore.CYAN + "||" + Fore.GREEN + " OMNISCIENCE REAL-TIME NETWORK SCANNER " + Fore.CYAN + "||")
        print(Fore.CYAN + "||" + Fore.YELLOW + " LIVE DEVICE DISCOVERY AND PROFILING " + Fore.CYAN + "||")
        print(Fore.CYAN + "=" * 100)
        print()
        
    def scan_network(self, network_range=None):
        """Perform real network scan."""
        self.scanning = True
        self.print_header()
        
        print(Fore.YELLOW + "[*] Initializing network interfaces...")
        
        # Get local network info
        local_ip = self.scanner.local_ip
        gateway = self.scanner.gateway
        if not network_range:
            network_range = self.scanner.network_range
        
        print(Fore.GREEN + f"[+] Local IP: {{local_ip}}")
        print(Fore.GREEN + f"[+] Gateway: {{gateway}}")
        print(Fore.GREEN + f"[+] Network Range: {{network_range}}")
        print()
        print(Fore.CYAN + "[*] Starting comprehensive network scan...")
        print(Fore.YELLOW + "[*] This may take 30-60 seconds depending on network size...")
        print()
        
        # Real device discovery
        print(Fore.CYAN + "[*] Phase 1: ARP Scanning (Layer 2)...")
        devices = self.exploiter.discover_all_devices(network_range)
        
        # Update devices dict
        for dev in devices:
            self.devices[dev.ip] = dev
        
        print(Fore.GREEN + f"[+] Discovered {{len(devices)}} devices")
        print()
        
        # Scan all devices for vulnerabilities
        print(Fore.CYAN + "[*] Phase 2: Vulnerability Assessment...")
        self.exploiter.scan_all_devices()
        
        # Display results
        self.display_devices()
        
        self.scanning = False
        return devices
    
    def display_devices(self):
        """Display all discovered devices with full details."""
        self.print_header()
        
        if not self.devices:
            print(Fore.RED + "[!] No devices discovered yet. Run a scan first.")
            return
        
        # Sort devices by IP
        sorted_devices = sorted(self.devices.values(), key=lambda d: tuple(map(int, d.ip.split('.'))))
        
        print(Fore.WHITE + "=" * 100)
        print(Fore.WHITE + "| IP Address      | Hostname            | OS            | Type     | Ports | Vulns | Pwn |")
        print(Fore.WHITE + "=" * 100)
        
        for dev in sorted_devices:
            ip = dev.ip[:15].ljust(15)
            hostname = (dev.hostname or dev.ip)[:18].ljust(18)
            os_type = (dev.os or 'Unknown')[:13].ljust(13)
            dev_type = (dev.device_type or 'unknown')[:7).ljust(7)
            ports = str(len(dev.open_ports)).ljust(5)
            vulns = str(len(dev.is_vulnerable)).ljust(5)
            pwn = Fore.GREEN + "YES" + Fore.WHITE if dev.can_pwn else Fore.RED + "NO" + Fore.WHITE
            
            # Color coding based on vulnerability
            if dev.can_pwn:
                color = Fore.RED
            elif dev.is_vulnerable:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
            
            print(color + f"| {{ip}} | {{hostname}} | {{os_type}} | {{dev_type}} | {{ports}} | {{vulns}} | {{pwn}} |")
        
        print(Fore.WHITE + "=" * 100)
        print()
        
        # Detailed view for compromised/vulnerable devices
        vulnerable_devices = [d for d in self.devices.values() if d.can_pwn or d.is_vulnerable]
        if vulnerable_devices:
            print(Fore.RED + "=" * 100)
            print(Fore.RED + "VULNERABLE/ACCESSIBLE DEVICES DETAILS:")
            print(Fore.RED + "=" * 100)
            
            for dev in vulnerable_devices[:10]:  # Show top 10
                print()
                print(Fore.YELLOW + f"Device: {{dev.ip}}")
                print(Fore.WHITE + f"  Hostname: {{dev.hostname or 'N/A'}}")
                print(Fore.WHITE + f"  OS: {{dev.os or 'Unknown'}}")
                print(Fore.WHITE + f"  Type: {{dev.device_type or 'unknown'}}")
                print(Fore.WHITE + f"  MAC: {{dev.mac or 'N/A'}}")
                print(Fore.WHITE + f"  Open Ports: {{list(dev.open_ports.keys())}}")
                print(Fore.WHITE + f"  Vulnerabilities: {{dev.is_vulnerable[:5]}}")
                print(Fore.WHITE + f"  Access Method: {{dev.access_method or 'None'}}")
                if dev.access_credential:
                    print(Fore.RED + f"  Credentials: {{dev.access_credential[0]}}:{{'*' * len(dev.access_credential[1])}}")
                if dev.harvested:
                    print(Fore.CYAN + f"  Harvested Data: {{list(dev.harvested.keys())[:5]}}")
        
        print()
        print(Fore.CYAN + "=" * 100)
        print(Fore.WHITE + f"Total Devices: {{len(self.devices)}} | Vulnerable: {{len([d for d in self.devices.values() if d.is_vulnerable])}} | Accessible: {{len([d for d in self.devices.values() if d.can_pwn])}}")
        print(Fore.CYAN + "=" * 100)
    
    def export_results(self, filename=None):
        """Export scan results to JSON."""
        if not filename:
            filename = f"scan_results_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
        
        results = {{
            'timestamp': datetime.now().isoformat(),
            'devices': [d.to_dict() for d in self.devices.values()]
        }}
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(Fore.GREEN + f"[+] Results exported to {{filename}}")
        return filename
    
    def interactive_mode(self):
        """Interactive scanner mode."""
        self.print_header()
        
        print(Fore.CYAN + "REAL-TIME NETWORK SCANNER - INTERACTIVE MODE")
        print(Fore.YELLOW + "Commands: scan [network], show, export, monitor, exit")
        print()
        
        while True:
            try:
                cmd = input(Fore.GREEN + "SCANNER> " + Fore.WHITE).strip().lower()
                
                if cmd == 'exit' or cmd == 'quit':
                    print(Fore.YELLOW + "[*] Exiting scanner...")
                    break
                
                elif cmd == 'scan' or cmd.startswith('scan '):
                    parts = cmd.split()
                    network = parts[1] if len(parts) > 1 else None
                    self.scan_network(network)
                
                elif cmd == 'show':
                    self.display_devices()
                
                elif cmd == 'export':
                    self.export_results()
                
                elif cmd == 'monitor':
                    self.monitor_mode()
                
                else:
                    print(Fore.YELLOW + "Commands: scan [network], show, export, monitor, exit")
            
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\\n[*] Use 'exit' to quit")
            except Exception as e:
                print(Fore.RED + f"[!] Error: {{e}}")
    
    def monitor_mode(self):
        """Continuous monitoring mode."""
        print(Fore.CYAN + "[*] Starting monitor mode (scans every 60 seconds, Ctrl+C to stop)...")
        
        try:
            while True:
                self.scan_network()
                print(Fore.YELLOW + "[*] Next scan in 60 seconds... (Ctrl+C to stop)")
                time.sleep(60)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\\n[*] Monitor mode stopped")


if __name__ == "__main__":
    scanner = RealTimeScanner()
    scanner.interactive_mode()
'''.format(repo_root=_repo_root.replace('\\', '\\\\'))
    
    # Write scanner script to temp file
    scanner_path = os.path.join(_repo_root, 'live_scanner.py')
    with open(scanner_path, 'w') as f:
        f.write(scanner_script)
    
    # Open in new window
    if sys.platform == 'win32':
        cmd = f'start "Omniscience Scanner" cmd /k "cd /d {_repo_root} && python live_scanner.py"'
        os.system(cmd)
    else:
        # Linux/Mac
        terminal = 'gnome-terminal' if os.system('which gnome-terminal') == 0 else 'xterm'
        os.system(f'{terminal} -e "cd {_repo_root} && python live_scanner.py"')
    
    return scanner_path


def open_command_window():
    """Open a new window for command execution."""
    cmd_script = '''
import sys
import os
import asyncio
import threading
from datetime import datetime

# Setup paths
sys.path.insert(0, r"{repo_root}")

from colorama import Fore, Style, init
init(autoreset=True)

# Import command center
from commandcenter import OmniShell

def run_command_shell():
    """Run the command shell in this window."""
    print(Fore.CYAN + "=" * 100)
    print(Fore.CYAN + "||" + Fore.GREEN + " OMNISCIENCE COMMAND CENTER " + Fore.CYAN + "||")
    print(Fore.CYAN + "||" + Fore.YELLOW + " INTERACTIVE COMMAND SHELL " + Fore.CYAN + "||")
    print(Fore.CYAN + "=" * 100)
    print()
    
    # Create shell instance
    shell = OmniShell()
    
    print(Fore.GREEN + "[+] Command Center initialized")
    print(Fore.YELLOW + "[*] Type 'help' for available commands")
    print(Fore.YELLOW + "[*] Type 'scan' to initiate network scan")
    print(Fore.YELLOW + "[*] Type 'pwn' to exploit accessible devices")
    print()
    
    # Run the shell
    asyncio.run(shell.start())

if __name__ == "__main__":
    run_command_shell()
'''.format(repo_root=_repo_root.replace('\\', '\\\\'))
    
    # Write command script to temp file
    cmd_path = os.path.join(_repo_root, 'live_command.py')
    with open(cmd_path, 'w') as f:
        f.write(cmd_script)
    
    # Open in new window
    if sys.platform == 'win32':
        cmd = f'start "Omniscience Command Center" cmd /k "cd /d {_repo_root} && python live_command.py"'
        os.system(cmd)
    else:
        # Linux/Mac
        terminal = 'gnome-terminal' if os.system('which gnome-terminal') == 0 else 'xterm'
        os.system(f'{terminal} -e "cd {_repo_root} && python live_command.py"')
    
    return cmd_path


async def main():
    """Main entry point for OMNISCIENCE."""
    
    # Ensure administrative privileges for Scapy and Raw Sockets
    if os.name == 'nt':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[!] SYSTEM ALERT: Framework requires Administrative privileges for Raw Socket operations.")
            print("[*] Please restart with administrator privileges.")
    elif os.name == 'posix':
        if os.geteuid() != 0:
            print("[!] SYSTEM ALERT: Framework requires root privileges for Scapy/Raw Socket operations.")
            print("[*] Please run with sudo.")

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

    # Check if command arguments are provided
    if len(sys.argv) > 1:
        # Non-interactive mode: execute command from arguments
        from commandcenter import OmniShell
        shell = OmniShell()
        
        cmd_input = " ".join(sys.argv[1:])
        print(f"[*] Executing command: {cmd_input}")
        try:
            await shell.handle_command(cmd_input)
        except Exception as e:
            print(f"[CRITICAL] Command execution failed: {e}")
    else:
        # Interactive mode - auto-open windows
        print("[*] OMNISCIENCE ULTRAMAX PRO v7.1 - MULTIPLE WINDOW MODE")
        print("[*] Opening separate windows for operations...")
        print()
        
        # Open scanner window
        print("[*] Opening Scanner Window (Real-time Device Discovery)...")
        scanner_path = open_scanner_window()
        time.sleep(2)
        
        # Open command window
        print("[*] Opening Command Center Window (Interactive Shell)...")
        cmd_path = open_command_window()
        time.sleep(2)
        
        print()
        print("[+] " + "=" * 70)
        print("[+] OMNISCIENCE WINDOWS LAUNCHED SUCCESSFULLY")
        print("[+] " + "=" * 70)
        print()
        print("[*] Two windows have been opened:")
        print("[*]   1. Scanner Window - Real-time network device discovery")
        print("[*]   2. Command Center - Interactive command execution")
        print()
        print("[*] This main process will now exit.")
        print("[*] Use the opened windows for all operations.")
        print()
        
        # Keep main process alive briefly to ensure windows open
        time.sleep(3)
        
        print("[+] Main process exiting. Windows remain active.")
        sys.exit(0)


if __name__ == "__main__":
    # Check dependencies before starting the event loop
    check_dependencies()
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
