---
name: q-mentor-verdict
description: >
  Choose classical now, research/PoC, or bounded experiment. State why and when to
  revisit. Use after framing or when the user asks “should we use quantum?”. Maximum
  ~450 words. Must be able to recommend classical now without hedging.
---

# q-mentor-verdict

## Hard gates (apply before scoring)

- Problem size trivial for classical exact methods → **classical now**.
- No precise mathematical kernel → **not ready**.
- No strong classical baseline exists or is unfair → demand baseline first.
- Confidential / production data without workflow → stop.

## Scoring dimensions (after gates)

| Dimension | Points | Question |
|-----------|-------:|----------|
| Problem structure | 25 | Precise optimization / simulation / sampling / algebraic kernel? |
| Formulation quality | 20 | Variables, objective, constraints, encodings explicit? |
| Classical comparison | 20 | Strong baseline and reason it may be insufficient? |
| Hardware fit | 15 | Device / algorithm can express the kernel at relevant scale? |
| Evidence level | 10 | Public reproducible results at similar scale? |
| Cost & risk | 10 | End-to-end cost, queue, credential, governance acceptable? |

## Verdict enum

- `classical_now`
- `research_poc`
- `bounded_experiment`
- `not_ready`

## Output

Follow `templates/verdict.md`. Always name the classical alternative and the revisit condition.

## Knowledge links

- `knowledge/quantum-fit.md`
- `knowledge/research-method.md`
- `templates/verdict.md`
