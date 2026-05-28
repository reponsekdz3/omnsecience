"""
OMNISCIENCE REAL-TIME NETWORK SCANNER
Functional network device discovery with real-time display
"""

import sys
import os
import time
import json
import threading
import socket
import subprocess
import ipaddress
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional

# Setup paths
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from colorama import Fore, Style, init
init(autoreset=True)

# Try to import scapy
try:
    import scapy.all as scapy
    from scapy.layers import inet, l2
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

# Try to import netifaces
try:
    import netifaces
    NETIFACES_OK = True
except ImportError:
    NETIFACES_OK = False


class LiveDevice:
    """Real-time device information."""
    def __init__(self, ip: str):
        self.ip = ip
        self.mac = ""
        self.hostname = ""
        self.os = "Unknown"
        self.device_type = "unknown"
        self.vendor = "Unknown"
        self.open_ports = {}
        self.services = []
        self.is_vulnerable = []
        self.can_pwn = False
        self.access_method = None
        self.last_seen = time.time()
        self.first_seen = time.time()
        
    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "os": self.os,
            "device_type": self.device_type,
            "vendor": self.vendor,
            "open_ports": self.open_ports,
            "services": self.services,
            "is_vulnerable": self.is_vulnerable,
            "can_pwn": self.can_pwn,
            "access_method": self.access_method,
            "last_seen": self.last_seen,
        }


class LiveNetworkScanner:
    """Real-time network scanner with live display."""
    
    # MAC OUI Database
    MAC_VENDORS = {
        "DC4F22": "Apple", "3C5AB4": "Apple", "AC61EA": "Apple", "A4B1E9": "Apple",
        "F0DCE2": "Apple", "C86F87": "Apple", "A46C2A": "Apple", "F0B479": "Apple",
        "9C2986": "Samsung", "C42C56": "Samsung", "00207C": "Samsung", "A82BCD": "Samsung",
        "18AF61": "Huawei", "2839AB": "Huawei", "F40154": "Huawei", "E8CD2D": "Huawei",
        "E4B318": "Xiaomi", "3CBD3E": "Xiaomi", "5865E6": "Xiaomi", "64B473": "Xiaomi",
        "B827EB": "Raspberry Pi", "DCA632": "Raspberry Pi", "E45F01": "Raspberry Pi",
        "000C29": "VMware", "005056": "VMware", "00155D": "Hyper-V", "08C6EB": "Xen",
        "9CDC6A": "Ubiquiti", "705A0F": "TP-Link", "D460E3": "Netgear",
        "C80E77": "D-Link", "001FC6": "ASUS", "001A2F": "Cisco", "002129": "Cisco",
    }
    
    # Common ports to scan
    SCAN_PORTS = [
        21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995,
        1433, 1521, 1723, 3306, 3389, 5432, 5900, 5985, 6379, 8080, 8443, 27017
    ]
    
    def __init__(self):
        self.devices: Dict[str, LiveDevice] = {}
        self._lock = threading.Lock()
        self.scanning = False
        self._stop_event = threading.Event()
        
        # Local network info
        self.local_ip = self._get_local_ip()
        self.gateway = self._detect_gateway()
        self.network_range = self._detect_network_range()
        
    def _get_local_ip(self) -> str:
        """Get local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _detect_gateway(self) -> str:
        """Detect network gateway."""
        try:
            if os.name == "nt":
                result = subprocess.run(["route", "print", "0.0.0.0"], 
                                       capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "0.0.0.0" in line:
                        parts = line.split()
                        for p in parts:
                            if p.count('.') == 3 and p != "0.0.0.0":
                                return p
            else:
                result = subprocess.run(["ip", "route"], 
                                       capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "default" in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2]
        except:
            pass
        
        # Fallback
        parts = self.local_ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.1"
    
    def _detect_network_range(self) -> str:
        """Detect local network range."""
        parts = self.local_ip.split(".")
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        return "192.168.1.0/24"
    
    def _get_mac_vendor(self, mac: str) -> str:
        """Get vendor from MAC address."""
        if not mac:
            return "Unknown"
        clean = mac.upper().replace(":", "").replace("-", "")
        if len(clean) < 6:
            return "Unknown"
        return self.MAC_VENDORS.get(clean[:6], "Unknown")
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print scanner header."""
        self.clear_screen()
        print(Fore.CYAN + "=" * 120)
        print(Fore.CYAN + "||" + Fore.GREEN + " OMNISCIENCE REAL-TIME NETWORK SCANNER " + Fore.CYAN + "||")
        print(Fore.CYAN + "||" + Fore.YELLOW + " LIVE DEVICE DISCOVERY AND PROFILING " + Fore.CYAN + "||")
        print(Fore.CYAN + "=" * 120)
        print()
    
    def _arp_scan(self, network_range: str) -> List[Dict[str, str]]:
        """ARP scan for Layer 2 discovery."""
        devices = []
        
        if not SCAPY_OK:
            return devices
        
        try:
            print(Fore.CYAN + "[*] Running ARP scan...")
            ans, _ = scapy.srp(
                scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network_range),
                timeout=3,
                verbose=0,
                retry=2
            )
            
            for _, rcv in ans:
                devices.append({
                    'ip': rcv.psrc,
                    'mac': rcv.hwsrc
                })
                
        except Exception as e:
            print(Fore.RED + f"[!] ARP scan error: {e}")
        
        return devices
    
    def _icmp_sweep(self, network_range: str) -> List[str]:
        """ICMP ping sweep."""
        devices = []
        
        try:
            print(Fore.CYAN + "[*] Running ICMP sweep...")
            network = ipaddress.ip_network(network_range, strict=False)
            ips = [str(ip) for ip in network.hosts()]
            
            def ping(ip):
                try:
                    if os.name == "nt":
                        result = subprocess.run(
                            ["ping", "-n", "1", "-w", "200", ip],
                            capture_output=True,
                            timeout=1
                        )
                        return ip if result.returncode == 0 else None
                    else:
                        result = subprocess.run(
                            ["ping", "-c", "1", "-W", "1", ip],
                            capture_output=True,
                            timeout=2
                        )
                        return ip if result.returncode == 0 else None
                except:
                    return None
            
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(ping, ip): ip for ip in ips}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        devices.append(result)
                        
        except Exception as e:
            print(Fore.RED + f"[!] ICMP sweep error: {e}")
        
        return devices
    
    def _port_scan(self, ip: str, ports: List[int] = None) -> Dict[int, str]:
        """Scan ports on a device."""
        if not ports:
            ports = self.SCAN_PORTS
        
        open_ports = {}
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    service = self._get_service_name(port)
                    open_ports[port] = service
            except:
                pass
        
        return open_ports
    
    def _get_service_name(self, port: int) -> str:
        """Get service name for port."""
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            80: "http", 110: "pop3", 135: "msrpc", 139: "netbios", 143: "imap",
            443: "https", 445: "smb", 993: "imaps", 995: "pop3s",
            1433: "mssql", 1521: "oracle", 1723: "pptp", 3306: "mysql",
            3389: "rdp", 5432: "postgresql", 5900: "vnc", 5985: "winrm",
            6379: "redis", 8080: "http-proxy", 8443: "https-alt", 27017: "mongodb"
        }
        return services.get(port, f"unknown-{port}")
    
    def _os_fingerprint(self, ip: str) -> str:
        """Basic OS fingerprinting."""
        if not SCAPY_OK:
            return "Unknown"
        
        try:
            # Try multiple ports
            for port in [80, 443, 22, 445]:
                pkt = scapy.IP(dst=ip) / scapy.TCP(dport=port, flags="S")
                resp = scapy.sr1(pkt, timeout=1, verbose=0)
                
                if resp and resp.haslayer(scapy.TCP):
                    ttl = resp.ttl
                    window = resp[scapy.TCP].window
                    
                    if ttl <= 64:
                        if window in (5840, 5720, 14600):
                            return "Linux"
                        elif window == 65535:
                            return "macOS"
                        return "Linux/Unix"
                    elif ttl <= 128:
                        return "Windows"
                    else:
                        return "Network Device"
        except:
            pass
        
        return "Unknown"
    
    def _detect_device_type(self, device: LiveDevice) -> str:
        """Detect device type from ports and vendor."""
        ports = set(device.open_ports.keys())
        
        # Check by vendor first
        vendor_lower = device.vendor.lower()
        if any(x in vendor_lower for x in ["apple", "samsung", "huawei", "xiaomi"]):
            if any(p in ports for p in [443, 8080]):
                return "mobile"
        
        # Check by ports
        if any(p in ports for p in [135, 139, 445, 3389, 5985]):
            return "windows"
        if 22 in ports and 80 not in ports and 443 not in ports:
            return "linux"
        if any(p in ports for p in [80, 443, 8080, 8443]):
            return "server"
        if any(p in ports for p in [500, 4500, 1723]):
            return "vpn"
        if any(p in ports for p in [161, 162]):
            return "network"
        
        return "unknown"
    
    def _check_vulnerabilities(self, device: LiveDevice):
        """Check for common vulnerabilities."""
        ports = set(device.open_ports.keys())
        
        # SMB vulnerabilities
        if 445 in ports:
            device.is_vulnerable.append("smb_exposed")
            # Check for anonymous SMB
            try:
                from impacket.smbconnection import SMBConnection
                conn = SMBConnection(device.ip, device.ip, timeout=3)
                conn.login("", "")
                device.can_pwn = True
                device.access_method = "smb_null"
                device.is_vulnerable.append("smb_null_session")
                conn.logoff()
            except:
                pass
        
        # SSH default creds
        if 22 in ports:
            device.is_vulnerable.append("ssh_exposed")
            # Try default credentials
            try:
                import paramiko
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                for user, pwd in [("root", ""), ("admin", "admin"), ("root", "root")]:
                    try:
                        client.connect(device.ip, username=user, password=pwd, timeout=2)
                        device.can_pwn = True
                        device.access_method = "ssh_default"
                        device.is_vulnerable.append("ssh_default_creds")
                        client.close()
                        break
                    except:
                        pass
            except:
                pass
        
        # RDP
        if 3389 in ports:
            device.is_vulnerable.append("rdp_exposed")
        
        # Databases
        if 3306 in ports:
            device.is_vulnerable.append("mysql_exposed")
        if 5432 in ports:
            device.is_vulnerable.append("postgres_exposed")
        if 27017 in ports:
            device.is_vulnerable.append("mongodb_exposed")
        if 6379 in ports:
            device.is_vulnerable.append("redis_exposed")
        
        # HTTP
        if 80 in ports or 443 in ports or 8080 in ports:
            device.is_vulnerable.append("http_exposed")
    
    def scan_device(self, ip: str, mac: str = None) -> Optional[LiveDevice]:
        """Comprehensive device scan."""
        device = LiveDevice(ip)
        
        if mac:
            device.mac = mac
            device.vendor = self._get_mac_vendor(mac)
        
        # Get hostname
        try:
            device.hostname = socket.gethostbyaddr(ip)[0]
        except:
            device.hostname = ip
        
        # Port scan
        print(Fore.CYAN + f"    [*] Scanning {ip}...")
        device.open_ports = self._port_scan(ip)
        
        if not device.open_ports:
            return None  # No open ports = not accessible
        
        # OS fingerprinting
        device.os = self._os_fingerprint(ip)
        
        # Detect device type
        device.device_type = self._detect_device_type(device)
        
        # Check vulnerabilities
        self._check_vulnerabilities(device)
        
        return device
    
    def scan_network(self, network_range: str = None) -> List[LiveDevice]:
        """Full network scan."""
        if self.scanning:
            print(Fore.YELLOW + "[!] Scan already in progress")
            return []
        
        self.scanning = True
        self._stop_event.clear()
        
        self.print_header()
        
        if not network_range:
            network_range = self.network_range
        
        print(Fore.GREEN + f"[+] Local IP: {self.local_ip}")
        print(Fore.GREEN + f"[+] Gateway: {self.gateway}")
        print(Fore.GREEN + f"[+] Network Range: {network_range}")
        print()
        
        discovered = []
        
        # Phase 1: ARP Scan
        print(Fore.CYAN + "=" * 120)
        print(Fore.CYAN + "PHASE 1: ARP SCANNING (Layer 2 Discovery)")
        print(Fore.CYAN + "=" * 120)
        
        arp_devices = self._arp_scan(network_range)
        print(Fore.GREEN + f"[+] ARP discovered: {len(arp_devices)} devices")
        
        for dev_info in arp_devices:
            if self._stop_event.is_set():
                break
            
            ip = dev_info['ip']
            mac = dev_info.get('mac')
            
            # Scan each ARP-discovered device
            device = self.scan_device(ip, mac)
            if device:
                with self._lock:
                    self.devices[ip] = device
                discovered.append(device)
        
        # Phase 2: ICMP Sweep for hosts not found by ARP
        print()
        print(Fore.CYAN + "=" * 120)
        print(Fore.CYAN + "PHASE 2: ICMP SWEEP (Additional Discovery)")
        print(Fore.CYAN + "=" * 120)
        
        icmp_devices = self._icmp_sweep(network_range)
        new_count = 0
        
        for ip in icmp_devices:
            if self._stop_event.is_set():
                break
            
            if ip not in self.devices:
                device = self.scan_device(ip)
                if device:
                    with self._lock:
                        self.devices[ip] = device
                    discovered.append(device)
                    new_count += 1
        
        print(Fore.GREEN + f"[+] ICMP discovered: {new_count} additional devices")
        
        # Display results
        self.display_results()
        
        self.scanning = False
        return discovered
    
    def display_results(self):
        """Display scan results."""
        self.print_header()
        
        if not self.devices:
            print(Fore.RED + "[!] No devices discovered")
            return
        
        # Sort devices by IP
        sorted_devices = sorted(
            self.devices.values(),
            key=lambda d: tuple(map(int, d.ip.split('.')))
        )
        
        print(Fore.WHITE + "=" * 120)
        print(Fore.WHITE + "| IP Address      | MAC Address       | Hostname            | OS            | Type     | Ports | Pwn |")
        print(Fore.WHITE + "=" * 120)
        
        for dev in sorted_devices:
            ip = dev.ip[:15].ljust(15)
            mac = (dev.mac or "N/A")[:17].ljust(17)
            hostname = (dev.hostname or dev.ip)[:18].ljust(18)
            os_type = (dev.os or "Unknown")[:13].ljust(13)
            dev_type = (dev.device_type or "unknown")[:7].ljust(7)
            ports = str(len(dev.open_ports)).ljust(5)
            pwn = Fore.GREEN + "YES" + Fore.WHITE if dev.can_pwn else Fore.RED + "NO" + Fore.WHITE
            
            # Color based on vulnerability
            if dev.can_pwn:
                color = Fore.RED
            elif dev.is_vulnerable:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
            
            print(color + f"| {ip} | {mac} | {hostname} | {os_type} | {dev_type} | {ports} | {pwn} |")
        
        print(Fore.WHITE + "=" * 120)
        print()
        
        # Show vulnerable devices
        vuln_devices = [d for d in self.devices.values() if d.can_pwn or d.is_vulnerable]
        
        if vuln_devices:
            print(Fore.RED + "=" * 120)
            print(Fore.RED + "VULNERABLE / ACCESSIBLE DEVICES:")
            print(Fore.RED + "=" * 120)
            
            for dev in vuln_devices:
                print()
                print(Fore.YELLOW + f"  [{dev.ip}] {dev.hostname or 'N/A'}")
                print(Fore.WHITE + f"    OS: {dev.os or 'Unknown'} | Type: {dev.device_type or 'unknown'}")
                print(Fore.WHITE + f"    Ports: {list(dev.open_ports.keys())}")
                
                if dev.is_vulnerable:
                    print(Fore.RED + f"    Vulnerabilities: {', '.join(dev.is_vulnerable[:5])}")
                
                if dev.access_method:
                    print(Fore.RED + f"    Access Method: {dev.access_method}")
        
        print()
        print(Fore.CYAN + "=" * 120)
        stats = f"Total: {len(self.devices)} | Vulnerable: {len([d for d in self.devices.values() if d.is_vulnerable])} | Accessible: {len([d for d in self.devices.values() if d.can_pwn])}"
        print(Fore.CYAN + stats)
        print(Fore.CYAN + "=" * 120)
    
    def export_results(self, filename: str = None) -> str:
        """Export results to JSON."""
        if not filename:
            filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'network_range': self.network_range,
            'local_ip': self.local_ip,
            'gateway': self.gateway,
            'devices': [d.to_dict() for d in self.devices.values()]
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(Fore.GREEN + f"[+] Results exported to {filename}")
        return filename
    
    def stop_scan(self):
        """Stop current scan."""
        self._stop_event.set()
        self.scanning = False
    
    def interactive_mode(self):
        """Interactive scanner mode."""
        self.print_header()
        
        print(Fore.CYAN + "REAL-TIME NETWORK SCANNER")
        print(Fore.YELLOW + "Commands: scan [network], show, export, monitor, help, exit")
        print()
        
        while True:
            try:
                cmd_input = input(Fore.GREEN + "SCANNER> " + Fore.WHITE).strip()
                
                if not cmd_input:
                    continue
                
                parts = cmd_input.split()
                cmd = parts[0].lower()
                
                if cmd in ['exit', 'quit']:
                    print(Fore.YELLOW + "[*] Exiting scanner...")
                    break
                
                elif cmd == 'help':
                    print()
                    print(Fore.CYAN + "Commands:")
                    print(Fore.WHITE + "  scan [network]  - Scan network (default: local subnet)")
                    print(Fore.WHITE + "  show           - Display discovered devices")
                    print(Fore.WHITE + "  export [file]  - Export results to JSON")
                    print(Fore.WHITE + "  monitor        - Continuous monitoring (60s interval)")
                    print(Fore.WHITE + "  stop           - Stop current scan/monitor")
                    print(Fore.WHITE + "  clear          - Clear device cache")
                    print(Fore.WHITE + "  exit           - Exit scanner")
                    print()
                
                elif cmd == 'scan':
                    network = parts[1] if len(parts) > 1 else None
                    self.scan_network(network)
                
                elif cmd == 'show':
                    self.display_results()
                
                elif cmd == 'export':
                    filename = parts[1] if len(parts) > 1 else None
                    self.export_results(filename)
                
                elif cmd == 'monitor':
                    print(Fore.CYAN + "[*] Starting monitor mode (60s interval, Ctrl+C to stop)...")
                    try:
                        while True:
                            self.scan_network()
                            print(Fore.YELLOW + "[*] Next scan in 60 seconds... (Ctrl+C to stop)")
                            for i in range(60):
                                if self._stop_event.is_set():
                                    break
                                time.sleep(1)
                    except KeyboardInterrupt:
                        print(Fore.YELLOW + "\n[*] Monitor mode stopped")
                
                elif cmd == 'stop':
                    self.stop_scan()
                    print(Fore.YELLOW + "[*] Scan stopped")
                
                elif cmd == 'clear':
                    self.devices.clear()
                    print(Fore.GREEN + "[+] Device cache cleared")
                
                else:
                    print(Fore.YELLOW + f"[!] Unknown command: {cmd}")
                    print(Fore.YELLOW + "    Type 'help' for available commands")
            
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n[*] Use 'exit' to quit")
            except Exception as e:
                print(Fore.RED + f"[!] Error: {e}")


if __name__ == "__main__":
    scanner = LiveNetworkScanner()
    scanner.interactive_mode()
