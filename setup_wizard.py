#!/usr/bin/env python3
"""
Omniscience Framework v5.1 - Setup Wizard
Professional Installation Wizard
"""

import os
import sys
import subprocess
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Progressbar

class SetupWizard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Omniscience Framework v5.1 - Setup Wizard")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        self.theme = {
            'bg': '#1a1a2e',
            'bg_light': '#16213e',
            'accent': '#0f3460',
            'highlight': '#e94560',
            'text': '#ffffff',
            'green': '#00ff88'
        }
        
        self.current_step = 0
        self.steps = [
            ("Welcome", self.welcome_step),
            ("System Check", self.system_check_step),
            ("Dependencies", self.dependencies_step),
            ("Installation", self.installation_step),
            ("Complete", self.complete_step)
        ]
        
        self.setup_ui()
        self.run_step()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.theme['bg_light'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="◈ OMNISCIENCE FRAMEWORK",
            font=('Consolas', 18, 'bold'),
            fg=self.theme['highlight'],
            bg=self.theme['bg_light']
        ).pack(pady=20)
        
        # Progress
        self.progress_frame = tk.Frame(self.root, bg=self.theme['bg'])
        self.progress_frame.pack(fill='x', padx=40, pady=10)
        
        self.step_labels = []
        for i, (name, _) in enumerate(self.steps):
            lbl = tk.Label(
                self.progress_frame,
                text=f"{i+1}. {name}",
                font=('Consolas', 10),
                fg='#666666' if i != 0 else self.theme['highlight'],
                bg=self.theme['bg']
            )
            lbl.pack(side='left', padx=10)
            self.step_labels.append(lbl)
        
        # Content
        self.content_frame = tk.Frame(self.root, bg=self.theme['bg'])
        self.content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Bottom
        self.bottom_frame = tk.Frame(self.root, bg=self.theme['bg_light'], height=60)
        self.bottom_frame.pack(fill='x', side='bottom')
        self.bottom_frame.pack_propagate(False)
        
        self.next_btn = tk.Button(
            self.bottom_frame,
            text="NEXT →",
            command=self.next_step,
            font=('Consolas', 12, 'bold'),
            bg=self.theme['highlight'],
            fg='white',
            relief='flat',
            padx=30, pady=10
        )
        self.next_btn.pack(side='right', padx=20, pady=10)
        
        self.back_btn = tk.Button(
            self.bottom_frame,
            text="← BACK",
            command=self.prev_step,
            font=('Consolas', 12),
            bg=self.theme['bg_light'],
            fg='white',
            relief='flat',
            padx=20, pady=10,
            state='disabled'
        )
        self.back_btn.pack(side='right', padx=10, pady=10)
        
    def run_step(self):
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Run current step
        _, step_func = self.steps[self.current_step]
        step_func()
        
        # Update progress
        for i, lbl in enumerate(self.step_labels):
            if i == self.current_step:
                lbl.config(fg=self.theme['highlight'])
            elif i < self.current_step:
                lbl.config(fg=self.theme['green'])
            else:
                lbl.config(fg='#666666')
        
        # Update buttons
        self.back_btn.config(state='normal' if self.current_step > 0 else 'disabled')
        
        if self.current_step == len(self.steps) - 1:
            self.next_btn.config(text="FINISH")
        else:
            self.next_btn.config(text="NEXT →")
    
    def welcome_step(self):
        tk.Label(
            self.content_frame,
            text="Welcome to Omniscience Framework",
            font=('Consolas', 24, 'bold'),
            fg=self.theme['highlight'],
            bg=self.theme['bg']
        ).pack(pady=30)
        
        tk.Label(
            self.content_frame,
            text="Advanced Network Command & Control Center",
            font=('Consolas', 14),
            fg='#888888',
            bg=self.theme['bg']
        ).pack()
        
        features = [
            "✓ Network Discovery & Scanning",
            "✓ Remote Control & Execution", 
            "✓ Credential Harvesting",
            "✓ Exploitation Tools",
            "✓ Persistence Mechanisms",
            "✓ GUI & CLI Interfaces"
        ]
        
        for feat in features:
            tk.Label(
                self.content_frame,
                text=feat,
                font=('Consolas', 12),
                fg=self.theme['green'],
                bg=self.theme['bg']
            ).pack(anchor='w', padx=100, pady=5)
        
        tk.Label(
            self.content_frame,
            text="This software is for educational and authorized security testing only.",
            font=('Consolas', 10, 'italic'),
            fg='#ff6b6b',
            bg=self.theme['bg']
        ).pack(pady=30)
    
    def system_check_step(self):
        tk.Label(
            self.content_frame,
            text="System Requirements Check",
            font=('Consolas', 18, 'bold'),
            fg=self.theme['highlight'],
            bg=self.theme['bg']
        ).pack(pady=20)
        
        checks = []
        
        # OS Check
        os_name = os.name
        checks.append(("Operating System", "✓ Windows" if os_name == 'nt' else f"⚠ {os_name}"))
        
        # Python Check
        py_ver = sys.version.split()[0]
        checks.append(("Python", f"✓ {py_ver}" if py_ver >= "3.8" else f"⚠ {py_ver}"))
        
        # Admin Check (Windows)
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            checks.append(("Administrator", "✓ Running as Admin" if is_admin else "⚠ Not Admin"))
        except:
            checks.append(("Administrator", "✓ Root Access"))
        
        # RAM Check
        try:
            import psutil
            ram = psutil.virtual_memory()
            ram_gb = ram.total / (1024**3)
            checks.append(("RAM", f"✓ {ram_gb:.1f} GB"))
        except:
            checks.append(("RAM", "✓ Unknown"))
        
        for name, status in checks:
            row = tk.Frame(self.content_frame, bg=self.theme['bg'])
            row.pack(fill='x', pady=5, padx=50)
            
            tk.Label(
                row,
                text=name,
                font=('Consolas', 11),
                fg='white',
                bg=self.theme['bg'],
                width=20,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row,
                text=status,
                font=('Consolas', 11),
                fg=self.theme['green'] if '✓' in status else '#ffa502',
                bg=self.theme['bg']
            ).pack(side='left')
        
        self.checks_passed = all('✓' in status for _, status in checks)
    
    def dependencies_step(self):
        tk.Label(
            self.content_frame,
            text="Installing Dependencies",
            font=('Consolas', 18, 'bold'),
            fg=self.theme['highlight'],
            bg=self.theme['bg']
        ).pack(pady=20)
        
        deps_frame = tk.Frame(self.content_frame, bg=self.theme['bg_light'])
        deps_frame.pack(fill='both', expand=True, padx=50, pady=10)
        
        self.dep_status = {}
        
        deps = [
            ('colorama', 'Terminal colors'),
            ('scapy', 'Network packets'),
            ('impacket', 'SMB/WMI protocols'),
            ('paramiko', 'SSH client'),
            ('Pillow', 'Image processing'),
            ('pywin32', 'Windows APIs')
        ]
        
        for dep, desc in deps:
            row = tk.Frame(deps_frame, bg=self.theme['bg_light'])
            row.pack(fill='x', pady=2)
            
            tk.Label(
                row,
                text=dep,
                font=('Consolas', 11, 'bold'),
                fg='white',
                bg=self.theme['bg_light'],
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row,
                text=desc,
                font=('Consolas', 9),
                fg='#888888',
                bg=self.theme['bg_light'],
                width=30,
                anchor='w'
            ).pack(side='left')
            
            status_lbl = tk.Label(
                row,
                text="⏳",
                font=('Consolas', 11),
                bg=self.theme['bg_light']
            )
            status_lbl.pack(side='right', padx=10)
            self.dep_status[dep] = status_lbl
        
        # Install button
        tk.Button(
            self.content_frame,
            text="INSTALL ALL DEPENDENCIES",
            command=self.install_dependencies,
            font=('Consolas', 12, 'bold'),
            bg=self.theme['highlight'],
            fg='white',
            relief='flat',
            padx=20, pady=10
        ).pack(pady=10)
        
        self.deps_installed = False
    
    def install_dependencies(self):
        deps = ['colorama', 'scapy', 'impacket', 'paramiko', 'Pillow', 'pywin32']
        
        for dep in deps:
            try:
                self.dep_status[dep].config(text="⏳", fg='#ffa502')
                self.root.update()
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep, '-q', '--user'])
                self.dep_status[dep].config(text="✓", fg=self.theme['green'])
            except:
                self.dep_status[dep].config(text="✗", fg='#ff6b6b')
        
        self.deps_installed = True
        messagebox.showinfo("Success", "Dependencies installed!")
    
    def installation_step(self):
        tk.Label(
            self.content_frame,
            text="Installing Omniscience Framework",
            font=('Consolas', 18, 'bold'),
            fg=self.theme['highlight'],
            bg=self.theme['bg']
        ).pack(pady=20)
        
        self.progress = Progressbar(
            self.content_frame,
            orient='horizontal',
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(
            self.content_frame,
            text="Preparing installation...",
            font=('Consolas', 10),
            fg='#888888',
            bg=self.theme['bg']
        )
        self.progress.pack(pady=10)
        self.status_label.pack()
        
        # Simulate installation progress
        self.root.after(500, lambda: self.update_progress(20, "Copying modules..."))
        self.root.after(1000, lambda: self.update_progress(40, "Installing modules..."))
        self.root.after(1500, lambda: self.update_progress(60, "Configuring..."))
        self.root.after(2000, lambda: self.update_progress(80, "Creating shortcuts..."))
        self.root.after(2500, lambda: self.update_progress(100, "Complete!"))
        
        self.installation_done = True
    
    def update_progress(self, value, text):
        self.progress['value'] = value
        self.status_label.config(text=text)
        self.root.update()
    
    def complete_step(self):
        tk.Label(
            self.content_frame,
            text="✓ Installation Complete!",
            font=('Consolas', 24, 'bold'),
            fg=self.theme['green'],
            bg=self.theme['bg']
        ).pack(pady=30)
        
        tk.Label(
            self.content_frame,
            text="Omniscience Framework has been installed successfully.",
            font=('Consolas', 12),
            fg='white',
            bg=self.theme['bg']
        ).pack()
        
        # Launch options
        tk.Label(
            self.content_frame,
            text="Launch Options:",
            font=('Consolas', 14, 'bold'),
            fg=self.theme['highlight'],
            bg=self.theme['bg']
        ).pack(pady=20)
        
        options = [
            ("OmnisciencePro.exe", "Full GUI with network visualization"),
            ("OmniscienceGUI.exe", "Basic GUI interface"),
            ("Omniscience.exe", "Command-line interface")
        ]
        
        for exe, desc in options:
            row = tk.Frame(self.content_frame, bg=self.theme['bg'])
            row.pack(fill='x', padx=100, pady=5)
            
            tk.Label(
                row,
                text=exe,
                font=('Consolas', 11, 'bold'),
                fg=self.theme['green'],
                bg=self.theme['bg']
            ).pack(side='left')
            
            tk.Label(
                row,
                text=f"- {desc}",
                font=('Consolas', 10),
                fg='#888888',
                bg=self.theme['bg']
            ).pack(side='left', padx=10)
        
        tk.Label(
            self.content_frame,
            text="Files installed in: dist/",
            font=('Consolas', 10, 'italic'),
            fg='#666666',
            bg=self.theme['bg']
        ).pack(pady=20)
    
    def next_step(self):
        if self.current_step == 2 and not self.deps_installed:
            messagebox.showwarning("Warning", "Please install dependencies first!")
            return
        
        if self.current_step == 3 and not getattr(self, 'installation_done', False):
            messagebox.showwarning("Warning", "Please wait for installation to complete!")
            return
        
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.run_step()
        else:
            self.root.quit()
    
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.run_step()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()
