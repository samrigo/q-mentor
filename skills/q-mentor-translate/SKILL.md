---
name: q-mentor-translate
description: "Map one canonical problem or source program to execution targets (Qiskit, Classiq, D-Wave, Pasqal/Pulser, PennyLane) through ProgramIR and a CapabilityReport, with a TranslationRecord. Use for convert, port, translate or 'same problem in another SDK' requests."
license: MIT
allowed-tools: read, search
---

# Q-Mentor · Translate

Semantic translation with an explicit status; one comparison table by default.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/providers-pasqal-pulser.md`, `knowledge/providers-classiq.md`, `knowledge/providers-qiskit.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

`CanonicalProblem` (frame first if missing) or source code; target(s).

## Output

Comparison table: semantic element · source · target · status. Plus `CapabilityReport` and `TranslationRecord` (schemas in `schemas/`). Load only the provider packs for the targets named (≤ 3).
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Pin the source SDK version; the source must import or parse. If not, repair or reject first.
2. Extract `ProgramIR`: variables, objective, constants, bit/wire order, Hamiltonians, register geometry, gates or pulses, timing, initial state, measurements, decoding, backend assumptions.
3. Per target, emit a `CapabilityReport`: `exact`, `approximate` (with error bound), `unsupported-exact`, or `unknown`.
4. Pasqal/Pulser: check coupling signs, geometry degrees of freedom, device distances, addressability/DMM, pulse limits before any code. Pulser → Classiq is never line-by-line: shared QUBOs are a *reimplementation*; analog evolution is `unsupported-exact`.
5. State conventions: Qiskit little-endian bitstrings; dimod SPIN = −canonical spin; PennyLane wire order; Classiq global-phase constant.
6. Code only for `exact` or user-approved `approximate` mappings, via `q-mentor-implement`.

## Stop when

Target cannot represent the semantics exactly and no approximation was approved; source does not parse; SDK version unknown.

## Handoffs

`q-mentor-evaluate`; `q-mentor-implement` only for exact or approved approximate mappings; `q-mentor-test`. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
