# Contributing

Improve a concrete user or research outcome. State the problem, why the existing approach is insufficient, a simpler alternative and what would demonstrate the improvement.

## Keep contributions public-safe

Use synthetic examples and sanitized explanations. Never attach actual engagement records, credentials, customer/target identifiers, private paths, raw captures, private chats or unpublished vulnerability details to public issues or pull requests. The ignore file is a convenience, not a privacy guarantee; inspect the exact diff and Git tree before publishing.

## Make changes traceable

Read [AGENTS.md](AGENTS.md) and the relevant [workflow](WORKFLOW.md). Keep original input, concise decisions, actual outputs, failed attempts and review in appropriate private project records. Public contributions should contain the reusable source, explanatory documentation and synthetic tests—not the author's private operational history.

Update affected contracts, examples, links and metadata together. Keep component versions distinct. A changed published artifact needs a new revision; do not rewrite release history.

## Verify the affected claim

Run checks appropriate to the change and preserve nonzero exits. The [verification guide](VERIFICATION.md) lists focused example checks and runtime-maintainer suites. Do not rerun broad unchanged suites without a relevant change, failure or release requirement.

For the Codex distribution, follow the [skill maintenance procedure](https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough/blob/v2.4.0/CODEX-SKILL.md): edit authoritative root resources, regenerate the bundle, run affected tests and retain actual outputs privately. The repository's required acceptance command is `python tools/accept.py --root PRIVATE_RECORD_ROOT --task TASK_ID --organisation relative/actual-organization.json`, using real current values. It checks generated-resource drift, the actual organization and the final workflow gate; it never generates judgments or receipts to make itself pass.

In a pull request, explain the resulting behavior, actual checks, source/revision scope, compatibility and recovery. Disclose self-review and limits. A passing test or model's agreement is not proof of permission, genuine independence, live affectedness or absence of other defects.

Keep contributions model-neutral. New tools should earn their maintenance cost; a catalogue entry does not require every user to install it. Do not add a model service, scheduler or recurring inference merely to appear autonomous.
