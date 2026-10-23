"""Interactive defensive command center backed by real scope-bound checks.

Legacy exploit, payload, remote-control, persistence, and lateral-movement commands
are intentionally not exposed here. Use only targets covered by written authorization.
"""
from __future__ import annotations

import cmd
import json
from dataclasses import asdict
from datetime import datetime, timezone

from safe_assessment import (
    DEFAULT_PORTS,
    assess_targets,
    parse_scope,
    validate_ports,
    validate_target,
    validate_timeout,
)


class OmniSecCommandCenter(cmd.Cmd):
    intro = (
        "OMNISEC defensive assessment console\n"
        "Set an authorized CIDR with 'scope <cidr>', add explicit IPs with "
        "'target <ip>', then run 'assess'. Type 'help' for commands.\n"
    )
    prompt = "OMNISEC> "

    def __init__(self) -> None:
        super().__init__()
        self.scope = None
        self.targets: list[str] = []
        self.ports = DEFAULT_PORTS
        self.timeout = 1.0

    def do_scope(self, arg: str) -> None:
        """Set authorized CIDR scope: scope 192.168.1.0/24"""
        if not arg.strip():
            print(f"Authorized scope: {self.scope or '(not set)'}")
            return
        try:
            scope = parse_scope(arg.strip())
        except ValueError as exc:
            print(f"Invalid scope: {exc}")
            return
        self.scope = scope
        self.targets.clear()
        print(f"Authorized scope set to {scope}. Existing targets were cleared.")

    def do_target(self, arg: str) -> None:
        """Add one explicit in-scope IP address: target 192.168.1.10"""
        if self.scope is None:
            print("Set an authorized CIDR first with 'scope <cidr>'.")
            return
        if not arg.strip():
            print("Usage: target <IP-address>")
            return
        try:
            address = validate_target(arg.strip(), self.scope)
        except ValueError as exc:
            print(f"Target rejected: {exc}")
            return
        if address not in self.targets:
            self.targets.append(address)
        print(f"Target registered: {address}")

    def do_targets(self, arg: str) -> None:
        """List only the explicitly registered in-scope targets."""
        if self.targets:
            for target in self.targets:
                print(target)
        else:
            print("No targets registered.")

    def do_ports(self, arg: str) -> None:
        """Set TCP ports: ports 22,80,443 (default is a short common-port list)."""
        if not arg.strip():
            print("TCP ports: " + ",".join(map(str, self.ports)))
            return
        try:
            raw_values = arg.split(",")
            if any(not value.strip() for value in raw_values):
                raise ValueError("Provide comma-separated port numbers without empty entries")
            ports = validate_ports(tuple(int(value.strip()) for value in raw_values))
        except ValueError as exc:
            print(f"Ports rejected: {exc}")
            return
        self.ports = ports
        print("TCP ports set to: " + ",".join(map(str, self.ports)))

    def do_timeout(self, arg: str) -> None:
        """Set connection timeout in seconds (0.1 to 5): timeout 1.5"""
        if not arg.strip():
            print(f"Connection timeout: {self.timeout:g} seconds")
            return
        try:
            timeout = validate_timeout(float(arg.strip()))
        except ValueError as exc:
            print(f"Timeout rejected: {exc}")
            return
        self.timeout = timeout
        print(f"Connection timeout set to {timeout:g} seconds.")

    def do_assess(self, arg: str) -> None:
        """Run actual TCP reachability checks against registered in-scope IPs."""
        if self.scope is None:
            print("Assessment blocked: set an authorized scope first.")
            return
        if not self.targets:
            print("Assessment blocked: add at least one explicit in-scope IP target.")
            return
        if arg.strip():
            print("This command takes no arguments; configure targets with 'target <ip>'.")
            return
        try:
            observations = assess_targets(
                self.targets, self.scope, self.ports, self.timeout
            )
        except (ValueError, OSError) as exc:
            print(f"Assessment failed: {type(exc).__name__}: {exc}")
            return
        report = {
            "schema_version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assessment_type": "tcp_exposure_only",
            "authorized_scope": str(self.scope),
            "limitations": [
                "TCP reachability does not prove service identity or vulnerability.",
                "No exploitation, authentication, command execution, or remote modification is performed.",
            ],
            "observations": [asdict(item) for item in observations],
        }
        print(json.dumps(report, indent=2))

    do_scan = do_assess

    def do_exit(self, arg: str) -> bool:
        """Exit the console."""
        return True

    def do_quit(self, arg: str) -> bool:
        """Exit the console."""
        return True

    def do_EOF(self, arg: str) -> bool:
        print()
        return True


if __name__ == "__main__":
    OmniSecCommandCenter().cmdloop()
