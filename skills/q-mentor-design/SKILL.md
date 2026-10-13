---
name: q-mentor-design
description: "Produce a target-neutral design and target-specific starter plan (canonical model, exact baseline, result schema, target plans, tests, stop condition) after a positive or teaching-PoC verdict. Use when the user wants to plan an experiment or architecture."
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Design

Fix every interface before code; ≤ 600 words.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/optimization-math.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Accepted `Verdict` and `CanonicalProblem`.

## Output

`templates/provider-design.md`: canonical model, exact baseline, `ResultRecord` fields, per-target plan with pins and CapabilityReport status, test plan, threat model, stop condition.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Keep business math SDK-independent; adapters may change syntax, never the objective.
2. Specify the exact classical baseline and the expected fixture result.
3. For each named target: algorithm, backend/device (offline first), encoding, resource estimate, version pins, capability status (`exact`, `approximate`, `unsupported-exact`, `unknown`).
4. Test plan: deterministic formulation/decoding, cross-target energy equivalence on all enumerable states, seeded statistics, noise sensitivity, opt-in remote smoke tests.
5. Every component gets a contract and a failure mode.

## Stop when

The design cannot preserve the canonical objective; verdict missing or classical-now without a teaching request.

## Handoffs

`q-mentor-translate` for named targets, then `q-mentor-evaluate`. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
