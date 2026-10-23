"""Legacy wide-range scanner retired; use the explicit scope-bound assessment CLI."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class AdvancedNetworkScanner(DisabledLegacyEngine):
    FEATURE_NAME = "unscoped legacy scanning"

def __getattr__(name):
    return resolve_legacy_symbol(name, "unscoped legacy scanning")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Unscoped legacy network scanning"))
