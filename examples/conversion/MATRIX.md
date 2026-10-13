# Five-by-five conversion matrix

Every cell goes source → `CanonicalProblem`/`ProgramIR` → `CapabilityReport` → target.
Statuses: `exact`, `reimplementation`, `approximate`, `unsupported`, `not-applicable`.
Mirrored in `registry/compatibility.yml` and checked by `scripts/validate_package.py`.

| Source ↓ / Target → | Qiskit | Classiq | D-Wave | Pasqal/Pulser | PennyLane |
|---|---|---|---|---|---|
| **Qiskit** (QUBO/QAOA) | not-applicable | exact (objective) | exact (BQM) | unsupported (six-bond); exact only for geometry-native QUBOs | exact |
| **Classiq** (Qmod QAOA) | exact (objective) | not-applicable | exact (BQM) | unsupported (six-bond) | exact |
| **D-Wave** (BQM) | exact | exact (objective) | not-applicable | unsupported (six-bond) | exact |
| **Pasqal/Pulser** (analog QAA) | reimplementation (QUBO only); analog schedule unsupported | reimplementation — [worked example](pulser-to-classiq/) | reimplementation (QUBO only) | not-applicable | reimplementation (QUBO only) |
| **PennyLane** (QNode QAOA) | exact | exact (objective) | exact (BQM) | unsupported (six-bond) | not-applicable |

"Exact" means identical canonical energy on every enumerated assignment and identical decoding.
It never means the same algorithm, hardware or performance. Gate-circuit ↔ gate-circuit conversion
of arbitrary programs (beyond the shared QUBO) is out of scope for v2.0.0 and must return `unknown`.

Evidence per cell: the energy-equivalence tests in each `examples/bond-selection/<target>/test_example.py`,
the Pulser capability report, and `evals/conversion/`.
