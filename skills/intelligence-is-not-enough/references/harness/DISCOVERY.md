# Discovery that follows the evidence

Use this loop when a new disclosure, code change or research result may change an investigation. It turns a changing signal into a small next question and a qualified consumer map. It runs on demand, offline, with Python3.12+ standard library. The configured human/agent host supplies research and tools; this package fetches nothing, calls no model and starts no monitor.

## The working loop

1. **Notice a change.** Use existing authorized retrieval tools, maintainer releases/security advisories, [GitHub advisories](https://github.com/advisories), [CVE records](https://www.cve.org/), [OSV](https://osv.dev/), original researchers and [Hacker News](https://news.ycombinator.com/). Social posts are useful leads; follow their original evidence. A feed notification is not independent corroboration. Use provider APIs/feeds within their actual terms and access; no scraper or paid subscription is required here.
2. **Keep the observation.** Retain a sanitized content snapshot privately. Record URL, source, exact captured revision, SHA256, publication/update/observation times, result and freshness. Append a uniquely identified observation with a higher sequence for that source. Preserve older observations. A new failed retrieval, withdrawal or contradiction is an observation too.
3. **Identify the primitive.** Decide whether names share an evidenced root cause. Keep aliases on one issue only when evidence supports the connection. Related protocol or runtime flaws remain separate issues. Never merge by similar names alone.
4. **Trace consumers.** Follow the affected library into bundled copies, runtimes, services, tools and deployments. Record each supported link, its configuration prerequisite, evidence IDs and both endpoint revisions. Check inbound request processing and outbound response processing separately, including the research toolchain itself.
5. **Derive the next work.** Run the report below. Pick a useful unresolved boundary by consequence, information gained, current obligations and cost. Use the existing investigation/authority/work-packet process for any actual experiment. A generated next action does not approve or dispatch one.
6. **Requalify and repeat on change.** Add actual results and controls; update affected links to the exact new evidence/revisions after reviewing compatibility. Rerun this cheap deterministic projection. Preserve unrelated valid work and original observation times. Stop when the useful question or budget is met.

Sources can disagree. Record contradictory evidence with the issue/link rather than discarding it or treating a newer marketing paragraph as a maintainer decision. The source ID denotes one consistently versioned claim/document stream: use separate IDs for independently changing subjects. Sequence is declared admission order, not SemVer, a network-authenticated provider revision or proof that history was append-only. Reconciliation must establish which upstream content is actually latest before appending it; a delayed older notification must not be relabeled a newer upstream fact.

Adding two contrary but `available` documents does not tell the tool they disagree: it cannot read their meaning. The researcher SHALL mark the affected claim's presence/reachability `unknown`, or append an appropriately attributed `conflict` observation for that source, and retain both references. New primary signals without an issue/link disposition and unusable latest primary observations generate intake actions even when no graph exists yet. Reposts preserve leads without automatically multiplying triage work after their source has been handled.

## Try the contained example

```sh
python tools/discovery.py report --record examples/discovery.json --as-of 2030-01-01T12:30:00Z
```

The example is entirely synthetic. It groups three names around one decoder defect, traces a runtime into an inbound shop and outbound fetch tool, preserves a dependent repost, and leaves a batch-job path unresolved. **Exit2 is expected** because that path needs evidence. No network or model account is used. Tests execute this command in a fresh temporary workspace and exercise correction, staleness, revision drift and recovery.

For real work, use your private record and omit `--as-of` to evaluate at the actual UTC time:

```sh
python tools/discovery.py report --record private/discovery.json --output private/new-report.json
```

The output must be a new file; existing files are refused. The input stays read-only. If an output write fails, preserve/inspect any partial new file and choose a new output path after reconciliation. A previous report retains its original evaluation time and becomes historical as inputs age or change. Recompute at the decision boundary; a saved JSON file is not a live subscription.

| Exit | Meaning |
| --- | --- |
| 0 | Projection completed for the declared paths, without an unresolved action. No security clearance, exploit proof or completeness beyond the declared graph. |
| 1 | Invalid input, file access or output conflict; inspect the error. |
| 2 | Useful report with unresolved evidence/frontier or exhausted work budget. Keep it visible; do not substitute old green. |

## One record, four small collections

Start from [the example](examples/discovery.json); no database or schema package is needed. `schema_version` is `1.0.0`. IDs are portable letters/digits/underscore/dot/hyphen, up to96 characters, beginning with a letter/digit. Optional contextual notes may be retained; unrecognized fields are not interpreted or checked.

| Collection | Contract |
| --- | --- |
| `observations` | `id`, stable `source`, positive unique per-source `sequence`, opaque `revision`, `url`, `kind` (`primary`/`repost`), `result`, `observed_at`, `fresh_for_seconds`; available content needs lowercase hex `sha256`. Optional `published_at`/`updated_at` are distinct timezone-bearing timestamps. A repost's optional `origin` references its original observation; unknown lineage stays unknown. |
| `components` | `id` and current exact `revision`. Include relevant source, build, configuration and/or deployed identity in that revision or an explicitly separately changing component. A package name alone is inadequate. |
| `issues` | `id`, explicit `aliases`, `root` component, bound `root_revision`, concise `root_cause`, nonempty `evidence` observation IDs. The same alias cannot belong to different issues. Evidence IDs include material supporting **and contrary** sources. |
| `links` | `id`, `issue`, `from` affected component, `to` consumer, `from_revision`, `to_revision`, `relation`, configuration `condition`, `presence`, `reachability`, `direction`, nonempty `evidence` observation IDs. Links point from primitive toward consumer; direction describes its untrusted input route. |

Results for observations: `available`, `failed`, `unknown`, `withdrawn`, `conflict`. Presence: `affected`, `fixed`, `absent`, `unknown`. Reachability: `reachable`, `excluded`, `unknown`. Direction: `inbound`, `outbound`, `local`, `unknown`. These are attributed declarations supported by retained evidence, not discoveries made by the JSON checker. Do not put a model's guess into an observed field. URL contents are never executed or interpreted as instructions.

An available primary source is not automatically truthful or sufficient. A link needs evidence for its own exact claim, not merely a copy of the upstream advisory. Reposts preserve provenance but cannot support a technical path alone; the reporter must follow the original evidence. A hash binds retained bytes; it does not authenticate the author, execution or model.

## Read the consumer map correctly

- **`reachable`:** every declared step on this witness has current qualified evidence, affected presence and stated reachability/direction. It is a **candidate source path**, not validated exploitation or current deployed impact.
- **`present`:** dependency presence is declared but end-to-end data flow or direction is missing. It cannot become a confirmed path merely through transitive dependencies.
- **`unknown`:** required source evidence is stale, failed, superseded, future, conflicting or absent, or an endpoint revision changed. Unknown upstream state carries into descendants.
- **`excluded`:** this declared path is fixed, absent or excluded by current evidence. Traversal stops on that branch; unvisited descendants remain a frontier. Other valid routes remain visible.

Only the latest declared observation per source can support a current path. Even an identical-content successful refresh needs explicit evidence requalification; a failure never revives old success. Source revisions are opaque; the tool does not guess version ranges or backport status. Changing either endpoint invalidates the link, while unrelated consumers can retain their evidence. Unsupported/unlisted consumers are outside coverage, never silently safe.

Traversal has deterministic ordering and at most one representative witness per consumer/state/final-edge direction. Cycles terminate; it does not enumerate all paths. Input limits:2MiB,512 observations,128 components,64 issues,256 links,32 evidence references per claim; freshness1second–30days. Default512 edge steps, configurable `--max-steps`1–4096. At exhaustion `incomplete` and unvisited links remain explicit. Reports include input/checker hashes, source identities, evaluation time, qualified paths and deduplicated next actions.

## Keep models and orchestration interchangeable

### Close irrelevant intake without inventing an issue

An unassigned primary observation remains an intake action in this projection. There is no interpreted standalone disposition field. For a signal that warrants no investigation, record its source ID/revision, decision, evidence/reason, reviewer/time and reopening trigger in the project's existing notes. Then exclude it from the active case input while retaining the original observation and prior record revision in project history. This is an explicit human/agent triage decision; the CLI does not verify that selection or claim complete feed coverage.

Do not create a fictional vulnerability to clear an action. Do not remove failed, stale or contrary evidence from an active technical claim to obtain a passing report. A changed source or reopening trigger returns the signal to intake. An unknown additional JSON field does not close an action.

Any model that can author this JSON and use its host's file/command tools can participate, including open weights. There is no special OpenAI prompt format or inference dependency. Keep exact model/provider/revision, tool identity, target revision, actual token/time budget and controls in the existing [notes](templates/NOTES.md); use UNKNOWN for unavailable usage. Supported backend lists and historical benchmark runs are not evidence of a model's success on your investigation.

Start with one scout/investigator and deterministic collection/projection. Use a separate validator for claims requiring independent reproduction; split consumer tracing into bounded tasks only when distinct consumers justify parallel work. Reuse the eight [responsibility owners](ORCHESTRATION.md), not eight permanent inference loops. Deduplicate root causes, preserve consumer-specific judgments, and feed unresolved paths into the existing queue. Publication, testing authority and consequential approvals remain separate.

## Design references

These explain the design; they are historical sources, not a permanent feed or proof that today's versions remain affected:

- [Node's October2026 security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases), [Python mapping](https://github.com/advisories/GHSA-9v8h-qqgm-4m35) and [Bun qualification](https://github.com/oven-sh/bun/security/advisories/GHSA-663w-cv8g-jj2p): shared primitive, different consumers, separate evidence levels.
- [Cloudflare's discovery pipeline](https://blog.cloudflare.com/cyber-frontier-models/): narrow hunts, independent validation, consumer tracing and feedback.
- [OpenAI's containment research](https://openai.com/index/securing-our-frontier-model-training-environment/): exact environments, multiple boundaries, triage and reproduction.

Run the focused software checks with `python -B -m unittest discover -s tests -p test_discovery.py -v`. Retain real reports and tests as ordinary task evidence, bind the record/report/tool and selected consumer evidence, and finish through the existing [required workflow](WORKFLOW.md). This utility supplements that workflow; it never replaces its review or final gate.
