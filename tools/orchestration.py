"""Read-only organization record check; declarations, not execution attestation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

TEAMS = {"coordination", "systems", "discovery", "engineering", "validation", "knowledge", "operations", "methods"}
STAGES = {"proposed", "admitted", "assigned", "started", "submitted", "reviewed", "integrated",
          "blocked", "interrupted", "cancelled", "superseded"}
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z")
RESERVED = {"con", "prn", "aux", "nul"} | {"com" + str(i) for i in range(1, 10)} | {"lpt" + str(i) for i in range(1, 10)}


def portable_path(path):
    if not isinstance(path, str) or not path or PurePosixPath(path).is_absolute():
        return False
    for part in path.split("/"):
        if (part in {"", ".", ".."} or part.rstrip(" .") != part or not part.isprintable() or
                any(char in part for char in '<>:"\\|?*') or part.split(".")[0].rstrip(" ").casefold() in RESERVED):
            return False
    return True


def check(record):
    failures, unknowns = [], []

    def fail(message):
        failures.append(message)

    def unknown(message):
        unknowns.append(message)

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def items(value, label, limit):
        if not isinstance(value, list) or len(value) > limit:
            fail(label + ": expected bounded array")
            return []
        if any(not isinstance(row, dict) for row in value):
            fail(label + ": expected objects")
            return []
        return value

    def index(rows, label):
        result = {}
        for row in rows:
            identity = row.get("id")
            if not isinstance(identity, str) or not ID.fullmatch(identity):
                fail(label + ": invalid ID")
            elif identity in result:
                fail(label + ": duplicate ID " + identity)
            else:
                result[identity] = row
        return result

    if not isinstance(record, dict):
        return {"status": "fail", "failures": ["Record must be an object"], "unknowns": []}
    if record.get("schema_version") != "1.0.0" or record.get("profile_version") != "2.0.0":
        fail("Unsupported organization schema/profile version")
    if not text(record.get("project")) or type(record.get("revision")) is not int or record["revision"] < 1:
        fail("Project and positive integer revision required")
    refs = record.get("references")
    if not isinstance(refs, dict) or any(not text(refs.get(key)) for key in ("brief", "authority", "evidence", "events")):
        fail("Existing brief/authority/evidence/events references required")
    capacity = record.get("max_concurrent_workers")
    if type(capacity) is not int or not 1 <= capacity <= 64:
        fail("Explicit worker capacity1–64 required")
        capacity = 0

    actors = index(items(record.get("actors"), "actors", 64), "actors")
    for identity, actor in actors.items():
        if not text(actor.get("identity_reference")):
            unknown("Actor identity reference unresolved: " + identity)
    for key in ("integrator", "state_writer"):
        if record.get(key) not in actors:
            fail("Invalid " + key + " actor reference")
    teams = index(items(record.get("teams"), "teams", 8), "teams")
    if set(teams) != TEAMS:
        fail("All eight exact team identities required")
    for identity, team in teams.items():
        if team.get("owner") is None:
            unknown("Unresolved team owner: " + identity)
        elif team.get("owner") not in actors:
            fail("Dangling team owner: " + identity)
        if team.get("state") not in {"ready", "active", "dormant", "blocked"} or not text(team.get("reason")):
            fail("Team state and reason required: " + identity)

    work = index(items(record.get("work"), "work", 256), "work")
    claims, running = [], set()
    for identity, job in work.items():
        for key in ("requester", "assignee", "integrator"):
            if job.get(key) not in actors:
                fail("Dangling " + key + " for " + identity)
        if job.get("team") not in TEAMS:
            fail("Invalid team for " + identity)
        contributors = job.get("contributors")
        if (not isinstance(contributors, list) or not contributors or len(contributors) > 64 or
                any(not isinstance(actor, str) or actor not in actors for actor in contributors) or
                job.get("assignee") not in contributors):
            fail("Declared contributors must include the assignee: " + identity)
            contributors = []
        stage = job.get("stage")
        if stage not in STAGES:
            fail("Invalid stage for " + identity)
        if type(job.get("packet_revision")) is not int or job["packet_revision"] < 1:
            fail("Positive packet revision required: " + identity)
        for key in ("objective", "authority_reference", "permitted_effects", "acceptance", "budget", "stop_recovery", "next_action"):
            if not text(job.get(key)):
                unknown("Unresolved " + key + " for " + identity)
        inputs = items(job.get("inputs"), "inputs for " + identity, 64)
        if not inputs or any(not text(row.get("reference")) or not text(row.get("revision")) for row in inputs):
            unknown("Exact input references/revisions required: " + identity)
        deps = job.get("dependencies")
        if not isinstance(deps, list) or len(deps) > 256 or any(not isinstance(dep, str) or dep not in work for dep in deps):
            fail("Dangling or invalid dependencies: " + identity)
            deps = []
        if len(set(deps)) != len(deps):
            fail("Duplicate dependencies: " + identity)
        if stage in {"assigned", "started"} and any(work[dep].get("stage") != "integrated" for dep in deps):
            unknown("Assigned work has unfinished dependency: " + identity)
        if stage == "started":
            running.add(job.get("assignee"))
        lease = job.get("output_claim")
        if lease not in {"held", "released", "unknown"}:
            fail("Explicit output claim required: " + identity)
        elif lease == "unknown":
            unknown("Unresolved output ownership: " + identity)
        paths = job.get("owned_outputs")
        if not isinstance(paths, list) or len(paths) > 16:
            fail("Bounded output paths required: " + identity)
            paths = []
        if stage == "started" and paths and lease == "released":
            fail("Started writer cannot declare outputs released: " + identity)
        for path in paths:
            if not portable_path(path):
                fail("Output path must be canonical root-relative: " + identity)
            elif lease in {"held", "unknown"}:
                claims.append((identity, tuple(part.casefold() for part in path.split("/"))))
        if len(paths) != len(set(path for path in paths if isinstance(path, str))):
            fail("Duplicate or invalid output path: " + identity)
        if type(job.get("independence_required")) is not bool:
            fail("Explicit independence requirement required: " + identity)
        handoff = job.get("handoff")
        if stage in {"submitted", "reviewed", "integrated"} and not isinstance(handoff, dict):
            unknown("Submission handoff missing: " + identity)
        if isinstance(handoff, dict):
            if type(handoff.get("packet_revision")) is not int or handoff["packet_revision"] < 1:
                fail("Handoff revision must be a positive integer: " + identity)
            elif handoff.get("packet_revision") != job.get("packet_revision"):
                unknown("Stale handoff packet revision: " + identity)
            for key in ("submission_revision", "observations", "limitations", "effects_recovery"):
                if not text(handoff.get(key)):
                    unknown("Handoff " + key + " unresolved: " + identity)
            artifacts = items(handoff.get("artifacts"), "handoff artifacts for " + identity, 64)
            if not artifacts or any(not text(row.get("reference")) or not text(row.get("revision")) for row in artifacts):
                unknown("Handoff artifact identities unresolved: " + identity)
        review = job.get("review")
        if stage in {"reviewed", "integrated"} and not isinstance(review, dict):
            unknown("Review missing: " + identity)
        if isinstance(review, dict):
            reviewer = review.get("actor")
            if reviewer not in actors:
                fail("Dangling review actor: " + identity)
            if not isinstance(handoff, dict) or review.get("submission_revision") != handoff.get("submission_revision"):
                unknown("Review does not bind current submission: " + identity)
            if review.get("verdict") == "fail":
                fail("Declared failed review: " + identity)
            elif review.get("verdict") != "pass" or not text(review.get("evidence_reference")):
                unknown("Review evidence/verdict unresolved: " + identity)
            if job.get("independence_required") and reviewer in actors:
                if reviewer in contributors or any(actors[reviewer].get("identity_reference") == actors[actor].get("identity_reference") for actor in contributors):
                    fail("Required independent review is declared self-review: " + identity)

    def visit(identity, stack, done):
        if identity in stack:
            fail("Dependency cycle detected")
            return
        if identity in done:
            return
        deps = work[identity].get("dependencies")
        for dep in deps if isinstance(deps, list) else []:
            if isinstance(dep, str) and dep in work:
                visit(dep, stack | {identity}, done)
        done.add(identity)

    done = set()
    for identity in work:
        visit(identity, set(), done)
    for index_a, (task_a, path_a) in enumerate(claims):
        for task_b, path_b in claims[index_a + 1:]:
            length = min(len(path_a), len(path_b))
            if task_a != task_b and path_a[:length] == path_b[:length]:
                fail("Conflicting held outputs: " + task_a + " / " + task_b)
    if len(running) > capacity:
        fail("Declared started workers exceed capacity")
    return {"status": "fail" if failures else ("unknown" if unknowns else "pass"),
            "failures": sorted(set(failures)), "unknowns": sorted(set(unknowns)),
            "teams": len(teams), "tasks": len(work),
            "claim": "Declared organization structure and cross-record consistency only",
            "limits": "No identity authentication, tool dispatch, locks, liveness, permission, artifact-content or semantic verification"}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check"])
    parser.add_argument("--record", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Optional exclusive new evidence file; never overwrite")
    args = parser.parse_args()
    try:
        with args.record.open("rb") as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError("Record exceeds1MiB")
        value = check(json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object))
        value.update(record_sha256=hashlib.sha256(raw).hexdigest(),
                     checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    except (OSError, ValueError, RecursionError, TypeError, KeyError) as error:
        value = {"status": "fail", "failures": ["Unreadable or malformed organization record: " + type(error).__name__], "unknowns": []}
    value["observed_at"] = datetime.now(timezone.utc).isoformat()
    serialized = json.dumps(value, indent=2)
    if args.output is not None:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(serialized + "\n")
        except OSError:
            print(json.dumps({"status": "fail", "failures": ["Evidence output unavailable or already exists; input untouched"], "unknowns": []}))
            return 1
    print(serialized)
    return {"pass": 0, "fail": 1, "unknown": 2}[value["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
