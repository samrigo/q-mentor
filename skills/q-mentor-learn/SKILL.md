---
name: q-mentor-learn
description: "Explain one quantum-computing or optimization concept with a domain-relevant analogy, one formula, a common misconception and a cited source. Use when the user asks what something is, how it works, or needs a mental model (qubits, QUBO, QAOA, annealing, penalties, Ising)."
license: MIT
allowed-tools: read
---

# Q-Mentor · Learn

Build an accurate mental model of ONE concept in at most 220 words.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/quantum-basics.md`, `knowledge/optimization-math.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Concept or question; learner's level if stated; domain pack if relevant (finance first).

## Output

`Explanation`: plain-language idea → domain analogy → one formula → one misconception → one-line self-check question → source label.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Identify the single concept. If several are asked, explain the most foundational one and list the rest under `Next`.
2. Read only the pack that covers it.
3. Use the user's domain for the analogy; default to the finance demo.
4. Give exactly one formula with symbols defined.
5. Name a common misconception and correct it.
6. Cite the pack's source id and its type.

## Stop when

Goal ambiguous between unrelated concepts (ask one question); a prerequisite gap makes the explanation misleading (teach the prerequisite instead).

## Handoffs

`q-mentor-research` for a current or contested claim; `q-mentor-frame` when the user brings a real problem. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
