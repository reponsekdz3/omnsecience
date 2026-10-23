"""Supported OMNISEC entry point.

This build exposes the non-invasive, scope-bound defensive assessment workflow.
Legacy exploit, payload, and remote-control engines are intentionally not
started from the primary entry point.
"""
from safe_assessment import main


if __name__ == "__main__":
    raise SystemExit(main())
