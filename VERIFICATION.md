# Verification and interpretation

Verification should test the claim at the boundary where the promised outcome matters. A source pattern, local reproduction, deployed-system observation and accepted remediation require different evidence. The required checker helps retain and bind selected evidence; technical judgment remains necessary.

## Package integrity

Before adopting the package, compare its files with `release-manifest.json`. Each listed file has a path, byte count and SHA256. Use a trusted local hashing tool to compare them. The manifest excludes its own self-hash to avoid a circular definition. A matching checksum detects a changed file relative to that manifest; it does not authenticate a distributor or make unfamiliar code trustworthy.

[PROFILE.json](PROFILE.json) separates profile, principles, workflow and schema versions and records required runtime identities. Keep published/pinned runtime files immutable; use a new revision for a change. Do not replace a different installed version automatically.

## Try the contained example

```text
python --version
python examples/ledger.py
python runtime/principles-2.0.0/workflow.py --help
python runtime/principles-2.0.0/principles.py --help
```

Use Python3.12+ and an extracted directory you control. The [example](examples/README.md) explains the expected synthetic observation and control. These commands execute a known in-memory example and show CLI usage; they do not validate a real service or create authorization. Neither Python's isolated mode nor a virtual environment is a security sandbox.

## Verify research apparatus before interpreting results

For generated or adapted instruments, first demonstrate relevant ordinary success and meaningful rejection; include a known faulty synthetic case when feasible. An instrument that rejects everything cannot establish an access-control invariant. Keep calibration and the target experiment separate. A control needs its actual authority and resource budget.

The [sequence experiment](examples/explore.py) includes working, deliberately faulty and reject-all variants, actual finite-space counts, a minimized replay and incomplete status at a case limit. Its [focused tests](examples/test_examples.py) can be run with `python -B -m unittest discover -s examples -p test_examples.py -v`. The example's calibration pass is not a real-system finding, whole-system proof or measured AI advantage.

The [complete walkthrough](examples/WALKTHROUGH.md) demonstrates actual local evidence collection and the mandatory final gate. The adapter adds no automatic review or receipt collection and must not be used as a shortcut for a real task's checks.

## Claims the required gate checks

The workflow checks the task/start/review/brief contract and selected local evidence bindings. It verifies the required ten review identities and references, checks current selected bytes against declared receipts and uses the newest relevant evidence. It checks the recorded workflow/core identities and frozen material brief. A small task also needs all required no-impact declarations.

Define useful acceptance before collecting evidence. Check positive, negative and failure/recovery behavior appropriate to the research unit. Important examples include:

- An unresolved draft or missing receipt must remain unknown.
- An actual negative research result may pass a check explicitly defined as investigating that behavior with a control; it does not prove the starting hypothesis.
- Changed selected notes/source/review or a materially changed frozen brief cannot silently reuse old evidence.
- A newer failure, unknown, stale, corrupt, tied, future or source-mismatched record cannot fall back to an older passing receipt.
- An independent review must identify the actual revision and its limits. Where self-review is sufficient, disclose it.
- A resumed client or long-running process must reconcile state after missed updates; a historical pass is not runner liveness or fresh coverage.

## Claims the gate cannot establish

The tool does not judge whether a hypothesis is insightful, a selected test is sufficient, a claimed output is genuine, a reviewer is independent, an omitted file matters or the action was authorized. A person able to edit all records can forge mutually matching files. Timestamps are records, not authenticated execution evidence.

The checker is not a sandbox, scanner, tool interceptor, scheduler, production monitor or approval authority. It does not execute project commands, contact targets, invoke AI, install dependencies or change global configuration. Runtime permission/containment and actual customer/program approvals remain separate.

## Limits and failure handling

The supported runtime uses Python3.12+ standard-library filesystem checks. Limits include128 selected subjects,64 checks,500 receipt-directory entries,1MiB JSON and16MiB per selected/evidence file. Record paths must be canonical and root-relative; nested symlinks/junctions and traversal are refused. Before/after sampling detects relevant observed changes but is not an atomic filesystem snapshot.

Exit0 means selected current declared checks pass; exit1 means failure/malformed input; exit2 means unknown/unresolved/insufficient evidence. Preserve a nonzero status in project acceptance commands. Investigate the actual reason, retain failure evidence and correct the applicable source/record/runtime issue. Do not widen permissions, exclude the latest adverse result or fabricate output to obtain a pass.

A blocked dependent completion does not prohibit genuinely independent authorized work. Missing storage, runtime or authority must remain visible with a next action. Reconcile uncertain external completion before retrying; a rollback cannot undo already observed confidential data or messages delivered to others.

## Software checks for runtime maintainers

The runtime includes its source tests and the optional structured-record validator/schema. If you are reviewing or changing the checker itself, use the appropriate software tests:

```text
python -B -m unittest discover -s runtime/principles-2.0.0/tests -v
python -B -m unittest discover -s runtime/principles-2.0.0/vendor/handbook/tests -v
```

These are checker software tests, not a required full-suite rerun for each research experiment. Select checks by changed behavior and actual risk; preserve genuine failures and their corrections. Your engagement's private evidence remains separate from a publicly shared methodology or software test fixture.


## Organization verification

Run `python tools/orchestration.py check --record ACTUAL_ORGANIZATION_RECORD` on the project's current record, not a sample. Replace the placeholder. Bind selected roster/packet/handoff/checker files and actual output through the existing required workflow. Structural pass means declared consistency only, not task completion, true identity, authentic independence, artifact contents, liveness or authority.

The [orchestration chapter](ORCHESTRATION.md) defines the mandatory teams and limits. The [compact](examples/organisation-compact.json) and [parallel](examples/organisation-parallel.json) records are synthetic illustrations. Run `python -B -m unittest discover -s examples -p test_orchestration.py -v` for focused checker cases; no full unchanged core rerun is required per experiment. Profile2.0.0 changes the demo adapter to require an explicit organization-record path and preserve its nonzero before any project check or final gate.
