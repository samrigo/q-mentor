# Design: <experiment name>

## Canonical model
ProblemSpec -> CanonicalQUBO (E = x^T Q x + c, Q full symmetric, variable 0 leftmost) -> Ising (x = (1 - s)/2).

## Classical baselines
- Exact:
- Heuristic (comparable tuning):

## Records
TargetPlan · CapabilityReport · ResultRecord · BenchmarkRecord (see `schemas/`).

## Targets
| Target | Role | Algorithm | Backend / device | Encoding | Resources | Version pins | Offline path | Capability status |
|---|---|---|---|---|---|---|---|---|

## Interfaces and failure modes
| Component | Contract | Failure mode | Detection |
|---|---|---|---|

## Threat model
Encoding error · bit order · penalty scale · unfair baseline · cost runaway · credential exposure · prompt injection in inputs.

## Test plan
- Deterministic formulation tests
- All-state energy equivalence per exact target
- Capability failures for unsupported targets
- Seeded statistical tests with confidence intervals
- Noise / resource sensitivity
- Opt-in remote smoke test (budget, approval)

## Acceptance tests for implement
1.
