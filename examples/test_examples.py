"""Focused software checks for the synthetic exploration apparatus."""
from itertools import product
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from explore import ACTIONS, apparatus, discrepancy, explore, minimize
from capture import main as capture_main


class ExplorationTests(unittest.TestCase):
    def test_working_baseline_and_distinct_event(self):
        self.assertIsNone(discrepancy(["accept-a", "retry-a", "accept-b", "outsider-a"], "correct"))
        self.assertEqual(apparatus("correct")["final_balance"], 8)

    def test_reject_all_is_inconclusive_not_safe(self):
        self.assertEqual(explore("reject-all")["status"], "inconclusive")
        self.assertEqual(explore("reject-all")["cases"], 0)

    def test_injected_defect_is_concretely_replayed(self):
        result = explore("faulty-retry")
        self.assertEqual(result["status"], "counterexample")
        self.assertEqual(result["first_witness"], ["accept-a", "accept-a"])
        self.assertEqual(result["replay"][-1]["balance"], 6)
        self.assertEqual(result["replay"][-1]["expected_balance"], 3)
        self.assertIsNone(discrepancy(result["first_witness"], "correct"))

    def test_complete_declared_space(self):
        explicit = list(sequence for size in range(1, 5) for sequence in product(ACTIONS, repeat=size))
        self.assertEqual(len(explicit), 340)
        result = explore("correct")
        self.assertEqual(result["cases"], len(explicit))
        self.assertEqual(result["status"], "holds-within-bound")

    def test_budget_exhaustion_is_not_pass(self):
        result = explore("correct", max_cases=17)
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["cases"], 17)
        self.assertEqual(result["declared_space"], 340)

    def test_minimization_preserves_failure_and_removes_noise(self):
        witness = minimize(["outsider-a", "accept-b", "accept-a", "retry-a"], "faulty-retry")
        self.assertEqual(witness, ["accept-a", "retry-a"])
        self.assertIsNotNone(discrepancy(witness, "faulty-retry"))


class CaptureFailureTests(unittest.TestCase):
    def capture_failure(self, failure):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "examples/ledger.py"
            fixture.parent.mkdir()
            fixture.write_text("# Disposable known fixture\n", encoding="utf-8")
            with patch("sys.argv", ["capture.py", "--root", directory]), patch("capture.subprocess.run", side_effect=failure) as invoked:
                with contextlib.redirect_stdout(io.StringIO()):
                    status = capture_main()
                record_path = root / "example-private/ledger-run.json"
                original = record_path.read_bytes()
                record = json.loads(original)
                self.assertEqual(status, 2)
                self.assertEqual(record["status"], "unknown")
                self.assertIsNone(record["returncode"])
                self.assertEqual(record["fixture_sha256_before"], record["fixture_sha256_after"])
                self.assertIsNotNone(record["fixture_sha256_before"])
                self.assertLessEqual(record["started_at"], record["observed_at"])
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(capture_main(), 2)
                self.assertEqual(record_path.read_bytes(), original)
                self.assertEqual(invoked.call_count, 1)
                return record

    def test_timeout_retains_partial_output_and_does_not_retry(self):
        result = self.capture_failure(subprocess.TimeoutExpired(["fixed-fixture"], 10,
                                      output=b"partial observation", stderr=b"partial error"))
        self.assertEqual(result["process_status"], "timed-out")
        self.assertEqual(result["stdout"], "partial observation")
        self.assertEqual(result["stderr"], "partial error")

    def test_launch_failure_is_retained_and_does_not_retry(self):
        result = self.capture_failure(OSError("Synthetic launch refusal"))
        self.assertEqual(result["process_status"], "launch-failed")
        self.assertEqual(result["error"], "Synthetic launch refusal")


if __name__ == "__main__":
    unittest.main()
