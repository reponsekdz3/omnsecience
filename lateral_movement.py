"""Legacy lateral-movement automation is disabled in the defensive build."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class AdvancedCommandCenter(DisabledLegacyEngine):
    FEATURE_NAME = "lateral movement"

def __getattr__(name):
    return resolve_legacy_symbol(name, "lateral movement")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Lateral movement"))
