import unittest

from advanced_scanner import AdvancedNetworkScanner
from exploitation_techniques import ExploitationTechniques
from exploit_engine import UniversalNetworkAccess
from lateral_movement import AdvancedCommandCenter
from omnisec_engine import RealOmniSecEngine
from remote_control import AgentlessControl
from remote_control_engine import RemoteControlEngine


class LegacyAdapterTests(unittest.TestCase):
    def assert_unsupported(self, result):
        self.assertFalse(result.get("success", True))
        self.assertEqual(result.get("status"), "unsupported")
        self.assertIn("no remote action was performed", result.get("error", ""))

    def test_exploit_engine_calls_fail_closed(self):
        result = ExploitationTechniques().exploit_04_psexec("192.0.2.10", "admin", "password")
        self.assert_unsupported(result)

    def test_remote_control_calls_fail_closed(self):
        result = AgentlessControl().execute_command("192.0.2.10", "whoami")
        self.assert_unsupported(result)

    def test_remote_control_engine_calls_fail_closed(self):
        result = RemoteControlEngine().start_session("192.0.2.10")
        self.assert_unsupported(result)

    def test_lateral_movement_calls_fail_closed(self):
        result = AdvancedCommandCenter().move_laterally("192.0.2.10", "192.0.2.11")
        self.assert_unsupported(result)

    def test_autonomous_engine_calls_fail_closed(self):
        result = RealOmniSecEngine().establish_persistence("192.0.2.10")
        self.assert_unsupported(result)

    def test_unscoped_scanner_calls_fail_closed(self):
        result = AdvancedNetworkScanner().scan_network("192.168.1.0/24")
        self.assert_unsupported(result)

    def test_legacy_module_functions_fail_closed(self):
        from omnisec_engine import run_full_operation

        self.assert_unsupported(run_full_operation("192.0.2.0/24"))


if __name__ == "__main__":
    unittest.main()
