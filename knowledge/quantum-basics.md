# Quantum Basics (operational)

## Gate-based vs annealing vs analog

- **Gate-based** (Qiskit, many Classiq backends, PennyLane): discrete unitary circuits; QAOA is a hybrid variational method.
- **Annealing** (D-Wave): continuous-time evolution toward low-energy states of an Ising/BQM; hybrid solvers mix classical heuristics.
- **Neutral-atom analog** (Pasqal/Pulser): geometry-encoded interactions; addressability and device limits constrain which QUBOs are representable.

## Superposition & measurement

A qubit state is a unit vector in ℂ². Measurement in the computational basis collapses to 0 or 1 with probabilities given by the amplitudes. Sampling many shots estimates expectation values; it does not give the full statevector on hardware.

## Common misconception

“Quantum is always faster.” Speed depends on problem structure, encoding overhead, noise, queue time, and classical post-processing. For small combinatorial problems, exact classical enumeration is usually preferable.

## Source

Standard textbooks and provider documentation; see `sources.yml`.
