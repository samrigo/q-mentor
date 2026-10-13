---
name: q-mentor-review
description: "Review math, code, hardware fit, claims, tests and simpler classical alternatives for quantum-computing work and report findings only. Use before accepting generated code or advice, or when asked to sanity-check a diff or result."
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Review

Findings with severity and evidence; no rewrites.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/optimization-math.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Diff, files, artifacts, claims.

## Output

Findings list: severity (high/medium/low) · location · evidence · why it matters · suggested fix. If none: `Result: No findings` and what was checked.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Objective faithful to the business problem? Units, bit order, matrix convention, penalties explicit?
2. Baseline strong and fairly tuned? Feasibility and decoding tested independently of the sampler?
3. Resources and costs end to end? Seeds, versions, backend metadata recorded?
4. Code: placeholders, undefined names, stale APIs (`registry/compatibility.yml`), undeclared network calls, secrets.
5. Conclusion matches the evidence level? Could classical software do this more simply?
6. If cryptography appears, recommend `q-mentor-pqc-scan`.

## Stop when

Material risk lacks mitigation or owner (escalate).

## Handoffs

`q-mentor-implement`/`q-mentor-test` for accepted fixes; `q-mentor-pqc-scan` when crypto is in scope. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
