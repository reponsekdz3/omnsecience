# OMNISEC / OMNISCIENCE

A Python security-assessment codebase under hardening. The repository historically described capabilities such as “100+ real exploits,” payload generation, remote control, and device takeover. Those claims were not substantiated by the code inspected: several routines treated a reachable port as proof of a CVE, and some routines returned success without performing the claimed operation.

This branch prioritizes **truthful results, safe defensive assessment, scope enforcement, tests, and reproducible quality gates**. It does not claim that the entire legacy codebase is production-ready.

## Supported in this branch

### Scope-bound TCP exposure assessment

The supported entry point is now `main.py`, which delegates to the same tested defensive assessment CLI. The legacy autonomous exploit/scanner launcher is not used by the primary entry point.

`safe_assessment.py` provides non-invasive TCP reachability checks against explicitly supplied IP addresses inside an explicitly supplied CIDR. It does not expand an entire CIDR into targets automatically.

```bash
python main.py --authorized-scope 192.168.1.0/24 --target 192.168.1.10 --ports 22,80,443,445 --output report.json
```

You can also run `python safe_assessment.py` directly. Repeat `--target` for additional IP addresses. Use only systems you own or are explicitly authorized to assess.

Reports use observations such as `open`, `closed_or_filtered`, and `error`. An open port is **not** reported as a vulnerability, and a timeout does not distinguish filtering from a closed service.

### Fail-closed legacy command center

The legacy command center no longer imports missing `payloads` or `remote_control_engine` modules at startup. Offensive exploit execution, payload generation, and remote-control providers are replaced with an explicit disabled adapter. Unsupported calls return `status: unsupported` and `success: false`; they do not claim that an action was performed. The command center displays this restricted mode when it starts.

### Corrected legacy checks

Several legacy methods now report service reachability as inconclusive rather than claiming EternalBlue, BlueKeep, Zerologon, PrintNightmare, WinRM execution, or PetitPotam success based only on a TCP connection. The SMB relay stub explicitly reports that the operation is unsupported instead of returning fabricated success.

### Automated quality checks

GitHub Actions runs Python bytecode compilation and the standard-library unit tests on pushes to this branch and pull requests targeting `master`.

```bash
python -m py_compile main.py safe_assessment.py safe_feature_guard.py command_center.py exploitation_techniques.py
python -m unittest discover -s tests -v
```

The compilation command above checks only the supported defensive entry points. The full legacy repository is **not yet syntax-clean**: older files including `omnisec_engine.py` contain known parse errors, so the current passing CI run must not be interpreted as a successful audit of every file. Those legacy engines remain out of the supported path and require separate remediation before production use.

## Important limitations

- This branch does **not** implement or claim to implement real exploitation, payload delivery, credential theft, persistence, stealth, remote device takeover, Android surveillance, or industrial-control operations.
- Legacy modules outside the hardened path may still contain unsafe or incomplete behavior. Do not run them against third-party systems or production infrastructure.
- Optional dependencies, OS-specific utilities, and third-party protocols have not all been validated on every supported platform.
- CI results must be observed on GitHub; a workflow file being present is not evidence that a run passed.
- A successful TCP connection is service exposure evidence only. CVE verification requires reliable protocol-level checks, authenticated configuration/patch evidence, or a trusted scanner.

## Security and authorization

Only assess assets within a written authorization scope. Prefer a staging environment first. Keep reports access-controlled because they may reveal internal network structure. Review all legacy commands before enabling them in an operational environment.

## Roadmap

1. Inventory all entry points, imports, and dependencies.
2. Replace misleading “success” booleans with typed outcomes and evidence.
3. Add tests for each supported defensive check and error path.
4. Isolate unsupported legacy attack functionality behind explicit disabled status.
5. Add dependency pinning, static analysis, secret scanning, and signed releases.
6. Expand only with documented, non-destructive checks that can be verified by tests.

## Project status

**Hardening in progress — not yet production-certified.** The project should not be described as fully functional or production-ready until the full codebase has been audited, tests pass in CI, security review is complete, and platform-specific behavior is verified.
