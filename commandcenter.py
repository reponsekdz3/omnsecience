"""Legacy multi-purpose command shell retired in favor of the safe command center."""
from command_center import OmniSecCommandCenter
from legacy_compat import disabled_main, resolve_legacy_symbol

OmniShell = OmniSecCommandCenter

def __getattr__(name):
    return resolve_legacy_symbol(name, "legacy command shell")

if __name__ == "__main__":
    OmniSecCommandCenter().cmdloop()
