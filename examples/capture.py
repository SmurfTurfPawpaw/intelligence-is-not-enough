"""Capture the fixed synthetic ledger experiment, without creating a receipt."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def source_hash(path):
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def partial_text(value):
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    fixture = root / "examples/ledger.py"
    destination = root / "example-private/ledger-run.json"
    if not fixture.is_file() or destination.exists():
        print("Fixture missing or capture already exists; preserve prior evidence.", file=sys.stderr)
        return 2
    before = source_hash(fixture)
    started = datetime.now(timezone.utc).isoformat()
    command = [sys.executable, "-B", str(fixture)]
    returncode, stdout, stderr, error = None, "", "", None
    process_status = "source-unreadable"
    if before is not None:
        try:
            run = subprocess.run(command, cwd=root, capture_output=True,
                                 text=True, encoding="utf-8", timeout=10, check=False)
            process_status, returncode, stdout, stderr = "completed", run.returncode, run.stdout, run.stderr
        except subprocess.TimeoutExpired as failure:
            process_status = "timed-out"
            stdout, stderr = partial_text(failure.stdout), partial_text(failure.stderr)
            error = "Fixed10-second process limit reached; partial output retained; no retry."
        except OSError as failure:
            process_status, error = "launch-failed", str(failure)
    observed = datetime.now(timezone.utc).isoformat()
    after = source_hash(fixture)
    try:
        result = json.loads(stdout)
    except ValueError:
        result = None
    passed = process_status == "completed" and returncode == 0 and before is not None and before == after and result == {
        "first": "accepted", "repeat": "refused", "control": "accepted"}
    unknown = process_status != "completed" or before is None or after is None or before != after
    status = "pass" if passed else ("unknown" if unknown else "fail")
    record = {"status": status, "process_status": process_status, "error": error, "started_at": started,
              "observed_at": observed, "fixture_sha256_before": before, "fixture_sha256_after": after,
              "python": sys.version, "command": command,
              "returncode": returncode, "stdout": stdout, "stderr": stderr,
              "limits": "Fixed synthetic example only; locally recorded execution, not authenticated attestation or live security evidence."}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as output:
        output.write(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"status": record["status"], "evidence": "example-private/ledger-run.json",
                      "observed_at": observed}))
    return 0 if passed else (2 if unknown else 1)


if __name__ == "__main__":
    raise SystemExit(main())
