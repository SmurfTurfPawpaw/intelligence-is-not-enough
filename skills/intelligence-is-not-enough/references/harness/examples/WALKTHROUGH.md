# Complete local workflow

This tutorial demonstrates one real local run, from begin to acceptance, in your own disposable extracted copy. It needs Python3.12+, no globally installed harness, no API account and no target. Commands run from the extracted package root. Review the supplied scripts first: ordinary Python and this workflow are not a sandbox.

The task/review JSON below the `examples` directory is **illustrative**, not a completed review or authorization. You must inspect actual output, supply your attribution and correct the judgments. The checker validates bindings and shape; it cannot recognize a dishonest copied review. Never use these demo judgments to approve a real engagement.

## 0. Map the organization

Read [orchestration](../ORCHESTRATION.md). In your disposable copy, create `example-private/organisation.json` using [the compact record](organisation-compact.json) as a starting structure. Keep all eight teams; map the actual owner/contributor, set the current work to an empty list before starting and retain actual state later. The sample's integrated work/review is illustrative and must not impersonate a run. No eight worker processes are needed. This record describes your owned synthetic tutorial project, not a real target.

## 1. Read, then begin

Read [the synthetic brief](investigation-brief.md). Populate any actual local ownership/budget facts before begin; the whole file is frozen afterward. Its question is repeated-identifier behavior, not a requirement to discover a vulnerability. Keep evolving notes elsewhere.

```text
python runtime/principles-2.0.0/workflow.py begin --root . --task DEMO-LOCAL-001 --plan examples/investigation-brief.md
python examples/accept.py --root . --task DEMO-LOCAL-001 --organisation example-private/organisation.json
```

The first command creates draft task/review/start records. The second runs the fixed fixture and the gate. At this stage expect exit2/unknown because records and evidence are unresolved. Inspect your actual output. Do not erase the draft to hide this result.

## 2. Capture an actual experiment

```text
python examples/capture.py --root .
```

Inspect `example-private/ledger-run.json`. It records actual timestamps, Python identity, command, exit status, stdout/stderr and fixture hashes before/after. The collector refuses to overwrite an existing capture. Expected behavior is first accepted, repeat refused, distinct control accepted. A prediction or this page's text is not a receipt. If the capture fails, investigate and preserve it rather than declaring a pass.

A timeout or process-launch failure retains an unknown capture, available partial output, actual times and source identities, then returns exit2 without retrying. A completed process with unexpected behavior returns fail/exit1. Null process exit status means no reliable completed-process status was obtained; it is not zero. Storage failure can prevent capture persistence and remains a real blocker—keep the host's failure output.

Create `example-private/notes.md` with your actual investigator identity, command/time, source hash and output reference. State what you observed and why the controls matter. Explain that refusal falsifies duplicate acceptance for this exact fixture/sequence; it says nothing about real services, concurrency or alternate identities. Include failed attempts, unresolved facts, actual usage if available or UNKNOWN, and next safe action. The supplied [illustrative notes](notes.md) show the distinction but are not your observation.

## 3. Populate the task and perform the review

Open the generated `.principles/tasks/DEMO-LOCAL-001/task.json`. Compare it with [demo-task.json](demo-task.json). Preserve the actual generated begin/review/brief subjects. Use the example's concrete outcome, selected paths and C-LEDGER criterion only after confirming they describe your task. All listed files, including your actual notes, must exist. `state: ready` means the contract is populated, not that it passed.

Open the generated `review.json`. [demo-review.json](demo-review.json) shows the full P01–P10 structure and scoped reasons. Inspect each row against your actual brief, scripts, capture and notes. Set the real `reviewer` and `summary`, disclose self-review, correct unsupported claims and retain unknown/fail where appropriate. The supplied `supported` statuses illustrate the shape of a justified review; copying them is not review evidence. No independent review is claimed by this tutorial.

Run the adapter again. With populated records but no receipts, the gate should still return exit2. The organization checker can pass its declared structure while research acceptance remains unresolved. The wrapper never manufactures acceptance to make its own check green.

## 4. Record what happened

Run `python tools/orchestration.py check --record example-private/organisation.json --output example-private/organization-check.json` through your actual host and inspect the actual saved JSON. It includes observation time and source/record hashes. Existing output is never overwritten; use a new evidence filename after an affected recheck and retain the earlier result. The record checker reads declarations without changing them; update actual work/handoff attribution as appropriate before capturing its final current output. In this tutorial the dossier may remain a compact roster with an empty work list; actual research details are in the existing task/notes.

The complete task example includes C-ORG and C-LEDGER. Record the organization receipt using its actual output:

```text
python runtime/principles-2.0.0/principles.py receipt --root . --task DEMO-LOCAL-001 --check C-ORG --result pass --evidence example-private/organization-check.json --method "Actual organization-record check inspected; declared consistency only, not research completion"
```

If you reuse the exact source-bound record-check output, retain its actual observation time; it makes no runner-liveness claim. A changed roster/checker requires an affected recheck and receipt. Then record the actual experiment evidence below.

Finalize selected notes/review first. Record a receipt only for a real result that satisfies the declared criterion:

```text
python runtime/principles-2.0.0/principles.py receipt --root . --task DEMO-LOCAL-001 --check C-LEDGER --result pass --evidence example-private/ledger-run.json --method "Actual synthetic fixture run, source hashes and controls inspected; attributed local review and notes; no live conclusion" --observed-at ACTUAL_TIMESTAMP_FROM_CAPTURE
```

Replace `ACTUAL_TIMESTAMP_FROM_CAPTURE` with the exact timezone-bearing `observed_at` value in your captured JSON. Do not execute the placeholder. Use fail/unknown if the required criterion is not established. `pass` refers to the declared research-quality criterion; it does not assert that the starting vulnerability hypothesis is true.

## 5. Use the actual acceptance command

```text
python examples/accept.py --root . --task DEMO-LOCAL-001 --organisation example-private/organisation.json
```

Exit0 is expected only if the organization check, fixed project check and actual task's required gate pass. The adapter uses fixed argv, an explicit root/task and no shell. It creates neither records nor receipts and propagates nonzero from any stage. The lower-level collector's check is not a substitute for `workflow.py check`.

For a real project, connect its **real** tests and this required gate to its existing acceptance command. The demo ledger is not a check for unrelated code. [The main workflow](../WORKFLOW.md) explains impact-based check selection and recovery.

## 6. Observe drift and resume

In this disposable copy, make a harmless comment change to selected `example-private/notes.md` after the receipt, then run the adapter. Expect exit2/source mismatch, even though the ledger still succeeds. Preserve the result. Review the change; if the same unchanged experiment still supports the exact criterion, record a new receipt with its **original** observation time and a truthful reuse reason. Otherwise run the affected experiment and retain both results. Do not overwrite a failed capture or invent a new observation date.

Do not edit the frozen brief to experiment with scope changes. A materially changed brief needs a linked new task. The [resume table](../WORKFLOW.md) covers other interrupted states.

## 7. Explore Beyond Human Patience

```text
python examples/explore.py
python examples/explore.py --max-cases 17
python -B -m unittest discover -s examples -p test_examples.py -v
```

The first calibrates a finite sequence experiment: the correct ledger holds within the bound; the injected retry fault has a short replay; reject-all is inconclusive. The second intentionally stops incomplete with exit2. The last runs focused software checks. These are separate experiments from DEMO-LOCAL-001; the ledger receipt does not certify them. For a substantive new investigation, define its actual criterion and selected evidence before begin.

The research idea is reusable: let AI propose invariants and consequential sequences; let deterministic code execute, count and shrink; let AI interpret a compact evidence summary. The scripts make no model calls and establish no AI speedup or real-world security guarantee.
