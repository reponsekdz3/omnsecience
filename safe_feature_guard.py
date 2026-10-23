"""Explicitly disabled adapter for retired offensive capabilities.

Unsupported legacy operations never contact hosts or claim success. Methods that
used to enumerate exploits, payloads, and remote sessions return explicit status
objects instead of empty lists that could be mistaken for verified results.
"""
from __future__ import annotations

from typing import Any


class DisabledFeatureProvider:
    """Compatibility adapter that fails closed for unsupported operations."""

    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def _unsupported(self, operation: str) -> dict[str, Any]:
        return {
            "success": False,
            "status": "unsupported",
            "feature": self.feature_name,
            "operation": operation,
            "error": "This operation is disabled in the defensive build; no remote action was performed.",
        }

    def get_all_techniques(self) -> dict[str, Any]:
        return self._unsupported("get_all_techniques")

    def get_all_payloads(self) -> dict[str, Any]:
        return self._unsupported("get_all_payloads")

    def list_sessions(self) -> dict[str, Any]:
        return self._unsupported("list_sessions")

    @property
    def active_sessions(self) -> dict[str, Any]:
        return self._unsupported("active_sessions")

    def __getattr__(self, name: str):
        if name.startswith("__"):
            raise AttributeError(name)

        def unsupported(*args, **kwargs):
            return self._unsupported(name)

        return unsupported


class DisabledLegacyEngine(DisabledFeatureProvider):
    """Compatibility base for retired legacy attack engines.

    Constructors accept historical arguments so importing old call sites does
    not accidentally execute network actions. All dynamic operations inherit
    the fail-closed result from DisabledFeatureProvider.
    """

    FEATURE_NAME = "legacy operation"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(self.FEATURE_NAME)


def disabled_cli(feature_name: str) -> int:
    """Explain why a retired legacy executable does not perform remote actions."""
    print(
        f"{feature_name} is disabled in this defensive build. "
        "No remote action was performed. Use 'python main.py --help' for the "
        "supported, scope-bound assessment workflow."
    )
    return 2
