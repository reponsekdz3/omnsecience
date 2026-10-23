"""Retired unsafe verification script.

The previous version attempted SSH login with hard-coded credentials and claimed
compromise based on connection behavior. Use the scope-bound assessment instead.
"""
from legacy_compat import disabled_main, resolve_legacy_symbol

def __getattr__(name):
    return resolve_legacy_symbol(name, "legacy verification")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Legacy compromise verification"))
