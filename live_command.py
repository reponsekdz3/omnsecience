
import sys
import os
import asyncio
import threading
from datetime import datetime

# Setup paths
sys.path.insert(0, r"C:\\Users\\user\\Desktop\\omnsecience")

from colorama import Fore, Style, init
init(autoreset=True)

# Import command center
from commandcenter import OmniShell

def run_command_shell():
    """Run the command shell in this window."""
    print(Fore.CYAN + "=" * 100)
    print(Fore.CYAN + "||" + Fore.GREEN + " OMNISCIENCE COMMAND CENTER " + Fore.CYAN + "||")
    print(Fore.CYAN + "||" + Fore.YELLOW + " INTERACTIVE COMMAND SHELL " + Fore.CYAN + "||")
    print(Fore.CYAN + "=" * 100)
    print()
    
    # Create shell instance
    shell = OmniShell()
    
    print(Fore.GREEN + "[+] Command Center initialized")
    print(Fore.YELLOW + "[*] Type 'help' for available commands")
    print(Fore.YELLOW + "[*] Type 'scan' to initiate network scan")
    print(Fore.YELLOW + "[*] Type 'pwn' to exploit accessible devices")
    print()
    
    # Run the shell
    asyncio.run(shell.start())

if __name__ == "__main__":
    run_command_shell()
