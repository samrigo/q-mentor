Status: complete

Decision
Run a bounded teaching experiment on Qiskit and D-Wave local samplers; production stays on enumeration.

Assumptions
Synthetic data only; learning is the goal.

Design
Canonical QUBO from `problem.json`; adapters for two targets; energy equivalence on all 64 states.

Validation
Not run.

Risks
Teams may read a toy match as advantage; the brief states evidence level 2.

Next
Approve the design so implementation can start.
