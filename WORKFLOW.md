# Investigation workflow

Use this procedure for a useful unit of authorized research. It combines a stable research boundary with flexible discovery and a required local acceptance gate. Read the [principles](base/PRINCIPLES-2.0.1.md), [agent rules](AGENTS.md) and actual engagement authority before acting. No workflow record creates permission.

## 1. Define the useful outcome and boundary

Begin with the beneficiary and the decision the investigation should support. Preserve the original question; separate facts, assumptions, hypotheses and proposals. Existing evidence and the owner's starting theory are inputs. They do not limit the hypotheses the agent may develop.

Populate the [investigation brief](templates/INVESTIGATION.md), reusing existing project records where possible. Define:

- The useful objective, included/excluded subjects and relevant trust path.
- Actual authority, its validity/revocation conditions, permitted identities and operating mode.
- Permitted effects, aggregate rates/concurrency, retries, elapsed work, usage and spending limits.
- Initial sources, unknowns, approach and simpler alternatives.
- Stable requirements and observable research acceptance, including any acceptable negative or inconclusive outcome.
- Evidence, freshness, review, stopping and recovery/cleanup requirements.

An open-ended objective is legitimate when its asset, effect, budget and completion boundaries are specific. “Investigate the trust boundaries of this owned local service and deliver reproducible observations plus ranked unresolved paths” permits emerging hypotheses. “Find anything anywhere until something works” supplies neither a bounded scope nor a useful completion condition.

Resolve the current root/task explicitly. Keep the brief separate from evolving notes: the checker freezes the entire brief file, not selected sections.

## 1a. Establish the organization

Follow [orchestration](ORCHESTRATION.md). At first material project admission, create/reconcile all eight team identities with accountable owners, references to existing authorities and current work packets. Reuse the organization's current record for later tasks; workers activate only when useful. Select the actual organization record, relevant packets/handoffs and the structural checker as subjects in the principles task. An unassigned or blocked independent-review duty remains visible.

Run `python tools/orchestration.py check --record ACTUAL_ORGANIZATION_RECORD` as an ordinary required check, retain actual output and record a receipt under the project's chosen organization check ID. Replace the placeholder; use the actual retained checker location. Exit1/2 blocks dependent acceptance. This supplements the existing workflow gate; it creates no task dispatch or authenticated execution evidence.

## 2. Begin before material work

From the extracted package root, these command shapes use the bundled runtime. In another project, replace the runtime path with its actual retained location. Replace every uppercase placeholder; never execute it as a real task name/path.

```text
python runtime/principles-2.0.0/workflow.py begin --root "PROJECT_ROOT" --task TASK_ID --plan research/investigation-brief.md
```

The existing brief path is relative to `PROJECT_ROOT`. The command creates unresolved records under `.principles/tasks/TASK_ID/`:

| Record | Meaning |
| --- | --- |
| `begin.json` | Actual recording time, mode, brief identity and workflow/core identities. |
| `task.json` | Outcome, scope, selected subjects and acceptance checks. |
| `review.json` | Attributed P01–P10 judgments, initially unresolved. |
| `receipts/` | Evidence receipts created later by the collector. |

Creation success is not acceptance. A recorded timestamp does not authenticate that no earlier work occurred. Existing or partial starts are not overwritten: inspect and resume them, or admit a linked new task when necessary.

For a genuinely minor correction, a small route is available:

```text
python runtime/principles-2.0.0/workflow.py begin --root "PROJECT_ROOT" --task TASK_ID --small-reason "Concrete minor change and why its meaning/behavior stays the same"
```

Initial setup and substantive behavior, contract, data/access, external-effect, dependency/migration or recovery changes need a material brief. A short command can have a material effect. The small route requires all six impact declarations to be true; they start unresolved. Do not use it to classify a real exploit validation as harmless paperwork.

## 3. Populate the actual task contract

Complete `task.json` using real facts:

- `outcome`, `beneficiary`, `scope`, `authority_reference` and `recovery` must be meaningful.
- `subjects` identifies every selected source/dependency/consumer/evidence-index file needed to support this claim, or an intentional absence. Preserve the generated begin/review/brief subjects. Do not select an entire repository for appearance.
- `checks` assigns each selected criterion a stable ID, observable acceptance and appropriate freshness budget. `max_age_seconds: null` means a static binding claim; it does not make a runtime observation permanently fresh.
- Set `state` to `ready` only once the contract is populated. `ready` grants no authority or completion status.

Paths inside records are canonical, root-relative forward-slash paths. Directories/globs are not selected file subjects. Preserve the evidence and source set appropriate to the claim; the tool cannot infer an omitted dependency or decide what matters semantically.

## 4. Investigate and adapt

When a disclosure, research result or dependency change starts the investigation, use [discovery and consumer tracing](DISCOVERY.md): preserve original provenance and revisions, identify the root cause, derive qualified consumer paths and select a useful next discriminator. The offline `tools/discovery.py` report reuses the same notes/evidence/acceptance path; it fetches nothing and grants no testing authority. Run it again on relevant source, endpoint or freshness change. Preserve its nonzero attention result as unresolved work, not a silently replaced old report.

Use the [discovery loop](AGENTS.md), [Beyond Human Patience](AI-NATIVE.md) and [tool guide](TOOLS.md): characterization question or hypothesis → cheapest discriminating experiment → valid apparatus/control → observation → revised explanation or next action. An open-ended characterization can produce the first hypothesis rather than pretending it was known beforehand. Keep experiment order, alternative explanations and concise decisions in [notes](templates/NOTES.md). Related probes can share one task; they do not each need a requirement document or reviewer.

Establish a relevant working baseline before interpreting an absent effect. If the instrument cannot observe ordinary success, a rejected request or missing signal is inconclusive; it does not falsify the security hypothesis. If a control cannot be performed within actual authority, retain the limit.

Record actual subject/revision, environment, principal, configuration, tool/rule identity, observation time, meaningful exit/status and private sanitized evidence reference. Keep a prediction separate from an observation. Include unsuccessful attempts, contradictions and usage, with UNKNOWN rather than an invented zero.

Choose effects by actual authority and consequence. Source analysis, an owned synthetic fixture, an authorized live request and a disclosure are different operations. A source finding does not expand live scope. Stop the dependent branch when a permission, effect, budget, data or recovery boundary is reached; continue independent authorized work when useful.

New hypotheses and methods within the admitted objective/boundaries can evolve in notes. A material scope/brief revision requires a linked new task. Retain its predecessor, failed evidence and reason for the change; do not edit the frozen brief to make a prior failure pass.

## 5. Review the final useful result

Before recording receipts, finalize selected notes/findings/source and complete `review.json`. Attribute the reviewer and disclose self-review or independent-review limits. Resolve each principle exactly once:

| ID | Required review question |
| --- | --- |
| P01 | Is the outcome useful, and were simpler explanations/alternatives considered? |
| P02 | Are requirements, research acceptance and scope adequate? |
| P03 | Do selected sources, consumers and records agree at the relevant revisions? |
| P04 | Are likely failures, containment, stop conditions and recovery addressed? |
| P05 | Is necessary knowledge durable, sourced and appropriately private? |
| P06 | Can a reader understand current work, ownership, blockers and next actions? |
| P07 | Are authority/component boundaries and compatibility clear? |
| P08 | Does the result serve the recipient's perspective with honest limits? |
| P09 | Is the approach sufficiently simple, usable and proportionate? |
| P10 | Are ownership, authority, effects and usage/maintenance accountable? |

`supported` needs a scoped reason and existing task check IDs. Several rows may cite one actual check; ten review questions do not require ten test suites. `not_applicable` needs a concrete scope reason; P01/P05/P10 always apply. Missing evidence is not N/A. An `unknown` or `fail` review disposition blocks its applicable completion.

For the small route, compact `unchanged` rows may share `scope_checks`, a review summary and the concrete minor-change reason. All six `no_impact` values must be true. A material change cannot use that shortcut.

Scientific uncertainty and workflow UNKNOWN are different. A bounded investigation can meet predeclared acceptance while an explanation remains uncertain. An unanswered required experiment or missing reliable evidence cannot be renamed success. A hypothesis falsified by a valid observation/control remains falsified even if the research-quality check passes.

## 6. Record actual evidence

Run the selected project checks or experiments through actual authorized tools. Inspect and retain their output privately. Record the result that occurred:

```text
python runtime/principles-2.0.0/principles.py receipt --root "PROJECT_ROOT" --task TASK_ID --check CHECK_ID --result pass --evidence private/actual-check.log --method "Actual method, evidence interpretation and scope"
```

Use `fail` or `unknown` when applicable. For a time-dependent observation, add `--observed-at` with its actual timezone-bearing time, for example the timestamp recorded by the experiment. Reused output keeps its original observation time. A receipt's recording time must not impersonate a new check execution.

Review edits, selected-file changes and changed contracts can invalidate existing receipts. Preserve old receipts and add applicable new evidence; do not delete an inconvenient latest result or silently switch to old green. Requalifying a changed record does not always require rerunning an unchanged experiment, provided its source/environment/freshness/permission and criterion still support reuse.

## 7. Run the required final gate

```text
python runtime/principles-2.0.0/workflow.py check --root "PROJECT_ROOT" --task TASK_ID
```

The final workflow command is mandatory before task completion and applicable acceptance/release boundaries. Calling only the lower-level collector's `check` omits the required workflow/review validation. Preserve nonzero status:

| Exit | Interpretation |
| --- | --- |
| 0 | Selected current declared checks and required record/review shape pass. |
| 1 | Failure or malformed input. |
| 2 | Unknown, unresolved, missing, stale, future, changed or otherwise insufficient evidence. |

The checker neither runs project tests nor establishes semantic adequacy, execution authenticity, target permission, current deployment exposure, containment, reporting acceptance or absence of vulnerabilities. See [verification](VERIFICATION.md).

## 8. Integrate and hand over

Keep the project's existing meaningful checks. Add the required final gate to its actual acceptance command and preserve its exit code. For example, a project command should stop on its own failed tests and should also fail if `workflow.py check` returns nonzero. Do not add a second scheduler, CI system or hook solely to adopt the method.

The [complete walkthrough](examples/WALKTHROUGH.md) shows concrete organization/task/review records and actual capture commands. Its explicit `--organisation` option identifies the current roster; the fixed adapter runs organization check → real synthetic project check → workflow gate, stopping on nonzero. Real projects must use their own actual roster and project checks. Its [fixed example adapter](examples/accept.py) runs the synthetic project check and then the explicit task's gate, preserving nonzero exits without creating judgments or receipts. Adapt the pattern to the actual project checks; do not use the demo check to certify unrelated work.

Record the real integration once. Subsequent work selects its actual current task and reuses the integration. Do not reuse a completed task to certify new work or repeat onboarding/full scans without a new decision need.

At completion, report what changed or was learned, exact source/evidence scope, uncertainty, findings status, effects/cleanup, required owner action and next safe step. Separate completed investigation, verified finding, current affectedness, submitted report and accepted remediation. Retain resumable state if interrupted; missing replies do not establish completion.


## Resume without hiding change

| Observed state | Next safe action |
| --- | --- |
| Begin only partly created records | Inspect actual files/errors. Preserve them; complete the supported resume path or use a linked task. Do not erase the partial start to invent a clean history. |
| Draft task/review, no accepted evidence | Populate actual facts and continue the same admitted question; unresolved records remain unknown. |
| Same brief, source, authority and valid current evidence | Resume from the next unfinished step. Reuse outputs with original observation times. |
| Selected source/notes/review changed | Assess impact; rerun affected checks or justify reuse, then record current bindings. Preserve the old results. |
| Frozen brief changed materially | Retain the predecessor; create a linked new task and reassess required permission. A new receipt cannot repair a changed frozen brief. |
| Latest result is failure/unknown or evidence is corrupt | Investigate that state; never select old green as a substitute. Continue independent useful work if allowed. |
| External action might have completed | Reconcile at the actual provider/boundary before retrying. No inference from a lost response. |
| Permission expired/revoked or resource cap reached | Stop the dependent branch, retain evidence and request only the genuinely needed decision/access. |

A resumed conversation is not proof of a live worker or current authority. Use the short notes handoff and actual files; do not repeat an unchanged full scan solely because the session changed.
