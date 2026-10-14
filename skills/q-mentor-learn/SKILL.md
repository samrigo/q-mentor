---
name: q-mentor-learn
description: Use when the user wants a quantum-computing concept explained — 'explain QAOA', 'what is a QUBO', 'how does quantum annealing work', 'what is a cat qubit', 'difference between Pulser and Qiskit', 'why do penalties matter' — with a domain analogy, one formula, a misconception, and a source.
license: MIT
allowed-tools: read
---

# Q-Mentor · Learn

Teach one concept so the user can restate it or pass a tiny check.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/quantum-basics.md`, `knowledge/optimization-math.md`, `knowledge/hardware-index.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `guide`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/guide.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Concept, the user's level if known, domain (finance by default).

## Output

One explanation: analogy from the user's domain, exactly one formula, one common misconception, one source id from `knowledge/sources.yml`, and a one-line self-check.

## Procedure

1. Pick the single concept asked; if two are asked, explain the one the second depends on first and offer the other as `Next`.
2. Use `knowledge/quantum-basics.md` or `knowledge/optimization-math.md`; for hardware families use `knowledge/hardware-index.md` (physical family ≠ computing model ≠ SDK).
3. Business audience: avoid acronyms or spell them out once. Technical audience: name conventions (bit order, `RX(θ)=exp(-iθX/2)`).
4. Label any claim about performance as fact/assumption/estimate/unknown; never imply practical speedup.

## Stop when

Ambiguous goal or a prerequisite gap (needs-input with one question).

## Handoffs

`q-mentor-research` for a current claim; `q-mentor-frame` when the user has a real problem. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
