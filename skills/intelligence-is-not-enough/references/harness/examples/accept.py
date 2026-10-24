"""Example-only acceptance: organization, fixed ledger, then explicit task gate.

No task discovery, record mutation, judgment generation, shell or target access.
The caller supplies an extracted root, current organization record and actual demo task ID.
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
    root = args.root.resolve()
    fixture = root / "examples/ledger.py"
    gate = root / "runtime/principles-2.0.0/workflow.py"
    organization_checker = root / "tools/orchestration.py"
    if not fixture.is_file() or not gate.is_file() or not organization_checker.is_file():
        print("Missing example fixture or bundled workflow; no acceptance performed.", file=sys.stderr)
        return 2
    organization = args.organisation if args.organisation.is_absolute() else root / args.organisation
    structure = subprocess.run([sys.executable, "-B", str(organization_checker), "check", "--record", str(organization)], cwd=root, check=False)
    if structure.returncode:
        return structure.returncode
    # Inputs/code must be reviewed first; this wrapper is not a sandbox.
    checked = subprocess.run([sys.executable, "-B", str(fixture)], cwd=root, check=False)
    if checked.returncode:
        return checked.returncode
    return subprocess.run([sys.executable, "-B", str(gate), "check", "--root", str(root),
                           "--task", args.task], cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
