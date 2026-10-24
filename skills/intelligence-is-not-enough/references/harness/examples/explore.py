"""Bounded synthetic sequence experiment; stdlib, no network or model calls."""
import argparse
from datetime import datetime, timezone
import hashlib
from itertools import product
import json
from pathlib import Path

ACTIONS = ("accept-a", "retry-a", "accept-b", "outsider-a")
PROPERTY_ID = "unique-authorized-events/1"


def specification(action):
    # Independent event meaning; the oracle does not call the implementation.
    if action == "outsider-a":
        return False, "a", 3
    return True, ("b" if action == "accept-b" else "a"), (5 if action == "accept-b" else 3)


class Ledger:
    def __init__(self, variant):
        self.variant = variant
        self.seen = set()
        self.balance = 0

    def apply(self, action):
        if self.variant == "reject-all" or action == "outsider-a":
            return "refused"
        # Implementation mapping is separate from the declarative test oracle.
        event = "b" if action == "accept-b" else "a"
        value = 5 if event == "b" else 3
        if self.variant != "faulty-retry" and event in self.seen:
            return "refused"
        self.seen.add(event)
        self.balance += value
        return "accepted"


def discrepancy(sequence, variant):
    ledger = Ledger(variant)
    expected = {}
    trace = []
    for action in sequence:
        authorized, event, value = specification(action)
        fresh = authorized and event not in expected
        if fresh:
            expected[event] = value
        status = ledger.apply(action)
        wanted = "accepted" if fresh else "refused"
        trace.append({"action": action, "status": status, "balance": ledger.balance,
                      "expected_status": wanted, "expected_balance": sum(expected.values())})
        if status != wanted or ledger.balance != sum(expected.values()):
            return trace
    return None


def apparatus(variant):
    ledger = Ledger(variant)
    first = ledger.apply("accept-a")
    outsider = ledger.apply("outsider-a")
    after_outsider = ledger.balance
    distinct = ledger.apply("accept-b")
    valid = first == "accepted" and outsider == "refused" and after_outsider == 3 and distinct == "accepted" and ledger.balance == 8
    return {"status": "usable" if valid else "inconclusive", "first": first,
            "outsider": outsider, "balance_after_outsider": after_outsider,
            "distinct": distinct, "final_balance": ledger.balance}


def minimize(sequence, variant):
    witness = list(sequence)
    for index in range(len(witness) - 1, -1, -1):
        smaller = witness[:index] + witness[index + 1:]
        if discrepancy(smaller, variant):
            witness = smaller
    return witness


def explore(variant, depth=4, max_cases=340):
    control = apparatus(variant)
    if control["status"] != "usable":
        return {"variant": variant, "status": "inconclusive", "apparatus": control, "cases": 0}
    tested = failures = 0
    witness = None
    total = sum(len(ACTIONS) ** length for length in range(1, depth + 1))
    for length in range(1, depth + 1):
        for sequence in product(ACTIONS, repeat=length):
            if tested >= max_cases:
                return {"variant": variant, "status": "incomplete", "apparatus": control,
                        "cases": tested, "declared_space": total, "failures": failures,
                        "first_witness": witness, "reason": "case budget reached"}
            tested += 1
            if discrepancy(sequence, variant):
                failures += 1
                if witness is None:
                    witness = minimize(sequence, variant)
    return {"variant": variant, "status": "counterexample" if witness else "holds-within-bound",
            "apparatus": control, "cases": tested, "declared_space": total, "failures": failures,
            "first_witness": witness, "replay": discrepancy(witness, variant) if witness else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, choices=range(1, 5), default=4)
    parser.add_argument("--max-cases", type=int, choices=range(1, 341), default=340)
    args = parser.parse_args()
    results = [explore(name, args.depth, args.max_cases) for name in ("correct", "faulty-retry", "reject-all")]
    complete = all(item["status"] != "incomplete" for item in results)
    calibrated = (results[0]["status"] == "holds-within-bound" and
                  results[1]["status"] == "counterexample" and results[2]["status"] == "inconclusive")
    status = "pass" if complete and calibrated else ("incomplete" if not complete or args.depth < 2 else "fail")
    print(json.dumps({"status": status, "observed_at": datetime.now(timezone.utc).isoformat(),
                      "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "property_id": PROPERTY_ID, "bounds": vars(args), "actions": ACTIONS,
                      "results": results,
                      "limits": "Known synthetic calibration only; sequential finite model, not concurrency, real payments, AI advantage or vulnerability absence."}, indent=2))
    return 0 if status == "pass" else (2 if status == "incomplete" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
