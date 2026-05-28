
import sys
import os
import time
import json
import threading
from datetime import datetime

# Setup paths
sys.path.insert(0, r"C:\\Users\\user\\Desktop\\omnsecience")

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
        self.devices = {}
        
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
        
        print(Fore.GREEN + f"[+] Local IP: {local_ip}")
        print(Fore.GREEN + f"[+] Gateway: {gateway}")
        print(Fore.GREEN + f"[+] Network Range: {network_range}")
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
        
        print(Fore.GREEN + f"[+] Discovered {len(devices)} devices")
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
            dev_type = (dev.device_type or 'unknown')[:7].ljust(7)
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
            
            print(color + f"| {ip} | {hostname} | {os_type} | {dev_type} | {ports} | {vulns} | {pwn} |")
        
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
                print(Fore.YELLOW + f"Device: {dev.ip}")
                print(Fore.WHITE + f"  Hostname: {dev.hostname or 'N/A'}")
                print(Fore.WHITE + f"  OS: {dev.os or 'Unknown'}")
                print(Fore.WHITE + f"  Type: {dev.device_type or 'unknown'}")
                print(Fore.WHITE + f"  MAC: {dev.mac or 'N/A'}")
                print(Fore.WHITE + f"  Open Ports: {list(dev.open_ports.keys())}")
                print(Fore.WHITE + f"  Vulnerabilities: {dev.is_vulnerable[:5]}")
                print(Fore.WHITE + f"  Access Method: {dev.access_method or 'None'}")
                if dev.access_credential:
                    print(Fore.RED + f"  Credentials: {dev.access_credential[0]}:{'*' * len(dev.access_credential[1])}")
                if dev.harvested:
                    print(Fore.CYAN + f"  Harvested Data: {list(dev.harvested.keys())[:5]}")
        
        print()
        print(Fore.CYAN + "=" * 100)
        print(Fore.WHITE + f"Total Devices: {len(self.devices)} | Vulnerable: {len([d for d in self.devices.values() if d.is_vulnerable])} | Accessible: {len([d for d in self.devices.values() if d.can_pwn])}")
        print(Fore.CYAN + "=" * 100)
    
    def export_results(self, filename=None):
        """Export scan results to JSON."""
        if not filename:
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'devices': [d.to_dict() for d in self.devices.values()]
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(Fore.GREEN + f"[+] Results exported to {filename}")
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
                print(Fore.YELLOW + "\n[*] Use 'exit' to quit")
            except Exception as e:
                print(Fore.RED + f"[!] Error: {e}")
    
    def monitor_mode(self):
        """Continuous monitoring mode."""
        print(Fore.CYAN + "[*] Starting monitor mode (scans every 60 seconds, Ctrl+C to stop)...")
        
        try:
            while True:
                self.scan_network()
                print(Fore.YELLOW + "[*] Next scan in 60 seconds... (Ctrl+C to stop)")
                time.sleep(60)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[*] Monitor mode stopped")


if __name__ == "__main__":
    scanner = RealTimeScanner()
    scanner.interactive_mode()
