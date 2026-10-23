import unittest

from safe_feature_guard import DisabledFeatureProvider


class DisabledFeatureProviderTests(unittest.TestCase):
    def test_unknown_operations_fail_closed(self):
        provider = DisabledFeatureProvider("remote control")
        result = provider.start_keylogger("192.0.2.10", 60)
        self.assertFalse(result["success"])
        self.assertEqual(result["status"], "unsupported")
        self.assertEqual(result["feature"], "remote control")
        self.assertIn("no remote action was performed", result["error"])

    def test_legacy_enumeration_returns_empty(self):
        provider = DisabledFeatureProvider("payload generation")
        self.assertEqual(provider.get_all_payloads(), [])
        self.assertEqual(provider.get_all_techniques(), [])
        self.assertEqual(provider.list_sessions(), [])
        self.assertEqual(provider.active_sessions, {})


if __name__ == "__main__":
    unittest.main()
