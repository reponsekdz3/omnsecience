import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from advanced_scanner import AdvancedNetworkScanner

print("[+] Initializing Omniscience Advanced Network Scanner...")
scanner = AdvancedNetworkScanner()

print(f"[+] Local IP: {scanner.local_ip}")
print(f"[+] Gateway: {scanner.gateway}")
print(f"[+] Network Range: {scanner.network_range}")

print("\n[*] Scanning local network for all devices...")
devices = scanner.discover_all_network_types()

# Display results
for net_type, devs in devices.items():
    if devs:
        print(f"\n[{net_type.upper()}] Found {len(devs)} devices:")
        for d in devs[:10]:
            print(f"  {d.ip} | {d.os or 'Unknown'} | {d.device_type} | {d.vendor[:20]}")

total = sum(len(d) for d in devices.values())
print(f"\n[+] Total: {total} devices discovered")

# Save results
import json
results = {
    "timestamp": str(os.popen('date').read().strip() if os.name != 'nt' else ''),
    "local_ip": scanner.local_ip,
    "gateway": scanner.gateway,
    "network_range": scanner.network_range,
    "devices": [d.to_dict() for devs in devices.values() for d in devs]
}
with open("scan_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("[+] Results saved to scan_results.json")