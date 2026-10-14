---
name: q-mentor-translate
description: Use when the user wants a quantum problem or program mapped between execution targets without code yet — 'can this run on Pasqal', 'what is lost moving my Qiskit circuit to Perceval', 'compare how each SDK represents this QUBO', 'map this Pulser sequence to Bloqade' — producing a CapabilityReport and TranslationRecord through a canonical model.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Translate

Classify a source → target route by computing model and state exactly what survives, before any code.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/conversion-atlas.md`, `knowledge/hardware-index.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `mapping`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/mapping.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

`CanonicalProblem` or parsed source code (`SourceCode`); target.

## Output

`ProgramIR`, `CapabilityReport`, `TranslationRecord` (schemas in `schemas/`) with route class: exact, conditional, reimplementation, approximate, unsupported.

## Procedure

1. Pin the source SDK version; the source must parse/import. If not, reject or repair first.
2. Extract `ProgramIR`: variables, objective, constants, bit/wire order, Hamiltonian, geometry, gates or pulses, timing, initial state, measurement, decoding, backend assumptions.
3. Look up both endpoints in `registry/backends.yml` (support level, model) and the route class in `knowledge/conversion-atlas.md` / `registry/conversion-edges.yml`. A shared QASM file, language, or cloud is not hardware equivalence.
4. Exact only on the supported subset with a proof fixture; conditional reports postselection success; reimplementation names the algorithm change; approximate states an error bound; unsupported names the nearest valid alternative.
5. Research-only targets → unsupported for executable code. Never route through an unmaintained bridge by default.

## Stop when

Target cannot represent the semantics and no approximation was approved; source does not parse; SDK version unknown.

## Handoffs

`q-mentor-convert` when code is requested; otherwise `q-mentor-evaluate`. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
