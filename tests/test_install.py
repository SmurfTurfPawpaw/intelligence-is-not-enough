"""Isolated user-profile setup/recovery; never touches the operator's real home."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills/intelligence-is-not-enough"
spec = importlib.util.spec_from_file_location("full_setup", SKILL / "scripts/install.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class UserSetup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="automatic profile test ")
        self.root = Path(self.temp.name)
        self.home = self.root / ".codex"
        self.skills = self.root / ".agents/skills"
        self.user = patch.object(Path, "home", return_value=self.root)
        self.user.start()

    def tearDown(self):
        self.user.stop()
        self.temp.cleanup()

    def install(self, **kw):
        return setup.setup(SKILL, self.home, self.skills, **kw)

    def save(self, name, data):
        path = self.home / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob("*") if p.is_file()}

    def test_fresh_has_complete_standing_rules_and_verified_resources(self):
        result = self.install()
        self.assertEqual(result["action"], "installed")
        guide = (self.home / "AGENTS.md").read_bytes()
        base = (SKILL / "references/harness/base/PRINCIPLES-2.0.1.md").read_bytes().rstrip()
        self.assertIn(base, guide)
        for i in range(1, 13):
            self.assertIn(("## G%02d." % i).encode(), guide)
        self.assertEqual(setup.check(SKILL, self.home, self.skills)["status"], "pass")

    def test_exact_repetition_has_no_backup_timestamp_or_content_churn(self):
        self.install()
        before = self.snapshot()
        self.assertEqual(self.install()["action"], "unchanged")
        self.assertEqual(before, self.snapshot())

    def test_existing_unrelated_guidance_and_skill_survive(self):
        original = b"# Local preferences\r\nPreserve these exact bytes.\r\n"
        self.save("AGENTS.md", original)
        other = self.skills / "other-skill/SKILL.md"
        other.parent.mkdir(parents=True)
        other.write_bytes(b"Unrelated skill")
        self.install()
        self.assertTrue((self.home / "AGENTS.md").read_bytes().startswith(original))
        self.assertEqual(other.read_bytes(), b"Unrelated skill")

    def test_reviewed_reuse_is_bound_to_current_bytes(self):
        original = b"# Existing reviewed G01-G12 and adoption rules"
        self.save("AGENTS.md", original)
        with self.assertRaises(ValueError):
            self.install(reuse="0" * 64)
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), original)
        self.install(reuse=setup.sha(original))
        guide = (self.home / "AGENTS.md").read_bytes()
        self.assertEqual(guide.count(b"# Existing reviewed"), 1)
        self.assertNotIn(b"## G01.", guide)  # Explicit operator judgment, not machine certification.
        before = self.snapshot()
        self.assertEqual(self.install()["action"], "unchanged")
        self.assertEqual(before, self.snapshot())

    def test_reuse_judgment_invalidates_on_unrelated_guidance_edit(self):
        self.save("AGENTS.md", b"Reviewed rules")
        self.install(reuse=setup.sha(b"Reviewed rules"))
        with (self.home / "AGENTS.md").open("ab") as f:
            f.write(b"Later changed rule")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_override_and_budget_refuse_before_mutation(self):
        self.save("AGENTS.override.md", b"Owner override")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, self.snapshot())
        (self.home / "AGENTS.override.md").unlink()
        self.save("config.toml", b"project_doc_max_bytes = 20\n")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_immutable_runtime_conflict_refuses_and_local_manual_is_preserved(self):
        self.save("principles-harness/2.0.0/workflow.py", b"Different runtime")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, self.snapshot())
        shutil.rmtree(self.home / "principles-harness")
        self.save("principles-harness/2.0.0/README.md", b"Existing operator manual")
        self.install()
        self.assertEqual((self.home / "principles-harness/2.0.0/README.md").read_bytes(), b"Existing operator manual")

    def test_different_skill_requires_explicit_upgrade_and_retains_backup(self):
        self.install()
        installed = self.skills / setup.NAME
        manifest = json.loads((installed / "bundle-manifest.json").read_bytes())
        manifest["version"] = "2.2.0-synthetic-prior"
        (installed / "bundle-manifest.json").write_text(json.dumps(manifest))
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, self.snapshot())
        result = self.install(upgrade=True)
        receipt = json.loads(Path(result["receipt"]).read_bytes())
        old = next(r for r in receipt["operations"] if r["role"] == "skill" and r["relative"] == "bundle-manifest.json")
        self.assertTrue((Path(result["receipt"]).parent / (old["id"] + "-old")).is_file())

    def test_partial_write_is_reconciled_without_duplicate_effect(self):
        real = setup.atomic
        for failure_role in ("runtime", "skill", "guidance", "after-guidance"):
            with self.subTest(failure_role=failure_role):
                shutil.rmtree(self.root)
                self.root.mkdir()
                failed = False
                def interrupted(path, data):
                    nonlocal failed
                    is_target = (failure_role == "runtime" and path.name == "workflow.py"
                                 or failure_role == "skill" and path == self.skills / setup.NAME / "SKILL.md"
                                 or failure_role == "guidance" and path == self.home / "AGENTS.md"
                                 or failure_role == "after-guidance" and path.name == "active.json")
                    if is_target and not failed:
                        failed = True
                        raise OSError("Synthetic interruption")
                    return real(path, data)
                with patch.object(setup, "atomic", side_effect=interrupted):
                    with self.assertRaises(OSError):
                        self.install()
                self.assertTrue(failed)
                self.assertEqual(setup.check(SKILL, self.home, self.skills)["status"], "unknown")
                self.assertEqual(self.install()["action"], "reconciled")
                self.assertEqual(setup.check(SKILL, self.home, self.skills)["status"], "pass")

    def test_rollback_restores_only_unchanged_owned_files_and_retains_pins(self):
        self.save("AGENTS.md", b"Prior preferences")
        result = self.install()
        folder = Path(result["receipt"]).parent
        setup.apply_pending(folder, self.home, self.skills, rollback=True)
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), b"Prior preferences")
        self.assertTrue((self.home / "principles-harness/2.0.0/workflow.py").is_file())
        self.assertFalse((self.skills / setup.NAME / "SKILL.md").exists())

    def test_later_edit_blocks_rollback_before_any_restoration(self):
        result = self.install()
        (self.home / "AGENTS.md").write_bytes(b"Later owner work")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            setup.apply_pending(Path(result["receipt"]).parent, self.home, self.skills, rollback=True)
        self.assertEqual(before, self.snapshot())

    def test_linked_destination_refused_without_outside_writes(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "sentinel").write_bytes(b"Keep")
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(self.home), str(outside)], check=True, capture_output=True)
        else:
            self.home.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual({p.name for p in outside.iterdir()}, {"sentinel"})

    def test_legacy_discovery_location_within_profile_is_supported(self):
        self.skills = self.home / "skills"
        self.install()
        self.assertEqual(setup.check(SKILL, self.home, self.skills)["status"], "pass")

    def test_setup_in_fresh_process_with_custom_user_home(self):
        env = dict(os.environ, USERPROFILE=str(self.root), HOME=str(self.root), CODEX_HOME=str(self.home))
        result = subprocess.run([sys.executable, "-B", str(REPO / "install.py"), "--scope", "user"],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["action"], "installed")
        result = subprocess.run([sys.executable, "-B", str(REPO / "install.py"), "check", "--scope", "user"],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reinstall_after_rollback_accepts_only_empty_remaining_destination(self):
        first = self.install()
        setup.apply_pending(Path(first["receipt"]).parent, self.home, self.skills, rollback=True)
        self.assertEqual(self.install()["status"], "pass")

    def test_unexpected_runtime_module_is_refused_without_execution(self):
        self.save("principles-harness/2.0.0/json.py", b"raise RuntimeError('shadow module')")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_linked_lock_does_not_touch_outside_file(self):
        outside = self.root / "outside-lock"
        outside.write_bytes(b"")
        lock = self.home / "principles-harness/installations/setup.lock"
        lock.parent.mkdir(parents=True)
        lock.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(outside.read_bytes(), b"")

    def test_final_readback_catches_late_reused_runtime_change(self):
        # Retained support must be checked too, even when not in mutation ops.
        files = setup.source_files(SKILL)[1]
        prefix = "references/harness/runtime/principles-2.0.0/"
        for name, data in files.items():
            if name.startswith(prefix):
                self.save("principles-harness/2.0.0/" + name[len(prefix):], data)
        real = setup.atomic
        def changed(path, data):
            real(path, data)
            if path == self.home / "AGENTS.md":
                (self.home / "principles-harness/2.0.0/workflow.py").write_bytes(b"Late owner edit")
        with patch.object(setup, "atomic", side_effect=changed):
            with self.assertRaises(ValueError):
                self.install()
        self.assertEqual(setup.check(SKILL, self.home, self.skills)["status"], "unknown")

    def test_reused_skill_cannot_change_its_own_expected_manifest(self):
        target = self.skills / setup.NAME
        shutil.copytree(SKILL, target)
        real = setup.atomic
        def changed(path, data):
            real(path, data)
            if path == self.home / "AGENTS.md":
                changed_bytes = (target / "SKILL.md").read_bytes() + b"\nSynthetic later change\n"
                (target / "SKILL.md").write_bytes(changed_bytes)
                manifest = json.loads((target / "bundle-manifest.json").read_bytes())
                row = next(r for r in manifest["files"] if r["path"] == "SKILL.md")
                row.update(bytes=len(changed_bytes), sha256=setup.sha(changed_bytes))
                (target / "bundle-manifest.json").write_text(json.dumps(manifest))
        with patch.object(setup, "atomic", side_effect=changed):
            with self.assertRaises(ValueError):
                self.install()
        self.assertEqual(setup.check(SKILL, self.home, self.skills)["status"], "unknown")


if __name__ == "__main__":
    unittest.main()
