"""Retired legacy scanner display. No network actions are performed by this module."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class LiveNetworkScanner(DisabledLegacyEngine):
    FEATURE_NAME = "unscoped legacy scanning"

class LiveDevice(DisabledLegacyEngine):
    FEATURE_NAME = "legacy device object"

def __getattr__(name):
    return resolve_legacy_symbol(name, "unscoped legacy scanning")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Unscoped legacy scanning"))
