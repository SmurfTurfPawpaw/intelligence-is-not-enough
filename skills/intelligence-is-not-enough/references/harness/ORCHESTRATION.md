# Orchestration

An agent organization needs more than several conversations running at once. It needs an objective, a current model of the system, people or agents accountable for distinct responsibilities, explicit work assignments, reliable evidence and a way to finish. Parallel activity without those connections produces duplication, incompatible changes and impressive-looking status with no accepted result.

This chapter defines the required organization for **each admitted material research project**. It applies to source investigations, owned-lab work, specifically authorized assessments and the engineering needed to support them. It is model-neutral and adds no model content filter or provider-specific refusal policy. The operator's actual engagement and execution facts remain separate from research-quality acceptance.

## 1. The eight teams that must exist

At project admission, the integrator SHALL create or reconcile the following eight team identities in one durable project record. Existing equivalent records can be reused. Each team SHALL have an accountable owner, a state and a useful reason for that state. Registering a team is not evidence that a worker has started.

| Stable ID | Team | Accountable result |
| --- | --- | --- |
| `coordination` | Coordination | A useful objective becomes prioritized, owned work and an integrated result. |
| `systems` | Systems | Workers use a current, source-linked understanding of the affected system. |
| `discovery` | Discovery | The investigation explores meaningful alternatives and unconventional possibilities. |
| `engineering` | Engineering | Instruments and experiments produce reproducible observations. |
| `validation` | Validation | Claims survive appropriate challenge, controls and exact-revision review. |
| `knowledge` | Knowledge | Evidence, negative results, corrections and lessons remain inspectable and reusable. |
| `operations` | Operations | Actual capability, execution state, limits, uncertain effects and recovery are known. |
| `methods` | Methods | The organization improves its approach without wasting effort or hiding gaps. |

**All eight responsibilities are mandatory; eight simultaneous models are not.** One contributor can own several compatible teams. A small project can have one investigator/integrator covering seven responsibilities and a second contributor handling an independent validation when required. A low-impact task may use disclosed self-review where the actual requirements allow it. Independent review cannot be manufactured by changing the author's role label.

A team may be **ready**, **active**, **dormant** or **blocked**. Dormant means no useful work currently needs a worker, with the responsibility and owner retained. Blocked means a real dependency prevents that team's selected contribution. An active declaration identifies assigned work; it does not establish process liveness. Never create ceremonial reports or idle model loops just to keep every team active.

## 2. Team, role, agent, task and tool are different

- A **team** is a stable responsibility and its contract.
- A **role** is a duty a contributor performs, such as investigator, integrator, skeptic or evidence custodian.
- An **actor** identifies the actual contributor: a person, agent session or declared host process. Keep aliases attributable to that contributor.
- An **agent worker** is an actual model/tool execution context. A roster entry does not create it.
- A **task** is a bounded useful outcome with inputs, acceptance, effects, limits and an owner.
- A **tool** executes or observes a particular operation. It is not automatically a supervisor, validator or authority.
- The **host** supplies actual dispatch, processes, tools, persistence and any event subscriptions. This package supplies contracts and local checks, not a running service.

Record team ownership separately from task assignment and observed execution. A person's responsibility for Operations does not mean they ran every command. An agent that generated a report is not automatically the reviewer of that report. A tool returning exit0 is an observation, not an organizational decision.

## 3. Coordination

**Mission:** turn the owner's useful objective into a coherent accepted result while preserving freedom over how to investigate.

**Inputs:** original request, current direction, engagement/brief, actual capabilities, system model, research frontier, previous findings and available capacity. **Owns:** admission, priorities, dependency decisions, assignments, aggregate resource allocation, shared-state ownership, integration and the operator's concise current overview.

**Produces:** the current roster and queue, bounded work packets, attributed decisions, accepted or rejected handoffs and an honest completion report. **Decides:** which eligible work to dispatch, serialize, stop, split, combine or retire. It can resolve competing implementation proposals with an attributed reason; it cannot erase an unresolved required check, manufacture permission or declare its own uncertain evidence conclusive.

**Activation:** project admission, material new direction, changed dependencies, a meaningful failure, a submitted result or a real operator decision. Routine experiments do not need another coordination ceremony. Workers can exchange relevant evidence directly within their packets.

**Acceptance:** each selected outcome has an owner and next action; dependencies and effects fit; integrated artifacts match reviewed revisions; unresolved scope is visible. **Failure to avoid:** becoming a manager that spends every turn summarizing other managers. Coordinate the smallest useful organization and keep the decision path short.

## 4. Systems

**Mission:** give workers a sufficiently accurate model of the whole affected path, without requiring each worker to rediscover it.

**Inputs:** exact source/artifact/configuration identities, authoritative documentation, observed interfaces and contradictory evidence. **Owns:** the source-linked model of input → identity/authority → state → processing → integration → recipient, component contracts, dependency relationships and important assumptions. It does not own a competing copy of raw evidence.

**Produces:** a compact map, claim/source table, unresolved boundaries and task-specific context packets. Each material component needs purpose, owner, inputs/outputs, dependencies and a reconsideration trigger. Distinguish intended architecture, actual code and observed deployment; a diagram cannot substitute for those identities.

**Activation:** a new component, changed interface/configuration, inconsistent consumer, unexplained behavior or a worker that needs a bounded context packet. Reuse unchanged source-bound knowledge rather than remapping the entire project after each experiment.

**Acceptance:** the next investigator can trace the relevant path, locate authority for each important fact and see what is unknown. **Failure to avoid:** a beautiful map detached from actual revisions, or claims that every interface is understood because all boxes have labels.

## 5. Discovery

**Mission:** prevent conventional checklists, the owner's initial hypothesis and the current tool catalogue from becoming a ceiling on discovery.

**Inputs:** characterization observations, system model, patch history, surprising results, research literature and unresolved invariants. **Owns:** competing explanations, unconventional methods, cross-component combinations and the research frontier. It asks what others might have skipped because it was tedious, lengthy, computationally expensive or difficult to connect.

**Produces:** ranked questions, hypotheses, discriminating experiments and instrument proposals. Each useful proposal explains what it could teach, the simpler alternative, expected observation, cost, controls, bounds and stop condition. [Beyond Human Patience](AI-NATIVE.md) offers methods, not a fixed campaign. Discovery may invalidate the initial theory, propose a new abstraction or invent a tool.

**Activation:** initial characterization, contradictory evidence, a saturated search, an untested structural boundary or a meaningful new capability. It is not a permanent idea generator that fills the backlog while nobody can execute it.

**Acceptance:** a proposal becomes a useful admitted experiment, a supported rejection or a documented unresolved path. **Failure to avoid:** rewarding novelty, alert counts or elaborate attack stories instead of information gained. Discovery does not validate its own proposal by asserting confidence.

## 6. Engineering

**Mission:** make the selected experiment real, reproducible and economical.

**Inputs:** admitted packet, exact source/inputs, property or observation contract, relevant controls and actual tool capabilities. **Owns:** assigned instruments, deterministic runners, calibration, permitted execution, reproducible outputs and assigned file changes. It chooses the smallest existing tool or local instrument that answers the question.

**Produces:** reviewed source/query/generator as needed, actual commands and outputs, counters, minimized witnesses, controls, failure records and a revision-bound handoff. The model proposes or interprets; deterministic code normally handles repetitive generation, execution and shrinking. Capture actual retries and failures, not only the successful final output.

**Activation:** an eligible experiment or useful instrument task. **Decision boundary:** it may change implementation or experiment order within the admitted question and effects. A changed oracle, material acceptance condition or effect boundary needs explicit reassessment. Generated code does not approve itself.

**Acceptance:** ordinary success and relevant controls establish apparatus validity; the stated experiment is reproducible at its actual source/configuration; incomplete coverage remains explicit. **Failure to avoid:** treating a reject-all instrument as secure behavior, or quietly changing a test until a candidate appears to pass.

## 7. Validation

**Mission:** try to disprove the strongest claim, not congratulate the investigator.

**Inputs:** immutable submitted revision, original criterion, actual evidence, controls, system path, known limitations and contradictory results. **Owns:** alternative explanations, apparatus validity, reproduction, reachability, scope/affectedness calibration and an attributed technical judgment.

**Produces:** a scoped pass, fail or unknown; actionable findings; reproduction/control evidence when performed; and a statement of what was inspected versus executed. It checks both the target claim and the research apparatus. Agreement between models is not independent execution proof.

**Independence:** where required, the actual reviewer SHALL differ from the implementer/contributors to the claim. Record the real identities or their private identity references and shared assumptions. A different prompt, role name or agent ID representing the same contributor is not enough. Distinct models can still have correlated errors. If the reviewer is unavailable, block that qualification and continue independent useful work.

**Activation:** a material implementation, a consequential candidate finding, an admitted independent-review boundary or a changed exact submission. Do not rerun an unchanged broad suite merely because a new reviewer arrived.

**Acceptance:** the judgment identifies exact subject, scope, evidence, time and limits; failure and unknown remain effective. **Failure to avoid:** reviewing an old commit while a writer continues changing the submission, or letting a fix author silently resolve their own required independent-review finding.

## 8. Knowledge

**Mission:** ensure that the useful result survives the worker and the conversation.

**Inputs:** original input, observations, source references, events, failed attempts, reviews and corrections. **Owns:** evidence indexing, provenance, contradictions, retention references, resumable handoffs and reconsiderable learning. Existing captures and the work log remain authoritative; Knowledge links them rather than creating another recorder with conflicting facts.

**Produces:** a compact current evidence index, an accurate handoff and proposed lessons with observation, context, cause, change, applicability, uncertainty and reconsideration conditions. Preserve original wording separately from refinement. A routine pass is execution evidence; it does not automatically justify a permanent instruction.

**Learning path:** capture candidate → deduplicate against applicable lessons → validate the behavior change → review/sanitize → adopt at the intended scope → apply on a later explicit plan → supersede or revert when contradicted. A candidate lesson never activates itself or silently changes a running packet. Keep private details outside reusable guidance.

**Activation:** material evidence/review/change, interruption, closeout or a correction that could alter future work. **Acceptance:** another contributor can resume without replaying the entire chat and can distinguish observation, interpretation and untested possibility. **Failure to avoid:** preserving every transcript forever but losing the exact artifact, negative control or decision that matters.

## 9. Operations

**Mission:** know whether the selected work can actually execute and how to stop, reconcile or recover it.

**Inputs:** actual host/tool availability, admitted effects, source/runtime configuration, resource limits, process/provider observations and recovery baseline. **Owns:** capability readiness, execution observation, aggregate limits, output ownership, pending effects, recovery obligations and stop coordination. Workers may execute their permitted experiments directly; Operations need not proxy every command.

**Produces:** actual readiness/unknown blockers, execution references, remaining capacity, retained failure evidence and a recovery result or next safe action. Separate task state, runner liveness, freshness, result and coverage. A recent journal entry does not prove a process is alive; a healthy process does not prove the experiment succeeded.

**Activation:** dispatch, changed capability, a failed or interrupted operation, uncertain completion, drift, exhausted limit or real recovery work. Prefer actual host events and bounded reconciliation; create no polling model just to discover that nothing changed.

**Acceptance:** the claimed capability was observed at the relevant boundary; incomplete effects and recovery remain visible; another worker will not repeat an uncertain operation blindly. **Failure to avoid:** assuming a worktree is a security sandbox, assuming a timeout killed every child, or restoring code while ignoring already-completed external effects. The actual host controls and permissions remain deployment concerns, not model content filters.

## 10. Methods

**Mission:** challenge how the organization thinks and works, including the orchestrator itself.

**Inputs:** original objective, accepted and rejected results, correction patterns, actual resource counters, bottlenecks, duplicated work and user feedback. **Owns:** bounded meta-analysis of process, model routing, experiment design, context retrieval, coordination cost and useful future improvements.

**Produces:** a concrete proposed change, a simpler alternative, expected benefit, evidence, uncertainty, compatibility impact and evaluation/stop plan. Ask: do we need this component? Can an existing tool do it? Is this an artifact of the model's habits? Are we optimizing the customer's decision or a vanity metric? Could different representation, stronger invariants or a generated instrument remove repeated effort?

**Activation:** an actual bottleneck, repeated correction, novel task class, disproportionate cost or an agreed project checkpoint. It does not review every shell command. It may challenge another team's conclusion but cannot rewrite facts, promote its own policy or recursively spawn methods teams without a bounded need.

**Acceptance:** an improvement is adopted through the normal requirements/review path or rejected with a reusable reason. Measure later results before claiming savings. **Failure to avoid:** permanent committees, optimization without a baseline or eight models producing variations of the same summary.

## 11. Hierarchy and decision rights

```text
Owner / sponsor — useful objective and retained consequential decisions
                         ↓
Integrator / Coordination — current priorities, packets and accepted integration
        ├── Systems ↔ Discovery ↔ Engineering ↔ Validation
        ├── Knowledge — evidence, handoff and proposed learning
        ├── Operations — actual readiness, effects and recovery
        └── Methods — bounded challenge of approach and cost
```

This is a responsibility map, not evidence of eight processes or a requirement for eight approval meetings. Each team has one accountable owner who may delegate a bounded subtask. One integrator decides how accepted outputs fit together. Teams can communicate directly through the existing message/work record; the integrator need not repeat every conversation.

Any contributor can flag a contradiction, failed invariant or reached boundary. The responsible owner resolves it with evidence. If Discovery and Validation disagree, compare hypotheses and choose a discriminating experiment. If Engineering and Systems disagree, check the actual source/contract. If the dispute changes a material requirement or retained owner decision, make that decision explicit. Do not settle technical truth by majority vote or suppress a dissent to maintain momentum.

Review, integration, deployment and external disclosure are separate transitions. A validated technical result does not automatically authorize publication. Reuse actual standing authority instead of asking for the same decision at every handoff.

## 12. The minimum durable record

Use one current organization record referencing existing project facts. [The compact example](examples/organisation-compact.json) and [parallel example](examples/organisation-parallel.json) show the format. Keep actual sensitive identities/evidence privately; published examples use synthetic references.

The record contains profile/project/revision, integrator, shared-state writer, real actor mappings, the eight team owners/states, current work packets and references to the brief, authority, evidence index and event log. It is a bounded current view, not a replacement for immutable history. An existing database or board can project equivalent records; do not create a parallel source of truth.

Each assignment SHALL carry the [work-packet contract](templates/WORK-PACKET.md): requester, responsible team/actor, objective, exact inputs/revisions, dependencies, permitted effects, owned outputs, acceptance, limits, stop/recovery rules and integrator. Before submission, retain the actual handoff: packet revision, submitted subject identity, artifacts/evidence, observations, limitations, effects/recovery and next action.

The checker reads declarations, not arbitrary referenced files. Source and evidence-file identity remain the existing principles collector's job. A structurally valid record does not establish that its referenced artifacts exist or its claims are true.

## 13. Assignment, priority and parallel work

Use the smallest useful lifecycle:

`proposed → admitted → assigned → started → submitted → reviewed → integrated`

Also retain `blocked`, `interrupted`, `cancelled` and `superseded`, with a reason and next action. “Started” records a work event; it is not a liveness promise. “Integrated” describes the accepted internal output, not deployment, disclosure or a successful customer outcome.

Priorities SHALL follow current value, urgency, impact, dependencies, uncertainty and available capacity. Keep structural criticality distinct from current urgency. A shared evidence path can be important yet have no urgent change; a small blocker can deserve immediate attention. Record why an item moved and what would change the decision. Use qualitative levels or a project-defined scoring model; do not invent precise business value.

Dispatch only ready work: dependencies resolved, required facts/authority present, owner available, outputs unclaimed by another live/uncertain assignment and resources sufficient. Bound concurrency by actual host capacity and aggregate project limits. A started writer with declared outputs must retain its output claim; declaring it released is contradictory. Overlapping output ownership must be serialized or explicitly integrated through one writer. A worktree isolates changes, not necessarily credentials, shared Git state, processes or network.

Share a concise context packet, not the whole repository or every past conversation. Parallelize genuinely independent questions—for example source-path analysis and a separate synthetic test design—then integrate at exact input/submission identities. Two workers rewriting the same file are a coordination failure even if both produce good code.

## 14. Shared state, events and resumption

Declare one authority for each changing fact. One named writer updates the shared organization/queue record; workers own only their assigned outputs and submit proposals/events to that writer. Existing host or database transaction rules remain effective. No record checker creates a distributed lock.

Lifecycle events should include event ID, project/task, packet revision, actor, kind, observed/recorded times, previous state/head or equivalent expected revision, evidence reference and concise reason. Group routine related steps. Append corrections rather than rewriting failures. Do not log private chain-of-thought or unnecessary secrets.

Prefer source-triggered notifications where the host supports them. Consumers reconcile the actual record revision after a gap or reconnect. Ignore an exact duplicate only after comparing its identity and content; a reused ID with changed content is a conflict. Do not let a late event move a newer task backward silently. Notifications are hints to reconcile, not permission to rerun an action.

Before resuming, Operations and the assignee reconcile packet/source revisions, latest contrary evidence, output claims, remaining budget and pending effects. If completion is uncertain, inspect the actual execution/provider boundary before retrying. Missing replies and old process IDs do not prove completion. Preserve uncertain output claims until their owner has reconciled them; changing a task label must not free a possibly active writer.

No mechanism here guarantees exactly-once effects. Use the real provider's idempotency/correlation facilities where applicable and reconcile uncertain completion. A synthetic interrupted/resumed record demonstrates state handling, not a real-world no-duplicate guarantee.

## 15. A practical research cycle

1. Coordination records a useful question, the standing boundary, all eight teams and owners. Operations checks actual capabilities; Systems supplies a compact relevant map. Other duties can remain dormant.
2. Discovery proposes two distinct explanations and the cheapest discriminator. Engineering calibrates a small instrument. A failed calibration is retained; it does not become a negative target result.
3. Engineering submits an exact source/trace revision. Knowledge indexes it. Validation challenges the oracle, control and claimed scope, then returns a bound judgment. A changed source needs an updated submission and applicable review.
4. If a worker disconnects, the integrator records interruption and retains uncertain output claims. Operations reconciles the actual attempt. It resumes the unfinished portion or submits the retained completed result; it does not repeat a possibly completed effect just to generate a fresh status.
5. Coordination integrates the accepted result and leaves blocked hypotheses explicit. Knowledge prepares a short handoff. Methods reviews only a real correction or cost problem and proposes a bounded improvement.
6. Run the selected project checks, the organization record check and the required principles workflow gate. Finish when the useful criteria are met; do not create work merely because a team is dormant.

The [parallel example](examples/organisation-parallel.json) includes an interrupted declaration, a submitted revision and a distinct reviewer. It is illustrative state, not evidence that those workers ran. Actual research needs actual artifacts and receipts.

## 16. Required organization check

From the package root:

```text
python tools/orchestration.py check --record examples/organisation-compact.json
python tools/orchestration.py check --record examples/organisation-parallel.json
```

For a material project, run the check against its **actual** current organization record and retain the output as an ordinary required acceptance check. Select that record, relevant packet/handoff artifacts and this checker source in the existing principles task. A fictional example is not evidence for your real organization.

The standard-library checker checks fixed team coverage, identities/references, required packet fields, dependency cycles, declared held-output conflicts, stale submitted/review identities and obvious required self-review. Exit0 means selected structural declarations are consistent; exit1 means invalid/conflicting/failed declarations; exit2 means unresolved declarations. It runs no agent, tool, model or network request and does not change its input record. Optional `--output NEW_EVIDENCE_PATH` exclusively saves the actual result, observation time and record/checker hashes; existing evidence is never overwritten.

It cannot authenticate people, detect aliases, establish genuine independence, observe actual locks/processes, judge permission, verify artifact contents or prove a useful result. The required [workflow gate](WORKFLOW.md) still binds actual selected evidence and review. The [demo acceptance adapter](examples/accept.py) shows the order: organization check → actual project check → required workflow gate, preserving nonzero exits.

Output names use a conservative portable lexical form: root-relative forward-slash paths, case-folded conflict comparison, no control characters, reserved Windows device names or trailing-dot/space components. This catches common naming aliases without accessing output files. It does not resolve symlinks, hardlinks, short names, Unicode filesystem normalization or all host aliases; actual workspace ownership and filesystem reconciliation remain Operations' responsibility. Handoff packet revisions must be actual positive integers, not booleans or a different packet's number.

## 17. Adoption, cost and retirement

Profile2.0.0 introduces this required organization contract; it is a breaking change from1.3.0. Keep principles2.0.1, workflow2.0.0 and core/schema1.0.0 separately pinned. Existing completed work remains historical; do not rewrite it as if the new roster/check ran previously.

On adoption, map existing owners/records into the eight responsibilities, record gaps, connect the organization check to actual acceptance and select the current records as subjects. Small later tasks reuse the organization; pure conversation needs no manufactured team record. A migration that changes real permission, storage or effects needs its own actual assessment.

Estimate recurring guidance/routing maintenance as a range of the project's defined weekly AI allowance, with denominator, assumptions and review trigger. An initial0.2–1% allocation for changed profile/orchestration maintenance is hypothetical and excludes investigations; use UNKNOWN if the denominator is absent. This is one shared maintenance estimate, not eight percentages to add. Measure actual model usage, deterministic compute and coordination separately; do not invent token-to-money or human-hour conversions.

Do not run a model for each heartbeat, status redraw or unchanged roster. Deterministic checks, source-triggered updates and bounded retrieval should do that work. Stop workers when their packet is accepted, superseded, blocked pending a real dependency or no longer useful. Preserve required evidence and reconcile effects before releasing outputs. Retire a project only after an honest final state and recovery handoff; a closed tab is not a completed organization.
