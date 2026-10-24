# Worked example: useful falsification

For the complete begin → task/review → actual capture → receipt → required acceptance path, follow [the walkthrough](WALKTHROUGH.md). The simpler fixture below demonstrates one observation; the later sequence experiment demonstrates AI-native research mechanics without an AI service.

The research question is whether an owned synthetic ledger accepts the same operation identifier twice. The investigator starts with a duplicate-acceptance hypothesis and compares a repeated identifier with a new one. This example demonstrates the research method using a small in-memory fixture; it is not a payment integration or target test.

## Run the fixture

From the extracted package root, use Python3.12+:

```text
python examples/ledger.py
```

Expected output:

```json
{"control": "accepted", "first": "accepted", "repeat": "refused"}
```

The first use establishes ordinary acceptance, the repeat tests the hypothesis, and the different identifier helps rule out a fixture that simply rejects everything. Compare the output you actually obtain. Expected text is not an execution receipt. The fixture does not read files, access a network, move money or persist data.

## Make it a bounded investigation

Use [the brief](investigation-brief.md) to populate your actual task/paths/ownership facts before begin. Freeze that file when starting the required workflow. Keep evolving explanations and observations in separate [notes](notes.md); their supplied content is illustrative and must not impersonate your actual record.

Define acceptance as demonstrating repeated/new-identifier behavior with reproducible source/output, a meaningful control and honest limits. If the check instead explicitly required proving duplicate acceptance, the observed refusal would fail that criterion. Never change a failed criterion retroactively to call it a success.

After running the fixture through actual permitted tools, retain its exact source hash, relevant environment, command, observation time, actual output and interpretation. Complete the task contract and attributed P01–P10 review, record honest receipts and run the required final gate as explained in [the workflow](../WORKFLOW.md).

## Interpret the result

The starting hypothesis is falsified for this exact source and sequence. The research task can still meet its useful acceptance because it produced a reliable observation and control. Concurrency, alternate identities, ordering variations, different implementations and deployed services remain untested.

An unexpected observation may suggest another in-scope hypothesis. Explore it within the actual brief's objective, remaining budgets and effect boundaries. A materially different question, environment or effect requires a linked new task. Changed selected notes/evidence require applicable requalification; changed frozen brief bytes cannot be excused as exploratory freedom.

A passing local research-quality gate establishes no live affectedness or reportable security impact. Keep the finding status and the research completion status separate.

## Bounded sequence exploration

Run `python examples/explore.py` from the package root. Four actions represent a valid event A, a retry of A, a distinct valid event B and an unauthorized attempt. At depth1–4 the finite space contains340 sequences. Each sequence starts with a new in-memory ledger; the ordinary-success and distinct-event controls establish a usable apparatus first.

The program compares a reference property with a correct implementation and a deliberately faulty implementation that applies a retry twice. It records actual cases, bounds, property/source identities and a minimized replay. A reject-all implementation is classified inconclusive before enumeration. `python examples/explore.py --max-cases 17` deliberately returns incomplete/exit2, rather than presenting a partial search as a pass.

The overall example's exit0 means its **known calibration expectations** were met: bounded correct behavior, detection of the injected fault and rejection of the invalid apparatus. It does not mean every implementation passed. The tiny action vocabulary/model is supplied by the example; AI did not autonomously discover the injected bug. The transferable method is model-assisted experiment design plus deterministic exploration, controls and replay. See [Beyond Human Patience](../AI-NATIVE.md) for applying it to a genuinely uncertain authorized question.
