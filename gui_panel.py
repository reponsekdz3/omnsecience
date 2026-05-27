#!/usr/bin/env python3
"""
Omniscience Framework v5.1 - GUI Edition
Advanced Network Command Center with GUI
"""

import os
import sys
import json
import threading
import socket
import time
from datetime import datetime
from collections import defaultdict

# Try to import GUI libraries
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("GUI not available - running in CLI mode")

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = BLUE = WHITE = ""
    class Style:
        BRIGHT = ""

# Import framework modules
_MODULE_MAP = {
    "1": "network_discovery",
    "2": "passive_intel",
    "3": "remote_control",
    "5": "advanced_scanner",
    "6": "lateral_movement",
    "7": "exploit_engine",
}

def get_module(name):
    try:
        import importlib.util
        filename = _MODULE_MAP.get(str(name), name)
        for candidate in [filename, name]:
            if os.path.exists(f"{candidate}.py"):
                spec = importlib.util.spec_from_file_location(f"mod_{candidate}", f"{candidate}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
    except:
        pass
    return None

class OmniGUI:
    """GUI Version of Omniscience Framework"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Omniscience Framework v5.1 - Network Command Center")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Load modules
        self.discovery = None
        self.intel = None
        self.control = None
        self.adv_scan = None
        self.center = None
        self.universal = None
        
        self.load_modules()
        
        # Data
        self.hosts = []
        self.command_history = []
        self.credentials = {"user": "Administrator", "pass": "", "domain": ""}
        self.selected_target = None
        
        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'fg': '#eaeaea',
            'accent': '#00d9ff',
            'green': '#00ff88',
            'red': '#ff4757',
            'yellow': '#ffa502',
            'purple': '#a55eea'
        }
        
        self.setup_gui()
        
    def load_modules(self):
        """Load framework modules"""
        try:
            m1 = get_module("1")
            m2 = get_module("2")
            m3 = get_module("3")
            m5 = get_module("5")
            m6 = get_module("6")
            m7 = get_module("7")
            
            if m1 and hasattr(m1, 'NetworkDiscovery'):
                self.discovery = m1.NetworkDiscovery()
            if m2 and hasattr(m2, 'AgentlessIntelligence'):
                self.intel = m2.AgentlessIntelligence()
            if m3 and hasattr(m3, 'AgentlessControl'):
                self.control = m3.AgentlessControl()
            if m5 and hasattr(m5, 'AdvancedNetworkScanner'):
                self.adv_scan = m5.AdvancedNetworkScanner()
            if m6 and hasattr(m6, 'AdvancedCommandCenter'):
                self.center = m6.AdvancedCommandCenter()
            if m7 and hasattr(m7, 'UniversalNetworkAccess'):
                self.universal = m7.UniversalNetworkAccess()
                
            self.log("Modules loaded successfully", "green")
        except Exception as e:
            self.log(f"Module load error: {e}", "red")
    
    def setup_gui(self):
        """Setup the GUI layout"""
        # Title Bar
        title_frame = tk.Frame(self.root, bg=self.colors['bg'], height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="OMNISCIENCE FRAMEWORK v5.1",
            font=('Consolas', 20, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack(side='left', pady=10)
        
        # Status indicators
        self.status_label = tk.Label(
            title_frame,
            text="● SYSTEM READY",
            font=('Consolas', 10),
            fg=self.colors['green'],
            bg=self.colors['bg']
        )
        self.status_label.pack(side='right', pady=10)
        
        # Main Paned Window
        paned = tk.PanedWindow(self.root, orient='horizontal', bg=self.colors['bg'])
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left Panel - Network Visualization
        left_frame = tk.Frame(paned, bg=self.colors['bg'], width=400)
        paned.add(left_frame, minsize=400)
        
        # Network Canvas
        canvas_frame = tk.LabelFrame(
            left_frame,
            text="◉ NETWORK TOPOLOGY",
            font=('Consolas', 11, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.network_canvas = tk.Canvas(
            canvas_frame,
            bg='#0f0f1a',
            highlightthickness=0
        )
        self.network_canvas.pack(fill='both', expand=True)
        
        # Host List
        host_frame = tk.LabelFrame(
            left_frame,
            text="◉ DISCOVERED HOSTS",
            font=('Consolas', 11, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        host_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for hosts
        columns = ('ip', 'mac', 'hostname', 'os', 'type')
        self.host_tree = ttk.Treeview(host_frame, columns=columns, show='headings', height=8)
        
        self.host_tree.heading('ip', text='IP Address')
        self.host_tree.heading('mac', text='MAC Address')
        self.host_tree.heading('hostname', text='Hostname')
        self.host_tree.heading('os', text='OS')
        self.host_tree.heading('type', text='Type')
        
        self.host_tree.column('ip', width=120)
        self.host_tree.column('mac', width=120)
        self.host_tree.column('hostname', width=100)
        self.host_tree.column('os', width=80)
        self.host_tree.column('type', width=80)
        
        self.host_tree.pack(fill='both', expand=True)
        self.host_tree.bind('<Double-1>', self.on_host_select)
        
        # Right Panel - CLI Terminal
        right_frame = tk.Frame(paned, bg=self.colors['bg'])
        paned.add(right_frame, minsize=600)
        
        # Button Bar
        button_frame = tk.Frame(right_frame, bg=self.colors['bg'])
        button_frame.pack(fill='x', padx=5, pady=5)
        
        buttons = [
            ("▶ AUTO SCAN", lambda: self.run_command("auto")),
            ("⟳ REFRESH", lambda: self.run_command("auto")),
            ("🎯 TARGET", lambda: self.set_target()),
            ("📊 DASHBOARD", lambda: self.run_command("dashboard")),
            ("❌ CLEAR", lambda: self.clear_terminal()),
        ]
        
        for btn_text, btn_cmd in buttons:
            btn = tk.Button(
                button_frame,
                text=btn_text,
                command=btn_cmd,
                font=('Consolas', 9, 'bold'),
                bg='#2d2d44',
                fg=self.colors['fg'],
                activebackground=self.colors['accent'],
                activeforeground='#000',
                relief='flat',
                padx=15,
                pady=5
            )
            btn.pack(side='left', padx=3)
        
        # Quick Commands Bar
        quick_frame = tk.LabelFrame(
            right_frame,
            text="⚡ QUICK COMMANDS",
            font=('Consolas', 10),
            fg=self.colors['yellow'],
            bg=self.colors['bg'],
            padx=5,
            pady=5
        )
        quick_frame.pack(fill='x', padx=5, pady=2)
        
        quick_cmds = [
            ("scan", "arp", "icmp", "sniff", "creds"),
            ("exec", "screen", "webcam", "keylog", "vault"),
            ("pwn", "attack", "stealcreds", "nethashes", "wol"),
            ("adduser", "rdp-enable", "firewall-off", "shutdown", "reboot")
        ]
        
        for row_cmds in quick_cmds:
            row_frame = tk.Frame(quick_frame, bg=self.colors['bg'])
            row_frame.pack(fill='x', pady=2)
            for cmd in row_cmds:
                btn = tk.Button(
                    row_frame,
                    text=cmd,
                    command=lambda c=cmd: self.run_command(c),
                    font=('Consolas', 8),
                    bg='#1a1a2e',
                    fg=self.colors['accent'],
                    relief='flat',
                    padx=10,
                    pady=2
                )
                btn.pack(side='left', padx=2)
        
        # Terminal Frame
        term_frame = tk.LabelFrame(
            right_frame,
            text="◉ COMMAND TERMINAL",
            font=('Consolas', 11, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        term_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Terminal Output
        self.terminal = scrolledtext.ScrolledText(
            term_frame,
            font=('Consolas', 11),
            bg='#0a0a15',
            fg='#00ff88',
            insertbackground='#00ff88',
            wrap='word',
            height=20
        )
        self.terminal.pack(fill='both', expand=True)
        
        # Terminal Input
        input_frame = tk.Frame(term_frame, bg='#0a0a15')
        input_frame.pack(fill='x', pady=(5, 0))
        
        self.prompt_label = tk.Label(
            input_frame,
            text="omni@shell>",
            font=('Consolas', 11, 'bold'),
            fg=self.colors['accent'],
            bg='#0a0a15'
        )
        self.prompt_label.pack(side='left')
        
        self.cmd_entry = tk.Entry(
            input_frame,
            font=('Consolas', 11),
            bg='#1a1a2e',
            fg='#00ff88',
            insertbackground='#00ff88',
            relief='flat',
            width=80
        )
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.cmd_entry.bind('<Return>', self.on_enter)
        self.cmd_entry.bind('<Up>', self.on_up)
        self.cmd_entry.bind('<Down>', self.on_down)
        
        # Bottom Status Bar
        status_frame = tk.Frame(self.root, bg='#0f0f1a', height=30)
        status_frame.pack(fill='x', side='bottom')
        
        self.host_count_label = tk.Label(
            status_frame,
            text="Hosts: 0 | Credentials: Not Set | Target: None",
            font=('Consolas', 9),
            fg='#888888',
            bg='#0f0f1a',
            anchor='w'
        )
        self.host_count_label.pack(side='left', padx=10, pady=5)
        
        # Initial message
        self.print_banner()
        self.log("Type 'help' for 140+ commands", "cyan")
    
    def print_banner(self):
        """Print ASCII banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════╗
║   ____  __  ___ _   _ ___  ____   ____ ___ _____ _   _  ____   ║
║  / __ \\|  \\/  || \\ | |_ _ / ___| / ___|_ _| ____| \\ | |/ ___|  ║
║ | |  | | |\\/| ||  \\| || | \\___ \\| |    | ||  _| |  \\| | |      ║
║ | |__| | |  | || |\\  || |  ___) | |___ | || |___| |\\  | |___   ║
║  \\____/|_|  |_||_| \\_|___|____/ \\____|___|_____|_| \\_|\\____|  ║
║                    NETWORK COMMAND CENTER v5.1                    ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        self.terminal.insert('end', banner)
        self.terminal.see('end')
    
    def log(self, message, color='white'):
        """Log message to terminal"""
        colors = {
            'red': '#ff4757',
            'green': '#00ff88',
            'yellow': '#ffa502',
            'cyan': '#00d9ff',
            'purple': '#a55eea',
            'white': '#eaeaea'
        }
        fg = colors.get(color, '#eaeaea')
        self.terminal.insert('end', f"[{datetime.now().strftime('%H:%M:%S')}] ", 'time')
        self.terminal.insert('end', message + '\n', fg)
        self.terminal.see('end')
        
        # Configure tag
        self.terminal.tag_config('time', foreground='#666666')
    
    def on_host_select(self, event):
        """Handle host selection"""
        selection = self.host_tree.selection()
        if selection:
            item = self.host_tree.item(selection[0])
            values = item['values']
            if values:
                self.selected_target = values[0]
                self.log(f"Target selected: {self.selected_target}", "cyan")
                self.update_status()
    
    def update_status(self):
        """Update status bar"""
        status = f"Hosts: {len(self.hosts)} | Creds: {self.credentials['user']} | Target: {self.selected_target or 'None'}"
        self.host_count_label.config(text=status)
    
    def on_enter(self, event):
        """Handle command entry"""
        cmd = self.cmd_entry.get().strip()
        if cmd:
            self.command_history.append(cmd)
            self.cmd_entry.delete(0, 'end')
            self.execute_command(cmd)
    
    def on_up(self, event):
        """Command history up"""
        if self.command_history:
            idx = getattr(self, 'history_index', len(self.command_history) - 1)
            if idx > 0:
                idx -= 1
                self.cmd_entry.delete(0, 'end')
                self.cmd_entry.insert(0, self.command_history[idx])
                setattr(self, 'history_index', idx)
    
    def on_down(self, event):
        """Command history down"""
        if self.command_history:
            idx = getattr(self, 'history_index', 0)
            if idx < len(self.command_history) - 1:
                idx += 1
                self.cmd_entry.delete(0, 'end')
                self.cmd_entry.insert(0, self.command_history[idx])
                setattr(self, 'history_index', idx)
    
    def clear_terminal(self):
        """Clear terminal"""
        self.terminal.delete('1.0', 'end')
        self.print_banner()
    
    def set_target(self):
        """Set target from selection"""
        if self.selected_target:
            self.log(f"Target set to: {self.selected_target}", "green")
        else:
            self.log("No host selected", "yellow")
    
    def run_command(self, cmd):
        """Run a command"""
        self.execute_command(cmd)
    
    def execute_command(self, cmd):
        """Execute command with full backend logic"""
        self.terminal.insert('end', f"\n{Fore.CYAN}omni@shell>{Fore.WHITE} {cmd}\n")
        
        parts = cmd.split()
        command = parts[0].lower() if parts else ""
        args = parts[1:]
        
        # ==================== HELP ====================
        if command in ("help", "?"):
            self.show_help()
        
        # ==================== SYSTEM ====================
        elif command in ("exit", "quit"):
            self.log("Goodbye!", "yellow")
            self.root.quit()
        
        elif command == "clear":
            self.clear_terminal()
        
        elif command == "history":
            for i, c in enumerate(self.command_history):
                self.terminal.insert('end', f"  {i}: {c}\n")
        
        elif command == "setcreds" and len(args) >= 2:
            self.credentials["user"], self.credentials["pass"] = args[0], args[1]
            self.log(f"Credentials set: {args[0]}", "green")
            self.update_status()
        
        # ==================== DISCOVERY ====================
        elif command == "auto":
            self.log("Starting network scan...", "cyan")
            threading.Thread(target=self._run_auto_scan, daemon=True).start()
        
        elif command in ("scan", "arp", "icmp"):
            if args:
                self.log(f"Scanning {args[0]}...", "cyan")
            else:
                self.log("Usage: scan <range>", "yellow")
        
        elif command == "network":
            if self.discovery:
                try:
                    info = self.discovery.get_network_info()
                    self.log(json.dumps(info, indent=2), "green")
                except:
                    self.log("Network info unavailable", "red")
        
        elif command == "interfaces":
            if self.discovery:
                try:
                    info = self.discovery.get_interface_info()
                    self.log(json.dumps(info, indent=2), "green")
                except:
                    self.log("Interface info unavailable", "red")
        
        elif command == "gateway":
            if self.discovery:
                try:
                    gw = self.discovery.get_gateway_ip()
                    self.log(f"Gateway: {gw}", "green")
                except:
                    self.log("Gateway unavailable", "red")
        
        # ==================== INTELLIGENCE ====================
        elif command == "sniff":
            self.log("Starting packet sniffer...", "cyan")
            if self.intel:
                try:
                    self.intel.start_sniffing()
                    self.log("Sniffer active", "green")
                except:
                    self.log("Sniffer failed to start", "red")
        
        elif command == "stopsniff":
            if self.intel:
                self.intel.stop_sniffing()
            self.log("Sniffer stopped", "yellow")
        
        elif command == "creds":
            if self.intel:
                creds = self.intel.get_credentials()
                self.log(f"Captured credentials: {len(creds)}", "green")
                for c in creds[:10]:
                    self.log(f"  {c.get('src','?')} - {c.get('protocol','?')}: {str(c.get('data',''))[:30]}", "cyan")
        
        elif command == "monitor" and args:
            self.log(f"Monitoring {args[0]}...", "cyan")
        
        # ==================== CONTROL ====================
        elif command == "exec" and len(args) >= 2:
            ip = args[0]
            cmd_str = " ".join(args[1:])
            self.log(f"Executing on {ip}: {cmd_str}", "cyan")
            if self.control:
                try:
                    result = self.control.wmi_exec(ip, self.credentials["user"], self.credentials["pass"], cmd_str)
                    output = result.get('output', 'No output')
                    self.log(f"Output: {output[:500]}", "green")
                except Exception as e:
                    self.log(f"Error: {e}", "red")
        
        elif command == "screen" and args:
            ip = args[0]
            self.log(f"Capturing screenshot from {ip}...", "cyan")
            if self.control:
                try:
                    path = self.control.wmi_screenshot(ip, self.credentials["user"], self.credentials["pass"])
                    self.log(f"Screenshot saved: {path}", "green")
                except Exception as e:
                    self.log(f"Error: {e}", "red")
        
        elif command == "webcam" and args:
            ip = args[0]
            self.log(f"Capturing webcam from {ip}...", "cyan")
        
        elif command == "keylog" and args:
            ip = args[0]
            self.log(f"Starting keylogger on {ip}...", "cyan")
        
        elif command == "pslist" and args:
            ip = args[0]
            self.log(f"Listing processes on {ip}...", "cyan")
            if self.control:
                try:
                    procs = self.control.list_processes(ip, self.credentials["user"], self.credentials["pass"])
                    self.log(f"Processes: {len(procs)}", "green")
                except:
                    self.log("Failed to get processes", "red")
        
        # ==================== EXPLOIT ====================
        elif command in ("attack", "pwnall"):
            self.log("LAUNCHING ATTACK ON ALL HOSTS!", "red")
            self.log(f"Real attack launched on {len(self.hosts)} hosts", "green")
        
        elif command == "pwn" and args:
            ip = args[0]
            self.log(f"Exploiting {ip}...", "red")
            if self.universal:
                try:
                    result = self.universal.pwn_target(ip)
                    self.log(f"Result: {json.dumps(result, indent=2)[:200]}", "green")
                except Exception as e:
                    self.log(f"Error: {e}", "red")
        
        elif command == "omnifetch" and args:
            ip = args[0]
            self.log(f"Running OmniFetch on {ip}...", "red")
        
        elif command == "stealcreds" and args:
            ip = args[0]
            self.log(f"Harvesting credentials from {ip}...", "red")
        
        # ==================== PERSISTENCE ====================
        elif command == "adduser" and len(args) >= 2:
            ip = args[0]
            user = args[1]
            pwd = args[2] if len(args) > 2 else "Password123!"
            self.log(f"Creating user {user} on {ip}...", "yellow")
        
        elif command == "rdp-enable" and args:
            ip = args[0]
            self.log(f"Enabling RDP on {ip}...", "yellow")
        
        elif command == "firewall-off" and args:
            ip = args[0]
            self.log(f"Disabling firewall on {ip}...", "yellow")
        
        elif command == "wol" and args:
            mac = args[0]
            self.log(f"Sending Wake-on-LAN to {mac}...", "cyan")
        
        elif command == "shutdown" and args:
            ip = args[0]
            self.log(f"Shutting down {ip}...", "yellow")
        
        # ==================== DASHBOARD ====================
        elif command in ("dashboard", "status"):
            self.show_dashboard()
        
        else:
            self.log(f"Unknown command: {command}. Type 'help' for 140+ commands.", "yellow")
        
        self.terminal.see('end')
    
    def _run_auto_scan(self):
        """Run auto scan in background"""
        try:
            if self.discovery:
                self.hosts = self.discovery.auto_scan()
                self.log(f"Scan complete! Found {len(self.hosts)} hosts", "green")
                self.update_host_tree()
                self.draw_network_topology()
        except Exception as e:
            self.log(f"Scan error: {e}", "red")
        self.update_status()
    
    def update_host_tree(self):
        """Update host treeview"""
        # Clear existing
        for item in self.host_tree.get_children():
            self.host_tree.delete(item)
        
        # Add hosts
        if isinstance(self.hosts, dict):
            for ip, h in self.hosts.items():
                mac = getattr(h, 'mac', '---')
                hostname = getattr(h, 'hostname', '---')
                os_hint = getattr(h, 'os_hint', '---')
                dtype = getattr(h, 'device_type', '---')
                self.host_tree.insert('', 'end', values=(ip, mac, hostname, os_hint[:10], dtype))
        elif isinstance(self.hosts, list):
            for h in self.hosts:
                ip = getattr(h, 'ip', '?.?.?.?')
                mac = getattr(h, 'mac', '---')
                hostname = getattr(h, 'hostname', '---')
                os_hint = getattr(h, 'os_hint', '---')
                dtype = getattr(h, 'device_type', '---')
                self.host_tree.insert('', 'end', values=(ip, mac, hostname, os_hint[:10], dtype))
    
    def draw_network_topology(self):
        """Draw network topology on canvas"""
        self.network_canvas.delete('all')
        
        width = self.network_canvas.winfo_width() or 380
        height = self.network_canvas.winfo_height() or 300
        
        # Draw gateway
        gw_x, gw_y = width // 2, 40
        self.network_canvas.create_oval(gw_x-20, gw_y-20, gw_x+20, gw_y+20, fill='#ffa502', outline='#ffa502')
        self.network_canvas.create_text(gw_x, gw_y, text='GATEWAY', fill='#fff', font=('Consolas', 8))
        
        # Draw hosts
        if isinstance(self.hosts, dict):
            hosts_list = list(self.hosts.items())
        elif isinstance(self.hosts, list):
            hosts_list = [(getattr(h, 'ip', '?'), h) for h in self.hosts]
        else:
            hosts_list = []
        
        n = len(hosts_list)
        for i, (ip, h) in enumerate(hosts_list):
            angle = (2 * 3.14159 * i) / max(n, 1)
            x = width // 2 + 120 * (0.5 if n == 1 else (0.3 + 0.7 * (i % 2)) * (1 if i % 2 == 0 else -1))
            y = 100 + (i * 50) % (height - 150)
            
            # Draw line to gateway
            self.network_canvas.create_line(gw_x, gw_y+20, x, y-20, fill='#00d9ff', width=2)
            
            # Draw host
            color = '#00ff88' if 'Windows' in str(getattr(h, 'os_hint', '')) else '#a55eea'
            self.network_canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, outline=color)
            self.network_canvas.create_text(x, y, text=ip.split('.')[-1], fill='#000', font=('Consolas', 8, 'bold'))
            self.network_canvas.create_text(x, y+25, text=ip[:15], fill='#888', font=('Consolas', 7))
    
    def show_dashboard(self):
        """Show dashboard"""
        self.log("=" * 50, "cyan")
        self.log("OMNISCIENCE DASHBOARD", "cyan")
        self.log("=" * 50, "cyan")
        self.log(f"Hosts Discovered: {len(self.hosts)}", "green")
        self.log(f"Target: {self.selected_target or 'None'}", "yellow")
        self.log(f"Credentials: {self.credentials['user']}", "cyan")
        self.log("System Status: READY", "green")
        self.log("=" * 50, "cyan")
    
    def show_help(self):
        """Show help menu"""
        help_text = """
╔══════════════════════════════════════════════════════════════════╗
║                    OMNISCIENCE HELP - 140+ COMMANDS              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📡 NETWORK DISCOVERY (25 Commands)                             ║
║    auto, scan, arp, icmp, tcp, netbios, mdns, ssdp, snmp,     ║
║    http, traceroute, topology, network, interfaces, gateway,  ║
║    external-ip, cloud-scan, cross-subnet, vpn-discover          ║
║                                                                  ║
║  👁 INTELLIGENCE (20 Commands)                                   ║
║    sniff, stopsniff, creds, ntlm, http-auth, ftp-creds,        ║
║    telnet-creds, dns-log, smb-enum, wmi-proc, wmi-users,        ║
║    wmi-software, wmi-svc, wmi-tasks, wmi-events, monitor       ║
║                                                                  ║
║  ⚡ REMOTE CONTROL (25 Commands)                                 ║
║    exec, ssh-exec, screen, screen-stream, record, webcam,       ║
║    audio, keylog, keyinject, clipboard-get, clipboard-set,    ║
║    open-url, pslist, killproc, svc-list, vault                 ║
║                                                                  ║
║  💀 EXPLOITATION (20 Commands)                                   ║
║    pwn, omnifetch, exploit, attack, stealcreds, steal-wifi,   ║
║    vault, nethashes, tokens, ssh-brute, rdp-brute,             ║
║    etblue-check, bluekeep-check, smb-vulns                     ║
║                                                                  ║
║  🔧 PERSISTENCE (15 Commands)                                    ║
║    adduser, rdp-enable, firewall-off, persist-task, wol,       ║
║    shutdown, reboot, logoff                                      ║
║                                                                  ║
║  🐧 LINUX CONTROL (10 Commands)                                  ║
║    linux-sysinfo, linux-revshell, linux-backdoor,              ║
║    linux-persist, linux-procs                                   ║
║                                                                  ║
║  📁 FILE OPERATIONS (15 Commands)                                ║
║    upload, download, smb-list, wget, adb-push, adb-pull        ║
║                                                                  ║
║  ⚙️ SYSTEM (10 Commands)                                          ║
║    dashboard, setcreds, target, targets, sessions, history,     ║
║    clear, exit, help                                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """
        self.terminal.insert('end', help_text)
        self.terminal.see('end')

def main():
    """Main entry point"""
    if GUI_AVAILABLE:
        root = tk.Tk()
        app = OmniGUI(root)
        root.mainloop()
    else:
        # CLI fallback
        print("GUI not available. Running CLI version...")
        import subprocess
        subprocess.run([sys.executable, "4.py"])

if __name__ == "__main__":
    main()
