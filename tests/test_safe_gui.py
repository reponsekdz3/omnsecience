import ipaddress
import unittest
from unittest.mock import patch

from safe_gui import assess_from_input, parse_ports_input, parse_target_input


class SafeGuiInputTests(unittest.TestCase):
    def test_target_list_requires_explicit_ip_addresses(self):
        scope = ipaddress.ip_network("192.168.1.0/24")
        with self.assertRaisesRegex(ValueError, "comma-separated IP addresses"):
            parse_target_input("", scope)
        with self.assertRaisesRegex(ValueError, "not a hostname"):
            parse_target_input("example.com", scope)
        with self.assertRaisesRegex(ValueError, "outside authorized scope"):
            parse_target_input("192.168.2.10", scope)

    def test_target_list_deduplicates_addresses(self):
        scope = ipaddress.ip_network("192.168.1.0/24")
        self.assertEqual(
            parse_target_input("192.168.1.10, 192.168.1.11,192.168.1.10", scope),
            ["192.168.1.10", "192.168.1.11"],
        )

    def test_target_list_is_bounded(self):
        scope = ipaddress.ip_network("10.0.0.0/24")
        addresses = ",".join(f"10.0.0.{n}" for n in range(1, 130))
        with self.assertRaisesRegex(ValueError, "Limit each assessment"):
            parse_target_input(addresses, scope)

    def test_ports_are_parsed_and_deduplicated(self):
        self.assertEqual(parse_ports_input("80, 443,80"), (80, 443))

    def test_ports_reject_empty_or_invalid_values(self):
        for value in ("", "80,,443", "0", "65536", "abc"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_ports_input(value)

    @patch("safe_gui.assess_targets")
    def test_assess_from_input_uses_real_assessment_api(self, assess):
        assess.return_value = []
        report = assess_from_input("192.168.1.0/24", "192.168.1.10", "80", "1.0")
        assess.assert_called_once_with(
            ["192.168.1.10"],
            ipaddress.ip_network("192.168.1.0/24"),
            (80,),
            1.0,
        )
        self.assertEqual(report["assessment_type"], "tcp_exposure_only")
        self.assertEqual(report["observation_count"], 0)


if __name__ == "__main__":
    unittest.main()
