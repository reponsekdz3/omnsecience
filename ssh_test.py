import paramiko
import time

print("[+] Testing SSH access to 10.15.155.1 with root:root")
print("[+] This reproduces the successful login from earlier...\n")

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("[*] Connecting...")
    client.connect('10.15.155.1', port=22, username='root', password='root', timeout=10)
    print("[+] Connected!")
    
    print("[*] Opening session...")
    chan = client.invoke_shell()
    time.sleep(2)
    
    print("[*] Sending command...")
    chan.send("whoami\n")
    time.sleep(2)
    
    if chan.recv_ready():
        output = chan.recv(1024).decode('utf-8')
        print(f"[+] Output: {output.strip()}")
    else:
        print("[-] No output received")
        
    # Try a simple command via exec_command too
    print("[*] Trying exec_command...")
    stdin, stdout, stderr = client.exec_command('echo "test"', timeout=5)
    output = stdout.read().decode('utf-8').strip()
    error = stderr.read().decode('utf-8').strip()
    if output:
        print(f"[+] Command output: {output}")
    if error:
        print(f"[-] Command error: {error}")
    
    client.close()
    print("\n[+] SSH test completed")
    
except Exception as e:
    print(f"[-] Error: {e}")
    import traceback
    traceback.print_exc()