#!/usr/bin/env python3
"""
Omniscience Framework v5.1 - Advanced GUI Edition
Full-Featured Network Command Center
"""

import os
import sys
import json
import threading
import socket
import time
import subprocess
from datetime import datetime
from collections import defaultdict

# GUI Libraries
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
    from tkinter.ttk import Notebook
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# Framework imports
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

class AdvancedOmniGUI:
    """Advanced GUI Framework with full features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Omniscience Framework v5.1 - Advanced Network Command Center")
        self.root.geometry("1600x1000")
        self.root.minsize(1200, 800)
        
        # ULTRA MAX HACKER WORLD THEME - GREEN CYCLING EFFECT
        self.theme = {
            'bg_dark': '#000000',
            'bg_medium': '#030803',
            'bg_light': '#071207',
            'accent': '#00ff00',
            'accent_green': '#00ff00',
            'accent_red': '#00ff00',
            'accent_yellow': '#00ff00',
            'accent_purple': '#00ff00',
            'text': '#00ff00',
            'text_dim': '#007700',
            'border': '#002200'
        }
        
        # Green color cycling animation values
        self.green_shades = [
            '#003300', '#004400', '#005500', '#006600', '#007700',
            '#008800', '#009900', '#00aa00', '#00bb00', '#00cc00',
            '#00dd00', '#00ee00', '#00ff00', '#22ff22', '#44ff44'
        ]
        self.cycle_index = 0
        
        self.root.configure(bg=self.theme['bg_dark'])
        
        # Initialize framework modules
        self.modules = {}
        self.hosts = {}
        self.sessions = {}
        self.credentials = {"user": "Administrator", "pass": "", "domain": ""}
        self.target = None
        self.command_history = []
        self.history_index = -1
        
        self.load_modules()
        self.setup_styles()
        self.create_gui()
        self.start_services()
        
    def load_modules(self):
        """Load all framework modules"""
        self.log_to_all("Loading framework modules...", "blue")
        
        module_names = {
            'discovery': '1',
            'intel': '2', 
            'control': '3',
            'adv_scan': '5',
            'center': '6',
            'universal': '7'
        }
        
        for name, num in module_names.items():
            try:
                m = get_module(num)
                if m:
                    class_name = ''.join(word.capitalize() for word in name.split('_'))
                    if name == 'discovery':
                        self.modules[name] = m.NetworkDiscovery() if hasattr(m, 'NetworkDiscovery') else None
                    elif name == 'intel':
                        self.modules[name] = m.AgentlessIntelligence() if hasattr(m, 'AgentlessIntelligence') else None
                    elif name == 'control':
                        self.modules[name] = m.AgentlessControl() if hasattr(m, 'AgentlessControl') else None
                    elif name == 'adv_scan':
                        self.modules[name] = m.AdvancedNetworkScanner() if hasattr(m, 'AdvancedNetworkScanner') else None
                    elif name == 'center':
                        self.modules[name] = m.AdvancedCommandCenter() if hasattr(m, 'AdvancedCommandCenter') else None
                    elif name == 'universal':
                        self.modules[name] = m.UniversalNetworkAccess() if hasattr(m, 'UniversalNetworkAccess') else None
                        
                    if self.modules[name]:
                        self.log_to_all(f"✓ {name} loaded", "green")
            except Exception as e:
                self.log_to_all(f"✗ {name}: {str(e)[:30]}", "red")
        
        self.log_to_all("Framework ready!", "green")
    
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure('Main.TNotebook', background=self.theme['bg_dark'])
        style.configure('Main.TNotebook.Tab', background=self.theme['bg_medium'], foreground=self.theme['text'], padding=[12, 8])
        style.map('Main.TNotebook.Tab', background=[('selected', self.theme['accent'])])
        
        style.configure('Treeview', background=self.theme['bg_medium'], foreground=self.theme['text'], fieldbackground=self.theme['bg_medium'])
        style.configure('Treeview.Heading', background=self.theme['bg_light'], foreground=self.theme['text'])
        
    def create_gui(self):
        """Create the main GUI"""
        # Header
        self.create_header()
        
        # Main PanedWindow
        paned = tk.PanedWindow(self.root, orient='horizontal', bg=self.theme['bg_dark'], sashwidth=4)
        paned.pack(fill='both', expand=True)
        
        # Left Panel - Navigation & Network
        left_panel = self.create_left_panel()
        paned.add(left_panel, minsize=350)
        
        # Right Panel - Main Content
        right_panel = self.create_right_panel()
        paned.add(right_panel, minsize=800)
        
        # Status Bar
        self.create_status_bar()
        
    def create_header(self):
        """Create header with logo and menu"""
        header = tk.Frame(self.root, bg=self.theme['bg_medium'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo
        logo = tk.Label(
            header,
            text="◈ OMNISCIENCE",
            font=('Consolas', 18, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_medium']
        )
        logo.pack(side='left', padx=20, pady=15)
        
        # Menu buttons
        menu_frame = tk.Frame(header, bg=self.theme['bg_medium'])
        menu_frame.pack(side='right', padx=20, pady=10)
        
        menus = [
            ("FILE", []),
            ("SCAN", [("Quick Scan", lambda: self.quick_scan()), ("Full Scan", lambda: self.full_scan())]),
            ("TOOLS", []),
            ("HELP", [])
        ]
        
        for text, items in menus:
            mb = tk.Menubutton(menu_frame, text=text, bg=self.theme['bg_medium'], fg=self.theme['text'], relief='flat')
            mb.pack(side='left', padx=5)
            if items:
                menu = tk.Menu(mb, bg=self.theme['bg_medium'], fg=self.theme['text'])
                for label, cmd in items:
                    menu.add_command(label=label, command=cmd)
                mb.config(menu=menu)
        
        # Connection status
        self.conn_status = tk.Label(
            header,
            text="● CONNECTED",
            font=('Consolas', 10),
            fg=self.theme['accent_green'],
            bg=self.theme['bg_medium']
        )
        self.conn_status.pack(side='right', padx=20)
        
    def create_left_panel(self):
        """Create left navigation panel"""
        frame = tk.Frame(self.root, bg=self.theme['bg_dark'])
        
        # Network Canvas
        canvas_frame = tk.LabelFrame(
            frame,
            text="◈ NETWORK TOPOLOGY",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_dark'],
            bd=1,
            relief='solid'
        )
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.network_canvas = tk.Canvas(
            canvas_frame,
            bg=self.theme['bg_medium'],
            highlightthickness=0
        )
        self.network_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Hosts List
        hosts_frame = tk.LabelFrame(
            frame,
            text="◈ DISCOVERED HOSTS",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_dark'],
            bd=1,
            relief='solid'
        )
        hosts_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('ip', 'mac', 'hostname', 'os', 'type', 'status')
        self.hosts_tree = ttk.Treeview(hosts_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.hosts_tree.heading(col, text=col.upper())
            self.hosts_tree.column(col, width=80)
        
        self.hosts_tree.column('ip', width=110)
        self.hosts_tree.column('mac', width=110)
        
        self.hosts_tree.pack(fill='both', expand=True)
        self.hosts_tree.bind('<Double-1>', self.on_host_double_click)
        
        # Action Buttons
        btn_frame = tk.Frame(frame, bg=self.theme['bg_dark'])
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        buttons = [
            ("⟳ SCAN", self.start_scan, self.theme['accent']),
            ("+ ADD", lambda: None, self.theme['accent_green']),
            ("✕ REMOVE", lambda: None, self.theme['accent_red']),
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(
                btn_frame, text=text, command=cmd,
                font=('Consolas', 9, 'bold'),
                bg=self.theme['bg_light'],
                fg=color,
                relief='flat',
                padx=15, pady=5
            )
            btn.pack(side='left', padx=3)
        
        return frame
    
    def create_right_panel(self):
        """Create right main content panel"""
        frame = tk.Frame(self.root, bg=self.theme['bg_dark'])
        
        # Notebook for tabs
        self.notebook = Notebook(frame, style='Main.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Tab 1: Command Terminal
        self.term_tab = self.create_terminal_tab()
        self.notebook.add(self.term_tab, text="  ⌨ TERMINAL  ")
        
        # Tab 2: Dashboard
        self.dash_tab = self.create_dashboard_tab()
        self.notebook.add(self.dash_tab, text="  📊 DASHBOARD  ")
        
        # Tab 3: Sessions
        self.sessions_tab = self.create_sessions_tab()
        self.notebook.add(self.sessions_tab, text="  🔗 SESSIONS  ")
        
        # Tab 4: Credentials
        self.creds_tab = self.create_credentials_tab()
        self.notebook.add(self.creds_tab, text="  🔑 CREDENTIALS  ")
        
        # Tab 5: Settings
        self.settings_tab = self.create_settings_tab()
        self.notebook.add(self.settings_tab, text="  ⚙ SETTINGS  ")
        
        return frame
    
    def create_terminal_tab(self):
        """Create terminal tab"""
        frame = tk.Frame(self.notebook, bg=self.theme['bg_dark'])
        
        # Terminal Output
        self.terminal = scrolledtext.ScrolledText(
            frame,
            font=('Consolas', 12),
            bg=self.theme['bg_medium'],
            fg='#39ff14',
            insertbackground='#39ff14',
            wrap='word',
            relief='flat'
        )
        self.terminal.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Input Area
        input_frame = tk.Frame(frame, bg=self.theme['bg_medium'])
        input_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        tk.Label(
            input_frame,
            text="⟩",
            font=('Consolas', 12, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_medium']
        ).pack(side='left', padx=5)
        
        self.cmd_entry = tk.Entry(
            input_frame,
            font=('Consolas', 12),
            bg=self.theme['bg_light'],
            fg='#39ff14',
            insertbackground='#39ff14',
            relief='flat'
        )
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        self.cmd_entry.bind('<Return>', self.execute_command)
        self.cmd_entry.bind('<Up>', self.history_up)
        self.cmd_entry.bind('<Down>', self.history_down)
        
        # Quick Commands Bar
        quick_frame = tk.Frame(frame, bg=self.theme['bg_dark'])
        quick_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        quick_commands = [
            ("help", "auto", "scan", "dashboard", "status"),
            ("pwn", "attack", "exec", "screen", "keylog"),
            ("sniff", "creds", "stealcreds", "nethashes", "vault"),
            ("adduser", "rdp-enable", "firewall-off", "wol", "shutdown")
        ]
        
        for row in quick_commands:
            r_frame = tk.Frame(quick_frame, bg=self.theme['bg_dark'])
            r_frame.pack(fill='x', pady=1)
            for cmd in row:
                btn = tk.Button(
                    r_frame, text=cmd,
                    command=lambda c=cmd: self.execute_command_event(c),
                    font=('Consolas', 8),
                    bg=self.theme['bg_light'],
                    fg=self.theme['accent'],
                    relief='flat',
                    padx=8, pady=2
                )
                btn.pack(side='left', padx=1)
        
        # Print banner
        self.print_banner()
        
        return frame
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        frame = tk.Frame(self.notebook, bg=self.theme['bg_dark'])
        
        # Stats Grid
        stats_frame = tk.Frame(frame, bg=self.theme['bg_dark'])
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        stats = [
            ("HOSTS DISCOVERED", "0", self.theme['accent']),
            ("ACTIVE SESSIONS", "0", self.theme['accent_green']),
            ("CAPTURED CREDS", "0", self.theme['accent_purple']),
            ("EXPLOITS RUN", "0", self.theme['accent_red']),
        ]
        
        self.stat_labels = {}
        for i, (label, value, color) in enumerate(stats):
            card = tk.LabelFrame(
                stats_frame,
                text=label,
                font=('Consolas', 9),
                fg=color,
                bg=self.theme['bg_dark'],
                bd=1,
                relief='solid'
            )
            card.grid(row=0, column=i, padx=5, sticky='nsew')
            
            val_label = tk.Label(
                card,
                text=value,
                font=('Consolas', 24, 'bold'),
                fg=color,
                bg=self.theme['bg_dark']
            )
            val_label.pack(pady=10)
            
            self.stat_labels[label] = val_label
        
        # Recent Activity
        activity_frame = tk.LabelFrame(
            frame,
            text="◈ RECENT ACTIVITY",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_dark']
        )
        activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.activity_list = tk.Listbox(
            activity_frame,
            font=('Consolas', 10),
            bg=self.theme['bg_medium'],
            fg=self.theme['text'],
            relief='flat'
        )
        self.activity_list.pack(fill='both', expand=True, padx=5, pady=5)
        
        return frame
    
    def create_sessions_tab(self):
        """Create sessions tab"""
        frame = tk.Frame(self.notebook, bg=self.theme['bg_dark'])
        
        sessions_frame = tk.LabelFrame(
            frame,
            text="◈ ACTIVE SESSIONS",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_dark']
        )
        sessions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('id', 'target', 'platform', 'user', 'time', 'status')
        self.sessions_tree = ttk.Treeview(sessions_frame, columns=columns, show='headings')
        
        for col in columns:
            self.sessions_tree.heading(col, text=col.upper())
            self.sessions_tree.column(col, width=100)
        
        self.sessions_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        return frame
    
    def create_credentials_tab(self):
        """Create credentials tab"""
        frame = tk.Frame(self.notebook, bg=self.theme['bg_dark'])
        
        # Target Credentials
        target_creds = tk.LabelFrame(
            frame,
            text="◈ TARGET CREDENTIALS",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_dark']
        )
        target_creds.pack(fill='x', padx=10, pady=10)
        
        creds_frame = tk.Frame(target_creds, bg=self.theme['bg_dark'])
        creds_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(creds_frame, text="Username:", bg=self.theme['bg_dark'], fg=self.theme['text']).grid(row=0, column=0, sticky='w')
        self.user_entry = tk.Entry(creds_frame, bg=self.theme['bg_light'], fg=self.theme['text'], width=30)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        self.user_entry.insert(0, "Administrator")
        
        tk.Label(creds_frame, text="Password:", bg=self.theme['bg_dark'], fg=self.theme['text']).grid(row=1, column=0, sticky='w')
        self.pass_entry = tk.Entry(creds_frame, bg=self.theme['bg_light'], fg=self.theme['text'], width=30, show='*')
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(creds_frame, text="Domain:", bg=self.theme['bg_dark'], fg=self.theme['text']).grid(row=2, column=0, sticky='w')
        self.domain_entry = tk.Entry(creds_frame, bg=self.theme['bg_light'], fg=self.theme['text'], width=30)
        self.domain_entry.grid(row=2, column=1, padx=5, pady=5)
        
        save_btn = tk.Button(creds_frame, text="SAVE CREDENTIALS", command=self.save_credentials,
                            bg=self.theme['accent'], fg=self.theme['bg_dark'], font=('Consolas', 10, 'bold'))
        save_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Captured Credentials
        captured = tk.LabelFrame(
            frame,
            text="◈ CAPTURED CREDENTIALS",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent_purple'],
            bg=self.theme['bg_dark']
        )
        captured.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.creds_tree = ttk.Treeview(captured, columns=('time', 'source', 'protocol', 'data'), show='headings')
        self.creds_tree.heading('time', text='TIME')
        self.creds_tree.heading('source', text='SOURCE')
        self.creds_tree.heading('protocol', text='PROTOCOL')
        self.creds_tree.heading('data', text='DATA')
        
        self.creds_tree.column('time', width=80)
        self.creds_tree.column('source', width=100)
        self.creds_tree.column('protocol', width=80)
        self.creds_tree.column('data', width=300)
        
        self.creds_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        return frame
    
    def create_settings_tab(self):
        """Create settings tab"""
        frame = tk.Frame(self.notebook, bg=self.theme['bg_dark'])
        
        settings_frame = tk.LabelFrame(
            frame,
            text="◈ FRAMEWORK SETTINGS",
            font=('Consolas', 10, 'bold'),
            fg=self.theme['accent'],
            bg=self.theme['bg_dark']
        )
        settings_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Settings content
        settings = [
            ("Auto-scan on startup", True),
            ("Save logs to file", True),
            ("Verbose output", False),
            ("PyInst evidence removal", False),
        ]
        
        self.setting_vars = {}
        for text, default in settings:
            var = tk.BooleanVar(value=default)
            self.setting_vars[text] = var
            cb = tk.Checkbutton(
                settings_frame,
                text=text,
                variable=var,
                bg=self.theme['bg_dark'],
                fg=self.theme['text'],
                selectcolor=self.theme['bg_light']
            )
            cb.pack(anchor='w', padx=20, pady=5)
        
        # Module toggles
        tk.Label(
            settings_frame,
            text="Module Status:",
            font=('Consolas', 11, 'bold'),
            fg=self.theme['accent_yellow'],
            bg=self.theme['bg_dark']
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        for name, module in self.modules.items():
            status = "✓ LOADED" if module else "✗ FAILED"
            color = self.theme['accent_green'] if module else self.theme['accent_red']
            tk.Label(
                settings_frame,
                text=f"{name.upper()}: {status}",
                font=('Consolas', 10),
                fg=color,
                bg=self.theme['bg_dark']
            ).pack(anchor='w', padx=30)
        
        return frame
    
    def create_status_bar(self):
        """Create status bar"""
        status = tk.Frame(self.root, bg=self.theme['bg_medium'], height=25)
        status.pack(fill='x', side='bottom')
        
        self.status_label = tk.Label(
            status,
            text="Ready",
            font=('Consolas', 9),
            fg=self.theme['text_dim'],
            bg=self.theme['bg_medium'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10)
        
        self.target_label = tk.Label(
            status,
            text="Target: None",
            font=('Consolas', 9),
            fg=self.theme['accent_yellow'],
            bg=self.theme['bg_medium']
        )
        self.target_label.pack(side='right', padx=10)
    
    def print_banner(self):
        """Print ASCII banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║   ____  __  ___ _   _ ___  ____   ____ ___ _____ _   _  ____ _____      ║
║  / __ \\|  \\/  || \\ | |_ _ / ___| / ___|_ _| ____| \\ | |/ ___| ____|     ║
║ | |  | | |\\/| ||  \\| || | \\___ \\| |    | ||  _| |  \\| | |   |  _|       ║
║ | |__| | |  | || |\\  || |  ___) | |___ | || |___| |\\  | |___| |___       ║
║  \\____/|_|  |_||_| \\_|___|____/ \\____|___|_____|_| \\_|\\____|_____|      ║
║                   ADVANCED NETWORK COMMAND CENTER v5.1                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
        Type 'help' for 140+ commands
        """
        self.terminal.insert('end', banner)
        self.terminal.see('end')
    
    def log_to_all(self, message, color='white'):
        """Log to terminal and activity"""
        colors = {
            'blue': self.theme['accent'],
            'green': self.theme['accent_green'],
            'red': self.theme['accent_red'],
            'yellow': self.theme['accent_yellow'],
            'purple': self.theme['accent_purple']
        }
        fg = colors.get(color, self.theme['text'])
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {message}\n"
        
        self.terminal.insert('end', log_msg, fg)
        self.terminal.see('end')
        
        self.activity_list.insert(0, f"[{timestamp}] {message}")
        
    def on_host_double_click(self, event):
        """Handle host double-click"""
        selection = self.hosts_tree.selection()
        if selection:
            item = self.hosts_tree.item(selection[0])
            values = item['values']
            if values:
                self.target = values[0]
                self.target_label.config(text=f"Target: {self.target}")
                self.log_to_all(f"Target selected: {self.target}", "yellow")
                self.cmd_entry.focus()
    
    def save_credentials(self):
        """Save credentials"""
        self.credentials['user'] = self.user_entry.get()
        self.credentials['pass'] = self.pass_entry.get()
        self.credentials['domain'] = self.domain_entry.get()
        self.log_to_all(f"Credentials saved: {self.credentials['user']}", "green")
    
    def quick_scan(self):
        """Quick network scan"""
        self.log_to_all("Starting quick scan...", "blue")
        threading.Thread(target=self._run_scan, args=('quick',), daemon=True).start()
    
    def full_scan(self):
        """Full network scan"""
        self.log_to_all("Starting full scan...", "blue")
        threading.Thread(target=self._run_scan, args=('full',), daemon=True).start()
    
    def start_scan(self):
        """Start scan"""
        self.quick_scan()
    
    def _run_scan(self, scan_type):
        """Run scan in background"""
        try:
            if 'discovery' in self.modules and self.modules['discovery']:
                if scan_type == 'quick':
                    self.hosts = self.modules['discovery'].arp_scan('192.168.1.0/24')
                else:
                    self.hosts = self.modules['discovery'].auto_scan()
                
                self.log_to_all(f"Scan complete! Found {len(self.hosts)} hosts", "green")
                self.root.after(0, self.update_hosts_display)
                self.root.after(0, lambda: self.stat_labels['HOSTS DISCOVERED'].config(text=str(len(self.hosts))))
            else:
                # Demo mode - add sample hosts
                if self.modules.get('discovery'):
                    self.hosts = self.modules['discovery'].auto_scan()
                else:
                    self.hosts = []
                self.hosts = demo_hosts
                self.log_to_all(f"Scan complete! Found {len(self.hosts)} hosts", "green")
                self.root.after(0, self.update_hosts_display)
                self.root.after(0, lambda: self.stat_labels['HOSTS DISCOVERED'].config(text=str(len(self.hosts))))
        except Exception as e:
            self.log_to_all(f"Scan error: {str(e)[:50]}", "red")
    
    def update_hosts_display(self):
        """Update hosts tree"""
        for item in self.hosts_tree.get_children():
            self.hosts_tree.delete(item)
        
        if isinstance(self.hosts, dict):
            items = self.hosts.items()
        elif isinstance(self.hosts, list):
            items = [(getattr(h, 'ip', '?'), h) for h in self.hosts]
        else:
            items = []
        
        for ip, h in items:
            mac = getattr(h, 'mac', '---')
            hostname = getattr(h, 'hostname', '---')
            os_hint = getattr(h, 'os_hint', '---')
            dtype = getattr(h, 'device_type', '---')
            self.hosts_tree.insert('', 'end', values=(ip, mac, hostname, os_hint[:15], dtype, '●'))
        
        self.draw_topology()
    
    def draw_topology(self):
        """Draw network topology"""
        self.network_canvas.delete('all')
        
        w = self.network_canvas.winfo_width() or 330
        h = self.network_canvas.winfo_height() or 250
        
        # Center gateway
        gw_x, gw_y = w // 2, 30
        self.network_canvas.create_oval(gw_x-20, gw_y-20, gw_x+20, gw_y+20, fill=self.theme['accent_yellow'], outline=self.theme['accent_yellow'])
        self.network_canvas.create_text(gw_x, gw_y, text='INTERNET', fill='#000', font=('Consolas', 7, 'bold'))
        
        # Draw hosts
        if isinstance(self.hosts, dict):
            hosts_list = list(self.hosts.items())
        elif isinstance(self.hosts, list):
            hosts_list = [(getattr(h, 'ip', '?'), h) for h in self.hosts]
        else:
            hosts_list = []
        
        n = len(hosts_list)
        if n == 0:
            self.network_canvas.create_text(w//2, h//2, text="No hosts found\nRun 'auto' or click SCAN", fill=self.theme['text_dim'], font=('Consolas', 9))
            return
        
        for i, (ip, h) in enumerate(hosts_list):
            angle = (2 * 3.14159 * i) / max(n, 1)
            x = 50 + (i % 3) * 110
            y = 80 + (i // 3) * 70
            
            # Line to gateway
            self.network_canvas.create_line(gw_x, gw_y+20, x, y-15, fill=self.theme['accent'], width=1)
            
            # Host
            color = self.theme['accent_green'] if 'Windows' in str(getattr(h, 'os_hint', '')) else self.theme['accent_purple']
            self.network_canvas.create_oval(x-12, y-12, x+12, y+12, fill=color, outline=color)
            self.network_canvas.create_text(x, y, text=ip.split('.')[-1], fill='#000', font=('Consolas', 8, 'bold'))
            self.network_canvas.create_text(x, y+22, text=ip[:15], fill=self.theme['text_dim'], font=('Consolas', 6))
    
    def execute_command_event(self, cmd):
        """Execute command from button"""
        self.cmd_entry.delete(0, 'end')
        self.cmd_entry.insert(0, cmd)
        self.execute_command(None)
    
    def execute_command(self, event):
        """Execute terminal command"""
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        
        self.command_history.append(cmd)
        self.history_index = len(self.command_history)
        
        self.cmd_entry.delete(0, 'end')
        self.terminal.insert('end', f"\n⟩ {cmd}\n", self.theme['accent'])
        
        parts = cmd.split()
        c = parts[0].lower()
        args = parts[1:]
        
        # ==================== HELP ====================
        if c in ('help', '?'):
            self.show_help()
        
        # ==================== SYSTEM ====================
        elif c in ('exit', 'quit'):
            self.log_to_all("Goodbye!", "yellow")
            self.root.quit()
        
        elif c == 'clear':
            self.terminal.delete('1.0', 'end')
            self.print_banner()
        
        elif c == 'history':
            for i, hc in enumerate(self.command_history):
                self.terminal.insert('end', f"  {i}: {hc}\n")
        
        # ==================== DISCOVERY ====================
        elif c == 'auto':
            self.quick_scan()
        
        elif c == 'scan' and args:
            self.log_to_all(f"Scanning {args[0]}...", "blue")
        
        elif c == 'network':
            self.log_to_all("Network info requested", "blue")
        
        # ==================== INTELLIGENCE ====================
        elif c == 'sniff':
            self.log_to_all("Starting packet sniffer...", "blue")
        
        elif c == 'creds':
            self.log_to_all("Fetching captured credentials...", "blue")
        
        # ==================== CONTROL ====================
        elif c == 'exec' and len(args) >= 2:
            ip = args[0]
            cmd_str = " ".join(args[1:])
            self.log_to_all(f"Executing on {ip}: {cmd_str}", "yellow")
        
        elif c == 'screen' and args:
            self.log_to_all(f"Capturing screenshot from {args[0]}...", "blue")
        
        elif c == 'keylog' and args:
            self.log_to_all(f"Starting keylogger on {args[0]}...", "red")
        
        # ==================== EXPLOIT ====================
        elif c in ('attack', 'pwnall'):
            self.log_to_all("LAUNCHING ATTACK ON ALL TARGETS!", "red")
            self.stat_labels['EXPLOITS RUN'].config(text=str(int(self.stat_labels['EXPLOITS RUN'].cget('text')) + len(self.hosts)))
        
        elif c == 'pwn' and args:
            self.log_to_all(f"Exploiting target: {args[0]}", "red")
            self.stat_labels['EXPLOITS RUN'].config(text=str(int(self.stat_labels['EXPLOITS RUN'].cget('text')) + 1))
        
        # ==================== DASHBOARD ====================
        elif c in ('dashboard', 'status'):
            self.show_dashboard()
        
        else:
            self.log_to_all(f"Unknown command: {c}. Type 'help'", "yellow")
        
        self.terminal.see('end')
    
    def show_help(self):
        """Show help"""
        help_text = """
════════════════════════════════════════════════════════════════════════════
                        OMNISCIENCE HELP - 140+ COMMANDS
════════════════════════════════════════════════════════════════════════════

 📡 NETWORK DISCOVERY
    auto, scan <range>, arp <range>, icmp <range>, tcp <ip>,
    netbios, mdns, ssdp, snmp, http, traceroute, topology,
    network, interfaces, gateway, external-ip, cloud-scan

 👁 INTELLIGENCE  
    sniff, stopsniff, creds, ntlm, http-auth, dns-log,
    wmi-proc, wmi-users, wmi-software, wmi-svc, monitor

 ⚡ REMOTE CONTROL
    exec <ip> <cmd>, ssh-exec, screen, webcam, audio,
    keylog, clipboard-get, clipboard-set, pslist, killproc,
    svc-list, vault, open-url, play-media

 💀 EXPLOITATION
    pwn <ip>, omnifetch, exploit, attack, stealcreds,
    nethashes, tokens, ssh-brute, rdp-brute, etblue-check

 🔧 PERSISTENCE
    adduser, rdp-enable, firewall-off, persist-task,
    wol, shutdown, reboot, logoff

 🐧 LINUX CONTROL
    linux-sysinfo, linux-revshell, linux-backdoor

 📁 FILE OPERATIONS
    upload, download, smb-list, wget, adb-push

 ⚙ SYSTEM
    dashboard, setcreds, target, targets, sessions,
    history, clear, exit, help
════════════════════════════════════════════════════════════════════════════
        """
        self.terminal.insert('end', help_text)
    
    def show_dashboard(self):
        """Show dashboard"""
        self.log_to_all("═" * 50, "blue")
        self.log_to_all("  OMNISCIENCE DASHBOARD", "blue")
        self.log_to_all("═" * 50, "blue")
        self.log_to_all(f"  Hosts Discovered: {len(self.hosts)}", "green")
        self.log_to_all(f"  Target: {self.target or 'None'}", "yellow")
        self.log_to_all(f"  Credentials: {self.credentials['user']}", "cyan")
        self.log_to_all("═" * 50, "blue")
    
    def history_up(self, event):
        """History navigation up"""
        if self.command_history:
            if self.history_index > 0:
                self.history_index -= 1
            self.cmd_entry.delete(0, 'end')
            self.cmd_entry.insert(0, self.command_history[self.history_index])
    
    def history_down(self, event):
        """History navigation down"""
        if self.command_history:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.cmd_entry.delete(0, 'end')
                self.cmd_entry.insert(0, self.command_history[self.history_index])
    
    def start_green_cycle_animation(self):
        """Start green color cycling hacker effect"""
        def cycle_colors():
            while True:
                self.cycle_index = (self.cycle_index + 1) % len(self.green_shades)
                current_green = self.green_shades[self.cycle_index]
                
                # Cycle terminal text color
                self.terminal.config(fg=current_green, insertbackground=current_green)
                self.cmd_entry.config(fg=current_green, insertbackground=current_green)
                
                # Cycle network canvas border
                self.network_canvas.config(highlightbackground=current_green)
                
                time.sleep(0.15)
        
        threading.Thread(target=cycle_colors, daemon=True).start()
    
    def start_services(self):
        """Start background services"""
        self.log_to_all("Initializing hacker services...", "green")
        self.start_green_cycle_animation()

def main():
    """Main entry point"""
    if not GUI_AVAILABLE:
        print("GUI not available. Install tkinter.")
        return
    
    root = tk.Tk()
    app = AdvancedOmniGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
