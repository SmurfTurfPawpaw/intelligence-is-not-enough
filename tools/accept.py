"""Maintainer acceptance: distribution drift, actual organization, required gate.

Run focused tests separately and retain actual evidence in the current task.
Creates no receipts or judgments and never dispatches project code.
"""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--task", required=True)
    parser.add_argument("--organisation", required=True, type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, "-B", str(repo / "tools/package_skill.py"), "check"], check=False)
    if result.returncode:
        return result.returncode
    return subprocess.run([sys.executable, "-B", str(repo / "skills/intelligence-is-not-enough/scripts/accept.py"),
                           "--root", str(args.root.resolve()), "--task", args.task, "--profile", "research",
                           "--organisation", str(args.organisation)], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
