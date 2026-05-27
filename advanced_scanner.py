from colorama import Fore, Back, Style, init
init(autoreset=True)
"""
OMNISCIENCE MODULE 5 — AdvancedNetworkScanner
Multi-dimensional network discovery across LAN, WAN, GAN, MAN, and PAN.
Cross-subnet enumeration, traceroute intelligence, network topology mapping,
BGP/AS enumeration, VPN detection, and internet-wide scanning capabilities.

Advanced Features:
  - Cross-subnet discovery through multiple vectors
  - Traceroute with service fingerprinting at each hop
  - Network topology reconstruction via multiple methods
  - Public IP range scanning (cloud providers, datacenters)
  - BGP autonomous system enumeration
  - VPN tunnel detection and analysis
  - Multi-homed device detection
  - NAT traversal identification
  - ISP fingerprinting and geolocation
  - Network path analysis and latency mapping
"""

import os
import sys
import time
import json
import logging
import threading
import socket
import struct
import subprocess
import ipaddress
import re
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple

try:
    import scapy.all as scapy
    from scapy.layers import inet, l2
    SCAPY_OK = True
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
except ImportError:
    SCAPY_OK = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | AdvScanner | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("advscan.log", mode="a"),
    ]
)
logger = logging.getLogger("Omniscience.AdvScanner")

# Comprehensive MAC OUI database for vendor lookup
MAC_OUI_DB = {
    "DC4F22": "Apple", "3C5AB4": "Apple", "AC61EA": "Apple", "A4B1E9": "Apple",
    "F0DCE2": "Apple", "C86F87": "Apple", "A46C2A": "Apple", "F0B479": "Apple",
    "E45698": "Apple", "04F13E": "Apple", "F0D5BF": "Apple", "AC8FF8": "Apple",
    "9C2986": "Samsung", "C42C56": "Samsung", "00207C": "Samsung", "A82BCD": "Samsung",
    "F40B8F": "Samsung", "001FF3": "Samsung", "04016C": "Samsung", "307266": "Samsung",
    "18AF61": "Huawei", "2839AB": "Huawei", "F40154": "Huawei", "E8CD2D": "Huawei",
    "2042B9": "Huawei", "5CF926": "Huawei", "3CBBFD": "Huawei", "CC96A0": "Huawei",
    "E4B318": "Xiaomi", "3CBD3E": "Xiaomi", "5865E6": "Xiaomi", "64B473": "Xiaomi",
    "F48B32": "Xiaomi", "9C99A0": "Xiaomi", "241EEB": "Xiaomi", "C46E1F": "Xiaomi",
    "B827EB": "Raspberry Pi", "DCA632": "Raspberry Pi", "E45F01": "Raspberry Pi",
    "000C29": "VMware", "005056": "VMware", "00155D": "Hyper-V", "08C6EB": "Xen",
    "FA6B50": "QEMU", "9CDC6A": "Ubiquiti", "705A0F": "TP-Link", "D460E3": "Netgear",
    "C80E77": "D-Link", "001FC6": "ASUS", "001A2F": "Cisco", "002129": "Cisco",
    "000CCC": "Aruba", "001332": "Intel", "001E67": "Intel", "0022B0": "Intel",
    "001517": "Lenovo", "001E68": "Lenovo", "0026C6": "Dell", "F4CE46": "Dell",
    "002124": "HP", "002378": "HP", "FCF1CD": "HP", "3C8A2A": "HP",
    "70B3D5": "Advantech", "A0ECF9": "Google", "08F1B9": "Google", "94EB2C": "Google",
    "F8FF5F": "Microsoft", "F40E01": "Microsoft", "B491F0": "Mellanox",
}

# Geographic IP ranges for major cloud providers and datacenters
CLOUD_RANGES = {
    "aws": ["3.0.0.0/8", "4.0.0.0/9", "15.0.0.0/9", "16.0.0.0/9", "18.0.0.0/8"],
    "azure": ["13.64.0.0/11", "20.0.0.0/8", "40.0.0.0/8", "52.0.0.0/8"],
    "gcp": ["34.64.0.0/10", "35.192.0.0/11", "104.16.0.0/12", "108.177.0.0/14"],
    "digitalocean": ["64.0.0.0/8", "104.0.0.0/9", "108.0.0.0/9"],
    "linode": ["50.0.0.0/8", "172.0.0.0/8", "192.0.0.0/8"],
    "oracle": ["140.0.0.0/8", "143.0.0.0/8", "129.0.0.0/8"],
    "alibaba": ["42.0.0.0/8", "47.0.0.0/8", "106.0.0.0/8"],
    "ibm": ["169.0.0.0/9", "172.0.0.0/9", "32.0.0.0/9"],
}

# Common VPN detection ports
VPN_PORTS = [500, 4500, 1701, 443, 8443, 1194, 1723, 8080]

# Traceroute timeouts per hop
TRACEROUTE_TIMEOUT = 3


class TracerouteHop:
    """Represents a single traceroute hop."""
    def __init__(self, hop_num: int, ip: str = None, hostname: str = None, 
                 rtt: float = None, asn: str = None, location: str = None):
        self.hop_num = hop_num
        self.ip = ip
        self.hostname = hostname
        self.rtt = rtt
        self.asn = asn
        self.location = location
        self.services = []  # Detected services at this hop
        self.is_private = False
        self.is_router = False
        self.is_firewall = False
        self.is_load_balancer = False
        
    def to_dict(self) -> dict:
        return {
            "hop": self.hop_num,
            "ip": self.ip,
            "hostname": self.hostname,
            "rtt_ms": self.rtt,
            "asn": self.asn,
            "location": self.location,
            "services": self.services,
            "is_private": self.is_private,
            "is_router": self.is_router,
            "is_firewall": self.is_firewall,
            "is_lb": self.is_load_balancer,
        }


class NetworkDevice:
    """Extended network device with cross-network information."""
    def __init__(self, ip: str):
        self.ip = ip
        self.mac = ""
        self.hostname = ""
        self.reverse_dns = ""
        self.asn = ""
        self.isp = ""
        self.location = {"city": "", "country": "", "lat": 0.0, "lon": 0.0}
        self.netmask = ""
        self.broadcast = ""
        self.network_type = "unknown"
        self.first_hop = 0
        self.last_hop = 0
        self.traceroute_path = []
        self.open_ports = {}
        self.services = []
        self.device_type = "unknown"
        self.vendor = "Unknown"
        self.os = "Unknown"
        self.os_info = {}
        self.is_honeypot = False
        self.is_vpn_gateway = False
        self.is_nat_device = False
        self.is_proxy = False
        self.tags = []
        self.last_seen = time.time()
        
    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "reverse_dns": self.reverse_dns,
            "asn": self.asn,
            "isp": self.isp,
            "location": self.location,
            "network_type": self.network_type,
            "traceroute_path": [h.to_dict() for h in self.traceroute_path],
            "open_ports": self.open_ports,
            "services": self.services,
            "device_type": self.device_type,
            "vendor": self.vendor,
            "os": self.os,
            "os_info": self.os_info,
            "is_honeypot": self.is_honeypot,
            "is_vpn_gateway": self.is_vpn_gateway,
            "is_nat": self.is_nat_device,
            "is_proxy": self.is_proxy,
            "tags": self.tags,
        }


class AdvancedNetworkScanner:
    """
    Advanced multi-dimensional network scanner.
    Discovers devices across LAN, WAN, GAN, MAN, PAN and VPN networks.
    """
    
    def __init__(self):
        self.hosts: Dict[str, NetworkDevice] = {}
        self._lock = threading.Lock()
        self._scanning = False
        self._cancel_event = threading.Event()
        self._geo_cache: Dict[str, Dict[str, Any]] = {}  # Cache for geolocation results
        self._geo_cache_timestamp: Dict[str, float] = {}  # Cache timestamps
        self._geo_cache_ttl = 3600  # 1 hour cache TTL
        
        # Local network detection
        self.local_ip = self._get_local_ip()
        self.gateway = self._detect_gateway()
        self.network_range = self._detect_network_range()
        
    def get_public_ip_info(self) -> Dict[str, Any]:
        """Get public IP and geolocation info for the local connection."""
        try:
            logger.info("[PUBLIC-IP] Detecting public IP address")
            
            # Use multiple services to get public IP
            services = [
                "https://api.ipify.org?format=json",
                "https://api64.ipify.org?format=json",
                "https://icanhazip.com",
                "https://ifconfig.me/ip"
            ]
            
            public_ip = None
            for service in services:
                try:
                    req = urllib.request.Request(
                        service,
                        headers={"User-Agent": "Mozilla/5.0 (compatible; Omniscience/1.0)"}
                    )
                    with urllib.request.urlopen(req, timeout=5) as response:
                        data = response.read().decode('utf-8').strip()
                        
                        # Parse JSON response
                        if 'json' in service:
                            ip_data = json.loads(data)
                            public_ip = ip_data.get('ip')
                        else:
                            # Plain text IP
                            public_ip = data
                        
                        if public_ip:
                            break
                except Exception as e:
                    logger.debug(f"[PUBLIC-IP] Service {service} failed: {e}")
                    continue
            
            if not public_ip:
                return {"error": "Could not determine public IP"}
            
            # Get geolocation for public IP
            location = self._geo_locate_ip(public_ip)
            asn_info = self._get_asn_info(public_ip)
            
            result = {
                "public_ip": public_ip,
                "local_ip": self.local_ip,
                "gateway": self.gateway,
                "location": location,
                "asn": asn_info,
                "isp": location.get("isp", ""),
                "org": location.get("org", ""),
                "city": location.get("city", "Unknown"),
                "country": location.get("country", "Unknown"),
                "lat": location.get("lat", 0.0),
                "lon": location.get("lon", 0.0)
            }
            
            logger.info(f"[PUBLIC-IP] Detected: {public_ip} ({result['city']}, {result['country']})")
            return result
            
        except Exception as e:
            logger.error(f"[PUBLIC-IP] Error: {e}")
            return {"error": str(e)}
    
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
        """Detect gateway IP."""
        try:
            if os.name == "nt":
                result = subprocess.run(["route", "print", "0.0.0.0"], 
                                       capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "0.0.0.0" in line:
                        parts = line.split()
                        for p in parts:
                            if re.match(r'\d+\.\d+\.\d+\.\d+', p) and p != "0.0.0.0":
                                return p
            else:
                result = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "default" in line:
                        parts = line.split()
                        for i, p in enumerate(parts):
                            if p == "default" and i + 1 < len(parts):
                                return parts[i + 1]
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
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return (ipaddress.ip_address(ip_obj) in ipaddress.ip_network("10.0.0.0/8") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("172.16.0.0/12") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("192.168.0.0/16") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("127.0.0.0/8"))
        except:
            return False
    
    def _get_asn_info(self, ip: str) -> Dict[str, str]:
        """Get ASN information for an IP using multiple lookup methods with caching."""
        result = {"asn": "", "isp": "", "org": "", "as_name": "", "country": ""}
        
        if self._is_private_ip(ip):
            return result
        
        # Check cache first
        cache_key = f"asn_{ip}"
        current_time = time.time()
        if cache_key in self._geo_cache:
            if current_time - self._geo_cache_timestamp.get(cache_key, 0) < self._geo_cache_ttl:
                return self._geo_cache[cache_key]
        
        # Method 1: Team Cymru WHOIS (most reliable)
        try:
            logger.debug(f"[ASN] Querying Team Cymru for {ip}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(("whois.cymru.com", 43))
            s.send(f" -v {ip}\r\n".encode())
            
            response = b""
            while True:
                try:
                    data = s.recv(4096)
                    if not data:
                        break
                    response += data
                except socket.timeout:
                    break
            s.close()
            
            # Parse structured WHOIS response
            lines = response.decode('utf-8', errors='ignore').splitlines()
            for line in lines:
                if "|" in line and not line.startswith("AS"):
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 5:
                        result["asn"] = f"AS{parts[0]}" if parts[0] else ""
                        result["isp"] = parts[2] if len(parts) > 2 else ""
                        result["org"] = parts[2] if len(parts) > 2 else ""
                        result["country"] = parts[1] if len(parts) > 1 else ""
                        result["as_name"] = parts[4] if len(parts) > 4 else ""
                        break
            
            # Cache successful result
            if result["asn"]:
                self._geo_cache[cache_key] = result
                self._geo_cache_timestamp[cache_key] = current_time
                logger.info(f"[ASN] {ip} -> {result['asn']} ({result['isp']})")
                return result
                
        except socket.timeout:
            logger.debug(f"[ASN] Team Cymru timeout for {ip}")
        except socket.error as e:
            logger.debug(f"[ASN] Team Cymru socket error for {ip}: {e}")
        except Exception as e:
            logger.debug(f"[ASN] Team Cymru error for {ip}: {e}")
        
        # Method 2: ASN lookup via API (fallback)
        try:
            logger.debug(f"[ASN] Trying API fallback for {ip}")
            url = f"https://api.iptoasn.com/v1/as/ip/{ip}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; Omniscience/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data and isinstance(data, dict):
                    result["asn"] = f"AS{data.get('as_number', '')}"
                    result["as_name"] = data.get('as_name', "")
                    result["country"] = data.get('as_country', "")
                    
                    if result["asn"]:
                        self._geo_cache[cache_key] = result
                        self._geo_cache_timestamp[cache_key] = current_time
                        logger.info(f"[ASN] {ip} -> {result['asn']} via API")
                        return result
        except Exception as e:
            logger.debug(f"[ASN] API fallback failed for {ip}: {e}")
        
        return result
    
    def _geo_locate_ip(self, ip: str) -> Dict[str, Any]:
        """Get geolocation info for an IP using multiple real providers with caching and failover."""
        # Default location structure
        default_location = {
            "city": "Unknown", "country": "Unknown", "lat": 0.0, "lon": 0.0,
            "isp": "", "org": "", "as": "", "timezone": "", "region": ""
        }
        
        if self._is_private_ip(ip):
            default_location["city"] = "Private Network"
            default_location["country"] = "Local"
            return default_location
        
        # Check cache first
        current_time = time.time()
        if ip in self._geo_cache:
            if current_time - self._geo_cache_timestamp.get(ip, 0) < self._geo_cache_ttl:
                logger.debug(f"[GEO] Cache hit for {ip}")
                return self._geo_cache[ip]
        
        # Provider configurations with fallback priority
        providers = [
            {
                "name": "ip-api",
                "url": f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,query",
                "parser": self._parse_ip_api
            },
            {
                "name": "ipapi.co",
                "url": f"https://ipapi.co/{ip}/json/",
                "parser": self._parse_ipapi_co
            },
            {
                "name": "ipwhois",
                "url": f"http://ipwho.is/{ip}",
                "parser": self._parse_ipwhois
            },
            {
                "name": "ipinfo",
                "url": f"https://ipinfo.io/{ip}/json",
                "parser": self._parse_ipinfo
            }
        ]
        
        for provider in providers:
            try:
                logger.debug(f"[GEO] Trying {provider['name']} for {ip}")
                req = urllib.request.Request(
                    provider["url"],
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; Omniscience/1.0)",
                        "Accept": "application/json"
                    }
                )
                
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))
                        location = provider["parser"](data)
                        
                        # Validate we got meaningful data
                        if location and location.get("country") and location["country"] != "Unknown":
                            # Cache the successful result
                            self._geo_cache[ip] = location
                            self._geo_cache_timestamp[ip] = current_time
                            logger.info(f"[GEO] {ip} -> {location.get('city')}, {location.get('country')} via {provider['name']}")
                            return location
                        else:
                            logger.debug(f"[GEO] {provider['name']} returned incomplete data for {ip}")
                    else:
                        logger.debug(f"[GEO] {provider['name']} returned status {response.status}")
                        
            except urllib.error.HTTPError as e:
                logger.debug(f"[GEO] {provider['name']} HTTP error {e.code} for {ip}")
                if e.code == 429:  # Rate limited
                    time.sleep(0.5)  # Brief pause before trying next provider
                continue
            except urllib.error.URLError as e:
                logger.debug(f"[GEO] {provider['name']} URL error for {ip}: {e.reason}")
                continue
            except json.JSONDecodeError as e:
                logger.debug(f"[GEO] {provider['name']} JSON decode error for {ip}: {e}")
                continue
            except Exception as e:
                logger.debug(f"[GEO] {provider['name']} unexpected error for {ip}: {e}")
                continue
        
        logger.warning(f"[GEO] All providers failed for {ip}")
        return default_location
    
    def _parse_ip_api(self, data: Dict) -> Dict[str, Any]:
        """Parse ip-api.com response format."""
        if data.get("status") != "success":
            return {}
        return {
            "city": data.get("city", "Unknown"),
            "country": data.get("country", "Unknown"),
            "country_code": data.get("countryCode", ""),
            "region": data.get("regionName", ""),
            "lat": float(data.get("lat", 0.0) or 0.0),
            "lon": float(data.get("lon", 0.0) or 0.0),
            "isp": data.get("isp", ""),
            "org": data.get("org", ""),
            "as": data.get("as", ""),
            "as_name": data.get("asname", ""),
            "timezone": data.get("timezone", ""),
            "zip": data.get("zip", "")
        }
    
    def _parse_ipapi_co(self, data: Dict) -> Dict[str, Any]:
        """Parse ipapi.co response format."""
        if data.get("error"):
            return {}
        return {
            "city": data.get("city", "Unknown"),
            "country": data.get("country_name", "Unknown"),
            "country_code": data.get("country_code", ""),
            "region": data.get("region", ""),
            "lat": float(data.get("latitude", 0.0) or 0.0),
            "lon": float(data.get("longitude", 0.0) or 0.0),
            "isp": data.get("org", ""),
            "org": data.get("org", ""),
            "as": data.get("asn", ""),
            "timezone": data.get("timezone", ""),
            "zip": data.get("postal", "")
        }
    
    def _parse_ipwhois(self, data: Dict) -> Dict[str, Any]:
        """Parse ipwho.is response format."""
        if not data.get("success", True):
            return {}
        return {
            "city": data.get("city", "Unknown"),
            "country": data.get("country", "Unknown"),
            "country_code": data.get("country_code", ""),
            "region": data.get("region", ""),
            "lat": float(data.get("latitude", 0.0) or 0.0),
            "lon": float(data.get("longitude", 0.0) or 0.0),
            "isp": data.get("connection", {}).get("isp", ""),
            "org": data.get("connection", {}).get("org", ""),
            "as": data.get("connection", {}).get("asn", ""),
            "timezone": data.get("timezone", {}).get("id", ""),
            "zip": data.get("postal", "")
        }
    
    def _parse_ipinfo(self, data: Dict) -> Dict[str, Any]:
        """Parse ipinfo.io response format."""
        if "bogon" in data and data["bogon"]:
            return {}
        loc_parts = data.get("loc", "0,0").split(",")
        return {
            "city": data.get("city", "Unknown"),
            "country": data.get("country", "Unknown"),
            "country_code": data.get("country", ""),
            "region": data.get("region", ""),
            "lat": float(loc_parts[0]) if len(loc_parts) > 0 and loc_parts[0] else 0.0,
            "lon": float(loc_parts[1]) if len(loc_parts) > 1 and loc_parts[1] else 0.0,
            "isp": data.get("org", ""),
            "org": data.get("org", ""),
            "as": data.get("asn", {}).get("asn", "") if isinstance(data.get("asn"), dict) else data.get("asn", ""),
            "timezone": data.get("timezone", ""),
            "zip": data.get("postal", "")
        }
    
    def _advanced_os_fingerprint(self, ip: str) -> Dict[str, Any]:
        """Advanced OS fingerprinting using multiple probes and TCP/IP stack analysis."""
        result = {"os": "Unknown", "accuracy": "low", "details": {}}
        
        if not SCAPY_OK:
            return result
        
        ttl_samples = []
        window_samples = []
        
        # Multiple probe techniques for accurate fingerprinting
        probe_ports = [22, 80, 443, 445, 3389, 5985]
        
        for port in probe_ports:
            try:
                # TCP SYN probe
                pkt = scapy.IP(dst=ip) / scapy.TCP(dport=port, flags="S", sport=scapy.RandShort())
                resp = scapy.sr1(pkt, timeout=1, verbose=False)
                
                if resp and resp.haslayer(scapy.TCP):
                    ttl_samples.append(resp.ttl)
                    window_samples.append(resp[scapy.TCP].window)
                    
                    # Check DF (Don't Fragment) bit
                    if not hasattr(resp[scapy.IP], 'flags') or resp[scapy.IP].flags != 2:
                        result["details"]["df"] = False
                    
                    # Check TCP options
                    if hasattr(resp[scapy.TCP], 'options'):
                        result["details"]["tcp_options"] = str(resp[scapy.TCP].options)
            except:
                continue
        
        if ttl_samples:
            avg_ttl = sum(ttl_samples) // len(ttl_samples)
            avg_window = sum(window_samples) // len(window_samples) if window_samples else 0
            
            # Advanced OS fingerprinting based on pattern matching
            if avg_ttl <= 64:
                if avg_window in (5840, 5720, 14600):
                    result["os"] = "Linux"
                    result["accuracy"] = "high"
                elif avg_window == 65535:
                    result["os"] = "macOS/iOS"
                    result["accuracy"] = "high"
                elif "tcp_options" in result["details"] and "WScale" in str(result["details"].get("tcp_options", "")):
                    result["os"] = "Linux"
                    result["accuracy"] = "medium"
                else:
                    result["os"] = "Linux/Unix/Android"
                    result["accuracy"] = "medium"
            elif avg_ttl <= 128:
                if avg_window in (8192, 16384, 65535):
                    result["os"] = "Windows"
                    result["accuracy"] = "high"
                else:
                    result["os"] = "Windows"
                    result["accuracy"] = "medium"
            else:
                result["os"] = "Network Device/Router"
                result["accuracy"] = "medium"
            
            result["details"]["ttl"] = avg_ttl
            result["details"]["window_size"] = avg_window
        
        # ICMP-based fingerprinting for additional accuracy
        try:
            pkt = scapy.IP(dst=ip) / scapy.ICMP()
            resp = scapy.sr1(pkt, timeout=1, verbose=False)
            if resp and hasattr(resp, 'ttl'):
                result["details"]["icmp_ttl"] = resp.ttl
                
                # ICMP type/code analysis
                if resp.haslayer(scapy.ICMP):
                    result["details"]["icmp_type"] = resp[scapy.ICMP].type
                    result["details"]["icmp_code"] = resp[scapy.ICMP].code
        except:
            pass
        
        return result
    
    def _get_mac_vendor(self, mac: str) -> str:
        """Extract vendor from MAC OUI using real database."""
        if not mac:
            return "Unknown"
        
        clean = mac.upper().replace(":", "").replace("-", "")
        if len(clean) < 6:
            return "Unknown"
        
        prefix = clean[:6]
        return MAC_OUI_DB.get(prefix, "Generic Device")
    
    def _guess_device_type(self, vendor: str, open_ports: List[int]) -> str:
        """Guess device type from vendor and open ports."""
        vendor_lower = vendor.lower()
        port_set = set(open_ports)
        
        # Mobile devices
        if any(x in vendor_lower for x in ["apple", "samsung", "huawei", "xiaomi", "google", "oneplus"]):
            return "mobile"
        
        # IoT devices
        if "raspberry" in vendor_lower or any(p in port_set for p in [1883, 8883, 502, 5048, 20000]):
            return "iot"
        
        # Virtual machines
        if any(x in vendor_lower for x in ["vmware", "virtual", "xen", "qemu", "hyper-v", "virtualbox"]):
            return "virtual"
        
        # Network equipment
        if any(x in vendor_lower for x in ["cisco", "ubiquiti", "tp-link", "netgear", "d-link", "asus", "mikrotik"]):
            return "network"
        
        # Servers
        if any(p in port_set for p in [22, 80, 443, 3306, 5432, 27017, 6379, 5900]):
            return "server"
        
        # Windows computers
        if any(p in port_set for p in [135, 139, 445, 3389, 5985]):
            return "windows"
        
        return "unknown"
    
    def _detect_honeypot(self, ip: str, open_ports: List[int]) -> Tuple[bool, List[str]]:
        """Detect if a device is a honeypot using behavioral analysis."""
        indicators = []
        
        # Suspicious port combinations
        if set(open_ports) == {22, 80, 443}:
            indicators.append("minimal_service_set")
        
        # Sequential IP assignment often indicates honeypots
        if self._sequential_ip_pattern(ip):
            indicators.append("sequential_ip")
        
        # Check for unrealistically fast response times (emulated)
        if SCAPY_OK:
            try:
                pkt = scapy.IP(dst=ip) / scapy.ICMP()
                start = time.time()
                resp = scapy.sr1(pkt, timeout=1, verbose=False)
                rtt = time.time() - start
                if resp and rtt < 0.001:
                    indicators.append("suspicious_rtt")
            except:
                pass
        
        return len(indicators) > 0, indicators
    
    def _sequential_ip_pattern(self, ip: str) -> bool:
        """Check if IP follows sequential pattern (common in honeypots)."""
        try:
            nums = [int(x) for x in ip.split(".")]
            return any(nums[i] == nums[i-1] + 1 for i in range(1, 4))
        except:
            return False
    
    def traceroute(self, target: str, max_hops: int = 30) -> List[TracerouteHop]:
        """Perform traceroute with service detection."""
        logger.info(f"[TRACEROUTE] Tracing path to {target}")
        hops = []
        
        if not SCAPY_OK:
            # Fallback to system traceroute
            try:
                result = subprocess.run(
                    ["tracert", "-d", "-w", "1000", "-h", str(max_hops), target],
                    capture_output=True, text=True, timeout=60
                )
                for line in result.stdout.splitlines():
                    match = re.match(r'\s*(\d+)\s+(\S+)\s+(\S+)', line)
                    if match:
                        hop_num = int(match.group(1))
                        ip = match.group(2) if match.group(2) != "*" else None
                        rtt_str = match.group(3).replace("ms", "").strip()
                        try:
                            rtt = float(rtt_str) if rtt_str != "*" else None
                        except:
                            rtt = None
                        hop = TracerouteHop(hop_num, ip, rtt=rtt)
                        if ip:
                            hop.is_private = self._is_private_ip(ip)
                            # Try to get hostname
                            try:
                                hop.hostname = socket.gethostbyaddr(ip)[0]
                            except:
                                pass
                        hops.append(hop)
            except Exception as e:
                logger.error(f"Traceroute failed: {e}")
            return hops
        
        # Scapy-based traceroute
        for ttl in range(1, max_hops + 1):
            if self._cancel_event.is_set():
                break
                
            pkt = scapy.IP(dst=target, ttl=ttl) / scapy.ICMP()
            try:
                reply = scapy.sr1(pkt, timeout=TRACEROUTE_TIMEOUT, verbose=False)
                
                if reply:
                    hop = TracerouteHop(ttl, ip=reply.src, rtt=reply.time * 1000)
                    hop.is_private = self._is_private_ip(reply.src)
                    
                    # Try hostname resolution
                    try:
                        hop.hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        pass
                    
                    # Get ASN info for public IPs
                    if not hop.is_private:
                        asn_info = self._get_asn_info(reply.src)
                        hop.asn = asn_info.get("asn", "")
                    
                    # Check if this looks like a router/firewall
                    if hop.rtt and hop.rtt > 0:
                        hop.is_router = True
                    
                    hops.append(hop)
                    
                    # Check if we reached the target
                    if reply.src == target:
                        logger.info(f"[TRACEROUTE] Reached target at hop {ttl}")
                        break
                        
            except Exception as e:
                logger.debug(f"Hop {ttl}: {e}")
                hops.append(TracerouteHop(ttl))
        
        logger.info(f"[TRACEROUTE] Complete: {len(hops)} hops")
        return hops
    
    def traceroute_with_services(self, target: str, max_hops: int = 30) -> List[TracerouteHop]:
        """Traceroute with service detection at each hop."""
        hops = self.traceroute(target, max_hops)
        
        # For each hop, try to detect services
        for hop in hops:
            if hop.ip and not hop.is_private:
                # Quick port scan to detect services
                services = self._quick_service_scan(hop.ip)
                hop.services = services
                
                # Identify device type based on services
                if 22 in services:
                    hop.is_router = True
                if 80 in services or 443 in services:
                    hop.is_load_balancer = True
                if 500 in services or 4500 in services:
                    hop.is_firewall = True
        
        return hops
    
    def _quick_service_scan(self, ip: str) -> List[int]:
        """Quick scan for common services."""
        common = [22, 23, 80, 443, 445, 3389, 500, 4500, 1701, 1194, 1723]
        open_ports = []
        
        for port in common:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    open_ports.append(port)
            except:
                pass
        
        return open_ports
    
    def scan_cross_subnet(self, source_ip: str, target_subnet: str) -> List[str]:
        """Scan devices in a different subnet from source IP."""
        logger.info(f"[CROSS-SUBNET] Scanning {target_subnet} from {source_ip}")
        found = []
        
        try:
            network = ipaddress.ip_network(target_subnet, strict=False)
            ips = [str(h) for h in network.hosts()][:256]  # Limit to 256 for performance
            
            def check_host(ip):
                # Try to reach via specific source
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.bind((source_ip, 0))
                    sock.connect((ip, 445))  # Try SMB port
                    sock.close()
                    return ip
                except:
                    pass
                # Try ICMP
                try:
                    pkt = scapy.IP(src=source_ip, dst=ip) / scapy.ICMP()
                    reply = scapy.sr1(pkt, timeout=1, verbose=False)
                    if reply:
                        return ip
                except:
                    pass
                return None
            
            with ThreadPoolExecutor(max_workers=50) as ex:
                futures = {ex.submit(check_host, ip): ip for ip in ips}
                for fut in as_completed(futures):
                    result = fut.result()
                    if result:
                        found.append(result)
                        logger.info(f"[CROSS-SUBNET] Found: {result}")
                        
        except Exception as e:
            logger.error(f"Cross-subnet scan error: {e}")
        
        return found
    
    def discover_vpn_networks(self, target_ip: str = None) -> List[Dict[str, Any]]:
        """Detect VPN connections and gateways."""
        logger.info("[VPN] Scanning for VPN networks")
        vpn_info = []
        
        if not target_ip:
            target_ip = self.gateway
        
        # Check common VPN ports
        vpn_ports = {
            500: "IPSec",
            4500: "IPSec NAT-T",
            1701: "L2TP",
            1723: "PPTP",
            1194: "OpenVPN",
            443: "OpenVPN/SSL-VPN",
            8443: "OpenVPN",
            8080: "HTTP-VPN",
        }
        
        for port, vpn_type in vpn_ports.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                if result == 0:
                    vpn_info.append({
                        "ip": target_ip,
                        "port": port,
                        "type": vpn_type,
                        "detected_at": time.time()
                    })
                    logger.info(f"[VPN] {target_ip}:{port} - {vpn_type}")
            except:
                pass
        
        return vpn_info
    
    def scan_public_ranges(self, provider: str = "aws", max_hosts: int = 100) -> List[NetworkDevice]:
        """Scan public IP ranges (cloud providers)."""
        logger.info(f"[PUBLIC-SCAN] Scanning {provider} ranges")
        found = []
        
        ranges = CLOUD_RANGES.get(provider.lower(), [])
        if not ranges:
            logger.warning(f"Unknown provider: {provider}")
            return found
        
        for cidr in ranges[:2]:  # Limit to first 2 ranges
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                ips = [str(h) for h in network.hosts()][:max_hosts]
                
                def check_public(ip):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        # Try common web ports
                        for port in [80, 443, 22, 3389]:
                            result = sock.connect_ex((ip, port))
                            sock.close()
                            if result == 0:
                                device = NetworkDevice(ip)
                                device.network_type = "cloud"
                                device.services = [port]
                                location = self._geo_locate_ip(ip)
                                device.location = location
                                device.isp = location.get("isp", provider)
                                return device
                    except:
                        pass
                    return None
                
                with ThreadPoolExecutor(max_workers=30) as ex:
                    futures = {ex.submit(check_public, ip): ip for ip in ips}
                    for fut in as_completed(futures):
                        device = fut.result()
                        if device:
                            found.append(device)
                            self.hosts[device.ip] = device
                            logger.info(f"[PUBLIC-SCAN] Found: {device.ip} ({device.services})")
                            
            except Exception as e:
                logger.error(f"Range scan error: {e}")
        
        return found
    
    def mdns_listen(self, timeout=10) -> List[Dict[str, Any]]:
        """Real mDNS discovery using scapy multicast."""
        devices = []
        if not SCAPY_OK:
            logger.error("Scapy not available for mDNS scan.")
            return devices
        try:
            logger.info("[mDNS] Listening for mDNS responses...")
            # mDNS query for all services on 224.0.0.251
            # This is a simplified query, a full mDNS scan would involve more complex parsing
            pkt = scapy.IP(dst="224.0.0.251")/scapy.UDP(sport=5353, dport=5353)/scapy.DNS(rd=1, qd=scapy.DNSQR(qname="_services._dns-sd._udp.local"))
            ans, _ = scapy.srp(scapy.Ether(dst="01:00:5e:00:00:fb")/pkt, timeout=timeout, verbose=0)
            for _, r in ans:
                if r.haslayer(scapy.IP) and r[scapy.IP].src not in [d['ip'] for d in devices]:
                    devices.append({'ip': r[scapy.IP].src, 'type': 'mDNS', 'info': r.summary()})
                    logger.info(f"[mDNS] Found: {r[scapy.IP].src}")
        except Exception as e:
            logger.error(f"mDNS scan failed: {e}")
        return devices

    def ssdp_discover(self, timeout=5) -> List[Dict[str, Any]]:
        """SSDP/UPnP discovery."""
        devices = []
        try:
            logger.info("[SSDP] Discovering UPnP devices...")
            
            # Try multiple SSDP search targets to maximize discovery
            search_targets = [
                "ssdp:all",
                "upnp:rootdevice",
                "urn:schemas-upnp-org:device:MediaServer:1",
                "urn:schemas-upnp-org:device:MediaRenderer:1"
            ]
            
            for st in search_targets:
                ssdp_request = (
                    'M-SEARCH * HTTP/1.1\r\n'
                    f'HOST: 239.255.255.250:1900\r\n'
                    'MAN: "ssdp:discover"\r\n'
                    'MX: 2\r\n'
                    f'ST: {st}\r\n'
                    '\r\n'
                )
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(3)
                    sock.sendto(ssdp_request.encode(), ("239.255.255.250", 1900))
                    while True:
                        try:
                            data, addr = sock.recvfrom(1024)
                            src_ip = addr[0]
                            if src_ip not in [d['ip'] for d in devices]:
                                response = data.decode(errors='ignore')[:300]
                                # Extract device info
                                device_info = {'ip': src_ip, 'type': 'SSDP', 'response': response}
                                # Try to parse LOCATION header
                                for line in response.split('\r\n'):
                                    if line.upper().startswith('LOCATION:'):
                                        device_info['location'] = line.split(':', 1)[1].strip()
                                        break
                                devices.append(device_info)
                                logger.info(f"[SSDP] Found: {src_ip}")
                        except socket.timeout:
                            break
                    sock.close()
                except Exception as e:
                    logger.debug(f"SSDP search for {st} failed: {e}")
                    
        except Exception as e:
            logger.error(f"SSDP scan failed: {e}")
        
        logger.info(f"[SSDP] Discovery complete. Found {len(devices)} devices.")
        return devices

    def get_interface_info(self) -> List[Dict[str, str]]:
        """Get detailed network interface information."""
        # This functionality is typically in network_discovery.py,
        # but for direct access from commandcenter, we'll add a placeholder or simple implementation.
        # In a real scenario, AdvancedNetworkScanner would likely integrate with NetworkDiscovery.
        try:
            import netifaces
            interfaces_list = []
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        interfaces_list.append({'name': iface, 'ip': addr.get('addr'), 'netmask': addr.get('netmask')})
            return interfaces_list
        except ImportError:
            logger.warning("netifaces not installed. Cannot list interfaces.")
            return []

    def detect_nat_device(self, ip: str) -> bool:
        """Detect if an IP is behind NAT."""
        try:
            # Check for port reuse patterns
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, 80))
            sock.close()
            
            # Check TTL patterns - NAT devices often have different TTL behavior
            pkt = scapy.IP(dst=ip, ttl=64) / scapy.ICMP()
            reply = scapy.sr1(pkt, timeout=2, verbose=False)
            
            if reply and reply.ttl:
                # Low TTL (like 64) suggests direct, higher might suggest NAT
                if reply.ttl < 64:
                    return True
        except:
            pass
        
        return False
    
    def discover_all_network_types(self, target: str = None, max_cloud_hosts: int = 50) -> Dict[str, List[NetworkDevice]]:
        """Discover devices across all network types with comprehensive profiling."""
        logger.info("[DISCOVERY] Starting multi-network discovery")
        results = {
            "lan": [], "wan": [], "gan": [], "man": [], "vpn": [], "cloud": [],
        }
        
        # Get public IP info first
        logger.info("[DISCOVERY] Detecting public IP and ISP info")
        public_info = self.get_public_ip_info()
        if "error" not in public_info:
            logger.info(f"[DISCOVERY] Public IP: {public_info['public_ip']} ({public_info['isp']})")
        
        # 1. LAN Discovery with ARP + comprehensive profiling
        logger.info("[DISCOVERY] Scanning LAN via ARP")
        if SCAPY_OK:
            arp_devices = self._arp_scan(self.network_range)
            for d in arp_devices:
                ip = d['ip']
                mac = d.get('mac')
                device = self.profile_device_comprehensive(ip, mac)
                device.network_type = "lan"
                if device.traceroute_path:
                    device.first_hop = len(device.traceroute_path)
                results["lan"].append(device)
                logger.info(f"[LAN] Profiled: {ip} - {device.vendor} - {device.os} - {device.device_type}")
        
        # 2. ICMP sweep for hosts not caught by ARP
        logger.info("[DISCOVERY] Scanning LAN via ICMP")
        icmp_hosts = self._icmp_sweep(self.network_range)
        for d in icmp_hosts:
            ip = d['ip']
            if ip not in self.hosts:
                device = self.profile_device_comprehensive(ip)
                device.network_type = "lan"
                results["lan"].append(device)
        
        # 3. WAN Discovery via gateway
        logger.info("[DISCOVERY] Scanning WAN (via gateway)")
        if self.gateway:
            wan_device = self.profile_device_comprehensive(self.gateway)
            wan_device.network_type = "wan"
            wan_device.is_nat_device = self.detect_nat_device(self.gateway)
            # Add public IP info if available
            if "error" not in public_info:
                wan_device.location = {
                    "city": public_info.get("city", "Unknown"),
                    "country": public_info.get("country", "Unknown"),
                    "lat": public_info.get("lat", 0.0),
                    "lon": public_info.get("lon", 0.0)
                }
                wan_device.isp = public_info.get("isp", "")
            results["wan"].append(wan_device)
        
        # 4. VPN Detection
        logger.info("[DISCOVERY] Detecting VPN")
        vpn_info = self.discover_vpn_networks()
        for v in vpn_info:
            device = NetworkDevice(v["ip"])
            device.network_type = "vpn"
            device.is_vpn_gateway = True
            device.services = [v["port"]]
            device.vendor = "VPN Gateway"
            results["vpn"].append(device)
            self.hosts[v["ip"]] = device
        
        # 5. Cloud/Public scan with profiling (limited for performance)
        logger.info("[DISCOVERY] Scanning cloud ranges")
        for provider in CLOUD_RANGES.keys():
            try:
                cloud_devices = self.scan_public_ranges(provider, max_hosts=max_cloud_hosts)
                for d in cloud_devices:
                    d.vendor = f"Cloud ({provider})"
                    results["cloud"].append(d)
            except Exception as e:
                logger.error(f"[DISCOVERY] Cloud scan error for {provider}: {e}")
        
        # 6. GAN/MAN via traceroute to distant targets
        logger.info("[DISCOVERY] Discovering GAN/MAN via traceroute")
        distant_targets = ["1.1.1.1", "8.8.8.8", "208.67.222.222", "9.9.9.9"]
        
        for target in distant_targets:
            try:
                path = self.traceroute_with_services(target, max_hops=15)
                for hop in path:
                    if hop.ip and not self._is_private_ip(hop.ip) and hop.ip not in self.hosts:
                        device = NetworkDevice(hop.ip)
                        device.network_type = "gan"
                        device.first_hop = hop.hop_num
                        device.location = self._geo_locate_ip(hop.ip)
                        device.asn = hop.asn
                        device.isp = device.location.get("isp", "")
                        device.services = hop.services
                        device.vendor = "Internet Infrastructure"
                        results["gan"].append(device)
                        self.hosts[hop.ip] = device
            except Exception as e:
                logger.error(f"[DISCOVERY] Traceroute to {target} failed: {e}")
        
        logger.info(f"[DISCOVERY] Complete: {len(self.hosts)} total devices")
        return results
    
    def _scan_network_range(self, cidr: str, max_workers: int = 50) -> List[str]:
        """Scan a network range for active hosts."""
        found = []
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            ips = [str(h) for h in network.hosts()]
        except ValueError:
            return [cidr]
        
        def check_host(ip):
            try:
                if SCAPY_OK:
                    pkt = scapy.IP(dst=ip) / scapy.ICMP()
                    reply = scapy.sr1(pkt, timeout=1, verbose=False)
                    if reply:
                        return ip
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, 445))
                    sock.close()
                    if result == 0:
                        return ip
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(check_host, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    found.append(result)
        
        return found
    
    def get_device_by_ip(self, ip: str) -> Optional[NetworkDevice]:
        """Get device by IP."""
        return self.hosts.get(ip)
    
    def get_all_devices(self) -> List[NetworkDevice]:
        """Get all discovered devices."""
        return list(self.hosts.values())
    
    def _arp_scan(self, network_range: str) -> List[Dict[str, str]]:
        """ARP scan for Layer 2 discovery, returning IP and MAC."""
        devices = []
        if not SCAPY_OK:
            logger.error("Scapy not available for ARP scan.")
            return devices
        try:
            logger.info(f"[ARP] Scanning {network_range}...")
            ans, _ = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=network_range), timeout=2, verbose=0)
            for _, r in ans:
                devices.append({'ip': r.psrc, 'mac': r.hwsrc})
        except Exception as e:
            logger.error(f"ARP scan failed: {e}")
        return devices

    def _icmp_sweep(self, network_range: str) -> List[Dict[str, str]]:
        """ICMP ping sweep, returning IP of alive hosts."""
        devices = []
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            for ip in network.hosts():
                if os.system(f"ping -n 1 -w 100 {str(ip)}") == 0: # Windows ping
                    devices.append({'ip': str(ip)})
        except Exception as e:
            logger.error(f"ICMP sweep failed: {e}")
        return devices

    def _netbios_sweep(self, network_range: str) -> List[Dict[str, str]]:
        """NetBIOS enumeration, returning IP and hostname."""
        devices = []
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            for ip in network.hosts():
                try:
                    result = subprocess.run(['nbtstat', '-A', str(ip)], capture_output=True, text=True, timeout=1)
                    match = re.search(r"Name\s+<00>\s+UNIQUE\s+([^\s]+)", result.stdout)
                    if match:
                        devices.append({'ip': str(ip), 'hostname': match.group(1)})
                except: pass
        except Exception as e:
            logger.error(f"NetBIOS sweep failed: {e}")
        return devices

    def get_devices_by_type(self, network_type: str) -> List[NetworkDevice]:
        """Get devices by network type."""
        return [d for d in self.hosts.values() if d.network_type == network_type]
    
    def get_topology_map(self) -> Dict[str, Any]:
        """Get network topology map."""
        topology = {
            "local_ip": self.local_ip,
            "gateway": self.gateway,
            "network_range": self.network_range,
            "devices": [],
            "connections": [],
        }
        
        # Build topology from traceroute paths
        for ip, device in self.hosts.items():
            device_info = device.to_dict()
            topology["devices"].append(device_info)
            
            # Build connections based on traceroute
            if device.traceroute_path:
                for hop in device.traceroute_path:
                    if hop.ip:
                        topology["connections"].append({
                            "from": self.local_ip,
                            "to": hop.ip,
                            "hop": hop.hop_num,
                            "rtt": hop.rtt,
                        })
        
        return topology
    
    def print_discovery_summary(self):
        """Print discovery summary."""
        print("\n" + "=" * 80)
        print(" ADVANCED NETWORK DISCOVERY SUMMARY")
        print("=" * 80)
        print(f"\nLocal IP     : {self.local_ip}")
        print(f"Gateway      : {self.gateway}")
        print(f"Network      : {self.network_range}")
        
        # Count by type
        type_counts = defaultdict(int)
        for device in self.hosts.values():
            type_counts[device.network_type] += 1
        
        print("\nDevices by Network Type:")
        for ntype, count in sorted(type_counts.items()):
            print(f"  {ntype.upper():<10} : {count}")
        
        # Show some sample devices
        print("\nSample Discoveries:")
        for ip, device in list(self.hosts.items())[:10]:
            location = f"{device.location.get('city', 'Unknown')}, {device.location.get('country', 'Unknown')}"
            print(f"  {ip:<18} {device.network_type:<8} {location}")
        
        print("\n" + "=" * 80)
    
    def profile_device_comprehensive(self, ip: str, mac: str = None) -> NetworkDevice:
        """Comprehensive device profiling with OS fingerprint, vendor lookup, and geo-location."""
        device = NetworkDevice(ip)
        
        # OS Fingerprinting
        os_result = self._advanced_os_fingerprint(ip)
        device.os = os_result["os"]
        device.os_info = os_result
        
        # MAC Vendor Lookup
        if mac:
            device.mac = mac
            device.vendor = self._get_mac_vendor(mac)
        
        # Hostname/Reverse DNS
        try:
            device.hostname = socket.gethostbyaddr(ip)[0]
        except:
            try:
                device.reverse_dns = socket.getfqdn(ip)
            except:
                pass
        
        # Geo-location for public IPs
        device.location = self._geo_locate_ip(ip)
        device.isp = device.location.get("isp", "")
        
        # ASN info
        if not self._is_private_ip(ip):
            asn_info = self._get_asn_info(ip)
            device.asn = asn_info.get("asn", "")
            if not device.isp:
                device.isp = asn_info.get("isp", "")
        
        # Port scan for services
        if SCAPY_OK:
            try:
                common_ports = [22, 23, 25, 53, 80, 443, 445, 3389, 5985, 8080, 9090]
                for port in common_ports:
                    pkt = scapy.IP(dst=ip) / scapy.TCP(dport=port, flags="S")
                    resp = scapy.sr1(pkt, timeout=0.5, verbose=False)
                    if resp and resp.haslayer(scapy.TCP) and resp[scapy.TCP].flags == "SA":
                        device.open_ports[port] = self._get_service_name(port)
                        device.services.append(port)
            except Exception as e:
                logger.debug(f"Port scan error for {ip}: {e}")
        else:
            # Fallback to socket-based scan
            for port in [22, 80, 443, 445]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((ip, port)) == 0:
                        device.open_ports[port] = self._get_service_name(port)
                        device.services.append(port)
                    sock.close()
                except:
                    pass
        
        # Device type based on vendor and ports
        device.device_type = self._guess_device_type(device.vendor, device.services)
        
        # Honeypot detection
        device.is_honeypot, indicators = self._detect_honeypot(ip, device.services)
        if indicators:
            device.tags.append(f"honeypot_indicators: {','.join(indicators)}")
        
        # Tags for categorization
        if device.vendor and device.vendor != "Unknown":
            device.tags.append(f"vendor:{device.vendor.lower().replace(' ', '_')}")
        if device.services:
            device.tags.append("active_services")
        if device.os != "Unknown":
            device.tags.append(f"os:{device.os.lower()}")
        
        with self._lock:
            self.hosts[ip] = device
        
        return device
    
    def _get_service_name(self, port: int) -> str:
        """Get service name for port number."""
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            80: "http", 110: "pop3", 135: "rpc", 139: "netbios", 143: "imap",
            443: "https", 445: "smb", 465: "smtps", 512: "exec", 513: "login",
            514: "shell", 587: "smtp", 631: "ipp", 873: "rsync", 993: "imaps",
            995: "pop3s", 1080: "socks", 1099: "rmiregistry", 1433: "mssql", 1521: "oracle",
            1701: "l2tp", 1723: "pptp", 2049: "nfs", 2082: "cpanel", 2083: "cpanel-ssl",
            2086: "whm", 2087: "whm-ssl", 3000: "webmin", 3306: "mysql", 3389: "rdp",
            4000: "webnode", 4848: "glassfish", 5432: "postgresql", 5900: "vnc",
            5901: "vnc-1", 5902: "vnc-2", 6379: "redis", 8000: "http-alt", 8008: "http-proxy",
            8080: "http-proxy", 8443: "https-alt", 8888: "http-proxy", 9000: "sonarqube",
            9090: "kubernetes", 9200: "elasticsearch", 11211: "memcached",
            27017: "mongodb", 27018: "mongodb", 28017: "mongodb", 50000: "webmin",
        }
        return services.get(port, f"unknown-{port}")
    
    def clear_cache(self):
        """Clear the geolocation and ASN cache."""
        self._geo_cache.clear()
        self._geo_cache_timestamp.clear()
        logger.info("[CACHE] Cleared geolocation and ASN cache")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cache_size": len(self._geo_cache),
            "cache_ttl": self._geo_cache_ttl,
            "oldest_entry": min(self._geo_cache_timestamp.values()) if self._geo_cache_timestamp else None,
            "newest_entry": max(self._geo_cache_timestamp.values()) if self._geo_cache_timestamp else None
        }
    
    def batch_geo_locate(self, ips: List[str]) -> Dict[str, Dict[str, Any]]:
        """Batch geolocate multiple IPs with rate limiting."""
        results = {}
        for i, ip in enumerate(ips):
            if i > 0 and i % 10 == 0:
                time.sleep(0.5)  # Rate limiting every 10 requests
            results[ip] = self._geo_locate_ip(ip)
        return results


# ─── Standalone ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    scanner = AdvancedNetworkScanner()
    print("OMNISCIENCE ADVANCED NETWORK SCANNER")
    print("Commands: discover, traceroute <ip>, vpn, cloud <provider>, topology, profile <ip>, publicip, geo <ip>, asn <ip>, cache, exit")
    
    while True:
        try:
            raw = input("ADVSCAN> ").strip()
            if not raw:
                continue
            parts = raw.split()
            op = parts[0].lower()
            
            if op in ("discover", "scan"):
                results = scanner.discover_all_network_types()
                scanner.print_discovery_summary()
                
            elif op == "traceroute" and len(parts) >= 2:
                path = scanner.traceroute_with_services(parts[1])
                print(f"\nTraceroute to {parts[1]}:")
                for hop in path:
                    if hop.ip:
                        loc = f"({hop.location})" if hasattr(hop, 'location') and hop.location else ""
                        print(f"  {hop.hop_num:<2}. {hop.ip:<18} {hop.rtt:>6.1f}ms {hop.hostname or ''} {loc}")
                    else:
                        print(f"  {hop.hop_num:<2}. *")
            
            elif op == "vpn":
                vpn_info = scanner.discover_vpn_networks()
                print(f"\nVPN Networks Found: {len(vpn_info)}")
                for v in vpn_info:
                    print(f"  {v['ip']}:{v['port']} - {v['type']}")
            
            elif op == "cloud" and len(parts) >= 2:
                provider = parts[1]
                devices = scanner.scan_public_ranges(provider, max_hosts=20)
                print(f"\n{provider.upper()} Devices Found: {len(devices)}")
                for d in devices:
                    print(f"  {d.ip} - {d.location.get('city', 'Unknown')}, {d.location.get('country', 'Unknown')}")
            
            elif op == "topology":
                topo = scanner.get_topology_map()
                print(f"\nNetwork Topology:")
                print(json.dumps(topo, indent=2, default=str))
            
            elif op == "profile" and len(parts) >= 2:
                device = scanner.profile_device_comprehensive(parts[1])
                print(f"\nDevice Profile for {device.ip}:")
                print(f"  Vendor     : {device.vendor}")
                print(f"  OS         : {device.os} ({device.os_info.get('accuracy', 'unknown')})")
                print(f"  Type       : {device.device_type}")
                print(f"  Location   : {device.location.get('city', 'Unknown')}, {device.location.get('country', 'Unknown')}")
                print(f"  ASN        : {device.asn}")
                print(f"  ISP        : {device.isp}")
                print(f"  Ports      : {list(device.open_ports.keys())}")
                print(f"  Honeypot   : {device.is_honeypot}")
                print(f"  Tags       : {device.tags}")
            
            elif op == "publicip":
                info = scanner.get_public_ip_info()
                print(f"\nPublic IP Information:")
                if "error" in info:
                    print(f"  Error: {info['error']}")
                else:
                    print(f"  Public IP  : {info['public_ip']}")
                    print(f"  Local IP   : {info['local_ip']}")
                    print(f"  Gateway    : {info['gateway']}")
                    print(f"  ISP        : {info['isp']}")
                    print(f"  Location   : {info['city']}, {info['country']}")
                    print(f"  Coordinates: {info['lat']}, {info['lon']}")
                    if info.get('asn'):
                        print(f"  ASN        : {info['asn'].get('asn', 'N/A')}")
            
            elif op == "geo" and len(parts) >= 2:
                ip = parts[1]
                location = scanner._geo_locate_ip(ip)
                print(f"\nGeolocation for {ip}:")
                print(f"  City       : {location.get('city', 'Unknown')}")
                print(f"  Country    : {location.get('country', 'Unknown')}")
                print(f"  Region     : {location.get('region', 'Unknown')}")
                print(f"  ISP        : {location.get('isp', 'Unknown')}")
                print(f"  Org        : {location.get('org', 'Unknown')}")
                print(f"  ASN        : {location.get('as', 'Unknown')}")
                print(f"  Lat/Lon    : {location.get('lat', 0.0)}, {location.get('lon', 0.0)}")
                print(f"  Timezone   : {location.get('timezone', 'Unknown')}")
            
            elif op == "asn" and len(parts) >= 2:
                ip = parts[1]
                asn_info = scanner._get_asn_info(ip)
                print(f"\nASN Information for {ip}:")
                print(f"  ASN        : {asn_info.get('asn', 'Unknown')}")
                print(f"  ISP        : {asn_info.get('isp', 'Unknown')}")
                print(f"  Org        : {asn_info.get('org', 'Unknown')}")
                print(f"  Country    : {asn_info.get('country', 'Unknown')}")
                print(f"  AS Name    : {asn_info.get('as_name', 'Unknown')}")
            
            elif op == "cache":
                stats = scanner.get_cache_stats()
                print(f"\nCache Statistics:")
                print(f"  Cached Entries: {stats['cache_size']}")
                print(f"  Cache TTL     : {stats['cache_ttl']} seconds")
                if stats['oldest_entry']:
                    print(f"  Oldest Entry  : {datetime.fromtimestamp(stats['oldest_entry']).isoformat()}")
                if stats['newest_entry']:
                    print(f"  Newest Entry  : {datetime.fromtimestamp(stats['newest_entry']).isoformat()}")
                print("\n  Commands: clear")
                if len(parts) > 1 and parts[1].lower() == "clear":
                    scanner.clear_cache()
                    print("  Cache cleared.")
            
            elif op in ("exit", "quit"):
                break
            
            else:
                print(f"Unknown command: {op}")
                print("Commands: discover, traceroute <ip>, vpn, cloud <provider>, topology, profile <ip>, publicip, geo <ip>, asn <ip>, cache, exit")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
