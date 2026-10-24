"""Required selected-profile gate; fixed local checkers only."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from verify_bundle import verify


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--task", required=True)
    parser.add_argument("--profile", required=True, choices=("base", "research"))
    parser.add_argument("--organisation", type=Path)
    args = parser.parse_args(argv)
    if args.profile == "research" and args.organisation is None:
        parser.error("research requires the actual --organisation record")
    skill = Path(__file__).resolve().parents[1]
    try:
        verify(skill)
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("Project root is not a directory")
        harness = skill / "references/harness"
        if args.organisation is not None:
            record = args.organisation if args.organisation.is_absolute() else root / args.organisation
            result = subprocess.run([sys.executable, "-B", str(harness / "tools/orchestration.py"),
                                     "check", "--record", str(record)], cwd=root, check=False)
            if result.returncode:
                return result.returncode
        return subprocess.run([sys.executable, "-B", str(harness / "runtime/principles-2.0.0/workflow.py"),
                               "check", "--root", str(root), "--task", args.task], cwd=root, check=False).returncode
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps({"status": "fail", "reason": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
