# Finance domain pack

`last_verified: 2026-10-12` · the first domain pack and the reference demo. The lifecycle, schemas, and evidence policy are domain-neutral; this pack adds vocabulary, models, failure modes, and fixtures only.

| File | Use |
|---|---|
| [portfolio-optimization](portfolio-optimization.md) | Binary mean-variance selection, penalties, and the six-bond demo model |
| [claims-and-limits](claims-and-limits.md) | What quantum-finance claims do and do not show; scope limits |

Fixture: [`demo/bond-selection`](../../demo/bond-selection/README.md).

Out of scope for every finance answer: investment recommendations, live trading, client data, positions, or production models.

## Adding another domain

Copy this folder's shape (`INDEX.md`, one model file, one claims-and-limits file, one toy fixture with an exact baseline). Do not fork lifecycle schemas, provider contracts, consent rules, or evidence policy.
