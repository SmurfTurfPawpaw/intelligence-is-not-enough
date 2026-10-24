"""Verify installed declared bytes; integrity, not authentication."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def verify(root):
    root = Path(root)
    if root.is_symlink() or root.is_junction():
        raise ValueError("Linked skill root refused")
    manifest = json.loads((root / "bundle-manifest.json").read_text(encoding="utf-8"))
    expected = {}
    for row in manifest["files"]:
        name = row["path"]
        parts = PurePosixPath(name).parts
        if (not parts or name != "/".join(parts) or "\\" in name or ":" in name
                or any(p in (".", "..") for p in parts) or name.startswith("/")
                or name in expected or name == "bundle-manifest.json"):
            raise ValueError("Invalid or repeated bundle path")
        expected[name] = row
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink() or path.is_junction():
            raise ValueError("Linked bundle member refused")
        if path.is_file():
            name = path.relative_to(root).as_posix()
            if "__pycache__" not in path.parts and name != "bundle-manifest.json":
                actual.add(name)
    if actual != set(expected):
        raise ValueError("Bundle file set differs: missing or unexpected member")
    for name, row in expected.items():
        data = (root / name).read_bytes()
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError("Bundle identity differs: " + name)
    return {"status": "pass", "version": manifest["version"], "files": len(actual),
            "bytes": sum(r["bytes"] for r in expected.values()),
            "claim": "Declared local bytes; not authenticated provenance or execution"}


def main():
    try:
        print(json.dumps(verify(Path(__file__).resolve().parents[1])))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps({"status": "fail", "reason": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
