"""Legacy remote-control engine is disabled in the defensive build."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class RemoteControlEngine(DisabledLegacyEngine):
    FEATURE_NAME = "remote control"

def __getattr__(name):
    return resolve_legacy_symbol(name, "remote control")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Remote control engine"))
