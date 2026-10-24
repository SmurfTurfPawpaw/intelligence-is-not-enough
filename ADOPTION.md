# Adoption and operating notes

**A Harness for Autonomous Discovery**

Red-team edition: a practical method for autonomous, evidence-led security research.

Security research begins with uncertainty. A useful agent must be able to question the starting theory, invent experiments, combine tools and pursue unexpected interactions. It also needs a clear research objective, actual permission, trustworthy records and a way to distinguish a promising idea from demonstrated impact.

This harness provides those working rules, reusable templates, tool guidance and a local verification workflow. It supports source review, owned-lab research and specifically authorized live validation. The operating method gives substantial freedom over discovery while keeping the actual asset, identity, data, effect and resource boundaries explicit.

The package is model-agnostic, including open-weight/local deployments. It contains no model content filter or provider-specific refusal policy. [Model portability](MODEL-PORTABILITY.md) explains the host contract and separates model policy, operator-configured execution and research-quality verification. No hosted AI subscription is required.

**Release:** 2.1.0 · **Profile contract:** 2.0.0 · **Principles:** 2.0.1 · **Workflow:** 2.0.0 · **Runtime requirement:** Python 3.12 or newer. The workflow uses the Python standard library and performs no network request, model call, project test or global installation. Optional research tools have their own requirements.

For the distinction between a model, agent, workflow harness and execution runtime, read [the architecture](ARCHITECTURE.md). This package provides the workflow layer; an actual agent host supplies the model/tool loop and configured controls.

## Orchestrate the work

Profile2.0.0 requires eight accountable teams for each admitted material project. Read [orchestration](ORCHESTRATION.md) for their contracts, hierarchy, activation, work packets, shared state, verification, learning and cost. Owners can cover several responsibilities; no eight-process service is implied. Pure conversation creates no artificial project and later small tasks reuse existing organization records.

## Start here

1. Read [the operating principles](base/PRINCIPLES-2.0.1.md) and [agent instructions](AGENTS.md). They define the required behavior and the freedom to explore.
2. Establish [the eight-team organization](ORCHESTRATION.md), then follow [the working method](WORKFLOW.md) to establish scope, begin an investigation, retain evidence and complete its required gate.
3. Follow [the complete synthetic walkthrough](examples/WALKTHROUGH.md), including real capture, task/review records, receipts and the acceptance command. [The examples](examples/README.md) also demonstrate bounded sequence exploration and a broken-apparatus control.
4. Read [Beyond Human Patience](AI-NATIVE.md) for AI-native investigations that combine model reasoning with deterministic experimentation. Consult [the tool guide](TOOLS.md) when choosing an instrument, [agent integrations](HOST-TOOLS.md) when using available capabilities, and [verification](VERIFICATION.md) when interpreting results or checking the package.

No previous project, conversation or globally installed harness is required. Extract the complete package into a directory you control. From that directory, confirm the interpreter and run the contained example:

```text
python --version
python runtime/principles-2.0.0/workflow.py --help
python examples/ledger.py
```

Use your platform's Python 3.12+ command if it is named differently. The example operates on an in-memory synthetic set; its expected result is first identifier accepted, repeated identifier refused, different identifier accepted. Expected output is explained in the example and must remain distinct from an observation you actually record.

## What the harness contains

| File or directory | Purpose |
| --- | --- |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Required teams, owners, hierarchy, packets, synchronization, independent challenge and recovery. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Components, responsibilities, data flow and actual enforcement boundaries. |
| [Beyond Human Patience](AI-NATIVE.md) | Semantic variant search, sequence/relationship exploration, generated tools, formal methods and cost-aware research. |
| [MODEL-PORTABILITY.md](MODEL-PORTABILITY.md) | Open-weight/hosted integration, tool-event mapping and model-policy separation. |
| [AGENTS.md](AGENTS.md) | Project instructions for the research agent. |
| [Base principles](base/PRINCIPLES-2.0.1.md) | First principles, system boundaries, synchronization, evidence, recovery, teams, efficiency and useful outcomes. |
| [WORKFLOW.md](WORKFLOW.md) | Complete begin → investigate → review → receipt → required check procedure. |
| [TOOLS.md](TOOLS.md) | Tool selection, practical usage, official links, evidence and limitations. |
| [HOST-TOOLS.md](HOST-TOOLS.md) | Conditional agent/MCP adapters and permission-preserving routing. |
| [Templates](templates/INVESTIGATION.md) | Engagement, investigation, evolving notes and finding records. |
| [Examples](examples/README.md) | Synthetic fixture, brief and illustrative notes. |
| [VERIFICATION.md](VERIFICATION.md) | What to verify, how the gate fails, package checks and interpretation limits. |
| [COVERAGE.md](COVERAGE.md) | Connection between the principles, research rules and required review. |
| [Runtime](runtime/principles-2.0.0/README.md) | Local checker source, supporting schema/example and software tests. |
| [PROFILE.json](PROFILE.json) | Component versions, paths and required runtime identities. |

Keep engagement records and sensitive evidence in the project's approved private storage, separate from publicly shared guidance.

## Adopt it in a project

For a new research project, the extracted package can be the initial layout. Keep investigation records outside immutable guidance/runtime files and use the project's actual root in every command.

For an existing project, retain the complete package under a directory such as `docs/red-team/releases/2.1.0/`. Merge the managed block from `AGENTS.md` into the project's root agent instructions, preserving local rules. Rewrite copied relative links to the actual retained locations, including:

```text
docs/red-team/releases/2.1.0/base/PRINCIPLES-2.0.1.md
docs/red-team/releases/2.1.0/templates/INVESTIGATION.md
docs/red-team/releases/2.1.0/README.md
docs/red-team/releases/2.1.0/TOOLS.md
docs/red-team/releases/2.1.0/AI-NATIVE.md
docs/red-team/releases/2.1.0/MODEL-PORTABILITY.md
docs/red-team/releases/2.1.0/ORCHESTRATION.md
```

The agent performs the authorized routine adoption: reads the base, identifies the real root/current task, reuses existing records/checks and connects the required final gate to the actual acceptance command. It must preserve the gate's nonzero exit. A setup marker or an instruction file alone does not prove the gate ran.

Global instructions are optional. If you already maintain equivalent global principles, avoid duplicating their full text; retain the domain rules and required references. In Codex, guidance discovery and configured size limits matter. Start a new session after installing project guidance and use the [official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) to understand its discovery rules. An agent's summary of loaded instructions is a useful diagnostic, not authenticated loader evidence.

## The research unit

A research unit has a useful question or broad authorized objective, a fixed boundary and predeclared acceptance. It can contain many related experiments and evolving hypotheses. Its objective may be “characterize the trust boundaries of this owned service”; it does not need a predetermined vulnerability list.

Keep these four records as separate files or equivalent existing records with clear ownership:

- [Engagement](templates/ENGAGEMENT.md): actual authority, assets, identities, exclusions, windows, permitted effects, limits and recovery. A completed template grants no authority.
- [Investigation](templates/INVESTIGATION.md): the frozen task question/boundary, sources, acceptance and stopping rules.
- [Notes](templates/NOTES.md): evolving hypotheses, experiments, observations, concise decisions and evidence references.
- [Finding](templates/FINDING.md): one useful candidate or supported root cause, reproduction, controls, affectedness, impact and reporting state.

The checker freezes the complete investigation brief file at begin. Evolving notes must be separate. A new experiment within the same objective/boundaries can proceed without a new task. A material change in objective, assets, identity, effects, risk envelope or acceptance requires a linked new task and any actual permission that change needs. Preserve previous work and unresolved results.

## Freedom and responsibility

Agents may invent local tools, change experiment order, pursue unexpected in-scope paths, compare explanations and falsify the original theory. A catalogue entry is never a requirement to run that product, and absence from a catalogue is not a ban on another technique.

The actual permission boundary, aggregate budgets, data protection, evidence honesty and required acceptance remain effective. A new severity estimate can be recorded in notes without another approval ceremony; the next proposed action must still fit its admitted effect/risk envelope and stop conditions. Actual tool, broker and platform protocols apply to that action.

## Verification has a specific meaning

The required local gate checks the selected task records, declared principle judgments and current evidence bindings. It does not authenticate execution, establish permission, prove a vulnerability, inspect every component or guarantee no vulnerabilities exist. Reviewers remain responsible for the adequacy of the reasoning and evidence.

A completed investigation may produce a supported finding, a useful falsification or a bounded inconclusive result if that outcome satisfies its predeclared research criteria. Missing required experiments, permission or reliable evidence remain incomplete. Never rewrite acceptance after failure simply to obtain a passing result.

## Cost and maintenance

Prefer existing tools, deterministic checks and one investigator. Use bounded specialists where independent expertise or challenge adds value. Reuse observations under their actual source/configuration/time/permission conditions. Run broader checks for changed contracts, new failures or a real release requirement; do not repeatedly scan unchanged state.

For planning, a project may initially allocate **0.2–1% of its defined weekly AI allowance** to changed profile routing/review, excluding the research itself. This is a hypothetical starting allocation, not a measured benchmark or token-to-money conversion. Name the denominator, basis and review trigger; use UNKNOWN when the allowance is unknown. Reassess after three accepted investigations or a relevant policy/tool change. The checker itself makes no AI calls.

## Versions and publication

Release2.1.0 adds the public GitHub distribution, quickstart and MIT license for original repository content. The operating contract and executable sources remain unchanged. The naming-only2.0.1 release remains an immutable prior distribution.

Release2.0.1 applies the titles "Intelligence Is Not Enough" and "Beyond Human Patience". The profile operating contract remains2.0.0; this editorial release changes no executable behavior or stable document paths.

Profile2.0.0 adds mandatory organization adoption/checking and an explicit organization-record option in the demo acceptance command; these break the1.3.0 operating contract. Existing completed investigations remain historical. Map current owners/records and wire the organization check before qualifying new material work. Principles2.0.1, workflow2.0.0 and core/schema1.0.0 are unchanged. Profile, principles, workflow and record schemas have separate versions. Treat published contents as immutable. Use a new major version for breaking contracts, minor for compatible additions and patch for compatible corrections; record deployment identity separately where a live service exists. Review compatibility before replacing a pinned component.

Use the file hashes in `release-manifest.json` to detect accidental changes before adoption. A checksum is not a signature or proof of a trusted distributor. Preserve applicable source notices and review unfamiliar code before executing it. References point to external tools and primary documentation; their installation, license, access and permission are separate facts.
