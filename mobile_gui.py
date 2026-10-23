"""Retired legacy UI; this Python repository does not contain a native mobile client.

The former UI exposed unreviewed remote-access workflows. No mobile simulation or
fake mobile client is substituted here. Use the desktop GUI ('python gui.py') or
the scope-bound CLI ('python main.py --help').
"""
from legacy_compat import disabled_main, resolve_legacy_symbol

def __getattr__(name):
    return resolve_legacy_symbol(name, "retired legacy UI")

def main() -> int:
    print("No native mobile client is implemented in this repository. Use 'python gui.py' for desktop assessment.")
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
