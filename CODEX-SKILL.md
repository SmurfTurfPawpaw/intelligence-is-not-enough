# Install once, apply across projects

Full setup installs the skill, compatible local checker and **standing global G01–G12 principles**. Subsequent ordinary project work needs no `$skill` invocation or repeated reminder. Existing project rules, tasks and tests remain in place; the standing instructions direct the agent to adopt the required workflow and integrate its real acceptance gate on first authorized project work.

## Recommended installation

Obtain and review the pinned release, then run one full-setup command with Python 3.12+:

```sh
git clone --branch v2.4.0 --depth 1 https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough.git
cd intelligence-is-not-enough
python install.py --scope user
```

Or give Codex this single installation request:

> Install the full user-scope setup from https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough/tree/v2.4.0. Read the installation guide and run `python install.py --scope user` from the reviewed checkout, then verify setup. Preserve my unrelated instructions and tools. Complete the global principles/runtime setup; do not stop at copying the skill folder.

Start a **new Codex run/session** after installation. The global rules are the always-present layer; the skill supplies deeper procedures when relevant. [Official AGENTS guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md) explains loading, precedence and size limits; [skill documentation](https://learn.chatgpt.com/docs/build-skills) explains optional explicit and implicit selection.

The setup command deliberately changes your user configuration. It uses `CODEX_HOME` or `~/.codex` for global instructions/support, and `~/.agents/skills/intelligence-is-not-enough` for the skill. It verifies sources, preserves unrelated instruction bytes and other skills, reuses compatible runtime code, backs up changed files privately and activates global guidance last. No dependency download, model API, service, hook, scheduler or ongoing process is added.

**A native skill-only installation is incomplete for always-on principles.** Codex's built-in skill installer copies files; it does not execute arbitrary setup scripts. If you already copied the complete skill folder, run `python "SKILL_DIR/scripts/install.py" --scope user` once. Replace `SKILL_DIR` with its actual location. Do not claim copying alone configured global guidance.

## Verify setup

From the reviewed checkout:

```sh
python install.py check --scope user
```

Or run the installed skill's `scripts/install.py check --scope user`. This read-only check verifies the selected source, installed bytes, managed guidance, compatible runtime, known instruction budget and transaction state. It reports configured local state, **not authenticated loading, perfect model compliance or execution of a project's checks**. Explicit skill invocation remains optional for requesting deeper guidance:

```text
$intelligence-is-not-enough Investigate this owned local fixture with the exploratory profile.
```

Base principles govern coding, research, design and business. The full exploratory profile and eight responsibility owners apply to research; eight responsibilities do not imply eight permanent workers. Actual project acceptance must run its meaningful checks and required gate. Guidance cannot intercept arbitrary tools or override higher-priority instructions.

## Existing installations and profiles

- An exact repeat verifies state and returns unchanged, with no new backups or timestamp churn.
- For a deliberate update from a previous verified skill, use `python install.py --scope user --upgrade`. Changed or unknown installations and different immutable runtime code are refused rather than silently overwritten.
- To reuse complete existing standing principles without duplicating them, the operator/agent must review the actual global instructions, then pass `--reuse-guidance-sha256 REVIEWED_DIGEST`. The digest binds that judgment to current bytes; the installer does not certify semantic equivalence. It adds the automatic routing block and retains the canonical principles source. Later unrelated changes invalidate that reuse judgment until reviewed again.
- `--codex-home PATH` and `--skills-dir PATH` select explicit alternative targets. `--codex-home` does not change how Codex is launched: use that profile in the actual host. Known same-name user installations elsewhere are reported to prevent shadowing duplicates.

A nonempty global `AGENTS.override.md`, malformed owned block, incompatible pin, linked destination or insufficient configured instruction budget blocks setup before activation. The command preserves the conflicting setting and explains the dependency. It never raises limits or trusts hooks automatically. Reported remaining instruction capacity cannot predict future project files or launch-time overrides. Other machines, cloud runners and agent hosts need their own corresponding configuration.

Runtime source/dependency checks refuse unexpected importable members. Existing manuals and separate review/test/template archives are preserved rather than executed or certified. Interpreter binaries, installed standard libraries and existing bytecode caches are outside this source-identity claim; setup is not execution attestation or an adversarial-filesystem sandbox.

## Interrupted setup and rollback

The installer saves private file backups and a transaction receipt under `CODEX_HOME/principles-harness/installations/`. These use local user filesystem protections, not encryption. Keep them private and outside source control.

An interrupted setup remains nonpassing. The global file may already have been replaced even if the receipt is pending; inspect current bytes rather than infer inactivity. Rerun the same reviewed installation command to reconcile expected old/new file identities without repeating completed effects. Intervening edits or a changed source stop recovery. Operations are atomic per file, not one atomic transaction over the entire profile.

To roll back the current or pending transaction, use the receipt path returned by setup:

```text
python install.py rollback --scope user --receipt "ACTUAL_RECEIPT_PATH"
```

Rollback preflights all affected identities, restores/removes only unchanged owned skill/guidance files and refuses later user edits. Shared runtime/principles pins, private backups and empty directories remain because other projects may rely on them. Roll back newer transactions before older ones. Never delete a whole profile to undo setup.

## Maintain without drift

Root harness resources remain authoritative; `tools/skill-sources.json` generates the skill's offline `references/harness/` copies. Edit sources, regenerate, then run affected tests:

```sh
python tools/package_skill.py build
python tools/package_skill.py check
python -B -m unittest discover -s tests -v
```

Retain real outputs privately, complete the attributed review/receipts and run the required maintainer boundary with actual values:

```text
python tools/accept.py --root "PRIVATE_RECORD_ROOT" --task TASK_ID --organisation relative/actual-organization.json
```

Preserve nonzero results; no unchanged broad rerun or recurring model call is required. Distribution2.4.0 adds offline discovery and consumer tracing while retaining full automatic setup; profile2.0.0, principles2.0.1 and workflow2.0.0 retain their separate contracts. Published releases remain immutable. Checks and manifests establish selected local identities, not distributor signatures or universal correctness.
