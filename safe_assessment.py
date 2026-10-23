"""Safe, scope-bound network exposure assessment.

This module performs TCP reachability checks only. It does not exploit services,
authenticate, brute-force credentials, execute commands, or modify remote systems.
Callers must provide an explicit authorized CIDR scope.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable, Sequence

DEFAULT_PORTS = (22, 80, 443, 445, 3389, 5985, 5986)


@dataclass(frozen=True)
class PortObservation:
    host: str
    port: int
    state: str
    service_hint: str
    evidence: str


def parse_scope(scope: str) -> ipaddress.IPv4Network | ipaddress.IPv6Network:
    """Parse a strict CIDR scope; hostnames and implicit scopes are rejected."""
    try:
        return ipaddress.ip_network(scope, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid authorized CIDR scope: {scope!r}") from exc


def validate_target(target: str, scope: ipaddress.IPv4Network | ipaddress.IPv6Network) -> str:
    try:
        address = ipaddress.ip_address(target)
    except ValueError as exc:
        raise ValueError(f"Target must be an IP address, not a hostname: {target!r}") from exc
    if address.version != scope.version or address not in scope:
        raise ValueError(f"Target {target} is outside authorized scope {scope}")
    return str(address)


def validate_ports(ports: Sequence[int]) -> tuple[int, ...]:
    """Validate and de-duplicate all requested TCP ports before connecting."""
    if not ports:
        raise ValueError("Provide at least one port")
    normalized: list[int] = []
    for port in ports:
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError("Every port must be an integer between 1 and 65535")
        if port not in normalized:
            normalized.append(port)
    return tuple(normalized)


def validate_timeout(timeout: float) -> float:
    """Keep each connection timeout bounded and reject booleans/non-numbers."""
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0.1 <= timeout <= 5.0:
        raise ValueError("Timeout must be a number between 0.1 and 5 seconds")
    return float(timeout)


def assess_tcp_port(
    host: str,
    port: int,
    timeout: float = 1.0,
    *,
    scope: ipaddress.IPv4Network | ipaddress.IPv6Network | None = None,
) -> PortObservation:
    """Record TCP reachability for an IP covered by an explicit authorized scope."""
    if scope is None:
        raise ValueError("An explicit authorized CIDR scope is required")
    host = validate_target(host, scope)
    port = validate_ports((port,))[0]
    timeout = validate_timeout(timeout)
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return PortObservation(
                host=host, port=port, state="open",
                service_hint={22: "ssh", 80: "http", 443: "https", 445: "smb",
                              3389: "rdp", 5985: "winrm-http", 5986: "winrm-https"}.get(port, "unknown"),
                evidence="TCP connection succeeded; service identity and vulnerability are unverified",
            )
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        return PortObservation(host, port, "closed_or_filtered", "unknown",
                               "Connection refused or timed out; result does not distinguish filtering from closure")
    except OSError as exc:
        return PortObservation(host, port, "error", "unknown", f"{type(exc).__name__}: {exc}")


def assess_targets(
    targets: Iterable[str],
    scope: ipaddress.IPv4Network | ipaddress.IPv6Network,
    ports: Sequence[int] = DEFAULT_PORTS,
    timeout: float = 1.0,
) -> list[PortObservation]:
    """Assess explicit IPs inside the authorized scope; no CIDR-wide expansion."""
    normalized = list(dict.fromkeys(validate_target(target, scope) for target in targets))
    if not normalized:
        raise ValueError("Provide at least one explicit target IP")
    validated_ports = validate_ports(ports)
    validated_timeout = validate_timeout(timeout)
    # Validate the complete request before the first socket connection, avoiding
    # partial network scans when a later port or timeout is invalid.
    return [
        assess_tcp_port(host, port, validated_timeout, scope=scope)
        for host in normalized
        for port in validated_ports
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scope-bound, non-invasive TCP exposure assessment")
    parser.add_argument("--authorized-scope", required=True, help="CIDR you are explicitly authorized to assess")
    parser.add_argument("--target", action="append", required=True, help="Explicit target IP; repeat as needed")
    parser.add_argument("--ports", default=",".join(map(str, DEFAULT_PORTS)), help="Comma-separated TCP ports")
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--output", default="-", help="JSON output path, or - for stdout")
    args = parser.parse_args(argv)
    try:
        scope = parse_scope(args.authorized_scope)
        ports = tuple(dict.fromkeys(int(value.strip()) for value in args.ports.split(",") if value.strip()))
        results = assess_targets(args.target, scope, ports, args.timeout)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assessment_type": "tcp_exposure_only",
        "authorized_scope": str(scope),
        "limitations": [
            "Open TCP ports do not prove a vulnerability or successful authentication.",
            "No exploitation, credential testing, command execution, or remote modification is performed.",
        ],
        "observations": [asdict(item) for item in results],
    }
    rendered = json.dumps(report, indent=2)
    if args.output == "-":
        print(rendered)
    else:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
