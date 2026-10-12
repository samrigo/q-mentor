---
name: q-mentor-brainstorm
description: >
  Suggest at most five quantum-computing use cases for a stated domain or problem
  class and rank their readiness. Use when the user asks “what could quantum help with”
  or wants a shortlist. Output one ranked table.
---

# q-mentor-brainstorm

## Workflow

1. Clarify domain and decision context if missing.
2. Propose ≤5 use cases.
3. Rank by readiness: classical production → research/PoC → bounded experiment → speculative.
4. For each, note the mathematical kernel and the strongest classical alternative.
5. Never claim readiness higher than current public evidence supports.

## Output

One table: Use case | Kernel | Readiness | Classical alternative | Key risk

## Knowledge links

- `knowledge/quantum-fit.md`
- `domains/finance/INDEX.md`
- `knowledge/research-method.md`
