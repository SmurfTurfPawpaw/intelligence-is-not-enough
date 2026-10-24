"""Explicit offline user setup. Native skill copying does not execute this script."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid

if sys.version_info < (3, 12):
    raise SystemExit("Python 3.12+ required; no interpreter is installed automatically")
import tomllib

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_bundle import verify

START = b"<!-- BEGIN intelligence-is-not-enough automatic -->"
END = b"<!-- END intelligence-is-not-enough automatic -->"
NAME = "intelligence-is-not-enough"
SKILL = Path(__file__).absolute().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def plain(path):
    path = Path(path).absolute()
    for part in reversed((path, *path.parents)):
        if part.is_symlink() or part.is_junction():
            raise ValueError("Linked setup path refused: " + str(part))
    return path


def read(path):
    plain(path)
    return path.read_bytes() if path.exists() else None


def identity(path):
    data = read(path)
    return sha(data) if data is not None else None


def atomic(path, data):
    plain(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if data is None:
        path.unlink(missing_ok=True)
        return
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    handle, name = tempfile.mkstemp(prefix=".iin-", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def write_json(path, value):
    atomic(path, (json.dumps(value, indent=2) + "\n").encode())


@contextmanager
def lock(home):
    folder = plain(home / "principles-harness/installations")
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock_path = plain(folder / "setup.lock")
    if lock_path.exists() and lock_path.stat().st_nlink != 1:
        raise ValueError("Shared lock-file inode refused")
    with lock_path.open("a+b") as stream:
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def bounds(home, skills, role, relative):
    roots = {"skill": skills / NAME, "runtime": home / "principles-harness/2.0.0",
             "principles": home / "principles-harness", "guidance": home}
    from pathlib import PurePosixPath
    parts = PurePosixPath(relative).parts
    if (not parts or relative != "/".join(parts) or "\\" in relative or ":" in relative
            or any(p in (".", "..") for p in parts) or relative.startswith("/")):
        raise ValueError("Invalid setup member")
    if role == "guidance" and relative != "AGENTS.md":
        raise ValueError("Unexpected guidance target")
    if role == "principles" and relative != "PRINCIPLES-2.0.1.md":
        raise ValueError("Unexpected principles target")
    return plain(roots[role].joinpath(*parts))


def preflight(home, skills, guidance):
    plain(home)
    plain(skills)
    plain(home / "principles-harness/installations/setup.lock")
    target, support = skills / NAME, home / "principles-harness"
    if (target == home or target in home.parents or target == support
            or target in support.parents or support in target.parents):
        raise ValueError("Profile support and skill destinations overlap")
    # A second same-name user installation would make selection ambiguous.
    known = {Path.home() / ".agents/skills", home / "skills"}
    for other in known - {skills}:
        if (other / NAME).exists():
            raise ValueError("Same-name skill exists at another user location: " + str(other / NAME))
    override = read(home / "AGENTS.override.md")
    if override and override.strip():
        raise ValueError("Nonempty AGENTS.override.md shadows standing setup; preserve it and resolve scope first")
    limit = 32768
    config = read(home / "config.toml")
    if config:
        if len(config) > 1024 * 1024:
            raise ValueError("Configuration exceeds setup inspection limit")
        limit = tomllib.loads(config.decode("utf-8")).get("project_doc_max_bytes", limit)
    if type(limit) is not int or limit <= 0 or len(guidance) > limit:
        raise ValueError("Global guidance exceeds the configured instruction budget; no limit changed")
    return {"global_bytes": len(guidance), "known_limit_bytes": limit,
            "remaining_bytes": limit - len(guidance),
            "limits": "Future project guidance and launch-time overrides remain unassessed"}


def merged(before, body):
    before = before or b""
    if before.count(START) != before.count(END) or before.count(START) > 1:
        raise ValueError("Malformed or repeated owned global block")
    block = START + b"\n" + body + b"\n" + END
    if START in before:
        a, b = before.index(START), before.index(END) + len(END)
        if a >= b:
            raise ValueError("Reversed owned block")
        return before[:a] + block + before[b:], block
    return before + (b"\n\n" if before else b"") + block + b"\n", block


def source_files(source):
    verify(source)
    manifest = json.loads((source / "bundle-manifest.json").read_bytes())
    files = {r["path"]: (source / r["path"]).read_bytes() for r in manifest["files"]}
    files["bundle-manifest.json"] = (source / "bundle-manifest.json").read_bytes()
    if (json.loads(files["bundle-manifest.json"]) != manifest
            or any(sha(files[r["path"]]) != r["sha256"] or len(files[r["path"]]) != r["bytes"] for r in manifest["files"])):
        raise ValueError("Source changed while preparing installation")
    return manifest, files


def runtime_guard(home, files):
    """Check the fixed runtime's source/import surface; archives are not executed."""
    root = home / "principles-harness/2.0.0"
    prefix = "references/harness/runtime/principles-2.0.0/"
    known = {name[len(prefix):] for name in files if name.startswith(prefix)}
    archives = {"reviews", "tests", "reference", "templates"}
    for path in root.rglob("*"):
        plain(path)
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or relative.parts[0] in archives:
            continue
        if relative.as_posix() in known:
            continue
        if path.suffix.lower() in {".md", ".txt", ".json", ".log"} or path.name == "LICENSE":
            continue
        raise ValueError("Unexpected runtime import/dependency member: " + relative.as_posix())


def operations(source, home, skills, upgrade=False, reuse=None):
    manifest, files = source_files(source)
    runtime_guard(home, files)
    agent_file = home / "AGENTS.md"
    before = read(agent_file)
    active_path = home / "principles-harness/installations/active.json"
    active = json.loads(read(active_path) or b"null")
    if START in (before or b""):
        if not active or sha((before or b"").split(START, 1)[1].split(END, 1)[0]) != active["block_body_sha256"]:
            raise ValueError("Owned guidance changed or installation record missing; inspect before replacement")
        if active.get("reuse") and reuse is None:
            outside = (before or b"").split(START, 1)[0] + (before or b"").split(END, 1)[1]
            if sha(outside) != active["outside_sha256"]:
                raise ValueError("Reviewed reused guidance changed; supply a newly reviewed digest")
            reuse = sha(before)
    if reuse is not None and (before is None or sha(before) != reuse):
        raise ValueError("Reviewed guidance digest differs; no reuse or mutation")
    base = files["references/harness/base/PRINCIPLES-2.0.1.md"]
    base_path = home / "principles-harness/PRINCIPLES-2.0.1.md"
    body = (b"# Standing project principles\n\n" if reuse else base.rstrip() + b"\n\n")
    body += ("These principles apply automatically to every coding, research, design and business project in this Codex profile. "
             "No skill invocation or owner reminder is required. On first project work, reuse existing compatible records and checks, "
             "perform proportionate adoption, and wire the required workflow gate into the real acceptance command. "
             "Preserve local instructions and unrelated work; do not repeat unchanged setup or broad checks.\n\n"
             f"Canonical principles: {json.dumps(str(base_path))}. "
             "Read and apply G01-G12 before project work if they are not already present in current guidance. "
             f"Trusted workflow: {json.dumps(str(home / 'principles-harness/2.0.0/workflow.py'))}. "
             f"Deeper optional procedures: {json.dumps(str(skills / NAME / 'SKILL.md'))}. "
             "The research profile and eight responsibility owners apply to exploratory research, not ordinary coding. "
             "Guidance does not intercept arbitrary tools or guarantee compliance.\n").encode()
    after, block = merged(before, body)
    budget = preflight(home, skills, after)
    oldskill = skills / NAME
    if oldskill.exists() and not oldskill.is_dir():
        raise ValueError("Skill destination is not a directory")
    members = list(oldskill.rglob("*")) if oldskill.exists() else []
    for path in members:
        plain(path)
    # Rollback retains empty directories. They contain no data to overwrite.
    if any(path.is_file() for path in members):
        verify(oldskill)
        existing = {r["path"] for r in json.loads((oldskill / "bundle-manifest.json").read_bytes())["files"]} | {"bundle-manifest.json"}
        differs = existing != set(files) or any(read(oldskill / n) != data for n, data in files.items())
        if differs and not upgrade:
            raise ValueError("Different installed skill; deliberate --upgrade required")
    else:
        existing = set()
    targets = []
    prefix = "references/harness/runtime/principles-2.0.0/"
    for name, data in files.items():
        if name.startswith(prefix) and not name.startswith(prefix + "tests/") and name != prefix + "README.md":
            targets.append(("runtime", name[len(prefix):], data))
    # Pin executable/dependency bytes, not a replacement for an existing local manual.
    if read(home / "principles-harness/2.0.0/README.md") is None:
        targets.append(("runtime", "README.md", files["references/runtime-README.md"]))
    targets.append(("principles", "PRINCIPLES-2.0.1.md", base))
    targets += [("skill", n, files.get(n)) for n in sorted(existing | set(files)) if n != "bundle-manifest.json"]
    targets += [("skill", "bundle-manifest.json", files["bundle-manifest.json"]), ("guidance", "AGENTS.md", after)]
    ops = []
    for role, name, data in targets:
        path = bounds(home, skills, role, name)
        old = read(path)
        if role in ("runtime", "principles") and old is not None and old != data:
            raise ValueError("Immutable versioned support differs; no overwrite: " + str(path))
        if old != data:
            ops.append({"role": role, "relative": name, "old": old, "new": data})
    outside = after.split(START, 1)[0] + after.split(END, 1)[1]
    info = {"version": manifest["version"], "source_sha256": sha(files["bundle-manifest.json"]),
            "home": str(home), "skills": str(skills), "reuse": reuse is not None,
            "reuse_is_operator_judgment": reuse is not None, "outside_sha256": sha(outside),
            "block_body_sha256": sha(block.split(START, 1)[1].split(END, 1)[0]), "budget": budget}
    return ops, info


def completed_readback(home, skills, receipt):
    if identity(skills / NAME / "bundle-manifest.json") != receipt["source_sha256"]:
        raise ValueError("Installed bundle differs from the selected source before completion")
    _, files = source_files(skills / NAME)
    runtime_guard(home, files)
    prefix = "references/harness/runtime/principles-2.0.0/"
    for name, data in files.items():
        if name.startswith(prefix) and not name.startswith(prefix + "tests/") and name != prefix + "README.md":
            if read(home / "principles-harness/2.0.0" / name[len(prefix):]) != data:
                raise ValueError("Required reused/runtime bytes changed before completion")
    if read(home / "principles-harness/PRINCIPLES-2.0.1.md") != files["references/harness/base/PRINCIPLES-2.0.1.md"]:
        raise ValueError("Canonical principles changed before completion")
    guidance = read(home / "AGENTS.md") or b""
    if guidance.count(START) != 1 or guidance.count(END) != 1:
        raise ValueError("Global guidance is not complete")
    if sha(guidance.split(START, 1)[1].split(END, 1)[0]) != receipt["block_body_sha256"]:
        raise ValueError("Global guidance changed before completion")
    outside = guidance.split(START, 1)[0] + guidance.split(END, 1)[1]
    if receipt.get("reuse") and sha(outside) != receipt["outside_sha256"]:
        raise ValueError("Reviewed reused guidance changed before completion")
    preflight(home, skills, guidance)


def apply_pending(folder, home, skills, rollback=False):
    receipt = json.loads((folder / "receipt.json").read_bytes())
    if receipt["home"] != str(home) or receipt["skills"] != str(skills):
        raise ValueError("Transaction targets differ from explicit current profile")
    if rollback:
        active = json.loads(read(home / "principles-harness/installations/active.json") or b"null")
        pending = json.loads(read(home / "principles-harness/installations/pending.json") or b"null")
        if not ((active and active.get("receipt") == str(folder / "receipt.json"))
                or (pending and pending.get("id") == folder.name)):
            raise ValueError("Only the current or pending transaction may be rolled back")
    selected = [op for op in receipt["operations"] if not rollback or op["role"] not in ("runtime", "principles")]
    # Validate all current bytes and private recovery payloads before any effect.
    for op in selected:
        if not isinstance(op["id"], str) or not op["id"].isdigit():
            raise ValueError("Invalid recovery payload identity")
        path = bounds(home, skills, op["role"], op["relative"])
        if identity(path) not in (op["old"], op["new"]):
            raise ValueError("Intervening edit; inspect pending transaction before recovery")
        for kind in ("old", "new"):
            if op[kind] is not None and identity(folder / (op["id"] + "-" + kind)) != op[kind]:
                raise ValueError("Recovery payload missing or changed")
    for op in (reversed(selected) if rollback else selected):
        path = bounds(home, skills, op["role"], op["relative"])
        want = "old" if rollback else "new"
        if identity(path) == op[want]:
            continue
        data = read(folder / (op["id"] + "-" + want)) if op[want] is not None else None
        # Recheck immediately before each replacement; unrelated editors do not share our lock.
        if identity(path) != op["new" if rollback else "old"]:
            raise ValueError("Concurrent edit detected")
        atomic(path, data)
    for op in selected:
        if identity(bounds(home, skills, op["role"], op["relative"])) != op["old" if rollback else "new"]:
            raise ValueError("Target changed during completion readback")
    if not rollback:
        completed_readback(home, skills, receipt)
    receipt["status"] = "rolled_back" if rollback else "complete"
    write_json(folder / "receipt.json", receipt)
    state = home / "principles-harness/installations"
    if rollback:
        previous = read(folder / "previous-active.json")
        atomic(state / "active.json", previous)
    else:
        write_json(state / "active.json", {**receipt, "receipt": str(folder / "receipt.json")})
    atomic(state / "pending.json", None)
    return receipt


def setup(source, home, skills, upgrade=False, reuse=None):
    home, skills = plain(home), plain(skills)
    state = home / "principles-harness/installations"
    pending = read(state / "pending.json")
    if pending:
        value = json.loads(pending)
        folder = plain(state / value["id"])
        if folder.parent != state or value["id"] != folder.name:
            raise ValueError("Invalid pending transaction identity")
        if value["source_sha256"] != sha((source / "bundle-manifest.json").read_bytes()):
            raise ValueError("Pending source differs; inspect or roll back first")
        verify(source)
        receipt = json.loads((folder / "receipt.json").read_bytes())
        planned = next((read(folder / (op["id"] + "-new")) for op in receipt["operations"] if op["role"] == "guidance"), read(home / "AGENTS.md") or b"")
        preflight(home, skills, planned)
        with lock(home):
            value = apply_pending(folder, home, skills)
        return {"status": "pass", "action": "reconciled", "receipt": str(folder / "receipt.json"), "version": value["version"]}
    ops, info = operations(source, home, skills, upgrade, reuse)
    if not ops:
        return {"status": "pass", "action": "unchanged", **info}
    with lock(home):
        # Revalidate after acquiring the installer lock before recording/backing up mutations.
        ops, info = operations(source, home, skills, upgrade, reuse)
        folder = state / uuid.uuid4().hex
        folder.mkdir(mode=0o700)
        previous = read(state / "active.json")
        if previous is not None:
            atomic(folder / "previous-active.json", previous)
        records = []
        for i, op in enumerate(ops):
            row = {"id": str(i), "role": op["role"], "relative": op["relative"]}
            for kind in ("old", "new"):
                data = op[kind]
                row[kind] = sha(data) if data is not None else None
                if data is not None:
                    atomic(folder / (str(i) + "-" + kind), data)
            records.append(row)
        receipt = {**info, "status": "pending", "operations": records}
        write_json(folder / "receipt.json", receipt)
        write_json(state / "pending.json", {"id": folder.name, "source_sha256": info["source_sha256"]})
        value = apply_pending(folder, home, skills)
    return {"status": "pass", "action": "installed", "receipt": str(folder / "receipt.json"), **info}


def check(source, home, skills):
    verify(source)
    state = home / "principles-harness/installations"
    if read(state / "pending.json"):
        return {"status": "unknown", "reason": "Partial setup: inspect current guidance; it may already be active. Rerun the same install to reconcile or use its receipt to roll back."}
    active = json.loads(read(state / "active.json") or b"null")
    if not active:
        return {"status": "unknown", "reason": "No complete full-setup record; skill-only copying is not automatic setup"}
    ops, info = operations(source, home, skills, upgrade=True)
    if ops:
        return {"status": "unknown", "reason": "Installed setup differs from selected source"}
    verify(skills / NAME)
    return {"status": "pass", "action": "configured", **info,
            "limits": "Static local setup only; new Codex run/session required. Overrides, model compliance and actual project gate execution remain separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", default="install", choices=("install", "check", "rollback"))
    parser.add_argument("--scope", required=True, choices=("user",))
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents/skills")
    parser.add_argument("--upgrade", action="store_true")
    parser.add_argument("--reuse-guidance-sha256", help="Explicit operator-reviewed current global guidance digest; semantic adequacy is not machine-verified")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 12):
            raise ValueError("Python 3.12+ required; no interpreter is installed automatically")
        home, skills = plain(args.codex_home), plain(args.skills_dir)
        if args.action == "check":
            result = check(SKILL, home, skills)
        elif args.action == "rollback":
            if args.receipt is None:
                parser.error("rollback requires --receipt")
            folder = plain(args.receipt).parent
            state = home / "principles-harness/installations"
            if folder.parent != state or args.receipt.name != "receipt.json":
                raise ValueError("Receipt is outside the explicit profile's installation store")
            with lock(home):
                apply_pending(folder, home, skills, rollback=True)
            result = {"status": "pass", "action": "rolled_back", "retained": "Shared runtime/principles pins and empty directories remain; later user edits are never overwritten"}
        else:
            result = setup(SKILL, home, skills, args.upgrade, args.reuse_guidance_sha256)
        print(json.dumps(result))
        return 0 if result["status"] == "pass" else 2
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps({"status": "fail", "reason": str(error), "recovery": "Inspect retained receipt/pending state before retry; an interrupted global write may already be active"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
