# Quantum finance: claims and limits

`last_verified: 2026-10-12` · sources: `egger-2020`, `hoefler-2023`

## Operational rule

Separate the **kernel** (optimization, Monte Carlo/amplitude estimation, ML) from the **business claim**. Most published finance results are formulated, executable, or competitive on a toy (levels 1-3). Treat any stronger claim as a candidate evidence card until reviewed.

## Common claims and what to check

| Claim pattern | Check before believing |
|---|---|
| "QAOA/annealing found the optimal portfolio" | Problem size; exact baseline; distribution over seeds; hybrid vs QPU; end-to-end time |
| "Quadratic speedup for Monte Carlo pricing" | Requires fault-tolerant amplitude estimation; state-preparation cost; error-correction overhead may erase quadratic gains |
| "Quantum ML outperforms classical" | Dataset size; tuned classical model; data-loading cost; replication |
| "Production-ready quantum risk engine" | Evidence level 4-5 with artifacts; otherwise reject |

## Scope limits for this plugin

- No investment recommendations, trading signals, or suitability statements.
- No client, position, or proprietary model data; synthetic or public data only.
- Model-risk, legal, and compliance approvals sit with the deploying organization, outside this plugin.
