# Beyond Human Patience

**AI-native security research**

AI should change which investigations are practical, not merely write a conventional checklist faster. A person may abandon a promising direction because it involves reading hundreds of related implementations, maintaining many competing explanations, constructing a test instrument, or exploring a tedious sequence space. An agent can help make that work economical enough to attempt.

Here, **AI-native** means designing the investigation around an agent's ability to propose, connect, program and revise. **AI-amplified** means an established method becomes practical at a different scale or cost. Neither term means that a human could never invent the method. Novelty and advantage must be demonstrated in the particular setting; fluent output and a large number of tests do not establish either.

This chapter supplies methods to select and combine, not a mandatory campaign. Use the [research rules](AGENTS.md), [workflow](WORKFLOW.md), [tool guide](TOOLS.md) and actual engagement boundaries. A larger search does not enlarge permission. No model service, scanner installation or live target is required to read or run the contained examples.

## 1. Put intelligence where it changes the experiment

A productive division of labor is:

```text
Question or unexplained observation
        ↓
Agent proposes abstractions, hypotheses, invariants and experiments
        ↓
Reviewed, bounded tool or existing deterministic runner
        ↓
Concrete cases, controls, traces and resource measurements
        ↓
Mechanical grouping, shrinking and reproducible evidence
        ↓
Agent challenges explanations and selects the next useful experiment
```

The model should usually stay **outside the repetitive inner loop**. It can write a generator once, inspect a compact failure summary and then improve the generator. Asking a model to reason through every ordinary input can be slower, more expensive and less reliable than executing code. Use a model per case only when the case actually requires semantic judgment, and calibrate that judgment.

Before scaling, identify the observation that would distinguish explanations. If the task begins without a vulnerability hypothesis, start with a bounded characterization question: which states are reachable, which component decides identity, or which transformations preserve meaning? Record surprises, then formulate testable hypotheses. Do not invent a premature vulnerability story just to complete a form.

The research frontier is the set of useful unresolved questions, with their dependencies, cheapest next experiment and stop reason. A short table is often sufficient. Expand it when an observation makes a different path worthwhile; stop expanding equivalent candidates that add no information.

## 2. Semantic variant research

### Why AI can help

The same trust mistake can appear under different names, languages or abstractions. A person may recognize one variant and lack the time to trace fifty cousins. An agent can connect a patch's underlying invariant to structurally different implementations, then propose targeted queries and counterexamples.

### Working method

1. Express the defect or uncertainty independently of syntax: which input is controlled, which boundary must hold, and where authority or state is consumed.
2. Use [ripgrep](https://github.com/BurntSushi/ripgrep), [Semgrep](https://docs.semgrep.dev/running-rules) or [CodeQL](https://codeql.github.com/docs/codeql-cli/) to collect a bounded source set. Record exclusions and relevant build/configuration coverage.
3. Let the agent group semantic candidates and explain why each could violate the invariant. Keep exact locations; an embedding similarity score is not a source trace.
4. Trace a few discriminating candidates through callers and configuration. Compare a similar implementation that correctly enforces the boundary.
5. Reproduce an actual disagreement in an authorized lab before promoting the lead. Preserve rejected candidates so later workers do not repeatedly rediscover them.

**Evidence:** patch/source identities, candidate selection method, reachable path, working control, minimum-impact witness and explicit affectedness limits. **Budget:** cap candidate retrieval and deep validation separately. **Stop:** equivalent candidates dominate, scope ends, or a useful supported answer is reached. **Failure modes:** semantic resemblance without reachability, omitted callers, generated explanations that invent code and an outdated fix mistaken for current exposure.

Google Project Zero's [Big Sleep report](https://projectzero.google/2024/10/from-naptime-to-big-sleep.html) describes AI-assisted variant research that found an unknown SQLite memory-safety flaw before its release. This is evidence that the approach can work in a particular setting; it is not a benchmark proving universal superiority over fuzzing or human research.

## 3. Long state sequences and interruption points

### Why AI can help

Many consequential failures involve valid actions in an unusual order: a retry after partial completion, a role change between checks, or a cancellation followed by a delayed event. The difficulty is often proposing the right state model and keeping track of explanations, not producing another random string.

### Working method

The agent proposes meaningful states, transitions, identity boundaries, interruption points and invariants. An existing test runner or small deterministic program enumerates bounded sequences, samples schedules or generates stateful cases. [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) supports property-based generation and shrinking; a small standard-library enumerator may be enough for a tiny model.

Define the oracle separately from the implementation where possible. For example, an event should contribute at most once and an unauthorized action should leave state unchanged. Include ordinary acceptance and a distinct valid action; otherwise a reject-all implementation might appear secure. Validate that modeled transitions are reachable in the actual implementation. A sequential model does not establish coverage of concurrent interleavings.

Retain a seed or exact schedule, model/source identities, explored bounds, actual cases and a minimized failing trace. Replay that trace against both the candidate and an appropriate control or corrected implementation. A state deduplication rule needs justification: collapsing two states is unsafe if they differ in an observation relevant to the property.

**Budget:** sequence length, states/cases, elapsed time, memory, processes and retries. **Stop:** a useful witness, exhausted admitted bound, diminishing new states or a resource limit. **Failure modes:** state explosion, impossible modeled actions, non-independent oracle, unrecorded nondeterminism and overstating bounded exploration as proof of absence.

The [contained sequence example](examples/README.md) explores340 sequences at depth1–4 over four synthetic actions. It includes a correct ledger, a deliberately faulty retry implementation and a reject-all apparatus control. It demonstrates bounded exploration and evidence quality, not AI productivity or real payment security.

## 4. Semantic transformation and differential testing

### Why AI can help

Agents can propose relationships that a researcher would rarely enumerate manually: equivalent encodings, omitted defaults, redundant fields, reordered independent operations, alternate adapters and boundary representations. The useful invention is the relationship, not the volume of mutations.

### Working method

State a **metamorphic relation**: what should remain equivalent, or change predictably, after a transformation? Alternatively, compare independently implemented versions against an explicit common contract. The agent proposes a small transformation matrix; deterministic code generates cases, normalizes only irrelevant differences and records disagreements. Parser-focused owned builds may suit [libFuzzer](https://llvm.org/docs/LibFuzzer.html) or [AFL++](https://aflplus.plus/docs/). Do not use them against a live service without the required specific authority.

Establish ordinary successful behavior and a deliberately relation-breaking synthetic case before trusting the apparatus. When outputs differ, examine whether the contract actually requires agreement. A stricter parser, a changed default or an accepted implementation choice can produce legitimate differences. Never normalize away the security-relevant discrepancy you are investigating.

**Evidence:** relation and rationale, exact implementations/configurations, generator version, seeds/input corpus, normalized and raw outputs, minimized witness and concrete replay. **Budget:** transformations, combinations, corpus/storage, CPU/time and deep triage. **Stop:** a supported disagreement or saturated meaningful relations. **Failure modes:** false equivalence, correlated reference implementations, environmental differences, lossy normalization and crash counts mistaken for impact.

This method is established testing practice. The AI-native opportunity is proposing better relationships and improving the generator from feedback; an advantage over a simpler baseline remains a hypothesis until measured.

## 5. Join assumptions across artifacts and components

### Why AI can help

The relevant contradiction may span a policy document, a configuration default, a database migration, an SDK and a UI fallback. Reading each artifact separately can miss a system-level gap. AI can help align the vocabulary and expose assumptions that no single file states in full.

### Working method

Select one consequential path: input → identity/authority → state → processing → integration → recipient. Build a compact claim table containing the claim, its authoritative owner, exact source/revision, implementation/configuration reference and uncertainty. Let the agent propose joins and contradiction candidates. Resolve identifiers, defaults and dependency versions mechanically where possible.

Use a known-consistent configuration and a seeded contradiction to test the instrument. Then validate the consequential disagreement in the actual authorized source or a controlled fixture. An inaccurate document is a documentation lead; it is not automatically demonstrated unauthorized access. A source setting is not proof of what is deployed. Third-party suppliers and other tenants do not enter scope merely because they appear in the path.

**Evidence:** attributed claims, exact path, configuration/source identities, disagreement, actual observed effect or clear inference, and downstream consumers. **Budget:** selected interfaces and claim count, not an unrestricted crawl of every document. **Stop:** the selected decision is supported or a missing authority/configuration blocks it. **Failure modes:** invented joins, stale copied facts, missing runtime overrides and treating generated architecture diagrams as observations.

The same approach can challenge the harness itself: do the instructions, tool adapter, evidence contract and acceptance command actually agree? This is a proposed application of the method, not proof that a self-checking system is correct.

## 6. Generate better instruments, not just more findings

### Why AI can help

A researcher may know which experiment is needed but abandon it because building a parser, stub, harness, trace reducer or local query would consume hours. An agent can draft that instrument, revise it from failures and make an otherwise uneconomical experiment practical.

### Working method

Define the instrument's input/output contract, permitted effects, bounds and oracle first. Prefer modifying a reviewed existing test to generating a framework. Inspect generated code as untrusted code: dependencies, subprocesses, dynamic evaluation, filesystem access, network/egress and output handling matter. Python isolation flags and virtual environments are not containment.

Calibrate against known-valid, known-invalid and deliberately faulty synthetic cases. Include a case that reveals a broken apparatus, such as every action being refused. Where useful, compare the generated instrument with a simpler independent implementation. Keep model-proposed mutations separate from evaluator decisions; the proposal must not approve itself or rewrite acceptance to improve its score.

**Evidence:** generator prompt/context references as appropriate, exact generated source, dependency/configuration identity, calibration results, actual exit/output and limits. Do not retain secrets or private reasoning transcripts. **Budget:** code variants, build/test time, model calls, artifact size and correction attempts. **Stop:** the instrument answers the selected question or calibration remains unreliable within the limit. **Failure modes:** a shared bug in generator and oracle, success-shaped fabricated output, hidden external calls and evaluator gaming.

DeepMind's [AlphaEvolve description](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) pairs model-generated programs with executable evaluation and selection. It concerns algorithms, not a cybersecurity benchmark. Applying that pattern to bounded research instruments is a proposed cross-domain adaptation; it needs its own evaluation.

## 7. Solver-assisted exploration and proof construction

### Why AI can help

Formal methods can be bottlenecked by translating a messy implementation into a useful model, constructing lemmas and understanding counterexamples. An agent can propose specifications, encodings and proof steps while a separate tool checks the formal result.

### Working method

- [KLEE](https://klee-se.org/docs/) symbolically explores compatible local programs under modeled inputs and an environment. Review build/runtime effects, path limits and external-call assumptions. Generated paths need concrete replay where the claim concerns an actual implementation.
- [Z3](https://microsoft.github.io/z3guide/) can solve a precisely encoded constraint problem. A satisfying assignment is a model of those constraints; translate it into a concrete witness when appropriate. Unsatisfiable means no model exists **within that encoding**. UNKNOWN, timeout and resource exhaustion are separate outcomes.
- [Lean](https://lean-lang.org/learn/) can check proofs against a formal statement and accepted assumptions. A proof of an incomplete specification does not establish the intended system property. Audit the specification, axioms, translation and trusted toolchain separately.

Begin with a small important invariant and a working known example. Include an intentionally invalid assertion or faulty fixture to ensure the pipeline distinguishes outcomes. Preserve specifications, assumptions, source/solver/prover identities, inputs, result and replay. Failure to prove can mean a missing lemma, an unsuitable encoding or a timeout; it is not itself a vulnerability.

**Budget:** paths, solver/prover time and memory, proof/model revisions and model calls. **Stop:** checked result for the selected claim, concrete counterexample, or an explicit inconclusive cutoff. **Failure modes:** wrong specification, unsupported environment, unsound translation, accidental assumptions and treating bounded absence as global proof.

Anthropic's [formal-verification research](https://www.anthropic.com/research/formal-verification) reports AI-assisted proof work and defect discovery in open-source libraries. This supports investigating proof-assisted methods; it does not transfer a guarantee to unrelated code or eliminate the need to review the specification and toolchain.

## 8. Reconstruct regressions and attack the repair hypothesis

### Why AI can help

The obvious defect may be fixed while a nearby path preserves the original mistaken assumption. An agent can read a bounded revision set, propose semantic cousins and distinguish competing explanations for why a repair works.

### Working method

Retain exact revisions and equivalent environments. Run the same minimized witness against the relevant baseline and candidate. Use controlled differential execution or bisection where the build and effect boundaries allow it. Ask what invariant the repair intends to restore, which consumers rely on it, and what alternate representation or sequence could challenge it. Do not reward finding a merely different failure.

Include a known-working case and an injected faulty fixture. Verify that a changed dependency, configuration or feature flag is not the true reason for a difference. A historical affected version is not proof that the current deployed service is affected. Restoration must account for data migrations and already-completed effects; reverting source alone may not restore state.

**Evidence:** exact versions, witness, controls, environment/configuration equivalence, change attribution and remaining variants. **Budget:** revisions, witness families, builds/time and storage. **Stop:** a discriminating cause is supported or further variants add no useful distinction. **Failure modes:** confounded environments, incomplete callers, nondeterministic timing and false current-affectedness claims.

## 9. Long-horizon research without memory theater

### Why AI can help

A long investigation may contain many small partial results that are tedious to maintain. Agents can keep the next useful question visible, generate local helpers and return to an unfinished branch without rebuilding the entire theory from chat history.

### Working method

Keep a durable frontier with hypothesis/question, exact subject, supporting and contradictory evidence, next discriminator, owner, remaining budget and stop condition. Maintain a short handoff linked to the actual artifacts. Reconcile current authority, source, effects and pending executions on resumption. Context compaction preserves references and constraints; it does not turn old evidence into a new observation.

Parallelize only independent branches with meaningful potential value. Give each worker exact scope, effects and aggregate limits. One integrator serializes shared writes and uncertain external effects. A second model's agreement is a challenge signal, not independent execution proof; models can share blind spots. Prefer a concrete reproducer or a different measurement over repeated conversational voting.

**Evidence:** real starts/finishes, source-bound observations, failed paths, actual resource counters and resumable state. **Budget:** total model calls/tokens when available, elapsed work, deterministic compute and coordination. **Stop:** accepted outcome, diminishing information, unresolved boundary or resource cap. **Failure modes:** stale cached authority, duplicated work, lost negative evidence, hidden retries and claims that a document creates a continuously running service.

Anthropic's [long-running-agent harness discussion](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) motivates incremental work and resumable artifacts. The reusable lesson is state discipline; the exact runtime and permission controls still have to exist. DARPA's [AIxCC results](https://www.darpa.mil/news/2025/aixcc-results) demonstrate combined automated discovery and repair in a controlled competition, not assurance for an arbitrary deployment.

## 10. Measure the method before scaling it

An AI-native investigation SHALL retain enough information to distinguish more useful research from more activity:

| Question | Useful measurement | Misleading substitute |
| --- | --- | --- |
| Did this answer the question? | Accepted evidence or a useful bounded falsification/inconclusive result | Number of alerts or generated hypotheses |
| Did the apparatus work? | Successful ordinary behavior, discriminating controls, known-defect detection | Exit0 alone |
| Did AI improve the approach? | Comparable baseline, same scope/limits, accepted outcomes and correction cost | A story about what a human might have spent |
| What did it cost? | Actual model calls/tokens if exposed; CPU/wall time, memory, cases and retries separately | UNKNOWN recorded as zero; overlapping totals added together |
| What remains? | Unexplored bounds, blocked branches and invalid assumptions | “Exhaustive” without a defined finite space |

Record an initial bound, a useful stop and an extension decision. For example: characterize one interface, examine a fixed candidate set, validate the strongest distinct explanations, then extend only if new evidence justifies the cost. Numerical bounds belong to the actual task; this chapter introduces no universal request count or mandatory model stack.

Reuse generated tools and results under their exact source/configuration/time/permission conditions. Cache deterministic outputs by meaningful input identity; retrieve durable evidence by reference. Do not reuse a result merely because its text looks similar. Evaluate cost per accepted outcome including failed attempts, false positives, review and integration. No general AI speedup or business-saving percentage is established by this package.

## 11. A compact investigation record

The existing [notes template](templates/NOTES.md) can hold the following; no new database is necessary:

```text
Question / invariant / competing explanation:
Why AI is useful here; simpler baseline:
AI responsibility; deterministic runner; independent oracle:
Exact assets, source/model/configuration identities and actual authority:
Candidate generation / search bounds / seed or schedule:
Working baseline / negative control / known-defect calibration:
Actual cases, failures, truncation and resource counters or UNKNOWN:
Minimized witness and concrete replay:
What was learned; what remains untested; next discriminator or stop:
```

Use [the worked example](examples/README.md) to practice the mechanics without a target, API account or model spend. Its automatic exploration is real local execution; the fictional research narrative remains illustrative. The required gate binds declared evidence and review. It cannot decide that a new technique is insightful, the oracle is correct or the action is authorized.


## Team implementation

[Orchestration](ORCHESTRATION.md) makes these methods operational: Systems supplies current context; Discovery invents discriminators; Engineering builds/runs instruments; Validation challenges claims; Knowledge preserves evidence/lessons; Operations reconciles execution/recovery; Methods challenges cost and approach; Coordination integrates. All eight duties exist at material project admission; useful workers activate within actual capacity. This is not a requirement to call eight models per experiment.
