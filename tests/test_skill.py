"""Synthetic integration fixtures, not review or receipts for a real project."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills/intelligence-is-not-enough"
spec = importlib.util.spec_from_file_location("skill_package", REPO / "tools/package_skill.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class SkillFlow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="standalone harness test ")
        self.area = Path(self.tmp.name)
        self.skill = self.area / "installed skill"
        shutil.copytree(SKILL, self.skill, ignore=shutil.ignore_patterns("__pycache__"))
        self.root = self.area / "project with spaces"
        self.root.mkdir()
        self.runtime = self.skill / "references/harness/runtime/principles-2.0.0"
        (self.root / "plan.md").write_text("Fixture: count distinct events, local only; run behavior checks; discard temporary copies for recovery.")
        (self.root / "app.py").write_text("assert len(set(['a', 'a', 'b'])) == 2\nprint('distinct/repeat checks passed')\n")
        self.run_python(self.runtime / "workflow.py", "begin", "--root", self.root,
                        "--task", "FIXTURE-001", "--plan", "plan.md", expected=0)

    def tearDown(self):
        self.tmp.cleanup()

    def run_python(self, script, *args, expected):
        # No parent-repository cwd, PYTHONPATH injection or network dependency.
        result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                                cwd=self.root, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def gate(self, expected, *extra):
        return self.run_python(self.skill / "scripts/accept.py", "--root", self.root,
                               "--task", "FIXTURE-001", "--profile", "base", *extra, expected=expected)

    def declare_fixture(self):
        # Deliberate fixture declarations test the gate; never used on user work.
        folder = self.root / ".principles/tasks/FIXTURE-001"
        task_path = folder / "task.json"
        task = json.loads(task_path.read_text())
        task.update(state="ready", outcome="Synthetic distinct-event behavior", beneficiary="Test runner",
                    scope="Disposable local fixture only", authority_reference="Synthetic test",
                    recovery="Discard temporary fixture; keep no external state")
        task["subjects"].append({"path": "app.py", "kind": "file"})
        task["checks"] = [{"id": "BEHAVIOR", "criterion": "Synthetic repeated/distinct event assertions pass", "max_age_seconds": None}]
        task_path.write_text(json.dumps(task))
        review_path = folder / "review.json"
        review = json.loads(review_path.read_text())
        review.update(reviewer="Synthetic fixture author; self-review", summary="Controlled gate fixture only, not semantic validation of real work", scope_checks=["BEHAVIOR"])
        for row in review["principles"]:
            row.update(status="supported", reason="Synthetic declaration for gate integration; no real project claim", checks=["BEHAVIOR"])
        review_path.write_text(json.dumps(review))
        output = self.run_python(self.root / "app.py", expected=0)
        (self.root / "actual.log").write_text(output.stdout)
        self.receipt("pass")

    def receipt(self, result):
        self.run_python(self.runtime / "principles.py", "receipt", "--root", self.root,
                        "--task", "FIXTURE-001", "--check", "BEHAVIOR", "--result", result,
                        "--evidence", "actual.log", "--method", "Actual synthetic assertion run; controlled fixture declaration", expected=0)

    def test_standalone_fresh_unresolved_is_not_accepted(self):
        self.gate(2)

    def test_standalone_actual_fixture_accepted(self):
        self.declare_fixture()
        result = self.gate(0)
        self.assertEqual(json.loads(result.stdout)["semantic_adequacy"], "unassessed by the deterministic checker")

    def test_changed_selected_source_invalidates(self):
        self.declare_fixture()
        (self.root / "app.py").write_text("raise AssertionError('changed')\n")
        self.gate(2)

    def test_newer_fail_never_falls_back(self):
        self.declare_fixture()
        self.receipt("fail")
        self.gate(1)

    def test_newer_unknown_never_falls_back(self):
        self.declare_fixture()
        self.receipt("unknown")
        self.gate(2)

    def test_research_requires_explicit_actual_organization(self):
        self.run_python(self.skill / "scripts/accept.py", "--root", self.root, "--task", "FIXTURE-001",
                        "--profile", "research", expected=2)

    def test_organization_failure_propagates(self):
        self.declare_fixture()
        (self.root / "roster.json").write_text("{}")
        self.gate(1, "--organisation", "roster.json")

    def test_valid_synthetic_organization_and_gate(self):
        self.declare_fixture()
        shutil.copyfile(self.skill / "references/harness/examples/organisation-compact.json", self.root / "roster.json")
        self.run_python(self.skill / "scripts/accept.py", "--root", self.root, "--task", "FIXTURE-001",
                        "--profile", "research", "--organisation", "roster.json", expected=0)

    def test_existing_records_rules_and_unrelated_edits_unchanged(self):
        self.declare_fixture()
        for name, content in {"AGENTS.md": "Retain my local rules", "unrelated.txt": "owner's unfinished work", "prior-evidence.log": "historical evidence"}.items():
            (self.root / name).write_text(content)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.gate(0)
        self.gate(0)  # Reuse is read-only; no duplicate task or receipt.
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_duplicate_begin_refused_without_rewriting_history(self):
        folder = self.root / ".principles/tasks/FIXTURE-001"
        before = {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}
        self.run_python(self.runtime / "workflow.py", "begin", "--root", self.root,
                        "--task", "FIXTURE-001", "--plan", "plan.md", expected=1)
        self.assertEqual(before, {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()})

    def test_bundle_drift_blocks_before_project_gate(self):
        self.declare_fixture()
        (self.skill / "references/harness/runtime/principles-2.0.0/workflow.py").write_text("raise SystemExit(0)")
        self.gate(1)

    def test_missing_and_extra_distribution_members_refused(self):
        member = self.skill / "references/harness/TOOLS.md"
        data = member.read_bytes()
        member.unlink()
        self.run_python(self.skill / "scripts/verify_bundle.py", expected=1)
        member.write_bytes(data)
        (self.skill / "unexpected-private-note.txt").write_text("Synthetic unexpected member")
        self.run_python(self.skill / "scripts/verify_bundle.py", expected=1)

    def test_acceptance_command_propagates_gate_failure(self):
        # An existing project's checks are retained, followed by the required gate.
        entry = self.root / "verify.py"
        entry.write_text("import subprocess,sys\nfrom pathlib import Path\nsubprocess.run([sys.executable,'app.py'],check=True)\nraise SystemExit(subprocess.run([sys.executable,'-B'," + repr(str(self.skill / "scripts/accept.py")) + ",'--root','.', '--task','FIXTURE-001','--profile','base']).returncode)\n")
        self.run_python(entry, expected=2)
        self.declare_fixture()
        self.run_python(entry, expected=0)


class Packaging(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="bundle build test ")
        self.root = Path(self.tmp.name)
        for name in ("tools", "skills"):
            shutil.copytree(REPO / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(REPO / "PROFILE.json", self.root / "PROFILE.json")
        for name in json.loads((REPO / "tools/skill-sources.json").read_text()):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, target)

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_is_repeatable(self):
        first = packager.package(self.root, True)
        manifest = (self.root / "skills/intelligence-is-not-enough/bundle-manifest.json").read_bytes()
        self.assertEqual(first, packager.package(self.root, True))
        self.assertEqual(manifest, (self.root / "skills/intelligence-is-not-enough/bundle-manifest.json").read_bytes())
        self.assertEqual(first, packager.package(self.root))

    def test_source_drift_refused_until_explicit_rebuild(self):
        (self.root / "TOOLS.md").write_text("Synthetic changed source")
        with self.assertRaises(ValueError):
            packager.package(self.root)
        packager.package(self.root, True)
        packager.package(self.root)

    def test_missing_resource_refused(self):
        (self.root / "skills/intelligence-is-not-enough/references/harness/TOOLS.md").unlink()
        with self.assertRaises(ValueError):
            packager.package(self.root)

    def test_unexpected_resource_never_silently_deleted(self):
        extra = self.root / "skills/intelligence-is-not-enough/references/harness/private.txt"
        extra.write_text("Synthetic unexpected source")
        for build in (False, True):
            with self.assertRaises(ValueError):
                packager.package(self.root, build)
        self.assertTrue(extra.exists())

    def linked_destination_refused(self, intermediate):
        outside = self.root / "separate destination"
        outside.mkdir()
        sentinel = outside / "TOOLS.md"
        sentinel.write_bytes(b"Original destination; must never change")
        link = self.root / "skills/intelligence-is-not-enough/references"
        if not intermediate:
            link = link / "harness"
        shutil.rmtree(link)
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                           check=True, capture_output=True)
        else:
            link.symlink_to(outside, target_is_directory=True)
        before = {p.relative_to(outside): p.read_bytes() for p in outside.rglob("*") if p.is_file()}
        for build in (False, True):
            with self.assertRaises(ValueError):
                packager.package(self.root, build)
        self.assertEqual(before, {p.relative_to(outside): p.read_bytes() for p in outside.rglob("*") if p.is_file()})

    def test_generated_root_link_refused_before_any_write(self):
        self.linked_destination_refused(False)

    def test_intermediate_parent_link_refused_before_any_write(self):
        self.linked_destination_refused(True)

    def test_distribution_command_propagates_unresolved(self):
        result = subprocess.run([sys.executable, "-B", str(self.root / "tools/accept.py"),
                                 "--root", str(self.root), "--task", "NO-SUCH-TASK",
                                 "--organisation", str(self.root / "examples/organisation-compact.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
