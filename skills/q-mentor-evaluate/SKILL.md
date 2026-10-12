---
name: q-mentor-evaluate
description: >
  Grade a paper, proposal, or experiment against evidence, baseline, resources,
  reproducibility, and cost. Use when the user wants a scorecard. Output one scorecard.
---

# q-mentor-evaluate

## Scorecard dimensions

| Dimension | What to check |
|-----------|---------------|
| Evidence | Source type, claim clarity, replication status |
| Baseline | Strength, fairness, end-to-end measurement |
| Resources | Qubits / annealer size, depth, shots, embedding overhead |
| Reproducibility | Seeds, versions, artifacts, decoding rules |
| Cost | Queue, hardware, classical post-processing, opportunity cost |
| Stop conditions | When to abandon the quantum path |

## Output

One scorecard table + short recommendation (classical_now / continue_poc / stop).

## Knowledge links

- `knowledge/research-method.md`
- `templates/evidence-card.md`
- `templates/experiment-record.md`
