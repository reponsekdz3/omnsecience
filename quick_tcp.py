import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from exploit_engine import UniversalNetworkAccess

print("[+] Initializing Omniscience scanner...")
exploiter = UniversalNetworkAccess()

print("[+] Performing quick TCP sweep on network...")
devices = exploiter._tcp_sweep("10.15.155.0/24")

print(f"\n[+] Found {len(devices)} devices with open ports:")
for d in devices:
    print(f"  {d.ip} | OS: {d.os} | Ports: {list(d.open_ports.keys())}")

# Save results
import json
results = {"devices": [d.to_dict() for d in devices]}
with open("scan_results_tcp.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("\n[+] Results saved to scan_results_tcp.json")