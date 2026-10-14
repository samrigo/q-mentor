---
name: q-mentor-implement
description: Use when quantum code must be written from an accepted design — 'implement the Qiskit version', 'generate the D-Wave example', 'build the PennyLane QAOA project', 'write the Cirq circuit', 'create the runnable examples' — producing complete, version-pinned files or a scoped diff. Never placeholders.
license: MIT
allowed-tools: read, search, edit
---

# Q-Mentor · Implement

Make the smallest complete, pinned repository change from an accepted design, with rollback.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/providers-qiskit.md`, `knowledge/providers-dwave.md`, `knowledge/framework-pennylane.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `code`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/code.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Accepted `Design`, `TargetPlan`, test plan (design runs first if missing).

## Output

Complete files or a scoped diff following the example contract (`examples/README.md`): README with version and source link, `requirements.in` + lock, `main.py`, `adapter.py`, `test_example.py`, `expected.json`.

## Procedure

1. Confirm the design is accepted and the target is `tested-local` in `registry/backends.yml` (profiled → capability record only; research-only → no code).
2. Load only the provider pack for the target in use (Qiskit, D-Wave, PennyLane packs are listed; others via `registry/backends.yml`).
3. Use only APIs confirmed in a version-matched official example; reject `stale_apis` from `registry/compatibility.yml`.
4. Optional dependencies per target; no network, credentials, or paid jobs by default; remote paths sit behind an explicit environment flag and approval.
5. No `...`, `TODO`, undeclared names, or notebook-only state. Code you could not run is labelled `draft` or `syntax-checked`.

## Stop when

Required dependency, permission, or mapping absent; design not accepted.

## Handoffs

Always `q-mentor-test`; then `q-mentor-review` for material code. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
