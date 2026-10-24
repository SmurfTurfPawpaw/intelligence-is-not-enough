# Base project workflow

This mode applies the common principles/workflow without adopting the exploratory research profile. It does not require a research roster. Use the bundled runtime at `harness/runtime/principles-2.0.0/` relative to this reference, or an existing compatible trusted pin. Read its [runtime guide](harness/runtime/principles-2.0.0/README.md); the separate research workflow's organization section applies only in research mode.

1. Reuse the current task if its frozen plan still fits. Otherwise record the material change before implementation and run `workflow.py begin --root ROOT --task TASK_ID --plan relative/plan.md`. Creation produces unresolved `.principles/tasks/TASK_ID/{task,begin,review}.json`; it is not acceptance. Existing/partial tasks are not overwritten. Initial adoption is material. For a genuinely minor change only, `--small-reason` replaces `--plan`; all six no-impact declarations must be true, with reasons.
2. Populate `task.json`: real outcome, beneficiary, scope, authority reference, recovery, exact selected file subjects and meaningful check IDs/criteria/freshness budgets. Keep the generated begin/review/plan subjects; directories/globs are not selected files. Set `state` to `ready` when the contract is populated; that is not completion.
3. Perform actual checks and retain output in appropriate project/private storage. Finish `review.json` with an attributed reviewer, summary and P01–P10 dispositions. `supported` needs scoped reasons and actual check IDs; `not_applicable` needs a real reason. Outcome, durable knowledge and accountability always apply. Missing or failed evidence is not N/A. Disclose self-review; another role label is not independence.
4. Record actual evidence after finalizing selected bytes:

```text
python "RUNTIME/principles.py" receipt --root "ROOT" --task TASK_ID --check CHECK_ID --result pass --evidence relative/actual.log --method "Actual scoped method and interpretation" --observed-at ACTUAL_ISO_TIME
```

Use the actual result, including fail/unknown. `max_age_seconds: null` is a static binding, not perpetual live freshness. Do not refresh an old output's time. Changes to selected bytes invalidate receipts; newer adverse/unknown/corrupt evidence cannot fall back to old green.

5. Run `workflow.py check --root ROOT --task TASK_ID` through the project's real acceptance command after existing checks, preserving nonzero. The skill's `scripts/accept.py --profile base` adapter verifies its installed bundle first. A missing trusted runtime, unresolved review or failed gate blocks dependent verified completion/effects; continue independent useful work and disclose the gap. The checker creates no permission or authenticated execution proof.

The unchanged runtime checks selected declared source/evidence bindings and review shape. It does not decide semantic adequacy or intercept arbitrary tools. No model, hook, service or recurring check is required. Retain original instructions, current records, history and compatible pins when adopting into an existing project.
