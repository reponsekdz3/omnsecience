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
        result = assess_tcp_port(
            "192.168.1.10", 445,
            scope=ipaddress.ip_network("192.168.1.0/24"),
        )
        self.assertEqual(result.state, "open")
        self.assertIn("vulnerability are unverified", result.evidence)
        self.assertEqual(result.service_hint, "smb")

    def test_rejects_invalid_port(self):
        with self.assertRaises(ValueError):
            assess_tcp_port(
                "127.0.0.1", 70000,
                scope=ipaddress.ip_network("127.0.0.0/8"),
            )

    def test_rejects_unsafe_timeout(self):
        with self.assertRaises(ValueError):
            assess_tcp_port(
                "127.0.0.1", 80, timeout=30,
                scope=ipaddress.ip_network("127.0.0.0/8"),
            )

    @patch("safe_assessment.socket.create_connection")
    def test_direct_port_check_requires_scope(self, connect):
        with self.assertRaisesRegex(ValueError, "authorized CIDR scope"):
            assess_tcp_port("192.168.1.10", 80)
        connect.assert_not_called()

    @patch("safe_assessment.socket.create_connection")
    def test_direct_port_check_rejects_out_of_scope_target(self, connect):
        with self.assertRaisesRegex(ValueError, "outside authorized scope"):
            assess_tcp_port(
                "192.168.2.10", 80,
                scope=ipaddress.ip_network("192.168.1.0/24"),
            )
        connect.assert_not_called()

    @patch("safe_assessment.socket.create_connection")
    def test_invalid_later_port_fails_before_any_network_io(self, connect):
        with self.assertRaises(ValueError):
            assess_targets(
                ["192.168.1.10"],
                ipaddress.ip_network("192.168.1.0/24"),
                [80, 70000],
            )
        connect.assert_not_called()

    @patch("safe_assessment.socket.create_connection")
    def test_probe_limit_rejects_request_before_network_io(self, connect):
        targets = [f"10.0.0.{n}" for n in range(1, 33)]
        ports = list(range(1, 66))  # 32 targets x 65 ports exceeds the request cap.
        with self.assertRaisesRegex(ValueError, "limit each request"):
            assess_targets(
                targets,
                ipaddress.ip_network("10.0.0.0/24"),
                ports,
            )
        connect.assert_not_called()

    @patch("safe_assessment.socket.create_connection")
    def test_duplicate_ports_are_checked_once(self, connect):
        connect.return_value.__enter__.return_value = object()
        results = assess_targets(
            ["192.168.1.10"],
            ipaddress.ip_network("192.168.1.0/24"),
            [80, 80],
        )
        self.assertEqual(len(results), 1)
        connect.assert_called_once()


if __name__ == "__main__":
    unittest.main()
