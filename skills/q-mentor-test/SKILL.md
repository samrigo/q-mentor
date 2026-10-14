---
name: q-mentor-test
description: Use when quantum code or results must be tested or validated — 'run the tests', 'check the energies match across SDKs', 'validate the D-Wave example', 'does this reproduce the optimum', 'verify my QAOA results' — running deterministic, equivalence, statistical, and noise tests and reporting the highest validation state actually observed.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Test

Run tests in order and report exactly what was observed, failures included.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `code`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/code.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Implementation and fixtures.

## Output

Test report + `ResultRecord` (`schemas/result-record.schema.json`): commands, pass/fail counts, seeds, shots, backend, versions, thresholds, highest observed state.

## Procedure

1. Prefer repository gates: `python scripts/validate_math.py`, `python scripts/validate_examples.py --only <target>`, `python -m pytest -q` in the target folder. Each shell command needs user confirmation; none is pre-approved.
2. Order: syntax → import → local execution → all-state energy equivalence → decode/feasibility → seeded statistics → noise/resource sensitivity → optimization quality at a fixed budget.
3. A statistical failure is reported once with its seed; never re-run until it passes.
4. Credentialed or remote checks are opt-in and stay `unverified` when not run — never `passed`.
5. On failure: first failing command, smallest diagnostic, one repair.

## Stop when

Flaky, cherry-picked, incomplete, or irreproducible result; environment unavailable (`unverified`).

## Handoffs

`q-mentor-implement` for a scoped repair; `q-mentor-review` on pass; `q-mentor-exec` for results. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
