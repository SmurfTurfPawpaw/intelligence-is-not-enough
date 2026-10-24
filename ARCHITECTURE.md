# What makes this a harness?

A model generates decisions or text. An agent uses a model to pursue a task through tools. A harness is the surrounding structure that supplies context, capabilities, state, feedback and a working loop, so the agent can do useful work repeatedly rather than depend on a single prompt.

The word covers several layers. This package is a **portable workflow harness**: it provides instructions, research records, tool-selection guidance and an executable acceptance gate. It is used inside an agent host such as Codex. It does not itself contain a model, tool-execution loop, sandbox, credential broker or scheduler. OpenAI's [Codex platform description](https://developers.openai.com/blog/codex-as-a-platform) explains the broader runtime role around the model.

The host can also use an open-weight model. [Model portability](MODEL-PORTABILITY.md) describes a provider-neutral adapter contract. The package contains no content filter or model refusal policy; those are distinct from source/evidence integrity and the operator's actual execution permissions.

## Components and responsibilities

| Component | Supplies | Does not establish |
| --- | --- | --- |
| [Principles](base/PRINCIPLES-2.0.1.md) and [research rules](AGENTS.md) | Outcome, first principles, exploratory freedom, permission/evidence/recovery obligations | Guaranteed instruction compliance or target permission |
| [Brief and notes](templates/INVESTIGATION.md) | Stable task boundary, evolving questions, observations, decisions and handoff | Authenticated execution or a continuously running researcher |
| [Discovery and consumer paths](DISCOVERY.md) | Offline source lineage, explicit root-cause grouping, revision-bound graph projection and next questions | Automatic source collection, verified exploitability, deployment impact or a running intelligence service |
| [Beyond Human Patience](AI-NATIVE.md) and [tool guide](TOOLS.md) | Ways to select/invent experiments and instruments | Installation, containment, availability or authority to run a tool |
| Existing project runner and [example adapter](examples/accept.py) | Actual selected checks followed by the required gate | Automatic technical judgment or independent review |
| Bundled [workflow runtime](runtime/principles-2.0.0/README.md) | Start/brief identity, review/receipt shape and selected current evidence bindings | Semantic truth, complete coverage, permission or sandboxing |
| Configured agent host | Actual model/tool loop, available tools, session and any configured access controls | Authorization beyond the owner's actual scope |
| Integrator and authorized owner | Interpretation, consequential approval, accepted scope and handover | Freedom to bypass higher-priority platform or target restrictions |

## The useful path

```text
Owner's original question + actual engagement authority
                    ↓
Frozen brief / task contract ──→ required begin record
                    ↓
Agent ↔ scoped tools / deterministic experiments
                    ↓
Evolving notes + private evidence + revised hypotheses
                    ↓
Final selected source/notes + attributed review
                    ↓
Actual receipts → required workflow check → honest handover
```

Tool responses and retrieved documents enter as evidence, never authority. Source-triggered notifications or subscriptions can help a host notice changes, but the receiver must reconcile revision and missed updates. This package starts no subscription or background service. Changed selected bytes can invalidate a receipt even if a UI still displays an old passing result.

## Why an instruction file alone is insufficient

“Be careful and investigate creatively” is guidance. It becomes an operational method when the agent also has an explicit task boundary, usable tools, durable state, controls, evidence and a completion gate connected to the real acceptance command. The [worked example](examples/README.md) exercises that path. The [resume table](WORKFLOW.md) explains how to continue after interruption without erasing drift or failure.

The gate is enforceable **where it is actually invoked and its exit code is respected**. It cannot intercept unrelated tools, authenticate editable records or force a host to obey prose. A real deployment needs its own configured execution controls. Do not mistake the workflow's pass for a security sandbox or an independent proof of the research conclusion.


## Organization

[The orchestration contract](ORCHESTRATION.md) assigns eight standing responsibilities without requiring eight processes. A separate read-only record checker validates declared team/task/output/review consistency. Actual host dispatch, genuine independence, liveness, file locks and effect reconciliation remain separate. The ordinary organization check is wired before project checks and the unchanged required workflow gate.
