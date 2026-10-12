---
name: q-mentor-research
description: >
  Build an evidence card from primary sources or user-supplied papers. Identify
  contradictions and gaps. Use when the user asks for evidence, paper review, or
  current research status. Output one evidence table.
---

# q-mentor-research

## Workflow

1. Require an attached paper, URL, or repository file when live research tools are unavailable. Never invent citations.
2. Extract the material claim without marketing language.
3. Fill the evidence-card fields (see template).
4. Score 0–2 on: source rigor, baseline strength, artifact completeness, scale relevance, replication.
5. Label new claims `candidate` until a maintainer promotes them into a knowledge pack.

## Evidence card fields

| Field | Question |
|-------|----------|
| Claim | What exactly is asserted? |
| Source status | Peer-reviewed / preprint / official docs / vendor result / secondary |
| Boundary | Problem, data, scale, hardware, algorithm, metric measured |
| Baseline | Was the comparator current, strong, fairly tuned, end-to-end? |
| Artifacts | Code, data, parameters, seeds, raw results available? |
| Limitations | Overhead, assumption, negative result, omitted cost |
| Replication | Independent / same-team / failed / unknown |

## Knowledge links

- `knowledge/research-method.md`
- `knowledge/sources.yml`
- `templates/evidence-card.md`
