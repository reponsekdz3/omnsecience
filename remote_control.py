"""Legacy remote-control and credential-access functionality is disabled."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class AgentlessControl(DisabledLegacyEngine):
    FEATURE_NAME = "remote control"

def __getattr__(name):
    return resolve_legacy_symbol(name, "remote control")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Remote control"))
