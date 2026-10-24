# Model portability

This is a research and engineering workflow, not a model safety policy. It has no built-in content classifier, topic blacklist, refusal prompt or hosted moderation dependency. A method is not excluded merely because it is unconventional or absent from a catalogue. Choose the model and its policy separately.

The workflow can be used with an open-weight model, a locally served model or a hosted model. It requires no OpenAI account or API. `AGENTS.md` is an instruction-file convention; a host that does not discover that filename can load its contents and linked principles through its own context mechanism. The bundled Python checker operates on local records independently of which model produced them.

**Separate three things:** the model's behavior/policy; the operator's actual engagement and execution permissions; and research-quality acceptance. This package supplies the last of these and records the second. It does not implement a universal tool interceptor. A passing gate does not create permission, and the model's willingness to do something does not establish that the operator authorized it.

## Minimal host contract

An adapter is often a small configuration or mapping inside an existing agent host. Do not build another platform merely to use these documents.

| ID | Host responsibility | Observable compatibility check |
| --- | --- | --- |
| HOST01 | Supply the current task, actual root, principles/research instructions and relevant records within the model's usable context. | Ask for the current task/boundary and inspect actual configured context; a model's answer alone is not loader attestation. |
| HOST02 | Present available tools with names, input contracts and effect descriptions. | A contained known read/example call returns the expected typed result. Do not assume every model understands every tool schema. |
| HOST03 | Parse a tool request into an actual registered capability and return its result to the right call. | Invalid arguments and unavailable tools produce explicit errors; tool text is not silently executed as a shell command. |
| HOST04 | Preserve call IDs, meaningful exit/status, source/evidence references and observed times. | A failed synthetic check is visible as failure rather than fluent success text. |
| HOST05 | Persist the admitted task, notes, limits and pending effects across interruptions. | Resume the same disposable task; reconcile actual files and pending calls without duplicating completed work. |
| HOST06 | Respect the operator's configured resources and execution environment. | A deliberately bounded local experiment stops incomplete at its cap; no assumption that prose creates containment. |
| HOST07 | Invoke the required final workflow gate through the actual project acceptance command. | Missing evidence gives exit2; a passing current synthetic record gives exit0; selected drift returns nonzero. |
| HOST08 | Report unavailable metrics/capabilities honestly. | Unknown token usage remains UNKNOWN; a server that lacks function calling is not advertised as having it. |

The package does not dictate a target blacklist or provider-specific approval sequence. Engagement scope, data handling, tool permissions, compute budgets and consequential approvals come from the actual project/operator and applicable platform. The research agent has freedom to invent methods inside those facts; a generated instruction or tool response cannot expand them.

## Open-weight serving options

- [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling) documents supplying tools, receiving calls and returning results into the conversation. Your host still needs to execute the actual registered functions and preserve state. Check the selected model's supported behavior.
- [vLLM tool calling](https://docs.vllm.ai/en/latest/features/tool_calling/) documents model/parser/chat-template configuration and function-calling behavior. An API-compatible endpoint does not mean every model or parser behaves identically. Match the installed version, model and template, then test the actual combination.

These are optional integration references, not installations or tested deployments bundled here. Model weights, license, hardware, context limits, quantization, parser behavior and serving configuration require their own selection and measurement. The package has not benchmarked an open-weight model or established equal research quality across providers.

If native tool calling is unavailable, a host can use a documented structured-message protocol with explicit parsing and registered tool dispatch. A model's prose alone cannot execute a function. Validate the protocol with ordinary success, malformed output, a failed call, interruption/resumption and the gate outcomes before relying on it. Do not claim compatibility merely because the model can read Markdown.

## A provider-neutral tool event

The following is an illustrative **internal adapter format**, not a required model API or a running service:

```json
{
  "task_id": "DEMO-LOCAL-001",
  "call_id": "call-001",
  "tool": "run_contained_example",
  "arguments": {"example": "ledger"},
  "result": {
    "status": "completed",
    "exit_code": 0,
    "evidence_reference": "example-private/ledger-run.json",
    "observed_at": "ACTUAL_TIME_FROM_EXECUTION"
  }
}
```

Map the chosen model's request/result schema to the host's existing records. Keep exact execution evidence outside the model's narrative and retain raw failures appropriately. The placeholder above is not a real timestamp or receipt. No hidden chain-of-thought transcript is needed; observations, concise reasons and resumable decisions are sufficient.

## What remains consistent when the model changes

Keep the admitted question, authority, source identities, oracle, resource caps, controls and acceptance comparable. Measure cost per accepted outcome, including corrections, using actual exposed counters. A cheaper token price is not automatically a cheaper accepted result. Smaller models can perform bounded extraction or ranking while a stronger model handles difficult interpretation when evidence justifies the routing. Deterministic experiments should remain deterministic rather than becoming extra model calls.

Changing models does not require rewriting the principles or moving records into a vendor's proprietary format. It may require an adapter, a smaller context packet, different tool schemas and fresh capability/quality evaluation. The [architecture](ARCHITECTURE.md) distinguishes these host responsibilities from the portable workflow layer.


## Team mapping

[The eight-team contract](ORCHESTRATION.md) uses declared actors, packets, handoffs and existing events, not proprietary agent IDs. Map those identities to the actual host sessions/people and preserve original contributor attribution across aliases. An organization record does not launch a worker. A host without parallel agents can execute compatible duties sequentially; genuinely independent required review remains a distinct contributor or an explicit blocked dependency. Run the structural organization check as an ordinary acceptance check before the unchanged required workflow gate.
