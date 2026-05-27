"""
OMNISCIENCE ULTRA ADVANCED UI ENGINE
Real-time monitoring, live panels, matrix effects
"""

import os
import sys
import time
import random
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

class LiveMonitor:
    """Real-time live monitoring system with multiple panels"""
    
    def __init__(self):
        self.active = True
        self.stats = {
            'packets_captured': 0,
            'hosts_discovered': 0,
            'exploits_attempted': 0,
            'exploits_successful': 0,
            'data_exfiltrated': 0,
            'commands_executed': 0,
            'active_connections': 0,
            'cpu_usage': 0,
            'memory_usage': 0,
            'network_traffic': 0
        }
        self.activity_log = []
        self.target_list = []
        self.compromised_hosts = []
        
    def update_stat(self, key, value):
        """Update a statistic"""
        if key in self.stats:
            self.stats[key] = value
            
    def increment_stat(self, key, amount=1):
        """Increment a statistic"""
        if key in self.stats:
            self.stats[key] += amount
            
    def add_activity(self, message, level='info'):
        """Add activity to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.append({
            'time': timestamp,
            'message': message,
            'level': level
        })
        if len(self.activity_log) > 50:
            self.activity_log = self.activity_log[-50:]
            
    def draw_top_panel(self):
        """Draw top status panel"""
        try:
            width = os.get_terminal_size().columns
            
            # Top bar with system status
            print(f"\033[1;1H{Fore.GREEN}{Style.BRIGHT}{'═' * width}")
            
            # System info line
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_line = f"  OMNISCIENCE v5.1 │ {now} │ ACTIVE │ Targets: {len(self.target_list)} │ Compromised: {len(self.compromised_hosts)}"
            padding = width - len(status_line) - 2
            print(f"\033[2;1H{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{status_line}{' ' * padding}")
            
            print(f"\033[3;1H{Fore.GREEN}{Style.BRIGHT}{'═' * width}")
            
        except:
            pass
            
    def draw_bottom_panel(self):
        """Draw bottom activity panel"""
        try:
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            
            # Bottom panel starts 10 lines from bottom
            panel_start = height - 12
            
            print(f"\033[{panel_start};1H{Fore.CYAN}{Style.BRIGHT}{'═' * width}")
            print(f"\033[{panel_start+1};1H{Fore.CYAN}{Style.BRIGHT}  LIVE ACTIVITY MONITOR")
            print(f"\033[{panel_start+2};1H{Fore.CYAN}{Style.BRIGHT}{'─' * width}")
            
            # Show last 8 activities
            for i, activity in enumerate(self.activity_log[-8:]):
                line_num = panel_start + 3 + i
                level_colors = {
                    'info': Fore.WHITE,
                    'success': Fore.GREEN,
                    'warning': Fore.YELLOW,
                    'error': Fore.RED,
                    'exploit': Fore.LIGHTRED_EX
                }
                color = level_colors.get(activity['level'], Fore.WHITE)
                msg = f"  [{activity['time']}] {activity['message']}"
                if len(msg) > width - 2:
                    msg = msg[:width-5] + "..."
                padding = width - len(msg)
                print(f"\033[{line_num};1H{color}{msg}{' ' * padding}")
                
        except:
            pass
            
    def draw_stats_panel(self):
        """Draw statistics panel on right side"""
        try:
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            
            # Right panel starts at 70% of width
            panel_x = int(width * 0.7)
            panel_width = width - panel_x - 2
            
            # Draw panel border
            for y in range(5, min(25, height - 15)):
                print(f"\033[{y};{panel_x}H{Fore.MAGENTA}│")
                
            # Panel header
            print(f"\033[5;{panel_x+2}H{Fore.MAGENTA}{Style.BRIGHT}SYSTEM STATISTICS")
            print(f"\033[6;{panel_x}H{Fore.MAGENTA}{'─' * panel_width}")
            
            # Statistics
            stats_display = [
                (f"Packets: {self.stats['packets_captured']}", Fore.CYAN),
                (f"Hosts: {self.stats['hosts_discovered']}", Fore.GREEN),
                (f"Exploits: {self.stats['exploits_attempted']}", Fore.YELLOW),
                (f"Success: {self.stats['exploits_successful']}", Fore.LIGHTGREEN_EX),
                (f"Data: {self.stats['data_exfiltrated']} MB", Fore.LIGHTCYAN_EX),
                (f"Commands: {self.stats['commands_executed']}", Fore.WHITE),
                (f"Connections: {self.stats['active_connections']}", Fore.LIGHTMAGENTA_EX),
                (f"CPU: {self.stats['cpu_usage']}%", Fore.LIGHTYELLOW_EX),
                (f"Memory: {self.stats['memory_usage']}%", Fore.LIGHTRED_EX),
                (f"Traffic: {self.stats['network_traffic']} KB/s", Fore.LIGHTBLUE_EX)
            ]
            
            for i, (stat, color) in enumerate(stats_display):
                y = 7 + i
                if y < height - 15:
                    print(f"\033[{y};{panel_x+2}H{color}{stat}")
                    
        except:
            pass
            
    def draw_matrix_background(self):
        """Draw matrix rain effect in background"""
        try:
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            
            # Random matrix characters in background
            chars = "01アイウエオカキクケコ"
            for _ in range(5):
                x = random.randint(1, width - 1)
                y = random.randint(5, height - 15)
                char = random.choice(chars)
                intensity = random.randint(1, 100)
                
                if intensity > 90:
                    color = Fore.LIGHTGREEN_EX
                elif intensity > 70:
                    color = Fore.GREEN
                else:
                    color = Fore.LIGHTBLACK_EX
                    
                print(f"\033[{y};{x}H{color}{char}", end='', flush=True)
                
        except:
            pass
            
    def refresh_display(self):
        """Refresh all panels"""
        self.draw_top_panel()
        self.draw_stats_panel()
        self.draw_bottom_panel()
        self.draw_matrix_background()
        
    def start_live_monitor(self):
        """Start live monitoring thread"""
        def monitor_loop():
            while self.active:
                try:
                    self.refresh_display()
                    time.sleep(0.5)
                except:
                    pass
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        
    def stop(self):
        """Stop monitoring"""
        self.active = False


class AdvancedVisualEffects:
    """Advanced visual effects for hacker terminal"""
    
    @staticmethod
    def glitch_text(text, duration=0.5):
        """Glitch effect on text"""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        end_time = time.time() + duration
        
        while time.time() < end_time:
            glitched = ""
            for char in text:
                if random.random() < 0.3:
                    glitched += random.choice(glitch_chars)
                else:
                    glitched += char
            print(f"\r{Fore.RED}{Style.BRIGHT}{glitched}", end='', flush=True)
            time.sleep(0.05)
            
        print(f"\r{Fore.GREEN}{Style.BRIGHT}{text}")
        
    @staticmethod
    def typewriter_effect(text, delay=0.03, color=Fore.GREEN):
        """Typewriter effect"""
        for char in text:
            print(f"{color}{char}", end='', flush=True)
            time.sleep(delay)
        print()
        
    @staticmethod
    def progress_bar_advanced(label, total, current, width=50):
        """Advanced progress bar with animations"""
        percent = int((current / total) * 100)
        filled = int((current / total) * width)
        bar = "█" * filled + "░" * (width - filled)
        
        # Color based on progress
        if percent < 30:
            color = Fore.RED
        elif percent < 70:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
            
        print(f"\r  {Fore.WHITE}{label:<20} {color}{Style.BRIGHT}[{bar}] {percent}%", end='', flush=True)
        
    @staticmethod
    def scanning_animation(text, duration=2.0):
        """Scanning animation"""
        chars = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            frame = chars[i % len(chars)]
            print(f"\r  {Fore.GREEN}{Style.BRIGHT}{frame} {Fore.LIGHTGREEN_EX}{text}...", end='', flush=True)
            i += 1
            time.sleep(0.08)
            
        print(f"\r  {Fore.GREEN}{Style.BRIGHT}✔ {Fore.LIGHTGREEN_EX}{text} {Fore.GREEN}[COMPLETE]{Style.RESET_ALL}   ")
        
    @staticmethod
    def data_stream_effect(lines=20):
        """Simulate data streaming"""
        hex_chars = "0123456789ABCDEF"
        
        for _ in range(lines):
            line = ""
            for _ in range(64):
                line += random.choice(hex_chars)
                if len(line) % 2 == 0:
                    line += " "
                    
            intensity = random.randint(1, 100)
            if intensity > 80:
                color = Fore.LIGHTGREEN_EX
            elif intensity > 50:
                color = Fore.GREEN
            else:
                color = Fore.LIGHTBLACK_EX
                
            print(f"{color}{line}")
            time.sleep(0.02)
            
    @staticmethod
    def target_lock_animation(target_ip):
        """Target lock animation"""
        frames = [
            "[ ⠋ ]",
            "[ ⠙ ]",
            "[ ⠹ ]",
            "[ ⠸ ]",
            "[ ⠼ ]",
            "[ ⠴ ]",
            "[ ⠦ ]",
            "[ ⠧ ]",
            "[ ⠇ ]",
            "[ ⠏ ]"
        ]
        
        for i in range(30):
            frame = frames[i % len(frames)]
            print(f"\r  {Fore.YELLOW}{Style.BRIGHT}{frame} {Fore.WHITE}Acquiring target: {Fore.LIGHTRED_EX}{target_ip}", end='', flush=True)
            time.sleep(0.1)
            
        print(f"\r  {Fore.GREEN}{Style.BRIGHT}[  ✓  ] {Fore.WHITE}Target locked: {Fore.LIGHTGREEN_EX}{target_ip}{' ' * 20}")
        
    @staticmethod
    def exploit_animation(exploit_name, target):
        """Exploit execution animation"""
        stages = [
            "Initializing exploit chain",
            "Bypassing security controls",
            "Injecting payload",
            "Establishing connection",
            "Gaining access",
            "Privilege escalation",
            "Installing backdoor",
            "Cleaning traces"
        ]
        
        print(f"\n{Fore.RED}{Style.BRIGHT}╔{'═' * 60}╗")
        print(f"{Fore.RED}║  EXPLOIT: {exploit_name:<48} ║")
        print(f"{Fore.RED}║  TARGET:  {target:<48} ║")
        print(f"{Fore.RED}╠{'═' * 60}╣")
        
        for i, stage in enumerate(stages):
            AdvancedVisualEffects.progress_bar_advanced(stage, len(stages), i + 1, 40)
            time.sleep(0.3)
            print()
            
        print(f"{Fore.RED}╚{'═' * 60}╝")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}  ✅ EXPLOIT SUCCESSFUL - FULL ACCESS GRANTED")
        
    @staticmethod
    def network_scan_visual(ip_range, hosts_found):
        """Visual network scanning"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}╔{'═' * 70}╗")
        print(f"{Fore.CYAN}║  NETWORK SCAN: {ip_range:<54} ║")
        print(f"{Fore.CYAN}╠{'═' * 70}╣")
        
        for i in range(20):
            ip = f"{ip_range.split('/')[0].rsplit('.', 1)[0]}.{random.randint(1, 254)}"
            status = random.choice(["OPEN", "FILTERED", "CLOSED"])
            
            if status == "OPEN":
                color = Fore.GREEN
                symbol = "✓"
            elif status == "FILTERED":
                color = Fore.YELLOW
                symbol = "◐"
            else:
                color = Fore.LIGHTBLACK_EX
                symbol = "✗"
                
            print(f"{Fore.CYAN}║  {color}{symbol} {ip:<15} {status:<10} {Fore.LIGHTBLACK_EX}{'█' * random.randint(5, 30)}{' ' * 20}{Fore.CYAN}║")
            time.sleep(0.1)
            
        print(f"{Fore.CYAN}╠{'═' * 70}╣")
        print(f"{Fore.CYAN}║  {Fore.GREEN}SCAN COMPLETE: {len(hosts_found)} hosts discovered{' ' * 35}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═' * 70}╝\n")


class CommandTree:
    """Tree-based command system with autocomplete and help"""
    
    def __init__(self):
        self.commands = {
            'scan': {
                'auto': {'desc': 'Automatic full network scan', 'args': []},
                'global': {'desc': 'ULTRAMAX 10km global scan', 'args': []},
                'fast': {'desc': 'Quick 10-second sweep', 'args': []},
                'range': {'desc': 'Scan specific IP range', 'args': ['<ip_range>']},
                'port': {'desc': 'Port scan target', 'args': ['<ip>', '[ports]']},
                'vuln': {'desc': 'Vulnerability scan', 'args': ['<ip>']}
            },
            'exploit': {
                'auto': {'desc': 'Auto-exploit target', 'args': ['<ip>']},
                'eternalblue': {'desc': 'MS17-010 EternalBlue', 'args': ['<ip>']},
                'smbghost': {'desc': 'CVE-2020-0796 SMBGhost', 'args': ['<ip>']},
                'printnightmare': {'desc': 'CVE-2021-34527 PrintNightmare', 'args': ['<ip>']},
                'petitpotam': {'desc': 'CVE-2021-36942 PetitPotam', 'args': ['<ip>']},
                'zerologon': {'desc': 'CVE-2020-1472 Zerologon', 'args': ['<ip>', '[dc_name]']},
                'bluekeep': {'desc': 'CVE-2019-0708 BlueKeep', 'args': ['<ip>']},
                'nopac': {'desc': 'CVE-2021-42278 NoPac', 'args': ['<ip>']}
            },
            'control': {
                'exec': {'desc': 'Execute command', 'args': ['<command>']},
                'shell': {'desc': 'Interactive shell', 'args': []},
                'screen': {'desc': 'Capture screenshot', 'args': []},
                'webcam': {'desc': 'Capture webcam', 'args': []},
                'audio': {'desc': 'Record audio', 'args': ['[duration]']},
                'keylog': {'desc': 'Start keylogger', 'args': []},
                'monitor': {'desc': 'Live monitoring', 'args': ['[duration]']}
            },
            'extract': {
                'all': {'desc': 'Extract all data', 'args': []},
                'passwords': {'desc': 'Browser passwords', 'args': []},
                'wifi': {'desc': 'WiFi passwords', 'args': []},
                'cookies': {'desc': 'Browser cookies', 'args': []},
                'history': {'desc': 'Browser history', 'args': []},
                'lsass': {'desc': 'LSASS memory dump', 'args': []},
                'hashes': {'desc': 'Password hashes', 'args': []},
                'tokens': {'desc': 'Auth tokens', 'args': []}
            },
            'persist': {
                'install': {'desc': 'Install backdoor', 'args': []},
                'task': {'desc': 'Scheduled task', 'args': ['<name>', '[path]']},
                'service': {'desc': 'Windows service', 'args': ['<name>', '[path]']},
                'registry': {'desc': 'Registry key', 'args': ['<key>', '<value>']},
                'user': {'desc': 'Create admin user', 'args': ['<username>', '[password]']}
            },
            'lateral': {
                'move': {'desc': 'Lateral movement', 'args': ['<source>', '<target>']},
                'psexec': {'desc': 'PsExec execution', 'args': ['<target>', '<command>']},
                'wmi': {'desc': 'WMI execution', 'args': ['<target>', '<command>']},
                'winrm': {'desc': 'WinRM execution', 'args': ['<target>', '<command>']},
                'smb': {'desc': 'SMB execution', 'args': ['<target>', '<command>']}
            },
            'database': {
                'dump': {'desc': 'Full database dump', 'args': ['<ip>', '<port>', '<type>']},
                'extract': {'desc': 'Extract specific data', 'args': ['<ip>', '<port>', '<type>', '<query>']},
                'mysql': {'desc': 'MySQL attack', 'args': ['<ip>']},
                'postgres': {'desc': 'PostgreSQL attack', 'args': ['<ip>']},
                'mongodb': {'desc': 'MongoDB attack', 'args': ['<ip>']},
                'redis': {'desc': 'Redis attack', 'args': ['<ip>']}
            },
            'cloud': {
                'aws': {'desc': 'AWS metadata attack', 'args': ['<target>']},
                'azure': {'desc': 'Azure IMDS attack', 'args': ['<target>']},
                'gcp': {'desc': 'GCP metadata attack', 'args': ['<target>']},
                's3': {'desc': 'S3 bucket scan', 'args': ['<bucket_name>']}
            },
            'ad': {
                'kerberoast': {'desc': 'Kerberoasting attack', 'args': ['<dc_ip>', '[domain]']},
                'spray': {'desc': 'Password spray', 'args': ['<domain>']},
                'asreproast': {'desc': 'AS-REP roasting', 'args': ['<dc_ip>']},
                'dcsync': {'desc': 'DCSync attack', 'args': ['<dc_ip>']},
                'golden': {'desc': 'Golden ticket', 'args': ['<domain>']}
            },
            'file': {
                'list': {'desc': 'List directory', 'args': ['[path]']},
                'upload': {'desc': 'Upload file', 'args': ['<local>', '<remote>']},
                'download': {'desc': 'Download file', 'args': ['<remote>', '[local]']},
                'delete': {'desc': 'Delete file', 'args': ['<path>']},
                'execute': {'desc': 'Execute file', 'args': ['<path>']}
            }
        }
        
    def get_command_tree(self):
        """Get full command tree"""
        return self.commands
        
    def find_command(self, cmd_parts):
        """Find command in tree"""
        if not cmd_parts:
            return None
            
        category = cmd_parts[0]
        if category not in self.commands:
            return None
            
        if len(cmd_parts) == 1:
            return self.commands[category]
            
        subcmd = cmd_parts[1]
        if subcmd in self.commands[category]:
            return self.commands[category][subcmd]
            
        return None
        
    def get_suggestions(self, partial):
        """Get command suggestions"""
        suggestions = []
        
        for category in self.commands:
            if category.startswith(partial):
                suggestions.append(category)
                
            for subcmd in self.commands[category]:
                full_cmd = f"{category} {subcmd}"
                if full_cmd.startswith(partial):
                    suggestions.append(full_cmd)
                    
        return suggestions
        
    def print_tree(self):
        """Print command tree"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}╔{'═' * 78}╗")
        print(f"{Fore.CYAN}║  COMMAND TREE - HIERARCHICAL STRUCTURE{' ' * 39}║")
        print(f"{Fore.CYAN}╠{'═' * 78}╣")
        
        for category, subcmds in self.commands.items():
            print(f"{Fore.CYAN}║  {Fore.LIGHTGREEN_EX}{Style.BRIGHT}▸ {category.upper()}{' ' * (73 - len(category))}║")
            
            for subcmd, info in subcmds.items():
                args_str = ' '.join(info['args'])
                cmd_line = f"    ├─ {subcmd} {args_str}"
                desc = info['desc']
                
                if len(cmd_line) + len(desc) > 74:
                    print(f"{Fore.CYAN}║  {Fore.GREEN}{cmd_line:<40}{Fore.LIGHTBLACK_EX}{desc[:30]}...{' ' * 2}║")
                else:
                    padding = 74 - len(cmd_line) - len(desc)
                    print(f"{Fore.CYAN}║  {Fore.GREEN}{cmd_line}{' ' * padding}{Fore.LIGHTBLACK_EX}{desc}{' ' * 2}║")
                    
        print(f"{Fore.CYAN}╚{'═' * 78}╝\n")
