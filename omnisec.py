# OMNISCIENCE — Complete Integration Module
# This file ties together all modules and provides the main entry point
# with full error handling and fallback mechanisms.

import asyncio
import sys
import os
import threading
import time
from typing import Optional, Dict, List, Any

# Try to import our core engine
try:
    from omnisec_engine import OmniSecEngine, Device, Session, run_full_operation
    ENGINE_OK = True
except ImportError as e:
    print(f"[!] OmniSec engine import error: {e}")
    ENGINE_OK = False

# Try to import original modules (fallback if omnisec_engine not yet complete)
try:
    from exploit_engine import UniversalNetworkAccess, UniversalDevice
    from lateral_movement import AdvancedCommandCenter
    from remote_control import AgentlessControl
    from advanced_scanner import AdvancedNetworkScanner
    from passive_intel import AgentlessIntelligence
    from commandcenter import OmniShell
    ORIGINAL_MODULES_OK = True
except ImportError as e:
    print(f"[!] Original modules import error: {e}")
    ORIGINAL_MODULES_OK = False

# Colorama
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLOR = True
except ImportError:
    class Dummy:
        def __getattr__(self, name): return ""
    Fore = Style = Dummy()
    COLOR = False

# ─── Unified Engine Wrapper ───────────────────────────────────────────────────────

class UnifiedEngine:
    """
    Unified wrapper that uses OmniSecEngine if available, otherwise falls back
    to original module-based implementation. Provides consistent interface.
    """
    def __init__(self):
        if ENGINE_OK:
            self.engine = OmniSecEngine()
            self.mode = "omnisec"
            print(f"{Fore.GREEN}[+] OmniSec Engine loaded (modern architecture)")
        elif ORIGINAL_MODULES_OK:
            # Fall back to original module composition
            self.scanner = AdvancedNetworkScanner()
            self.exploiter = UniversalNetworkAccess()
            self.lateral = AdvancedCommandCenter()
            self.control = AgentlessControl()
            self.intel = AgentlessIntelligence()
            
            # Wire modules together
            self.lateral.set_modules(discovery=self.scanner, intel=self.intel, control=self.control)
            
            self.mode = "original"
            print(f"{Fore.YELLOW}[*] Using legacy module architecture")
        else:
            print(f"{Fore.RED}[!] No engine available — check dependencies")
            sys.exit(1)
        
        self.devices = {}
        self.sessions = {}
        self._lock = threading.RLock()
    
    # ─── Discovery ────────────────────────────────────────────────────────────────
    
    def discover(self, network_range: str = None, exhaustive: bool = True) -> List[Any]:
        """Discover devices on network."""
        if self.mode == "omnisec":
            devices = self.engine.discover_devices(network_range, exhaustive)
        else:
            # Original implementation
            if not network_range:
                network_range = self.scanner.network_range
            devices = self.exploiter.discover_all_devices(network_range)
        with self._lock:
            self.devices.update({d.ip: d for d in devices})
        return devices
    
    # ─── Exploitation ─────────────────────────────────────────────────────────────
    
    def exploit_all(self) -> Dict[str, Any]:
        """Exploit all discovered devices."""
        if self.mode == "omnisec":
            return self.engine.pwn_all()
        else:
            # Original implementation
            return self.exploiter.pwn_all_devices()
    
    # ─── Control ──────────────────────────────────────────────────────────────────
    
    def execute(self, command: str, session_ids: List[str] = None) -> Dict[str, Any]:
        """Execute command on sessions."""
        if self.mode == "omnisec":
            return self.engine.execute_on_all(command)
        else:
            # Original implementation
            return self.lateral.execute_on_all_sessions(command)
    
    def interactive(self, session_id: str):
        """Enter interactive shell for a session."""
        if self.mode == "omnisec":
            sess = self.engine.sessions.get(session_id)
            if sess:
                dev = self.engine.devices[sess.device_ip]
                print(f"\nInteractive session: {sess.device_ip} ({sess.platform})")
                print("Type 'exit' to quit\n")
                while True:
                    cmd = input("shell> ").strip()
                    if cmd.lower() in ("exit", "quit"):
                        break
                    result = self.execute(cmd, session_ids=[session_id])
                    print(result.get(session_id, {}).get("output", "No output"))
            else:
                print("Session not found")
        else:
            self.lateral.interactive_session(session_id)
    
    # ─── Reporting ─────────────────────────────────────────────────────────────────
    
    def report(self, format: str = "json") -> str:
        """Generate penetration test report."""
        if self.mode == "omnisec":
            return self.engine.generate_report(format)
        else:
            # Generate basic report from original modules
            timestamp = int(time.time())
            fname = f"report_{timestamp}.json"
            report = {
                "devices": [d.to_dict() for d in self.devices.values()],
                "sessions": list(self.sessions.values()),
            }
            import json
            with open(fname, "w") as f:
                json.dump(report, f, indent=2, default=str)
            return fname
    
    def summary(self):
        """Print summary."""
        if self.mode == "omnisec":
            self.engine.print_summary()
        else:
            print(f"\nDevices: {len(self.devices)}")
            print(f"Sessions: {len(self.sessions)}")

# ─── Main CLI Entrypoint ──────────────────────────────────────────────────────────

def main():
    """Main entry point for OmniSec."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="OmniSec Ultimate — Autonomous Network Domination Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python omnisec.py discover              # Discover devices on local network
  python omnisec.py scan 192.168.1.0/24  # Full fingerprinting
  python omnisec.py pwn 192.168.1.0/24   # Full exploitation chain
  python omnisec.py shell session_001    # Interactive shell on session
  python omnisec.py exec "whoami" all    # Execute on all compromised
  python omnisec.py report               # Generate report
        """
    )
    
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("args", nargs="*", help="Arguments for command")
    parser.add_argument("--network", "-n", help="Target network range (CIDR)")
    parser.add_argument("--threads", "-t", type=int, default=100, help="Max worker threads")
    parser.add_argument("--timeout", type=float, default=3.0, help="Network timeout")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    parser.add_argument("--load-state", help="Load previous session state")
    parser.add_argument("--save-state", action="store_true", help="Save state after operation")
    
    args = parser.parse_args()
    
    # Logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load state if specified
    engine = UnifiedEngine()
    
    if args.load_state:
        if hasattr(engine, 'engine'):
            engine.engine.load_state(args.load_state)
        print(f"[*] State loaded from {args.load_state}")
        engine.summary()
        sys.exit(0)
    
    # Command dispatch
    cmd = args.command.lower() if args.command else "interactive"
    network = args.network
    
    if cmd in ("discover", "scan", "find"):
        print(f"{Fore.CYAN}[*] Starting device discovery...{Style.RESET_ALL}")
        devices = engine.discover(network, exhaustive=(cmd=="discover"))
        print(f"{Fore.GREEN}[+] Found {len(devices)} devices")
        for d in devices[:20]:
            print(f"    {d.ip:<18} {getattr(d, 'hostname', 'N/A'):<30} {getattr(d, 'os', 'unknown')}")
        if len(devices) > 20:
            print(f"    ... and {len(devices)-20} more")
    
    elif cmd in ("pwn", "exploit", "own"):
        print(f"{Fore.RED}[!] AUTONOMOUS EXPLOITATION INITIATED{Style.RESET_ALL}")
        results = engine.exploit_all()
        print(f"\n{Fore.GREEN}[+] Results:{Style.RESET_ALL}")
        print(f"    Total devices: {results.get('total', 0)}")
        print(f"    Exploited:     {results.get('exploited', 0)}")
        print(f"    Compromised:   {results.get('compromised', 0)}")
        print(f"    Failed:        {results.get('failed', 0)}")
        engine.summary()
        
        if args.save_state and hasattr(engine, 'engine'):
            state_path = engine.engine.save_state()
            print(f"[*] State saved: {state_path}")
    
    elif cmd in ("exec", "execute"):
        if len(args.args) < 1:
            print("Usage: python omnisec.py exec <command> [session_id...]")
            sys.exit(1)
        command = args.args[0]
        session_ids = args.args[1:] if len(args.args) > 1 else None
        results = engine.execute(command, session_ids)
        for sid, res in results.items():
            print(f"\n[{sid}]")
            print(res.get("output", res.get("error", "No output")))
    
    elif cmd in ("shell", "interactive"):
        if len(args.args) < 1:
            print("Usage: python omnisec.py shell <session_id>")
            sys.exit(1)
        engine.interactive(args.args[0])
    
    elif cmd in ("report", "generate"):
        fmt = args.args[0] if args.args else "json"
        report_path = engine.report(fmt)
        print(f"{Fore.GREEN}[+] Report saved: {report_path}")
    
    elif cmd in ("status", "sessions"):
        engine.summary()
    
    elif cmd in ("help", "?"):
        parser.print_help()
    
    else:
        # Interactive shell mode if no command given
        if not args.command:
            from commandcenter import OmniShell
            shell = OmniShell()
            try:
                asyncio.run(shell.start())
            except KeyboardInterrupt:
                print("\n[*] Shutting down...")
        else:
            print(f"Unknown command: {cmd}")
            parser.print_help()
            sys.exit(1)

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("exfil", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[CRITICAL] {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
