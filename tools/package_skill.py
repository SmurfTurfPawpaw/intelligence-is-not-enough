"""Build/check the offline skill from an explicit public-source list. No network."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def plain_path(root, path):
    """Check every output ancestor before any build writes; no sandbox claim."""
    relative = path.relative_to(root)
    for index in range(len(relative.parts) + 1):
        part = root.joinpath(*relative.parts[:index])
        if part.is_symlink() or part.is_junction():
            raise ValueError("Linked package path refused before writing")


def package(root, build=False):
    root = Path(root)
    skill = root / "skills/intelligence-is-not-enough"
    sources = json.loads((root / "tools/skill-sources.json").read_text(encoding="utf-8"))
    expected = {}
    for name in sources:
        parts = PurePosixPath(name).parts
        if (not parts or name != "/".join(parts) or "\\" in name or ":" in name
                or any(p in (".", "..") for p in parts) or name.startswith("/")
                or parts[0] in ("skills", ".git", "internal", ".principles") or name in expected):
            raise ValueError("Invalid or duplicate public source path")
        source = root / name
        if any(root.joinpath(*parts[:i]).is_symlink() or root.joinpath(*parts[:i]).is_junction()
               for i in range(1, len(parts) + 1)):
            raise ValueError("Linked public source refused")
        expected[name] = source.read_bytes()
    bundle = skill / "references/harness"
    plain_path(root, bundle)
    plain_path(root, skill / "bundle-manifest.json")
    # Validate the complete selected destination set before the first write.
    # A late refusal cannot undo a write through a junction or symbolic link.
    for name in expected:
        plain_path(root, bundle / name)
    actual = set()
    if bundle.exists():
        for path in bundle.rglob("*"):
            if path.is_symlink() or path.is_junction():
                raise ValueError("Linked bundle refused")
            if path.is_file() and "__pycache__" not in path.parts:
                actual.add(path.relative_to(bundle).as_posix())
    if actual - set(expected):
        raise ValueError("Unexpected generated resource; inspect and remove explicitly")
    for path in skill.rglob("*"):
        if path.is_symlink() or path.is_junction():
            raise ValueError("Linked skill member refused before writing")
    for name, data in expected.items():
        target = bundle / name
        if build:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        elif not target.is_file() or target.read_bytes() != data:
            raise ValueError("Missing or stale generated resource: " + name)
    files = []
    for path in sorted(skill.rglob("*")):
        if path.is_symlink() or path.is_junction():
            raise ValueError("Linked skill member refused")
        if not path.is_file() or "__pycache__" in path.parts or path.name == "bundle-manifest.json":
            continue
        data = path.read_bytes()
        files.append({"path": path.relative_to(skill).as_posix(), "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()})
    version = json.loads((root / "PROFILE.json").read_text(encoding="utf-8"))["release_version"]
    manifest = {"name": "intelligence-is-not-enough", "version": version,
                "generated_resources": "Exact copies of tools/skill-sources.json; edit source then rebuild",
                "files": files}
    manifest_path = skill / "bundle-manifest.json"
    data = (json.dumps(manifest, indent=2, ensure_ascii=True) + "\n").encode()
    if build:
        manifest_path.write_bytes(data)
    elif manifest_path.read_bytes() != data:
        raise ValueError("Skill manifest drift; rebuild and review before distribution")
    return {"status": "pass", "version": version, "resources": len(expected),
            "skill_files": len(files) + 1, "bytes": sum(r["bytes"] for r in files) + len(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    args = parser.parse_args()
    try:
        print(json.dumps(package(ROOT, args.command == "build")))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps({"status": "fail", "reason": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
