---
name: q-mentor-convert
description: Use when the user wants verified code moved across SDKs or hardware families, or asks whether converted code is better — 'convert this Pulser code to Classiq', 'port my Qiskit circuit to pytket and Perceval', 'rewrite this QUBO for D-Wave', 'is the Classiq QAOA version optimized'. Produces complete pinned files, a TranslationRecord, and an OptimizationRecord for optimization tasks.
license: MIT
allowed-tools: read, search, edit
---

# Q-Mentor · Convert

Produce complete, pinned target code only for a classified route, prove its class with a fixture, and measure optimization quality before using the word optimized.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/conversion-atlas.md`, `knowledge/providers-classiq.md`, `knowledge/providers-pasqal-pulser.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `conversion`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/conversion.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Parsed source + `ProgramIR` + `CapabilityReport` (translate runs first if missing); target SDK and version.

## Output

Complete files (README, lock, `main.py`, `adapter.py`, `test_example.py`, `expected.json`) or an exact diff; `TranslationRecord`; `ConversionEdge` entry; `OptimizationRecord` (`schemas/optimization-record.schema.json`) for optimization tasks.

## Procedure

1. Route by `knowledge/conversion-atlas.md`. Load only the requested edge, two provider packs, and one version-matched official example (README-12 map in `knowledge/sources.yml`). Check the bridge's maintenance state and open issues; unmaintained bridges are never the default.
2. Convert source → canonical problem and program semantics → capability report → target. Never line-by-line; never drop pulses, constraints, offsets, measurements, or decoding.
3. Prove the class: exact = all-state energy or operator equality (up to global phase, stated bit order); conditional = conditional distribution + unconditional success rate; reimplementation = same canonical energy and decode, algorithm change named; approximate = error tolerance; unsupported = negative fixture, no code.
4. Pulser → Classiq: shared QUBO → Classiq QAOA is reimplementation. Use named `cost_layer`/`mixer_layer`/`qaoa_ansatz`, `gammas=params[:p]`, `betas=params[p:]`; state `RX(θ)=exp(-iθX/2)` and test it; test `@qperm` vs `@qfunc` on the pinned SDK (see `knowledge/providers-classiq.md`).
5. Optimization: hold QUBO, penalty, feasible set, initial state, decode, and total budget fixed; compare p=1/2 first, p=4 only if the gap justifies it; ≥ 2 seeds, two optimizer modes where supported; never compare CVaR with mean energy. `improved` only on the predeclared metric without breaking the resource cap; else `not improved` and keep the simpler variant.
6. Run syntax → import → local run → semantic test in a clean pinned env (needs user confirmation for shell). Credential-gated steps stay `unverified`.

## Stop when

Missing SDK or source parse; unsupported mapping (return the negative result); unverified optimization claim.

## Handoffs

`q-mentor-test`, then `q-mentor-review` for material code; `q-mentor-evaluate` if the optimization claim needs assessment. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
