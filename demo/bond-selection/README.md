# Demo: six-bond selection

A deliberately sober end-to-end walkthrough. The toy is useful for learning and provider translation; **exact classical enumeration is the production answer at this size.** All values are synthetic, normalized scores, not market data or investment advice.

## Problem

Select exactly 3 of 6 bonds, balancing yield score `mu`, covariance risk `Sigma`, and closeness to a total duration of 15.0:

```text
E(x) = 1.5 x^T Sigma x - mu^T x + 15 (sum(x) - 3)^2 + 0.25 (d^T x - 15)^2
```

`Sigma` is the full symmetric matrix, so cross terms count twice. Variable A is the leftmost bit. Inputs: [`problem.json`](problem.json); ground truth: [`expected.json`](expected.json).

| Result | Bits | Bonds | Energy |
|---|---|---|---:|
| Unique optimum | `101010` | A, C, E (yield 11.9, risk 1.67, duration 14.7) | -9.3725 |
| Next-best feasible | `100110` | A, D, E | -9.1675 |

## Run it (offline, no credentials)

```bash
pip install -e ".[dev,all-targets]"        # or just ".[dev]" for the core
python -m qmentor.demo                     # writes results/result-record.json and results/executive-brief.md
python -m qmentor.demo --skip-quantum      # skip the local QAOA simulations (~30 s)
```

The runner: validates the `ProblemSpec`, builds the canonical QUBO, enumerates all 64 states, proves penalty separation, runs a seeded simulated-annealing baseline, checks energy equivalence for Qiskit, PennyLane, Classiq (Pyomo model), and D-Wave (dimod) on all 64 states, issues the Pasqal/Pulser capability report, runs seeded local QAOA on Qiskit `StatevectorSampler` and PennyLane `default.qubit`, and writes the executive brief **only** from the result record.

## Lifecycle walkthrough in Copilot

| Step | Invoke | What you should get |
|---|---|---|
| 1 | `/q-mentor-learn` QUBO, penalties, provider paradigms | <=300 words, one formula, one misconception, source |
| 2 | `/q-mentor-research` one current optimization claim | Evidence card, `status: candidate`; knowledge base unchanged |
| 3 | `/q-mentor-frame` the business statement | Variables, units, objective, constraints, assumptions, validation plan |
| 4 | `/q-mentor-verdict` | **classical-now**; teaching PoC only (64 states are trivial to enumerate) |
| 5 | `/q-mentor-design` canonical model + local Qiskit and PennyLane | Exact solver, result schema, tests defined before quantum code |
| 6 | `/q-mentor-translate` Classiq, D-Wave, Pasqal/Pulser | Exact mappings preserve energy; Pulser reports `unsupported-exact` first |
| 7 | `/q-mentor-evaluate` the design | Baseline fairness, resources, evidence level, cost, stop conditions |
| 8 | `/q-mentor-implement`, then `/q-mentor-test` | Local, seeded, no credentials or paid jobs |
| 9 | `/q-mentor-review` | Math, code, thresholds, hardware fit, claims, simpler alternatives |
| 10 | `/q-mentor-exec` | One-page brief from `results/result-record.json` |
| 11 | `/q-mentor-improve` (only on explicit opt-in) | Sanitized lesson candidate and a failing eval |

## Why Pasqal/Pulser says no

Rydberg couplings are `C6 / r^6`: positive and fixed by geometry. This QUBO has 15 independent couplings among 6 atoms; the implied distances need a 5-dimensional embedding (MDS rank 5), and the non-uniform linear terms need local detuning that `AnalogDevice` lacks. The report lists alternatives and offers a 2D projection only as a labeled approximation with its coupling error.

## Second verdict fixture

"Use quantum computing to sort a 200-row CSV" must also return **classical-now** (`evals/behavior/behavior.yml`, `behavior-csv-sort`).
