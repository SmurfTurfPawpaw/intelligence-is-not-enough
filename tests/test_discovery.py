"""Behavior and recovery tests on synthetic declarations, not real exposure."""
import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/discovery.py"
spec = importlib.util.spec_from_file_location("discovery", TOOL)
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)
NOW = datetime(2030, 1, 1, 12, 30, tzinfo=timezone.utc)


class Discovery(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/discovery.json").read_text())

    def run_report(self):
        return discovery.report(self.data, NOW)

    def paths(self, node, result=None):
        issue = (result or self.run_report())["issues"][0]
        return next(row["paths"] for row in issue["consumers"] if row["id"] == node)

    def states(self, node, result=None):
        return {row["state"] for row in self.paths(node, result)}

    def test_shared_root_aliases_keep_distinct_consumers_and_directions(self):
        result = self.run_report()
        self.assertEqual(len(result["issues"]), 1)
        self.assertEqual(self.states("web-shop"), {"reachable"})
        self.assertEqual(self.paths("fetch-tool")[0]["direction"], "outbound")
        self.assertEqual(self.paths("web-shop")[0]["direction"], "inbound")
        self.assertEqual(self.states("batch-job"), {"present"})
        self.assertEqual(result["status"], "attention")
        self.assertIn("no deployment", result["issues"][0]["consumers"][0]["impact"])

    def test_reposts_share_lineage_without_independent_evidence(self):
        result = self.run_report()
        self.assertEqual(next(s for s in result["sources"] if s["source"] == "social-repost")["lineage"], "maintainer")
        self.data["issues"][0]["evidence"] = ["repost-1"]
        self.assertEqual(self.states("web-shop"), {"unknown"})

    def test_related_root_remains_separate(self):
        other = copy.deepcopy(self.data["issues"][0])
        other.update(id="protocol-demo", aliases=["DEMO-2030-0002"], root_cause="Different synthetic protocol defect")
        self.data["issues"].append(other)
        self.assertEqual(len(self.run_report()["issues"]), 2)

    def test_unassigned_primary_signal_needs_intake_even_without_graph(self):
        self.data.update(issues=[], links=[])
        result = self.run_report()
        self.assertEqual(result["status"], "attention")
        self.assertTrue(any("Triage" in a["next"] for a in result["next_actions"]))

    def test_unassigned_latest_failure_never_becomes_empty_success(self):
        self.data.update(issues=[], links=[])
        self.data["observations"][0]["result"] = "failed"
        result = self.run_report()
        self.assertEqual(result["status"], "attention")
        self.assertTrue(any(a["subject"] == "maintainer" and "failed" in a["reasons"][0] for a in result["next_actions"]))

    def test_conflicting_alias_refused(self):
        other = copy.deepcopy(self.data["issues"][0])
        other["id"] = "distinct-root"
        self.data["issues"].append(other)
        with self.assertRaisesRegex(ValueError, "Alias"):
            self.run_report()

    def test_latest_adverse_never_falls_back(self):
        for adverse in ("failed", "unknown", "withdrawn", "conflict"):
            with self.subTest(adverse=adverse):
                data = copy.deepcopy(self.data)
                latest = copy.deepcopy(data["observations"][0])
                latest.update(id="advisory-2", sequence=2, result=adverse, observed_at="2030-01-01T12:10:00Z")
                data["observations"].append(latest)
                result = discovery.report(data, NOW)
                self.assertEqual(self.states("web-shop", result), {"unknown"})

    def test_newer_available_requires_explicit_requalification(self):
        latest = copy.deepcopy(self.data["observations"][0])
        latest.update(id="advisory-2", sequence=2, observed_at="2030-01-01T12:10:00Z")
        self.data["observations"].append(latest)
        self.assertEqual(self.states("web-shop"), {"unknown"})
        self.data["issues"][0]["evidence"] = ["advisory-2"]
        self.assertEqual(self.states("web-shop"), {"reachable"})

    def test_stale_root_cannot_support_current_paths(self):
        self.data["observations"][0]["fresh_for_seconds"] = 1
        self.assertEqual(self.states("web-shop"), {"unknown"})

    def test_future_time_is_unknown_not_green(self):
        for key in ("observed_at", "published_at", "updated_at"):
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                data["observations"][0][key] = "2030-01-02T12:00:00Z"
                self.assertEqual(self.states("web-shop", discovery.report(data, NOW)), {"unknown"})

    def test_both_endpoint_revisions_invalidate_only_their_consumers(self):
        self.data["components"][2]["revision"] = "rev-2"
        self.assertEqual(self.states("web-shop"), {"unknown"})
        self.assertEqual(self.states("fetch-tool"), {"reachable"})
        self.data["components"][1]["revision"] = "rev-2"
        self.assertEqual(self.states("fetch-tool"), {"unknown"})

    def test_root_revision_drift_blocks_paths(self):
        self.data["components"][0]["revision"] = "rev-2"
        self.assertEqual(self.states("web-shop"), {"unknown"})

    def test_unknown_intermediate_blocks_confirmed_transitive_reachability(self):
        self.data["links"][0]["presence"] = "unknown"
        self.assertEqual(self.states("web-shop"), {"unknown"})

    def test_presence_only_does_not_promote_downstream(self):
        self.data["links"][0]["reachability"] = "unknown"
        self.assertEqual(self.states("fetch-tool"), {"present"})

    def test_excluded_route_does_not_hide_valid_alternate(self):
        blocked = copy.deepcopy(self.data["links"][1])
        blocked.update(id="excluded-other-path", reachability="excluded")
        self.data["links"].append(blocked)
        self.assertEqual(self.states("web-shop"), {"reachable", "excluded"})

    def test_same_consumer_retains_inbound_and_outbound_paths(self):
        other = copy.deepcopy(self.data["links"][1])
        other.update(id="outbound-same-consumer", direction="outbound")
        self.data["links"].append(other)
        self.assertEqual({p["direction"] for p in self.paths("web-shop")}, {"inbound", "outbound"})

    def test_diamond_collapses_repeated_states_and_keeps_consumers(self):
        other = copy.deepcopy(self.data["links"][1])
        other.update(id="diamond", **{"from": "fetch-tool", "to": "web-shop"})
        self.data["links"].append(other)
        result = self.run_report()
        self.assertEqual(len(self.paths("web-shop", result)), 1)
        self.assertFalse(result["incomplete"])

    def test_downstream_unknown_explains_upstream_boundary(self):
        self.data["links"][0]["evidence"] = ["repost-1"]
        self.assertIn("upstream path unresolved", " ".join(self.paths("web-shop")[0]["reasons"]))

    def test_fixed_or_absent_is_not_an_affected_path(self):
        for state in ("fixed", "absent"):
            self.data["links"][1]["presence"] = state
            self.assertEqual(self.states("web-shop"), {"excluded"})

    def test_cycle_terminates_with_bounded_duplicate_free_states(self):
        cycle = copy.deepcopy(self.data["links"][0])
        cycle.update(id="cycle", **{"from": "runtime", "to": "decoder"})
        self.data["links"].append(cycle)
        result = self.run_report()
        self.assertFalse(result["incomplete"])
        self.assertLessEqual(result["steps"], len(self.data["links"]))
        consumers = result["issues"][0]["consumers"]
        self.assertEqual(len(consumers), len({row["id"] for row in consumers}))

    def test_disconnected_frontier_stays_visible(self):
        self.data["links"].pop(0)
        result = self.run_report()
        self.assertEqual(result["issues"][0]["consumers"], [])
        self.assertEqual(len(result["issues"][0]["unvisited_links"]), 3)

    def test_budget_exhaustion_is_incomplete_not_empty_success(self):
        result = discovery.report(self.data, NOW, max_steps=1)
        self.assertTrue(result["incomplete"])
        self.assertEqual(result["status"], "attention")
        self.assertTrue(result["issues"][0]["unvisited_links"])

    def test_reordered_input_replays_identically_without_new_observations(self):
        before = copy.deepcopy(self.data)
        first = self.run_report()
        for rows in self.data.values():
            if isinstance(rows, list):
                rows.reverse()
        self.assertEqual(self.run_report(), first)
        self.assertEqual(len(self.data["observations"]), len(before["observations"]))

    def test_malformed_declarations_refused(self):
        mutators = [lambda d: d["observations"].append(copy.deepcopy(d["observations"][0])),
                    lambda d: d["observations"][0].update(sha256="bad"),
                    lambda d: d["observations"][0].update(fresh_for_seconds=True),
                    lambda d: d["observations"][0].update(observed_at="2030-01-01"),
                    lambda d: d["links"][0].update(evidence=["missing"]),
                    lambda d: d["links"][0].update(to="missing"),
                    lambda d: d["observations"][-1].update(origin="repost-1")]
        for mutate in mutators:
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                discovery.report(data, NOW)

    def test_sequence_tie_or_time_reversal_refused(self):
        latest = copy.deepcopy(self.data["observations"][0])
        latest.update(id="advisory-2")
        self.data["observations"].append(latest)
        with self.assertRaisesRegex(ValueError, "sequence"):
            self.run_report()
        latest.update(sequence=2, observed_at="2030-01-01T11:59:00Z")
        with self.assertRaisesRegex(ValueError, "reverses"):
            self.run_report()

    def cli(self, folder, *args):
        return subprocess.run([sys.executable, "-B", str(TOOL), "report", "--record", str(folder / "record.json"),
                               "--as-of", NOW.isoformat(), *map(str, args)], cwd=folder,
                              capture_output=True, text=True, check=False)

    def test_actual_cli_works_in_fresh_workspace_and_preserves_input(self):
        with tempfile.TemporaryDirectory(prefix="offline discovery ") as tmp:
            folder = Path(tmp)
            path = folder / "record.json"
            path.write_text(json.dumps(self.data))
            before = path.read_bytes()
            result = self.cli(folder, "--output", folder / "report.json")
            self.assertEqual(result.returncode, 2, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(json.loads((folder / "report.json").read_text()), output)
            self.assertEqual(output["input_sha256"], discovery.hashlib.sha256(before).hexdigest())
            self.assertEqual(len(output["checker_sha256"]), 64)

    def test_complete_declarations_exit_zero_without_impact_claim(self):
        self.data["links"].pop()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "record.json").write_text(json.dumps(self.data))
            result = self.cli(folder)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("unassessed", result.stdout)

    def test_existing_output_and_malformed_input_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            path, output = folder / "record.json", folder / "report.json"
            path.write_text(json.dumps(self.data))
            output.write_bytes(b"prior usable report")
            self.assertEqual(self.cli(folder, "--output", output).returncode, 1)
            self.assertEqual(output.read_bytes(), b"prior usable report")
            path.write_text('{"schema_version":"1.0.0","schema_version":"broken"}')
            self.assertEqual(self.cli(folder).returncode, 1)
            path.write_text('x' * (discovery.LIMIT_BYTES + 1))
            self.assertEqual(self.cli(folder).returncode, 1)


if __name__ == "__main__":
    unittest.main()
