# Mandatory Response Templates

This is the build source for `templates/responses/`. **Every user-facing answer from every skill uses its registered template**, including a direct skill call, a clarification, a failure, and an unsupported request. `q-mentor-orchestrate` produces no separate answer; a multi-skill task returns one answer in the terminal skill's template. The rule is not optional prompt advice: generate the named template files, record each `template_id` in `registry/skills.yml`, cite it in each `SKILL.md`, and validate rendered answers. Contract: `qmentor.response.v3`.

## Small, consistent answer envelope

1. Start with the template's **lead field and actual answer**, not “Status: complete” or a process summary. Put `Status: complete | needs-input | blocked | unsupported | unverified` on the next line. Use `complete` only for the work actually verified.
2. Follow the template's fixed field order below. Each field is one sentence or one compact row; omit only fields marked optional. Do not add an introduction, repeated conclusion, praise, raw log, or generic disclaimer. A `needs-input` answer asks **one material question** in its lead or final action field; `blocked` names the first actionable gate.
3. Default business mode uses plain language, one decision and its implication. Technical mode keeps the same fields but may link a detailed artifact. Use the per-template prose caps below; requested files, exact diffs, references, and full-help rows are outside the cap. Brevity never hides a material loss, uncertainty, or failed test.
4. Cite one to three decisive primary sources inline for external claims. A longer bibliography lives in an evidence artifact. Numbers carry units, baseline, and context; no unobserved “works,” “optimized,” or “quantum advantage” claim.
5. A user-requested format or depth takes precedence. Preserve the template's *information fields* in that format (for example, JSON keys or a code-file manifest); do not inject prose into a JSON-only or code-only answer. Keep a validated internal `ResponseEnvelope` even when headings cannot be displayed.

## Route by skill, not by whim

Fields listed below are in exact display order. The lead field is followed by `Status`, then the remaining fields. `Next` is a concrete next action or the single missing input, not “let me know.”

| Template ID | Skills (`q-mentor-` prefix omitted) | Lead; then fields after `Status` | Prose cap | Must carry |
|---|---|---|---:|---|
| `guide` | `help`, `learn` | `Answer`; `When to use`, `Next` | 100 | One plain-language explanation or best 1–3 skills; prerequisite or tiny example |
| `options` | `brainstorm` | `Best option`; `Alternatives`, `Tradeoff`, `Next` | 140 | Classical path and why a quantum path is or is not worth exploring |
| `evidence` | `research`, `pqc-scan` | `Finding`; `Evidence`, `Limit`, `Next` | 140 | Claim, source/date, confidence, and what the evidence does not establish |
| `frame` | `frame` | `Problem`; `Model`, `Assumption`, `Check` | 140 | Objective, units/constraints, unresolved assumption, feasibility check |
| `decision` | `verdict`, `exec` | `Decision`; `Why`, `Cost / risk`, `Next gate` | 140 | Classical baseline, confidence, business implication, decision boundary |
| `design` | `design` | `Design`; `Why`, `Check`, `Next` | 160 | Architecture choice, rejected alternative, acceptance test |
| `mapping` | `translate` | `Route`; `Preserved`, `Lost / limited`, `Next` | 160 | Source/target model, capability class, semantic loss or none |
| `evaluation` | `evaluate` | `Result`; `Baseline`, `Fairness / uncertainty`, `Next` | 160 | Same instance/budget, metric, variability, and limit on the conclusion |
| `conversion` | `convert` | `Result`; `Route`, `Equivalence`, `Optimization`*, `Validation`, `Files` | 180 | Complete target artifacts or exact diff; `E/C/R/A/U` route and observed tests |
| `code` | `implement`, `test` | `Result`; `Files`, `Checks`, `Next` | 180 | Complete files/diff or test report, exact commands, pass/fail counts |
| `review` | `review` | `Finding`; `Impact`, `Evidence`, `Fix / owner` | 140 | Highest-severity actionable finding first, or “No findings” with review scope |
| `improvement` | `improve` | `Failure`; `Proposed change`, `Regression`, `Review` | 160 | Sanitized lesson/source, failing eval first, consent and human review |

*`Optimization` appears only for an optimization request; say `not improved` when the fair comparison did not improve the declared metric. For `conversion`, `Route` spells out `exact`, `conditional`, `reimplementation`, `approximate`, or `unsupported` rather than assuming users know the letters. For `review`, repeat the four-field finding block at most three times; link a full findings artifact for more. Full `help` may instead render all registry-derived rows as `skill | use when | prerequisite | output`, up to 20 rows or 350 words, with no second hand-maintained menu.

## Copy-ready assessment patterns

Fit/verdict or executive decision:

```text
Decision: {classical now | run a bounded quantum experiment | no-go, and why}
Status: {complete | needs-input | blocked | unsupported | unverified}
Why: {one measured fact against a named classical baseline; confidence}
Cost / risk: {time, money, or technical risk most likely to change the choice}
Next gate: {one measurable threshold, approval, or material question}
```

Research, security, or evidence assessment:

```text
Finding: {one answer to the question}
Status: {status}
Evidence: {primary source/date and strongest relevant measurement}
Limit: {missing baseline, replication, access, or unresolved contradiction}
Next: {one decision or check}
```

Evaluation of an algorithm or provider choice:

```text
Result: {winner, tie, or insufficient evidence on the declared metric}
Status: {status}
Baseline: {classical or incumbent method, instance, metric, value}
Fairness / uncertainty: {same budget/seeds, interval or limitation}
Next: {one validation gate or decision}
```

These are field skeletons, not canned claims. A business answer spells out QUBO/QAOA once or avoids the acronym; a technical answer may link the underlying `EvidenceCard`, `BenchmarkRecord`, or `ResultRecord`.

## Copy-ready code patterns

Implementation or testing (show this compact result first, then link or include the complete requested files or exact diff):

```text
Result: {what changed or which test passed/failed}
Status: {status}
Files: {paths to complete files/diff or test report; “none” if blocked before writing}
Checks: {exact command and observed result; include failing test name and cause}
Next: {one repair, review, or no action}
```

Cross-hardware conversion:

```text
Result: {what was produced, or why no executable conversion is valid}
Status: {status}
Route: {source model -> target model; exact | conditional | reimplementation | approximate | unsupported}
Equivalence: {what was preserved, what was not, and the toy proof/decoder}
Validation: {syntax, import, local run, semantic test, versions; observed vs unavailable}
Files: {complete target files/diff and test fixture, or none}
```

For optimization, insert `Optimization: {declared metric, fixed budget, result or not improved}` between `Equivalence` and `Validation`. Show this compact result before inline code. Never truncate code to satisfy a prose cap. “Runnable” means complete imports, dependency pins, entry point, test command, and clean-environment observation; otherwise label the artifact `illustrative` or `unverified`. If execution requires credentials, do not imply a local test ran. For a review request, report findings without writing a patch unless the user asked for a fix.

## Build and enforcement contract

The builder creates one file per template under `templates/responses/` and a deterministic renderer/linter. Each registry entry has exactly one `template_id`; every `SKILL.md` contains this local instruction with its own ID: “For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/{template_id}.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.” Internal skills emit typed artifacts only.

Machine mode is JSON-only under `schemas/response-v3.schema.json` with `contract_version`, `status`, `mode`, `template_id`, `audience`, `result`, `evidence`, `uncertainty`, `validation`, `artifacts`, `skills_used`, and `next_action`; reject extra keys. The renderer maps the selected text fields into these keys and validates both shapes. A user-requested custom format changes presentation, not truth or test evidence.

Acceptance evals cover **every skill** in business, technical, detailed, JSON-only, code-only (where relevant), success, `needs-input`, `blocked`, `unsupported`, direct invocation, and multi-skill handoff. Assert one terminal answer, template ID, lead-first order, required fields, 1–3 decisive citations when needed, word cap, complete code, exact observed validation, no duplicate ending, and no false certainty. A format repair may run once; repeated failure is `blocked`, not a free-form fallback. Track output tokens and retries, but reject a shorter response that loses the decision boundary.
