"""Retired unsafe manual package installer.

The supported defensive assessment uses only the Python standard library.
This script intentionally performs no downloads, disables no TLS checks, and
does not extract or overwrite files inside site-packages.
"""
import importlib.util

def main() -> int:
    available = importlib.util.find_spec("impacket") is not None
    print(f"Optional third-party Impacket package: {'present' if available else 'not installed'}")
    print("It is not required by the supported defensive assessment workflow.")
    print("No network request, archive extraction, or package modification occurred.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
