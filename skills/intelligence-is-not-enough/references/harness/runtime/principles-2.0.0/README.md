# Local principles workflow

**Workflow2.0.0 · declared-evidence core/schema1.0.0 · Python3.12+ · standard library.**

This directory supplies the local runtime for the required [investigation workflow](../../WORKFLOW.md). Keep `workflow.py`, `principles.py` and `vendor/` together. Use their actual trusted project-pinned location or an approved installed copy. No installation command, account, network service or global configuration is required.

## Required commands

```text
python runtime/principles-2.0.0/workflow.py begin --root "PROJECT_ROOT" --task TASK_ID --plan research/investigation-brief.md
python runtime/principles-2.0.0/principles.py receipt --root "PROJECT_ROOT" --task TASK_ID --check CHECK_ID --result pass --evidence private/actual-check.log --method "Actual scoped check and interpretation"
python runtime/principles-2.0.0/workflow.py check --root "PROJECT_ROOT" --task TASK_ID
```

These paths assume commands run from the extracted package root. Replace every uppercase placeholder and populate generated task/review records before receipts. The required final `workflow.py check` is stronger than the lower-level `principles.py check`; the latter alone does not complete the required workflow. The core's `init` command similarly does not replace the workflow's required `begin`.

`begin` creates unresolved records and refuses overwriting an existing/partial task. Material brief bytes are frozen. `receipt` records a declared result and binds current selected source/tool/log identities; it does not run the underlying experiment. `check` uses the latest relevant receipts and required judgments. Exit0 means selected current declared checks pass,1 means failure/malformed input,2 means unknown/unresolved/insufficient evidence. File creation returning0 is not acceptance.

Use the [full workflow](../../WORKFLOW.md) for the task contract, P01–P10 review, small-change eligibility, source selection, freshness and actual acceptance integration. [Verification](../../VERIFICATION.md) explains tool limits and software tests.

## Optional larger project record

Projects with an existing need for a structured component/requirement record can use the separate schema under `vendor/handbook/spec/project.schema.json`. Its illustrative record is `vendor/handbook/starter/project.example.json`; its validator version is0.2.0 and record schema version2.0.0. These versions are distinct from workflow2.0.0 and core/task schema1.0.0.

```text
python runtime/principles-2.0.0/principles.py validate-project --root "PROJECT_ROOT" --record path/to/project-record.json
```

The example is fictional, not a declaration about a real project. This optional larger record does not replace the required per-task workflow and is not a questionnaire to complete for every command. It adds no live permissions or monitoring. The bundled validator and its source dependencies support this optional command without private files.

## Trust and privacy

Inspect unfamiliar source and compare file identities with the package manifest before adopting it. A manifest is an integrity reference, not a signature. The runtime performs no project command execution, network call, AI inference or global configuration write; it reads selected files and writes task/receipt records within the explicit project root.

Store actual engagement records/evidence in the approved private project location. The runtime validates declared local bindings and required record/review shape; it does not authenticate execution, approve effects or establish semantic research quality.
