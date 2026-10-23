"""Legacy packet sniffing/credential-harvesting module is disabled."""
from safe_feature_guard import DisabledLegacyEngine
from legacy_compat import disabled_main, resolve_legacy_symbol

class AgentlessIntelligence(DisabledLegacyEngine):
    FEATURE_NAME = "passive packet capture and credential collection"

def __getattr__(name):
    return resolve_legacy_symbol(name, "passive packet capture and credential collection")

if __name__ == "__main__":
    raise SystemExit(disabled_main("Passive intelligence / packet capture"))
