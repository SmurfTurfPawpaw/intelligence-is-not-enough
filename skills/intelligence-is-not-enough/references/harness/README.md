# Intelligence Is Not Enough

### A Harness for Autonomous Discovery

**Give an AI agent a research method, not just a bigger prompt.**

Intelligence Is Not Enough is a model-agnostic workflow harness for autonomous, evidence-led security research. It combines exploratory freedom with clear ownership, useful experiments, durable evidence and an executable acceptance workflow.

Use it with a hosted or open-weight model and an agent host that can read project files and run tools. The package requires no model subscription or API key to try its local examples. It supplies no model content filter or provider-specific refusal policy.

**Release 2.4.0 · Python 3.12+ · standard library · MIT**

## Try it locally

```sh
git clone https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough.git
cd intelligence-is-not-enough
python --version
python examples/ledger.py
python examples/explore.py
python tools/orchestration.py check --record examples/organisation-compact.json
```

Use your platform's Python 3.12+ command if it is named differently. No `pip install` is needed for these examples.

- **Ledger:** first identifier accepted, repeated identifier refused, distinct identifier accepted.
- **Exploration:** ordinary code explores a bounded synthetic action space, detects an intentionally planted retry defect and identifies a reject-all apparatus as inconclusive. The overall calibration result is `pass`; that does not mean every implementation passed.
- **Organization:** checks the declared eight-team structure. The example is fictional; it does not launch workers or certify your actual project.

These commands use contained synthetic data. They do not contact a target, move money or call a model. Run `python examples/explore.py --max-cases 17` to see an intentionally incomplete search return exit2.

For the complete begin → task → experiment → review → evidence receipt → acceptance path, follow [the worked walkthrough](examples/WALKTHROUGH.md). Expected output in a document is never a substitute for an actual observation.

Try the offline [discovery example](DISCOVERY.md) with `python tools/discovery.py report --record examples/discovery.json --as-of 2030-01-01T12:30:00Z`. Exit2 is expected: it preserves one deliberately unresolved consumer path. No model or network is involved.

## What you get

- **Operating principles:** first principles, system design, synchronization, recovery and accountable work.
- **Eight standing teams:** Coordination, Systems, Discovery, Engineering, Validation, Knowledge, Operations and Methods. Responsibilities are mandatory; eight permanently running models are not.
- **Beyond Human Patience:** methods that make tedious, lengthy or compute-heavy investigations practical with AI-assisted reasoning and deterministic execution.
- **Discovery loop:** source lineage, explicit aliases, inbound/outbound consumer paths and an offline next-action report. See [discovery](DISCOVERY.md).
- **Tool guidance:** selection, usage, official links, evidence requirements and limitations.
- **Durable work records:** a stable investigation brief, evolving notes, work packets, findings and handoffs.
- **Required local checks:** declared organization consistency and a workflow gate that binds selected evidence to current source and attributed review.

## Use it with an agent

**Codex: install once, apply across projects.** Obtain this reviewed release and run `python install.py --scope user`. It installs the skill and compatible runtime, preserves unrelated global instructions and adds standing G01–G12 rules. Start a new Codex run/session; ordinary project work then needs no skill invocation or reminder. See the [full installation guide](https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough/blob/v2.4.0/CODEX-SKILL.md). Copying the skill alone does not perform full setup.

Start in a directory you control. Have your agent read [AGENTS.md](AGENTS.md), [the principles](base/PRINCIPLES-2.0.1.md) and [orchestration](ORCHESTRATION.md), then give it a useful objective and the actual project boundary. For example:

> Follow this project's AGENTS.md and linked principles. Investigate the supplied local synthetic fixture. Establish the required team ownership, define useful acceptance, preserve observations and controls, and use the required workflow before declaring completion. Keep evolving hypotheses separate from the frozen brief. Do not infer permission for a different asset or effect.

The host must actually load the instructions, expose the selected tools and preserve work state. Markdown alone does not create an agent runtime. [Model portability](MODEL-PORTABILITY.md) covers hosted and open-weight integrations, including optional Ollama/vLLM references and an observable host contract. No particular model has been benchmarked or installed by this repository.

### In an existing project

1. Retain the complete package under a versioned path, such as `docs/red-team/releases/2.4.0/`.
2. Merge the managed instructions into the project's root `AGENTS.md`, preserving its existing rules. Update copied relative links to their retained locations.
3. Map current owners and records into the required organization. Reuse existing work logs and evidence storage instead of creating a competing source of truth.
4. Connect the organization check and required workflow gate to the project's **real acceptance command**, preserving nonzero exits. Use the actual task/root and retained runtime paths.

The [adoption guide](ADOPTION.md) preserves the complete setup, research-unit, cost, versioning and publication notes. [WORKFLOW.md](WORKFLOW.md) gives the exact commands. Keep published/pinned files immutable; do not overwrite an older version with different bytes.

## How the work flows

```text
Useful objective → bounded work packet → question or hypothesis
        → discriminating experiment → observations and controls
        → challenge and review → source-bound evidence → accepted result
```

Agents may invent instruments, revise hypotheses, pursue unexpected in-scope connections and disprove the starting theory. Use models where semantic reasoning helps; keep repetitive generation, execution and shrinking in deterministic code when practical. Track accepted outcomes and correction cost, not payload volume or the appearance of activity.

Actual scope, tool permissions, resource budgets and consequential approvals come from the operator/project and host. A task name, generated policy or passing checker creates none of those facts.

## Read by topic

| Guide | Use it for |
| --- | --- |
| [Orchestration](ORCHESTRATION.md) | Required teams, owners, hierarchy, parallel work, shared state and recovery. |
| [Beyond Human Patience](AI-NATIVE.md) | Semantic variants, long sequences, differential testing, generated tools and formal methods. |
| [Discovery](DISCOVERY.md) | Changed-source intake, qualified blast radius and cheap deterministic requalification. |
| [Workflow](WORKFLOW.md) | Begin, define, investigate, review, record receipts and complete the required gate. |
| [Complete example](examples/WALKTHROUGH.md) | Run the whole workflow in a disposable local copy. |
| [Adoption](ADOPTION.md) | Detailed setup, research records, cost, compatibility and publication notes. |
| [Architecture](ARCHITECTURE.md) | What the workflow package and the agent host each provide. |
| [Model portability](MODEL-PORTABILITY.md) | Hosted/open-weight host and tool-event integration. |
| [Tools](TOOLS.md) | Capability selection, usage and official documentation. |
| [Host tools](HOST-TOOLS.md) | Conditional agent/MCP adapters and routing. |
| [Verification](VERIFICATION.md) | Checked claims, failure handling and explicit limits. |
| [Coverage](COVERAGE.md) | Links between principles, research rules and required review. |
| [Work-packet template](templates/WORK-PACKET.md) | A concrete assignment, submission and review contract. |
| [Investigation template](templates/INVESTIGATION.md) | A useful question, boundaries and acceptance before material work. |
| [Notes template](templates/NOTES.md) | Evolving hypotheses, experiments, decisions and resumable state. |
| [Engagement template](templates/ENGAGEMENT.md) | Actual authority and effect boundaries. |
| [Finding template](templates/FINDING.md) | Reproduction, controls, impact, affectedness and reporting state. |

## Verification has limits

The checker tests selected record shape and evidence/source bindings. It does not authenticate execution or identity, decide whether an experiment is insightful, prove target permission, establish live affectedness, guarantee containment or show that no vulnerabilities exist.

This repository is a reusable workflow and local checker—not an autonomous worker service, sandbox, scheduler or production monitor. A configured host supplies actual execution. [Verification](VERIFICATION.md) explains positive, negative and recovery cases and how to maintain the checker.

## Versions and integrity

The public distribution is **2.4.0**. Its operating profile remains **2.0.0**, principles **2.0.1**, workflow **2.0.0**, and core/task schema **1.0.0**. [PROFILE.json](PROFILE.json) records the separate identities. This release adds offline discovery intake and revision-bound consumer tracing, including synthetic examples and tested failure paths. Full automatic user setup remains available. The principles, workflow runtime and organization checker remain unchanged; the discovery record has its own1.0.0 schema.

[release-manifest.json](https://github.com/SmurfTurfPawpaw/intelligence-is-not-enough/blob/v2.4.0/release-manifest.json) lists public payload hashes. A checksum detects changes relative to that manifest; it is not a distributor signature or authenticated execution record. The manifest excludes itself from its file list to avoid a circular self-hash. The skill has its own offline manifest.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep examples synthetic. Do not upload real engagement records, private chats, credentials, captures or unpublished findings to issues, pull requests or public logs.

## License

Original repository code and guidance are available under the [MIT License](LICENSE). Referenced external tools, models and services retain their own licenses and access requirements.
