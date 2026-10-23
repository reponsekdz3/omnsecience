"""Retired unscoped network-discovery routines."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class NetworkDiscovery(DisabledLegacyEngine):
    FEATURE_NAME = "unscoped legacy network discovery"

def __getattr__(name):
    return resolve_legacy_symbol(name, "unscoped legacy network discovery")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Unscoped legacy network discovery"))
