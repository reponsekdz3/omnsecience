import socket

print("[+] Scanning single target: 10.15.155.1 (gateway)...")
ip = "10.15.155.1"
ports = [22, 80, 443, 445, 3389, 5985, 8080, 3306, 5432, 27017]

open_ports = []
for port in ports:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((ip, port)) == 0:
            open_ports.append(port)
            print(f"  [+] Port {port} OPEN")
        sock.close()
    except Exception as e:
        pass

print(f"\n[+] Done. Found {len(open_ports)} open ports: {open_ports}")