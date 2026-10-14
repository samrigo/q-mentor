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

The user asks once: “Analyze, design, implement, and validate the six-bond example across the supported targets.” The orchestrator then applies the following skills without requiring slash commands:

1. `q-mentor-learn` explains QUBO, penalties, and execution paradigms only if the user's request or profile indicates a learning need.
2. `q-mentor-research` checks one current optimization claim and creates an evidence card without changing the knowledge base.
3. `q-mentor-frame` returns variables, units, objective, constraints, assumptions, and validation plan.
4. `q-mentor-verdict` returns **classical now; quantum teaching PoC only** because 64 states are trivial to enumerate.
5. `q-mentor-design` defines the canonical model, exact solver, result schema, target plans, and tests before quantum code.
6. `q-mentor-translate` produces capability mappings for the nine `tested-local` paths in README-11; `q-mentor-convert` generates complete code only for representable targets. Pulser and Bloqade first issue geometry/interaction reports; Perceval reports photon and postselection constraints.
7. `q-mentor-evaluate` checks baseline fairness, resources, evidence level, reproducibility, cost, and stop conditions.
8. `q-mentor-implement` and `q-mentor-test` create and validate complete local examples with fixed seeds; they use no remote credentials or paid jobs.
9. `q-mentor-review` checks math, syntax/import evidence, code, statistics, hardware fit, claims, and simpler alternatives.
10. `q-mentor-exec` produces a one-page brief from result records, not intentions.
11. `q-mentor-improve` runs only after explicit opt-in and turns an observed failure or correction into a sanitized lesson candidate and failing eval.

## Generated repository artifacts

The builder should create, but this brief does not prescribe exact filenames for:

- a validated JSON/YAML problem fixture;
- a canonical energy function;
- exhaustive enumeration and expected-result fixture;
- local Qiskit and PennyLane implementations;
- complete Classiq and D-Wave examples behind optional dependency groups;
- a Pasqal/Pulser capability report and, only if supported, a complete local-emulator example;
- local Cirq, pytket, Bloqade, and Perceval examples where the canonical problem is representable, or a tested unsupported report;
- `ProgramIR` and `TranslationRecord` files for the Pasqal/Pulser-to-Classiq path;
- a separate five-variable, ten-term QUBO Pasqal/Pulser-to-Classiq regression with p=1/2/4 and `OptimizationRecord`; it must not replace the six-bond demo fixture;
- unit, property, and cross-provider equivalence tests;
- a machine-readable result record;
- a short executive report generated only from result records.

## Acceptance tests

- `Sigma` is symmetric and positive definite within numeric tolerance.
- Enumeration returns the unique bit vector and energy above.
- Every exact target encoding matches canonical energy for all 64 assignments after documented constant/sign conversion.
- Every generated Python file passes `compileall`, imports in a clean pinned environment, and runs its offline smoke test. Classiq synthesis or remote execution that requires credentials remains a separate opt-in gate.
- Each example contains a dependency file, complete entry point, seed, fixture, expected output, validation command, SDK version, and source link; no notebook-only hidden state, ellipses, or undefined names.
- PennyLane identifies its actual device (`default.qubit` for the offline demo) and its gradient/optimizer configuration.
- Pasqal/Pulser refuses an exact mapping when the QUBO cannot satisfy neutral-atom geometry, coupling, addressability, or device constraints; an approximation is never mislabeled as equivalent.
- The conversion eval includes one intentionally incomplete or outdated source fixture and proves that v3 rejects it instead of returning partial Classiq code.
- The Classiq QAOA regression checks named layers, a version-tested `@qperm`/`@qfunc` choice, explicit beta convention, sliced parameter arrays, and a fair optimizer/depth comparison. It may report `not-improved`; four layers are not assumed sufficient.
- Separate README-14 fixtures demonstrate gate↔gate, Pulser↔another Rydberg analog model, QUBO→anneal versus gate reimplementation, and gate→photonic DV; the six-bond demo itself does not pretend every hardware family can represent the portfolio objective.
- Any sampled result is decoded in the declared bit order and marked feasible or infeasible.
- The report never calls matching the toy optimum an advantage.
- The default test suite works offline and without provider credentials.
- Live-provider tests are opt-in, budget-capped, and require explicit confirmation.
- The research card states source status, baseline, artifact availability, limitations, and replication status.
- No conversation text is retained unless the user opts in; retained lessons are sanitized summaries, not transcripts.
- The final user-facing success response follows the terminal skill's mandatory `qmentor.response.v3` template and stays within its word budget unless the user asks for detail.

## Optional second verdict fixture

Include one obviously unsuitable request—“use quantum computing to sort a 200-row CSV”—whose expected verdict is classical now. This catches a common failure mode: recommending quantum merely because the user asked for it.

