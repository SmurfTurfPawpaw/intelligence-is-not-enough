# Use the Codex skill

Apply the harness to actual project work: inspect current state, reuse rules and records, define the change, implement it and require evidence-bound acceptance. The short skill entry point loads deeper guides only when needed. Runtime resources are included; using the skill makes no network or model API call by itself.

## Install

Ask Codex's built-in skill installer:

> Install the skill from https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough/tree/v2.2.0/skills/intelligence-is-not-enough

Alternatively, copy the **complete** `skills/intelligence-is-not-enough` folder from this release to your user skills directory, `~/.agents/skills/`, or the project's `.agents/skills/`. Preserve a different existing installation and review compatibility before replacement. Codex also supports installations managed by its built-in installer. See the [official skill guide](https://learn.chatgpt.com/docs/build-skills) for discovery/invocation.

Invoke explicitly in a new turn:

```text
$intelligence-is-not-enough Apply the harness to this project and complete the current task.
```

For research:

```text
$intelligence-is-not-enough Investigate this owned local fixture with the exploratory profile.
```

Matching requests also permit implicit selection. Selection does not intercept arbitrary tool calls. The skill must connect the required gate to the project's actual acceptance command; that command must run. Host automatic selection is separate from file installation and validation.

## Two modes

**Base** applies the principles/workflow to general project work. **Research** additionally adopts the exploratory profile, eight responsibility owners and organization check. Eight teams do not mean eight workers or permanent calls. Normal coding does not become a red-team engagement.

Existing projects retain local rules, tests, current tasks, compatible pins and evidence history. Fresh projects get one material adoption record and acceptance integration. Conflicting versions require compatibility review. No dashboard, service, CI or paid connection is created.

## Check an installation

From the installed folder, using Python 3.12+:

```sh
python scripts/verify_bundle.py
```

The skill includes a manifest, runtime, templates, examples and guides. The check rejects missing, changed or unexpected distribution files. It compares declared local bytes, not a signature or authenticated execution proof. Keep installed bytes immutable; actual plans, reviews, captures and receipts belong in appropriate private/project storage.

Select the applicable adapter after existing checks, replacing actual paths/task:

```text
python "SKILL_DIR/scripts/accept.py" --root "PROJECT_ROOT" --task TASK_ID --profile base
python "SKILL_DIR/scripts/accept.py" --root "PROJECT_ROOT" --task TASK_ID --profile research --organisation relative/actual-organization.json
```

It verifies the skill, runs the organization check when applicable and finishes with the mandatory workflow gate. It creates no tasks, judgments or receipts and runs no project tests. Missing/failed/unknown evidence blocks completion. Reuse a compatible already-integrated gate.

## Maintain without drift

Root harness files are authoritative. `tools/skill-sources.json` selects public sources; the skill's `references/harness/` is generated. Do not edit those copies. From the repository root:

```sh
python tools/package_skill.py build
python tools/package_skill.py check
python -B -m unittest discover -s tests -v
```

`build` copies selected sources and updates the skill manifest. It refuses unexpected generated files instead of deleting them. `check` changes nothing and rejects drift. Tests use disposable synthetic projects and a standalone skill copy; they do not establish automatic loader selection, live security, customer acceptance or model quality.

For an actual maintainer task, retain outputs privately, complete its attributed review/receipts and run the required repository boundary:

```text
python tools/accept.py --root "PRIVATE_RECORD_ROOT" --task TASK_ID --organisation relative/actual-organization.json
```

Preserve nonzero results. No unchanged broad rerun or recurring model call is required. Distribution 2.2.0 adds this skill; profile/workflow remain 2.0.0. Removal means deleting only the exact new skill directory after checking for user changes; project records/copies stay separate. Updates are deliberate versioned replacements, not runtime auto-updates.
