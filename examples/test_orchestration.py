"""Focused checks of declared organization consistency, not real execution."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("organization", ROOT / "tools/orchestration.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OrganizationTests(unittest.TestCase):
    def setUp(self):
        self.compact = json.loads((ROOT / "examples/organisation-compact.json").read_text(encoding="utf-8"))
        self.parallel = json.loads((ROOT / "examples/organisation-parallel.json").read_text(encoding="utf-8"))

    def status(self, value):
        return module.check(value)["status"]

    def test_compact_single_actor_and_disclosed_self_review(self):
        self.assertEqual(self.status(self.compact), "pass")
        self.assertEqual(len({team["owner"] for team in self.compact["teams"]}), 1)

    def test_parallel_interruption_does_not_fake_completion(self):
        self.assertEqual(self.status(self.parallel), "pass")
        self.assertEqual(self.parallel["work"][1]["stage"], "interrupted")
        self.assertIsNone(self.parallel["work"][1]["handoff"])

    def test_missing_team(self):
        self.compact["teams"].pop()
        self.assertEqual(self.status(self.compact), "fail")

    def test_duplicate_team(self):
        self.compact["teams"][-1] = copy.deepcopy(self.compact["teams"][0])
        self.assertEqual(self.status(self.compact), "fail")

    def test_unknown_owner_is_unknown(self):
        self.compact["teams"][0]["owner"] = None
        self.assertEqual(self.status(self.compact), "unknown")

    def test_dangling_owner(self):
        self.compact["teams"][0]["owner"] = "missing"
        self.assertEqual(self.status(self.compact), "fail")

    def test_duplicate_task(self):
        self.compact["work"].append(copy.deepcopy(self.compact["work"][0]))
        self.assertEqual(self.status(self.compact), "fail")

    def test_dangling_dependency(self):
        self.compact["work"][0]["dependencies"] = ["missing"]
        self.assertEqual(self.status(self.compact), "fail")

    def test_dependency_cycle(self):
        self.parallel["work"][0]["dependencies"] = ["CHALLENGE"]
        self.assertEqual(self.status(self.parallel), "fail")

    def test_unfinished_dependency_is_not_ready_to_start(self):
        self.parallel["work"][2]["stage"] = "started"
        self.assertEqual(self.status(self.parallel), "unknown")

    def test_held_prefix_overlap(self):
        extra = copy.deepcopy(self.parallel["work"][1])
        extra.update(id="SECOND", owned_outputs=["example-private/experiment/output.json"])
        self.parallel["work"].append(extra)
        self.assertEqual(self.status(self.parallel), "fail")

    def test_serialized_released_output_does_not_conflict(self):
        extra = copy.deepcopy(self.parallel["work"][1])
        extra.update(id="SECOND", output_claim="released", owned_outputs=["example-private/experiment/output.json"])
        self.parallel["work"].append(extra)
        self.assertEqual(self.status(self.parallel), "pass")

    def test_unknown_output_claim_is_nonpassing(self):
        self.parallel["work"][1]["output_claim"] = "unknown"
        self.assertEqual(self.status(self.parallel), "unknown")

    def test_started_writer_cannot_release_its_output_claim(self):
        self.parallel["work"][1].update(stage="started", output_claim="released")
        self.assertEqual(self.status(self.parallel), "fail")

    def test_boolean_handoff_revision_is_not_integer_one(self):
        self.compact["work"][0]["handoff"]["packet_revision"] = True
        self.assertEqual(self.status(self.compact), "fail")

    def test_portable_path_aliases_and_controls_are_rejected(self):
        for path in ("example-private/file.txt.", "example-private/file.txt ", "example-private/line\nbreak",
                     "example-private/nul\0name", "example-private/CON.txt", "example-private/file?.txt"):
            with self.subTest(path=path):
                self.compact["work"][0]["owned_outputs"] = [path]
                self.assertEqual(self.status(self.compact), "fail")

    def test_self_review_cannot_be_required_independent_review(self):
        self.compact["work"][0]["independence_required"] = True
        self.assertEqual(self.status(self.compact), "fail")

    def test_alias_with_same_identity_reference_is_not_independent(self):
        self.parallel["actors"][2]["identity_reference"] = self.parallel["actors"][1]["identity_reference"]
        self.assertEqual(self.status(self.parallel), "fail")

    def test_contributor_is_not_an_independent_reviewer(self):
        self.parallel["work"][0]["contributors"].append("reviewer")
        self.assertEqual(self.status(self.parallel), "fail")

    def test_stale_handoff(self):
        self.compact["work"][0]["packet_revision"] = 2
        self.assertEqual(self.status(self.compact), "unknown")

    def test_stale_review(self):
        self.compact["work"][0]["review"]["submission_revision"] = "old"
        self.assertEqual(self.status(self.compact), "unknown")

    def test_failed_review_is_not_old_green(self):
        self.compact["work"][0]["review"]["verdict"] = "fail"
        self.assertEqual(self.status(self.compact), "fail")

    def test_missing_review_evidence(self):
        self.compact["work"][0]["review"]["evidence_reference"] = ""
        self.assertEqual(self.status(self.compact), "unknown")

    def test_unsafe_output_shape(self):
        self.compact["work"][0]["owned_outputs"] = ["../outside"]
        self.assertEqual(self.status(self.compact), "fail")

    def test_resume_declaration_preserves_identity_and_old_evidence(self):
        job = self.parallel["work"][1]
        job.update(stage="started", next_action="Resume unfinished synthetic work after actual boundary reconciliation; no duplicate operation assumed")
        self.assertEqual(self.status(self.parallel), "pass")
        self.assertEqual(job["packet_revision"], 2)
        self.assertEqual(self.parallel["work"][0]["handoff"]["submission_revision"], "map-v1")

    def test_cli_duplicate_json_keys_fail_and_output_is_exclusive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root / "record.json"
            output = root / "output.json"
            record.write_text('{"project":"a","project":"b"}', encoding="utf-8")
            command = [sys.executable, "-B", str(ROOT / "tools/orchestration.py"), "check", "--record", str(record), "--output", str(output)]
            bad = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(bad.returncode, 1)
            initial = output.read_bytes()
            again = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(again.returncode, 1)
            self.assertEqual(output.read_bytes(), initial)


if __name__ == "__main__":
    unittest.main()
