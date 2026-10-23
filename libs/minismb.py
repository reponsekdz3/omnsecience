"""Retired custom SMB client.

The former implementation included null-session authentication and SMB file
operations. Use standard, vendor-supported tooling in a separately reviewed
authorized workflow; this client deliberately performs no network operations.
"""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class SMBConnection(DisabledLegacyEngine):
    FEATURE_NAME = "legacy custom SMB client"

def __getattr__(name):
    return resolve_legacy_symbol(name, "legacy custom SMB client")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Custom SMB client"))
