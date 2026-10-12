---
name: q-mentor-learn
description: >
  Explain one quantum-computing or optimization concept with a domain-relevant analogy,
  formula, common misconception, and cited source. Use when the user asks “what is”,
  “explain”, or needs a mental model. Maximum ~300 words.
---

# q-mentor-learn

## Workflow

1. Identify the single concept the user asked about.
2. Load at most one knowledge pack from `knowledge/` (e.g. `quantum-basics.md`, `optimization-math.md`).
3. Structure the answer:
   - One-sentence definition
   - Domain-relevant analogy (prefer finance starter pack when relevant)
   - One core formula or rule
   - One common misconception and why it is wrong
   - One primary source or knowledge-pack citation
4. Stop at ~300 words. Offer a follow-up skill if the user wants to apply the concept.

## Output contract

- Fact / assumption / estimate / unknown labels where useful
- Classical baseline mentioned when the concept has a classical counterpart
- No advantage claims

## Knowledge links

- `knowledge/quantum-basics.md`
- `knowledge/optimization-math.md`
- `knowledge/quantum-fit.md`
- `domains/finance/INDEX.md` (when finance context is present)
