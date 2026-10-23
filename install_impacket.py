"""Retired custom Impacket installer.

The supported defensive assessment workflow uses only the Python standard
library. This helper no longer downloads, builds, or installs a network attack
toolkit. Install third-party dependencies only through reviewed, pinned package
management in an isolated environment.
"""
import importlib.util

def main() -> int:
    available = importlib.util.find_spec("impacket") is not None
    print(f"Optional third-party Impacket package: {'present' if available else 'not installed'}")
    print("It is not required by the supported defensive assessment workflow.")
    print("No package was downloaded or installed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
