"""Legacy GUI-manager launcher redirected to the supported assessment UI."""
from safe_gui import main
from legacy_compat import resolve_legacy_symbol

def __getattr__(name):
    return resolve_legacy_symbol(name, "retired GUI integration")

if __name__ == "__main__":
    raise SystemExit(main())
