# OMNISEC — Defensive Exposure Assessment

OMNISEC is currently maintained as a **scope-bound, non-invasive defensive assessment tool**. The legacy repository advertised autonomous exploitation, credential collection, remote command execution, persistence, and device takeover; source review found misleading success claims and hard-coded credential tests. Those legacy offensive paths have been retired from the first-party application entry points.

This is a functioning defensive assessment workflow, **not a claim that the whole historical repository is production-certified**.

## Supported functionality

### CLI: real TCP reachability

The supported command performs actual TCP connection attempts against a list of explicit IP addresses, checks that every address is inside an explicitly supplied CIDR, validates the complete request before network I/O, and writes a JSON report from the actual socket observations. It never expands a subnet automatically.

Requirements: Python 3.10 or later. The supported CLI uses only the Python standard library.

```bash
python main.py --help
python main.py --authorized-scope 192.168.1.0/24 --target 192.168.1.10 --ports 22,80,443,445 --output report.json
```

Repeat `--target` to add more explicit IPs. Each request is limited to 128 targets, 128 ports, and 2,048 target/port probes, with at most 32 concurrent connection workers and a per-connection timeout from 0.1 to 5 seconds. These are guardrails, not authorization; assess only systems in your written scope.

The report uses `open`, `closed_or_filtered`, or `error` observations. A successful TCP handshake is not proof of the service identity, a CVE, weak authentication, or compromise. No credentials are tested and no remote commands or changes are made.

### Desktop UI: `gui.py`

Run `python gui.py` on a desktop environment with Tkinter. The UI is wired to the same assessment functions as the CLI: it validates the scope and explicit target list, performs real TCP checks on a worker thread, displays the resulting JSON report, and exports the actual report through a save dialog. It does not show fabricated device lists or fake successful results. If Tkinter is unavailable or the environment is headless, use the CLI.

### Interactive command center: `command_center.py`

Run `python command_center.py` to use the console, or `python live_command.py`. Use these commands:

- `scope 192.168.1.0/24` — register the authorized scope.
- `target 192.168.1.10` — add one explicit IP inside the scope.
- `targets` — list registered targets.
- `ports 22,80,443` — configure TCP ports.
- `timeout 1.0` — configure the bounded timeout.
- `assess` — run the real checks and print an evidence-based JSON report.
- `exit` — leave the console.

Legacy commands for exploitation, payload generation, packet-based credential collection, remote control, persistence, and lateral movement return an explicit unsupported status or are retired. Their failure is not reported as successful operation.

## Tests and CI

The GitHub Actions workflow compiles all **first-party Python source files** outside `.local/` and the vendored `impacket_src/` tree, then runs the deterministic standard-library tests:

```bash
python -m unittest discover -s tests -v
```

For the same first-party syntax check locally, run:

```bash
python - <<'PY'
from pathlib import Path
import sys

excluded_parts = {".git", ".local", "impacket_src", "__pycache__"}
files = [
    path for path in Path(".").rglob("*.py")
    if not any(part in excluded_parts for part in path.parts)
]
errors = []
for path in sorted(files):
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, UnicodeError, SyntaxError) as exc:
        errors.append(f"{path}: {exc}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"Successfully compiled {len(files)} first-party Python files.")
PY
```

Tests use mocks only to verify boundary/error behavior deterministically; the application workflow itself uses actual TCP sockets and actual file export. Test success is not equivalent to a security certification or proof of behavior on every operating system.

## Repository boundary and remaining limitations

- The top-level legacy application modules that previously provided exploit, remote-control, credential-collection, and unscoped scanning paths have been replaced with fail-closed compatibility shims or safe launchers.
- `impacket_src/` is a vendored third-party project with its own example utilities. It is outside OMNISEC's supported runtime, is excluded from OMNISEC's first-party CI check, and has **not** been audited as part of this change. Do not run its example scripts as part of this application.
- This Python project does not currently provide a native Android/iOS client. The old `mobile_gui.py` entry point clearly states that limitation rather than simulating a mobile app.
- The supported assessment does not perform protocol-level CVE checks, authenticated configuration review, TLS certificate evaluation, service fingerprinting, or remediation. Those should be separate, well-scoped features with their own verified implementations and tests.
- Avoid committing real assessment reports or operational logs to version control; they can disclose internal asset information and can be mistaken for verified evidence.

## Authorization

Only assess assets covered by written authorization. Start with a small allowlisted target set, protect exported reports, and do not infer vulnerability or compromise from port reachability alone.

## Project status

**Defensive hardening in progress.** The supported CLI, console, and desktop assessment path is being tested in CI. The broader third-party/vendor tree and platform-specific behavior have not been certified for production.
