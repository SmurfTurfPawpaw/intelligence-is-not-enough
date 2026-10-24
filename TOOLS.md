# Tool guide

This is an optional, non-exhaustive selection guide. Agents MAY choose other tools, combine techniques or write a smaller local instrument when that better answers the question. No tool below is a mandatory step, installation claim or permission grant.

## Choose a tool for a question

1. State the observation needed to distinguish explanations. Reuse applicable saved evidence or inspect source before adding a scanner.
2. Check actual availability and applicable instructions: exposed capability, installed version, supported platform, license/access, configuration and data/egress behavior. A documentation page is not proof that a capability is callable. Installation, account creation, payment or external upload needs its actual authority.
3. Select the smallest sufficient tool. Fix the subject/environment, mode, inputs, rate/resource limits and output location. Pin relevant rule/query/template versions. Review what the tool will read, execute, download, transmit or change.
4. Capture the observation plus a control, then interpret it. Preserve meaningful stderr and exit status. A successful invocation, scanner alert or crash is not by itself a verified security impact. Reuse only while subject/configuration/time/permission remain applicable.
5. Record a concise tool event in [notes](templates/NOTES.md); complete the normal research/checker workflow. No separate form is needed for every shell command.

## Source and artifact inspection

| Tool and official documentation | Useful usage | Prerequisites and evidence | Important limit |
| --- | --- | --- | --- |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | Find entry points, checks and consumers; start with a literal symbol or bounded file set. | Authorized source and installed `rg`; retain searched paths/options and relevant matches. | Ignore rules/hidden files affect coverage; no matches can reflect exclusions. Matches are not reachability or impact. |
| [Git diff](https://git-scm.com/docs/git-diff) | Compare exact revisions and review affected paths before repeating analysis. | Actual repository/revisions and inspected configuration; record commit IDs, dirty state and selected diff. | Committed diffs omit untracked files; Git can invoke configured helpers. Disable external diff/text conversion when needed. |
| [Semgrep](https://docs.semgrep.dev/running-rules) | Find structural patterns or encode a focused local hypothesis as a rule. | Compatible CLI/language and reviewed rules; retain rule identity, source identity and structured findings. | Rule matches need validation. Registry rules, logged-in modes and [metrics settings](https://github.com/semgrep/semgrep/blob/develop/metrics.md) have different network/data behavior. Use approved local rules for an offline task; metrics-off alone is not network isolation. |
| [CodeQL](https://codeql.github.com/docs/codeql-cli/) | Trace richer code/data relationships when simpler search cannot answer reachability. | Supported language, appropriate database/extraction, queries and license/access; retain query/database/source identities and paths. | Extraction/builds can execute project tooling and omit configurations. Review build effects and coverage before running. |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Inspect permitted files/history for potential exposed secrets. | Reviewed scope/rules and supported CLI; retain sanitized location/rule/context with secret values private. | A match is not proof a credential is valid. Do not try a credential to establish validity without separate authority. |
| [Trivy](https://trivy.dev/docs/latest/guide/) | Assess permitted dependency, image or configuration artifacts. | Appropriate scanner/database/cache/configuration; record artifact identity and advisory/database time. | Database/image retrieval may contact providers. Advisory matches are leads; exploitability and deployed affectedness need evidence. |

## Observe application behavior

Choose one browser/proxy path that supplies the needed evidence rather than stacking all of them.

| Tool and official documentation | Useful usage | Prerequisites and evidence | Important limit |
| --- | --- | --- | --- |
| [Chrome DevTools Network](https://developer.chrome.com/docs/devtools/network/) | Explain which requests an approved browser action makes and how the UI reacts. | An authorized session/action; retain relevant timing, headers/status and sanitized captures. | Loading a page can change state or call third parties. Exports can contain tokens, cookies and personal data. |
| [Playwright trace viewer](https://playwright.dev/docs/trace-viewer) | Make an owned-lab UI sequence reproducible and inspect its actions/network timeline. | Reviewed test/browser setup and contained test identities/data; retain trace plus source/configuration. | Automation executes actions; a trace may contain sensitive state. Saved traces do not establish current production behavior. |
| [Burp Suite](https://portswigger.net/burp/documentation/desktop/getting-started) | Inspect approved proxy traffic and conduct controlled comparisons. | Appropriate edition, scoped project/browser, credentials handled through approved channels; retain sanitized evidence. | Manual replay or scanners send requests and can mutate state. Edition availability/license is separate from the docs. |
| [ZAP](https://www.zaproxy.org/docs/desktop/start/) | Inspect approved traffic and use selected analysis where appropriate. | Scoped context/browser and reviewed scan policy; retain relevant messages, configuration and alerts. | Quick Start can spider and actively scan. Passive analysis of captured traffic does not make the browsing or collection itself harmless. |
| [mitmproxy](https://docs.mitmproxy.org/stable/overview/getting-started/) | Script inspection/transformation of an owned-lab flow when a small repeatable instrument is useful. | Explicitly scoped proxy/client, appropriate certificate trust and flow handling; retain script/configuration and sanitized flows. | Interception changes trust. Contain listeners and certificate trust to the approved lab; capture files can hold credentials. |
| [Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/) | Explain permitted packet captures and protocol behavior. | Authorized capture/data access and appropriate interfaces/filters; retain capture identity/time and relevant frames. | Capture may expose unrelated traffic. An offline file does not imply permission to inspect its contents. |
| [Nmap](https://nmap.org/book/man.html) | Answer a specific authorized service/inventory question on exact permitted assets. | Explicit assets, permitted probes, rates/window and suitable privileges; retain options/time/raw output privately. | Active traffic, scripts and version detection have different effects. Never infer vulnerability from a service fingerprint alone. No live-target command is prescribed here. |

## Reproduce, instrument and test hypotheses

| Tool and official documentation | Useful usage | Prerequisites and evidence | Important limit |
| --- | --- | --- | --- |
| [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) | Generate local input sequences and shrink counterexamples to a small useful case. | Reviewed owned code/test environment and bounded settings; retain failing example, seed/database settings and source. | Running tests executes code; generated coverage is not exhaustive or proof of exploitability. |
| [libFuzzer](https://llvm.org/docs/LibFuzzer.html) / [AFL++](https://aflplus.plus/docs/) | Explore a local parser/state boundary with a coverage-guided harness. | Compatible reviewed build, instrumented target, seed corpus and strict process/resource/egress limits; retain crash input, build/configuration and reproduction/control. | Fuzzing executes the target and may create many artifacts. A crash must be triaged; no live-service fuzzing follows from this example. |
| [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Understand an authorized shipped binary when source is unavailable or differs. | Supported artifact, analysis environment and artifact hash; retain function/address context and evidence of the inference. | Decompilation is an interpretation. It does not establish the deployed version or runtime reachability; do not execute the artifact merely to identify it. |
| [Frida](https://frida.re/docs/home/) | Observe selected function/state behavior in an authorized lab process. | Compatible runtime, process access and reviewed instrumentation; retain script, process/artifact identity and observations. | Instrumentation can alter timing/behavior and expose secrets. Attaching to a process requires actual permission and containment. |
| [Codex Security](https://learn.chatgpt.com/docs/security) | Use a scoped source scan, diff review or supplied-finding triage when it answers the task. | Actual access/capability and the matching installed skill; retain scan subject, findings, validation evidence and limits. | AI findings need review; inference may consume usage and receive code/context. A source scan is not live authorization or proof of deployment exposure. |

The existing principles checker is a separate evidence-binding gate, documented in [README](README.md). It is not a vulnerability scanner. A small reviewed Python fixture or existing project test can be more useful than any listed product. The catalogue's breadth is not an instruction to install or run everything.

## Agent and MCP capabilities

[HOST-TOOLS.md](HOST-TOOLS.md) explains capability discovery, conditional adapters and routing. Availability is observed separately from configuration, permission and successful execution. Preserve actual skill/broker requirements; a CLI, browser, reverse-engineering tool or generic HTTP client SHALL NOT be used to route around a refused operation.

## AI-guided instruments and formal methods

[Beyond Human Patience](AI-NATIVE.md) explains how to combine semantic reasoning with bounded deterministic execution, calibrated generators and concrete replay. Generated code is an untrusted instrument until reviewed and calibrated; it does not approve its own oracle.

| Tool and official documentation | Useful usage | Prerequisites and evidence | Important limit |
| --- | --- | --- | --- |
| [KLEE](https://klee-se.org/docs/) | Explore selected paths of a compatible local program symbolically. | Reviewed build/runtime, modeled environment, bounded paths/resources; retain input/path, tool/build identity and concrete replay. | Environment/translation assumptions constrain coverage; unmodeled calls and path limits are not proof of safety. |
| [Z3](https://microsoft.github.io/z3guide/) | Test precise constraints or obtain a model for a proposed invariant violation. | Explicit encoding/assumptions and solver settings; retain formula/result/model and concrete interpretation. | SAT/UNSAT applies to the encoding; UNKNOWN/timeouts are not either answer. |
| [Lean](https://lean-lang.org/learn/) | Check a formal statement/proof assembled with or without AI assistance. | Reviewed specification, accepted assumptions and toolchain; retain exact statement/proof and checker result. | A checked proof does not establish that the statement captures the whole implementation or intended security policy. |

## Minimal local example

The following shapes inspect files; they do not scan a network. Use them only after resolving the real authorized directory and checking actual executable/configuration. Their paths describe an owned synthetic fixture, not a target:

```text
rg --files --glob "*.py" examples
rg -n --glob "*.py" "def |assert " examples
```

The first lists visible Python files; the second locates simple function/assertion lines. The distributed `examples` directory is the actual contained fixture path. An extracted archive is not necessarily a Git repository. Only inside an actual authorized Git checkout, `git --no-pager diff --no-ext-diff --no-textconv --stat` summarizes tracked working changes. Record relevant exclusions. `rg` commonly exits1 for no match, which must be interpreted separately from an invocation error. A clean Git diff does not cover untracked/ignored files or deployed services. Protect sensitive matches rather than dumping them into a shared log.

For an executable local reproducer, use the existing [synthetic example](examples/README.md): preserve the reviewed fixture hash, actual output, repeat/new-input control and remaining uncertainty. `python -I` or a virtual environment is not a security sandbox. Establish containment separately before executing unfamiliar code. No live target or attack request is included in this guide.

## One concise tool record

Retain: task/hypothesis; tool and version; capability/configuration/rule identity; actual subject/revision/principal; scope/mode/effect limit; start/end or observation time; relevant invocation; actual exit/status and sanitized output reference/hash; control; interpretation/limits; cumulative usage or UNKNOWN; cleanup/next action. Reuse the existing notes entry rather than creating another database.

Product documentation can change. Read the exact installed-version help and relevant official page before using an unfamiliar feature, a changed option or any consequential effect. Documentation describes capabilities; establish installation, licensing, configuration and permission separately. Evaluate effectiveness against the actual research question and evidence.
