import ipaddress
import unittest
from unittest.mock import patch

from safe_assessment import assess_tcp_port, assess_targets, parse_scope, validate_target


class ScopeValidationTests(unittest.TestCase):
    def test_rejects_invalid_scope(self):
        with self.assertRaises(ValueError):
            parse_scope("not-a-cidr")

    def test_rejects_hostname(self):
        with self.assertRaises(ValueError):
            validate_target("example.com", ipaddress.ip_network("192.168.1.0/24"))

    def test_rejects_target_outside_scope(self):
        with self.assertRaises(ValueError):
            validate_target("192.168.2.10", ipaddress.ip_network("192.168.1.0/24"))

    def test_rejects_ipv4_target_for_ipv6_scope(self):
        with self.assertRaises(ValueError):
            validate_target("192.168.1.10", ipaddress.ip_network("2001:db8::/32"))

    def test_requires_explicit_targets(self):
        with self.assertRaises(ValueError):
            assess_targets([], ipaddress.ip_network("192.168.1.0/24"), [80])


class PortAssessmentTests(unittest.TestCase):
    @patch("safe_assessment.socket.create_connection")
    def test_open_port_is_not_reported_as_vulnerability(self, connect):
        connect.return_value.__enter__.return_value = object()
        result = assess_tcp_port("192.168.1.10", 445)
        self.assertEqual(result.state, "open")
        self.assertIn("vulnerability are unverified", result.evidence)
        self.assertEqual(result.service_hint, "smb")

    def test_rejects_invalid_port(self):
        with self.assertRaises(ValueError):
            assess_tcp_port("127.0.0.1", 70000)

    def test_rejects_unsafe_timeout(self):
        with self.assertRaises(ValueError):
            assess_tcp_port("127.0.0.1", 80, timeout=30)


if __name__ == "__main__":
    unittest.main()
