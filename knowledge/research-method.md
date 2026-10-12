# Research method: evidence cards

`last_verified: 2026-10-12` · sources: `hoefler-2023`

## Operational rule

Every material claim becomes an evidence card with a linked source. If no source is available, say so; never cite from memory. New cards are `candidate` until a maintainer promotes them.

## Source hierarchy (never flatten)

peer-reviewed > preprint > official documentation (for API facts) > vendor result > secondary commentary. Vendor documentation is authoritative for *how an SDK works*, not for *whether it beats classical methods*.

## Card fields

Claim (no marketing words) · Source and status · Boundary (problem, data, scale, hardware, algorithm, metric) · Baseline (current, strong, tuned, end to end?) · Artifacts (code, data, parameters, seeds, raw results) · Limitations (overheads, assumptions, omitted costs, negative results) · Replication (independent, same-team only, attempted and failed, unknown).

## Scoring (0-2 each, total 0-10, triage only)

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Source rigor | secondary/vendor marketing | preprint or vendor technical report | peer-reviewed |
| Baseline strength | none or naive (random search) | reasonable but untuned/partial | exact or strong, tuned, end to end |
| Artifact completeness | none | partial | code + data + seeds + raw results |
| Scale relevance | toy only | mid-size | decision-relevant scale |
| Replication | unknown | same team | independent |

Reading priority: >= 7 high, 4-6 medium, <= 3 low. A high score does not make a claim true.

## Red flags

Comparator is random search or an untuned default · time excludes compilation, queue, embedding, or decoding · "best of N runs" without distribution · hybrid solver reported as QPU result · advantage claimed from a simulator · no negative results reported.

## Contradictions

Keep conflicting cards side by side with their boundaries. Retain negative and null results; they prevent repeated hype.

## Freshness

Record `source_date` and `last_verified`; re-check SDK, pricing, hardware, and PQC status claims before release.
