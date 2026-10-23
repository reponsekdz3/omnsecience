"""Legacy Kivy attack UI retired; use the supported scope-bound desktop UI."""
from safe_gui import main
from legacy_compat import resolve_legacy_symbol

def __getattr__(name):
    return resolve_legacy_symbol(name, "retired Kivy attack UI")

if __name__ == "__main__":
    raise SystemExit(main())
