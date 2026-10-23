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

    def test_legacy_enumeration_reports_unsupported_instead_of_fake_empty_results(self):
        provider = DisabledFeatureProvider("payload generation")
        for result in (
            provider.get_all_payloads(),
            provider.get_all_techniques(),
            provider.list_sessions(),
            provider.active_sessions,
        ):
            self.assertFalse(result["success"])
            self.assertEqual(result["status"], "unsupported")
            self.assertIn("no remote action was performed", result["error"])


if __name__ == "__main__":
    unittest.main()
