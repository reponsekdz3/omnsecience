"""Desktop UI for the supported, scope-bound defensive TCP assessment.

All network activity is delegated to safe_assessment after validating an explicit
CIDR, explicit IP targets, bounded TCP ports, and a bounded timeout. The worker
thread keeps the window responsive; reports reflect actual socket observations.
"""
from __future__ import annotations

import json
import queue
import threading
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from safe_assessment import (
    DEFAULT_PORTS,
    PortObservation,
    assess_targets,
    parse_scope,
    validate_ports,
    validate_target,
    validate_timeout,
)

MAX_TARGETS = 128


def parse_target_input(value: str, scope) -> list[str]:
    """Parse a comma-separated list of explicit in-scope IPs."""
    pieces = [part.strip() for part in value.split(",")]
    if not pieces or any(not part for part in pieces):
        raise ValueError("Enter one or more comma-separated IP addresses")
    if len(pieces) > MAX_TARGETS:
        raise ValueError(f"Limit each assessment to {MAX_TARGETS} explicit targets")
    return list(dict.fromkeys(validate_target(part, scope) for part in pieces))


def parse_ports_input(value: str) -> tuple[int, ...]:
    """Parse and validate a comma-separated port list."""
    pieces = [part.strip() for part in value.split(",")]
    if not pieces or any(not part for part in pieces):
        raise ValueError("Enter comma-separated port numbers")
    try:
        return validate_ports(tuple(int(part) for part in pieces))
    except ValueError as exc:
        raise ValueError(f"Invalid ports: {exc}") from exc


def build_report(scope, observations: Sequence[PortObservation]) -> dict[str, Any]:
    """Build a report exclusively from observed results."""
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assessment_type": "tcp_exposure_only",
        "authorized_scope": str(scope),
        "target_count": len({item.host for item in observations}),
        "observation_count": len(observations),
        "limitations": [
            "TCP reachability does not establish service identity or vulnerability.",
            "No exploitation, authentication, credential testing, command execution, or remote modification is performed.",
            "Closed and filtered ports cannot always be distinguished from TCP timeout evidence.",
        ],
        "observations": [asdict(item) for item in observations],
    }


def assess_from_input(
    scope_text: str, targets_text: str, ports_text: str, timeout_text: str
) -> dict[str, Any]:
    """Validate a complete request before beginning any network I/O."""
    scope = parse_scope(scope_text.strip())
    targets = parse_target_input(targets_text, scope)
    ports = parse_ports_input(ports_text)
    try:
        timeout = validate_timeout(float(timeout_text.strip()))
    except ValueError as exc:
        raise ValueError(f"Invalid timeout: {exc}") from exc
    observations = assess_targets(targets, scope, ports, timeout)
    return build_report(scope, observations)


class DefensiveAssessmentApp:
    def __init__(self, root) -> None:
        import tkinter as tk
        from tkinter import ttk

        self.tk = tk
        self.ttk = ttk
        self.root = root
        self.events: queue.Queue[tuple[str, Any]] = queue.Queue()
        self.last_report: dict[str, Any] | None = None
        self.running = False

        root.title("OMNISEC — Defensive Exposure Assessment")
        root.geometry("1024x760")
        root.minsize(760, 560)

        shell = ttk.Frame(root, padding=18)
        shell.pack(fill="both", expand=True)
        ttk.Label(shell, text="Defensive Exposure Assessment", font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(
            shell,
            text="Non-invasive TCP reachability checks. Explicit authorization scope and IP targets are required.",
            wraplength=950,
        ).pack(anchor="w", pady=(4, 14))

        form = ttk.Frame(shell)
        form.pack(fill="x")
        self.scope_var = tk.StringVar(value="")
        self.targets_var = tk.StringVar(value="")
        self.ports_var = tk.StringVar(value=",".join(map(str, DEFAULT_PORTS)))
        self.timeout_var = tk.StringVar(value="1.0")

        def row(label: str, variable, hint: str = "") -> None:
            line = ttk.Frame(form)
            line.pack(fill="x", pady=4)
            ttk.Label(line, text=label, width=17).pack(side="left")
            ttk.Entry(line, textvariable=variable).pack(side="left", fill="x", expand=True)
            if hint:
                ttk.Label(line, text=hint, width=18).pack(side="left", padx=(8, 0))

        row("Authorized CIDR", self.scope_var, "e.g. 192.168.1.0/24")
        row("Explicit targets", self.targets_var, "comma-separated IPs")
        row("TCP ports", self.ports_var, "comma-separated")
        row("Timeout seconds", self.timeout_var, "0.1–5.0")

        actions = ttk.Frame(shell)
        actions.pack(fill="x", pady=(12, 8))
        self.run_button = ttk.Button(actions, text="Run assessment", command=self._start_assessment)
        self.run_button.pack(side="left")
        self.save_button = ttk.Button(actions, text="Export JSON report", command=self._save_report, state="disabled")
        self.save_button.pack(side="left", padx=8)
        ttk.Button(actions, text="Clear results", command=self._clear_results).pack(side="left")

        self.status_var = tk.StringVar(value="Ready — no network activity has been started.")
        ttk.Label(shell, textvariable=self.status_var).pack(anchor="w", pady=(0, 8))

        results_frame = ttk.Frame(shell)
        results_frame.pack(fill="both", expand=True)
        self.results = tk.Text(results_frame, wrap="none", height=22, font=("Consolas", 10), state="disabled")
        yscroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.results.yview)
        xscroll = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results.xview)
        self.results.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.results.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        root.protocol("WM_DELETE_WINDOW", self._close)
        root.after(100, self._poll_events)

    def _set_results(self, rendered: str) -> None:
        self.results.configure(state="normal")
        self.results.delete("1.0", "end")
        self.results.insert("1.0", rendered)
        self.results.configure(state="disabled")

    def _start_assessment(self) -> None:
        if self.running:
            return
        try:
            scope = parse_scope(self.scope_var.get().strip())
            targets = parse_target_input(self.targets_var.get(), scope)
            ports = parse_ports_input(self.ports_var.get())
            timeout = validate_timeout(float(self.timeout_var.get().strip()))
        except (ValueError, TypeError) as exc:
            from tkinter import messagebox
            messagebox.showerror("Invalid assessment request", str(exc), parent=self.root)
            self.status_var.set("Assessment not started; correct the invalid inputs.")
            return

        self.running = True
        self.run_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.status_var.set(
            f"Running real TCP checks for {len(targets)} explicit target(s) across {len(ports)} port(s)…"
        )

        def worker() -> None:
            try:
                observations = assess_targets(targets, scope, ports, timeout)
                self.events.put(("complete", build_report(scope, observations)))
            except Exception as exc:
                self.events.put(("error", f"{type(exc).__name__}: {exc}"))

        threading.Thread(target=worker, name="omnisec-assessment", daemon=True).start()

    def _poll_events(self) -> None:
        try:
            kind, payload = self.events.get_nowait()
        except queue.Empty:
            if self.root.winfo_exists():
                self.root.after(100, self._poll_events)
            return

        self.running = False
        self.run_button.configure(state="normal")
        if kind == "complete":
            self.last_report = payload
            self._set_results(json.dumps(payload, indent=2))
            self.save_button.configure(state="normal")
            self.status_var.set(
                f"Assessment complete: {payload['observation_count']} real observation(s). "
                "No vulnerability is inferred from TCP reachability alone."
            )
        else:
            self.status_var.set("Assessment failed; see the error below.")
            self._set_results(str(payload))
        if self.root.winfo_exists():
            self.root.after(100, self._poll_events)

    def _save_report(self) -> None:
        if self.last_report is None:
            self.status_var.set("Nothing to export; run an assessment first.")
            return
        from tkinter import filedialog, messagebox
        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save assessment report",
            defaultextension=".json",
            filetypes=[("JSON report", "*.json")],
            initialfile="omnisec-assessment.json",
        )
        if not filename:
            return
        try:
            Path(filename).write_text(json.dumps(self.last_report, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc), parent=self.root)
            self.status_var.set("Report export failed.")
            return
        self.status_var.set(f"Report saved to {filename}")

    def _clear_results(self) -> None:
        if self.running:
            self.status_var.set("Cannot clear results while an assessment is running.")
            return
        self.last_report = None
        self._set_results("")
        self.save_button.configure(state="disabled")
        self.status_var.set("Results cleared. No network activity has been started.")

    def _close(self) -> None:
        if self.running:
            from tkinter import messagebox
            if not messagebox.askyesno(
                "Assessment running",
                "Close the window while the current bounded assessment is running?",
                parent=self.root,
            ):
                return
        self.root.destroy()


def main() -> int:
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter is unavailable in this Python installation; use 'python main.py --help'.")
        return 2
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print(f"Unable to open desktop UI: {exc}. Use 'python main.py --help' instead.")
        return 2
    DefensiveAssessmentApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
