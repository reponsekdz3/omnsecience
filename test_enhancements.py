"""Legacy active-network enhancement script retired.

Older tests made live network calls and expected unverified device fingerprint
values. Deterministic unit tests live under tests/ and are run with unittest.
"""
import unittest

def main() -> int:
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())
