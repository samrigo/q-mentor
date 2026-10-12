# End-to-End Demo: Six-Bond Selection

## Demo promise

The demo shows the complete Q-Mentor workflow while reaching an intentionally sober conclusion: the toy is useful for learning and provider translation, but exact classical enumeration is the production choice at this size.

All values are synthetic, normalized scores. They are not market data or investment advice.

## Problem

Select exactly three of six bonds. Balance expected yield, covariance risk, and closeness to a target total duration of `15.0`.

| ID | Label | Yield score `mu` | Duration `d` |
|---|---|---:|---:|
| A | Short Treasury | 2.8 | 2.1 |
| B | Agency | 3.2 | 3.8 |
| C | Investment-grade corporate | 4.1 | 5.2 |
| D | Municipal | 3.5 | 6.0 |
| E | BBB corporate | 5.0 | 7.4 |
| F | Long Treasury | 3.7 | 8.1 |

Use this symmetric, strictly diagonally dominant risk matrix:

```text
Sigma = [
  [0.20, 0.04, 0.03, 0.02, 0.01, 0.03],
  [0.04, 0.28, 0.06, 0.03, 0.04, 0.04],
  [0.03, 0.06, 0.45, 0.07, 0.12, 0.05],
  [0.02, 0.03, 0.07, 0.32, 0.05, 0.07],
  [0.01, 0.04, 0.12, 0.05, 0.70, 0.08],
  [0.03, 0.04, 0.05, 0.07, 0.08, 0.38]
]
```

For bit vector `x = [x_A, ..., x_F]`, minimize:

```text
E(x) = 1.5 x^T Sigma x - mu^T x
     + 15 (sum(x) - 3)^2
     + 0.25 (d^T x - 15)^2
```

The matrix product uses the full symmetric matrix, so cross terms occur twice when expanded. This convention must remain fixed across adapters.

## Ground truth

Enumerate all `2^6 = 64` assignments. The unique optimum is:

```text
x*          = [1, 0, 1, 0, 1, 0]  # A, C, E
bitstring   = 101010                # same left-to-right order as the vector
yield score = 11.9
risk        = 1.67
duration    = 14.7
energy      = -9.3725
```

The next-best feasible assignment is A, D, E with energy `-9.1675`; the gap is `0.2050`. Tests should use numeric tolerances rather than formatted strings.

## End-to-end user path

1. Invoke `q-mentor-learn` for QUBO, penalties, and provider paradigms.
2. Invoke `q-mentor-research` on one current optimization claim; produce an evidence card without changing the knowledge base.
3. Invoke `q-mentor-frame` with the business statement. It returns variables, units, objective, constraints, assumptions, and validation plan.
4. Invoke `q-mentor-verdict`. Expected answer: **classical now; quantum teaching PoC only** because 64 states are trivial to enumerate.
5. Invoke `q-mentor-design` for the canonical model and local Qiskit and PennyLane paths. Define the exact solver, result schema, and tests before quantum code.
6. Invoke `q-mentor-translate` for Classiq, D-Wave, and Pasqal/Pulser. Exact mappings must preserve energy; Pulser must first issue a representability report.
7. Invoke `q-mentor-evaluate` on the design. It checks baseline fairness, resources, evidence level, reproducibility, cost, and stop conditions.
8. Invoke `q-mentor-implement`, then `q-mentor-test`. Run the exact baseline and local simulators with fixed seeds; use no remote credentials or paid jobs.
9. Invoke `q-mentor-review`. It checks math, code, statistical thresholds, hardware fit, claims, and simpler alternatives.
10. Invoke `q-mentor-exec`. It produces a one-page brief from result records, not intentions.
11. If the user explicitly opts in, invoke `q-mentor-improve` to turn one observed failure or useful correction into a sanitized lesson candidate and a failing eval.

## Generated repository artifacts

The builder should create, but this brief does not prescribe exact filenames for:

- a validated JSON/YAML problem fixture;
- a canonical energy function;
- exhaustive enumeration and expected-result fixture;
- local Qiskit and PennyLane implementations;
- Classiq and D-Wave translation plans or adapters behind optional dependency groups;
- a Pasqal/Pulser capability report and, only if supported, a local-emulator plan;
- unit, property, and cross-provider equivalence tests;
- a machine-readable result record;
- a short executive report generated only from result records.

## Acceptance tests

- `Sigma` is symmetric and positive definite within numeric tolerance.
- Enumeration returns the unique bit vector and energy above.
- Every exact target encoding matches canonical energy for all 64 assignments after documented constant/sign conversion.
- PennyLane identifies its actual device (`default.qubit` for the offline demo) and its gradient/optimizer configuration.
- Pasqal/Pulser refuses an exact mapping when the QUBO cannot satisfy neutral-atom geometry, coupling, addressability, or device constraints; an approximation is never mislabeled as equivalent.
- Any sampled result is decoded in the declared bit order and marked feasible or infeasible.
- The report never calls matching the toy optimum an advantage.
- The default test suite works offline and without provider credentials.
- Live-provider tests are opt-in, budget-capped, and require explicit confirmation.
- The research card states source status, baseline, artifact availability, limitations, and replication status.
- No conversation text is retained unless the user opts in; retained lessons are sanitized summaries, not transcripts.

## Optional second verdict fixture

Include one obviously unsuitable request—“use quantum computing to sort a 200-row CSV”—whose expected verdict is classical now. This catches a common failure mode: recommending quantum merely because the user asked for it.

