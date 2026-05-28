import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from exploit_engine import UniversalNetworkAccess

print("[+] Initializing Omniscience network scanner...")
exploiter = UniversalNetworkAccess()
print("[+] Scanning local network for devices...")
devices = exploiter.ultramax_global_scan()
print(f"[+] Found {len(devices)} devices total")
for d in list(devices)[:15]:
    print(f"  {d.ip} | {d.os or 'Unknown'} | {d.device_type} | Ports: {list(d.open_ports.keys())[:5]}")

# Save results
import json
results = {"devices": [d.to_dict() for d in devices]}
with open("scan_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("[+] Results saved to scan_results.json")