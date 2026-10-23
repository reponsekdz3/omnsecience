"""Explicitly disabled adapter for legacy offensive capabilities.

The legacy command center references payload delivery, exploit execution, and
remote-control operations that are not supported by this defensive build.
This adapter makes unsupported actions fail closed and never reports success.
"""
from __future__ import annotations

from typing import Any


class DisabledFeatureProvider:
    """Compatibility adapter that fails closed for unsupported operations."""

    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def get_all_techniques(self) -> list[str]:
        return []

    def get_all_payloads(self) -> list[str]:
        return []

    def list_sessions(self) -> list[Any]:
        return []

    @property
    def active_sessions(self) -> dict[str, Any]:
        return {}

    def __getattr__(self, name: str):
        if name.startswith("__"):
            raise AttributeError(name)

        def unsupported(*args, **kwargs):
            return {
                "success": False,
                "status": "unsupported",
                "feature": self.feature_name,
                "operation": name,
                "error": "This operation is disabled in the defensive build; no remote action was performed.",
            }
        return unsupported
