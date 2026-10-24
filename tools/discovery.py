"""Offline discovery frontier and declared consumer paths. No network/model calls."""
import argparse
from collections import defaultdict, deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

SCHEMA = "1.0.0"
LIMIT_BYTES = 2 * 1024 * 1024
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")


def text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 4096


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timezone-bearing ISO timestamp required")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("Timezone-bearing ISO timestamp required")
    return result.astimezone(timezone.utc)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def plain(path):
    path = Path(path).absolute()
    if any(p.is_symlink() or p.is_junction() for p in (path, *path.parents)):
        raise ValueError("Linked record/output paths refused")
    return path


def load(path):
    with plain(path).open("rb") as stream:
        data = stream.read(LIMIT_BYTES + 1)
    if len(data) > LIMIT_BYTES:
        raise ValueError("Record exceeds 2 MiB")
    record = json.loads(data, object_pairs_hook=unique_object,
                        parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON number")))
    return record, hashlib.sha256(data).hexdigest()


def index(record, key, limit):
    rows = record.get(key)
    if not isinstance(rows, list) or len(rows) > limit:
        raise ValueError(f"{key}: bounded array required (maximum {limit})")
    result = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not ID.fullmatch(row["id"]):
            raise ValueError(key + ": object with portable ID required")
        if row["id"] in result:
            raise ValueError(key + ": duplicate ID " + row["id"])
        result[row["id"]] = row
    return result


def references(row, observations):
    refs = row.get("evidence")
    if (not isinstance(refs, list) or not refs or len(refs) > 32 or
            any(not isinstance(ref, str) or ref not in observations for ref in refs) or
            len(refs) != len(set(refs))):
        raise ValueError("Nonempty, unique evidence observation IDs required: " + row["id"])
    return refs


def report(record, as_of, max_steps=512):
    """Assess declarations at an explicit time; this does not verify their truth."""
    if not isinstance(record, dict) or record.get("schema_version") != SCHEMA:
        raise ValueError("Unsupported discovery schema")
    if type(max_steps) is not int or not 1 <= max_steps <= 4096:
        raise ValueError("max_steps must be 1–4096")
    observations = index(record, "observations", 512)
    components = index(record, "components", 128)
    issues = index(record, "issues", 64)
    links = index(record, "links", 256)
    sources, latest, aliases = defaultdict(list), {}, {}
    for row in observations.values():
        if (not isinstance(row.get("source"), str) or not ID.fullmatch(row["source"]) or
                type(row.get("sequence")) is not int or row["sequence"] < 1 or
                not text(row.get("revision")) or not text(row.get("url")) or
                row.get("kind") not in {"primary", "repost"} or
                row.get("result") not in {"available", "failed", "unknown", "withdrawn", "conflict"} or
                type(row.get("fresh_for_seconds")) is not int or not 1 <= row["fresh_for_seconds"] <= 2592000):
            raise ValueError("Invalid source observation: " + row["id"])
        timestamp(row.get("observed_at"))
        for key in ("published_at", "updated_at"):
            if row.get(key) is not None:
                timestamp(row[key])
        if row["result"] == "available" and not HASH.fullmatch(str(row.get("sha256", ""))):
            raise ValueError("Available content needs SHA256: " + row["id"])
        if row["kind"] == "primary" and row.get("origin") is not None:
            raise ValueError("Primary observation cannot declare a repost origin")
        if row["kind"] == "repost" and row.get("origin") is not None and row["origin"] not in observations:
            raise ValueError("Dangling repost origin: " + row["id"])
        sources[row["source"]].append(row)
    for source, rows in sources.items():
        rows.sort(key=lambda row: row["sequence"])
        if len({row["sequence"] for row in rows}) != len(rows):
            raise ValueError("Conflicting source sequence: " + source)
        if any(timestamp(a["observed_at"]) > timestamp(b["observed_at"]) for a, b in zip(rows, rows[1:])):
            raise ValueError("Source sequence reverses observation time: " + source)
        latest[source] = rows[-1]

    def lineage(identity):
        seen = set()
        while identity is not None:
            if identity in seen:
                raise ValueError("Repost lineage cycle")
            seen.add(identity)
            row = observations[identity]
            if row["kind"] == "primary":
                return row["source"]
            identity = row.get("origin")
        return None

    for identity in observations:
        lineage(identity)
    for row in components.values():
        if not text(row.get("revision")):
            raise ValueError("Component revision required: " + row["id"])
    for row in issues.values():
        if row.get("root") not in components or not text(row.get("root_revision")) or not text(row.get("root_cause")):
            raise ValueError("Issue root, revision and root cause required: " + row["id"])
        names = row.get("aliases")
        if not isinstance(names, list) or len(names) > 32 or any(not text(name) for name in names):
            raise ValueError("Bounded explicit aliases required")
        for name in [row["id"], *names]:
            key = name.strip().casefold()
            if key in aliases and aliases[key] != row["id"]:
                raise ValueError("Alias assigned to distinct issues: " + name)
            aliases[key] = row["id"]
        references(row, observations)
    outgoing = defaultdict(list)
    for row in links.values():
        if (row.get("issue") not in issues or row.get("from") not in components or row.get("to") not in components or
                not text(row.get("from_revision")) or not text(row.get("to_revision")) or
                not text(row.get("relation")) or not text(row.get("condition")) or
                row.get("presence") not in {"affected", "fixed", "absent", "unknown"} or
                row.get("reachability") not in {"reachable", "excluded", "unknown"} or
                row.get("direction") not in {"inbound", "outbound", "local", "unknown"}):
            raise ValueError("Invalid directed link: " + row["id"])
        references(row, observations)
        outgoing[(row["issue"], row["from"])].append(row)
    for rows in outgoing.values():
        rows.sort(key=lambda row: row["id"])

    def usable(identity):
        row = observations[identity]
        if latest[row["source"]]["id"] != identity:
            return "superseded observation; requalify against latest source"
        if row["result"] != "available":
            return "latest source is " + row["result"]
        when = timestamp(row["observed_at"])
        if when > as_of or any(timestamp(row[key]) > when for key in ("published_at", "updated_at") if row.get(key)):
            return "future observation or source timestamp"
        if (as_of - when).total_seconds() > row["fresh_for_seconds"]:
            return "stale source observation"
        if row["kind"] == "repost":
            return "repost is a lead, not independent technical evidence"
        return None

    def reasons(row):
        return sorted({usable(ref) for ref in row["evidence"] if usable(ref) is not None})

    results, actions, steps, incomplete = [], [], 0, False
    for issue_id, issue in sorted(issues.items()):
        root_reasons = reasons(issue)
        if issue["root_revision"] != components[issue["root"]]["revision"]:
            root_reasons.append("root component revision changed")
        start = "unknown" if root_reasons else "reachable"
        queue = deque([(issue["root"], start, [])])
        visited, consumers, traversed = set(), defaultdict(dict), set()
        while queue:
            node, state, path = queue.popleft()
            if (node, state) in visited:
                continue
            visited.add((node, state))
            for edge in outgoing.get((issue_id, node), []):
                if steps >= max_steps:
                    incomplete = True
                    break
                steps += 1
                traversed.add(edge["id"])
                why = reasons(edge)
                for endpoint in ("from", "to"):
                    if edge[endpoint + "_revision"] != components[edge[endpoint]]["revision"]:
                        why.append(endpoint + " component revision changed")
                if state == "unknown" and not root_reasons:
                    why.append("upstream path unresolved; inspect witness links")
                if why or state == "unknown" or edge["presence"] == "unknown":
                    effective = "unknown"
                elif edge["presence"] in {"fixed", "absent"} or edge["reachability"] == "excluded":
                    effective = "excluded"
                elif state == "present" or edge["reachability"] == "unknown" or edge["direction"] == "unknown":
                    effective = "present"
                else:
                    effective = "reachable"
                witness = {"links": path + [edge["id"]], "state": effective,
                           "reasons": sorted(set(root_reasons + why)), "direction": edge["direction"],
                           "condition": edge["condition"], "evidence": sorted(edge["evidence"])}
                consumers[edge["to"]].setdefault((effective, edge["direction"]), witness)
                if effective != "excluded":
                    queue.append((edge["to"], effective, witness["links"]))
                if effective in {"unknown", "present"}:
                    actions.append({"issue": issue_id, "subject": edge["id"],
                                    "next": "Requalify evidence/revisions" if why else "Establish missing data-flow/configuration evidence",
                                    "reasons": witness["reasons"] or ["end-to-end reachable path not established"]})
            if incomplete:
                break
        disconnected = sorted(row["id"] for row in links.values() if row["issue"] == issue_id and row["id"] not in traversed)
        if root_reasons or not outgoing.get((issue_id, issue["root"])):
            actions.append({"issue": issue_id, "subject": issue["root"], "next": "Requalify root evidence or map first consumers",
                            "reasons": root_reasons or ["no consumer coverage declared"]})
        if disconnected:
            actions.append({"issue": issue_id, "subject": issue["root"], "next": "Resolve unvisited consumer frontier",
                            "reasons": disconnected})
        results.append({"id": issue_id, "aliases": sorted(set(issue["aliases"])), "root": issue["root"],
                        "root_cause": issue["root_cause"],
                        "primary_source_lineages": sorted({observations[ref]["source"] for ref in issue["evidence"] if usable(ref) is None}),
                        "root_reasons": sorted(root_reasons), "unvisited_links": disconnected,
                        "consumers": [{"id": node, "revision": components[node]["revision"],
                                       "paths": [states[key] for key in sorted(states)],
                                       "impact": "unassessed; no deployment or exploit proof from this graph"}
                                      for node, states in sorted(consumers.items())]})
    assigned_sources = {observations[ref]["source"] for row in [*issues.values(), *links.values()] for ref in row["evidence"]}
    for source, row in sorted(latest.items()):
        if row["kind"] != "primary":
            continue
        problem = usable(row["id"])
        if problem or source not in assigned_sources:
            actions.append({"issue": None, "subject": source,
                            "next": "Reconcile latest source observation" if problem else "Triage new primary signal into an issue or record its disposition",
                            "reasons": [problem or "primary signal has no declared issue/link disposition"]})
    source_view = [{"source": source, "latest": row["id"], "sequence": row["sequence"],
                    "revision": row["revision"], "observed_at": row["observed_at"], "kind": row["kind"],
                    "url": row["url"], "sha256": row.get("sha256"),
                    "published_at": row.get("published_at"), "updated_at": row.get("updated_at"),
                    "lineage": lineage(row["id"]), "attention": usable(row["id"])} for source, row in sorted(latest.items())]
    # Deduplicate actions reached by multiple graph paths without losing alternative path states.
    actions = [json.loads(item) for item in sorted({json.dumps(item, sort_keys=True) for item in actions})]
    return {"schema_version": SCHEMA, "status": "attention" if actions or incomplete else "complete",
            "evaluated_at": as_of.isoformat(), "steps": steps, "incomplete": incomplete,
            "sources": source_view, "issues": results, "next_actions": actions,
            "witness_policy": "First deterministic witness per consumer, state and final-edge direction; not an enumeration of every path",
            "limits": "Declared source paths only; no fetching, dispatch, authenticated execution, exploit or live affectedness verification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("report",))
    parser.add_argument("--record", required=True, type=Path)
    parser.add_argument("--as-of", help="Timezone-bearing evaluation time; default actual UTC now")
    parser.add_argument("--max-steps", type=int, default=512)
    parser.add_argument("--output", type=Path, help="Exclusive new file; never overwrites")
    args = parser.parse_args()
    try:
        data, digest = load(args.record)
        result = report(data, timestamp(args.as_of) if args.as_of else datetime.now(timezone.utc), args.max_steps)
        result.update(input_sha256=digest, checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
        if args.output:
            with plain(args.output).open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(encoded)
        print(encoded, end="")
        return 2 if result["status"] == "attention" else 0
    except (OSError, ValueError, KeyError, TypeError, RecursionError, OverflowError) as error:
        print(json.dumps({"status": "fail", "reason": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
