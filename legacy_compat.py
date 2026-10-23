"""Fail-closed compatibility utilities for retired legacy attack modules.

Only the explicit safe_assessment entry point performs network operations.
Legacy imports resolve to disabled adapters so importing old names does not
restore remote-control, exploit, persistence, or credential-access behavior.
"""
from __future__ import annotations

from typing import Any

from safe_feature_guard import DisabledLegacyEngine


def unsupported_result(feature: str, operation: str, **details: Any) -> dict[str, Any]:
    return {
        "success": False,
        "status": "unsupported",
        "feature": feature,
        "operation": operation,
        "error": "This operation is disabled in the defensive build; no remote action was performed.",
        **details,
    }


def resolve_legacy_symbol(name: str, feature: str):
    """Resolve historical imports to inert classes/results, never real operations."""
    if name.startswith("__"):
        raise AttributeError(name)
    if name.endswith("_OK"):
        return False
    if name.endswith("_MAP") or name.endswith("_DB") or name.endswith("_DICT"):
        return {}
    if name.isupper():
        return ()
    if name[:1].isupper():
        return type(name, (DisabledLegacyEngine,), {"FEATURE_NAME": feature, "__module__": __name__})

    def unsupported(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return unsupported_result(feature, name)

    return unsupported


def disabled_main(feature: str) -> int:
    print(
        f"{feature} is disabled in this defensive build. No remote action was performed. "
        "Use 'python main.py --help' for the supported scope-bound assessment workflow."
    )
    return 2
