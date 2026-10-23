"""Optional packager for the safe CLI; dependencies are never auto-installed."""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Package the scope-bound defensive assessment CLI")
    parser.add_argument("--build", action="store_true", help="Build a standalone CLI with an already-installed PyInstaller")
    args = parser.parse_args(argv)
    if not args.build:
        print("No installation or build was started.")
        print("Run the app directly: python main.py --help")
        print("For a standalone executable, install a reviewed PyInstaller version in a virtual environment, then rerun with --build.")
        return 0
    if importlib.util.find_spec("PyInstaller") is None:
        print("PyInstaller is not installed. No automatic installation will be attempted.", file=sys.stderr)
        return 2
    target = ROOT / "main.py"
    if not target.is_file():
        print("main.py was not found.", file=sys.stderr)
        return 2
    return subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--clean", "--onefile", "--name", "omnisec-assessment", str(target)],
        cwd=ROOT,
        check=False,
    ).returncode

if __name__ == "__main__":
    raise SystemExit(main())
