"""Legacy hard-coded SSH credential test retired; no host is contacted."""
from legacy_compat import disabled_main, resolve_legacy_symbol

def __getattr__(name):
    return resolve_legacy_symbol(name, "legacy SSH credential test")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Legacy SSH credential test"))
