"""Synthetic in-memory example; no files, network or real transactions."""
import json


def observe():
    seen = set()

    def accept(identifier):
        if identifier in seen:
            return "refused"
        seen.add(identifier)
        return "accepted"

    result = {
        "first": accept("synthetic-a"),
        "repeat": accept("synthetic-a"),
        "control": accept("synthetic-b"),
    }
    assert result == {"first": "accepted", "repeat": "refused", "control": "accepted"}
    return result


if __name__ == "__main__":
    print(json.dumps(observe(), sort_keys=True))
