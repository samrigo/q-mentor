# Quantum basics

`last_verified: 2026-10-12` · sources: `feynman-1982`, `deutsch-1985`, `preskill-2018`

## Operational rule

Explain quantum behavior with the classical baseline in view. A qubit is not "both 0 and 1 doing parallel work"; useful algorithms need interference that amplifies good answers and a readout that preserves the gain.

## Core ideas

- **Qubit state:** |psi> = a|0> + b|1>, with |a|^2 + |b|^2 = 1. Measuring gives 0 with probability |a|^2. n qubits have 2^n amplitudes, but one measurement returns only n bits.
- **Gates** are unitary operations; circuits compose them. **Entanglement** creates correlations no product of single-qubit states can produce.
- **Measurement** samples; estimating a probability p to precision e needs on the order of 1/e^2 shots.
- **Observables:** Pauli Z has eigenvalues +1 (|0>) and -1 (|1>); diagonal Hamiltonians of Z and ZZ terms encode QUBO/Ising energies.

## Hardware paradigms (do not mix their results)

| Paradigm | Examples | What a result means |
|---|---|---|
| Gate-based (digital) | superconducting, trapped-ion, neutral-atom digital mode | circuit executed on a QPU or a simulator |
| Quantum annealing | D-Wave QPUs | low-energy samples of an Ising model after embedding |
| Analog / pulse | neutral atoms (Pasqal) | evolution under a native Hamiltonian set by geometry and pulses |
| Hybrid solver | vendor hybrid services | classical + quantum pipeline; not a pure-QPU benchmark |
| Simulator | statevector, tensor network | classical computation; exact or noisy emulation |

## NISQ reality

Current devices are noisy and limited in qubit count and depth. Error mitigation reduces bias at extra sampling cost; full fault tolerance requires error correction with large physical-to-logical overheads. Resource estimates must separate logical from physical qubits.

## Common misconceptions

- "Exponential state space means exponential speedup": readout and data loading usually erase it.
- "Simulator success proves hardware success": noise, connectivity, and queue time are absent.
- "More qubits is always better": quality, connectivity, and depth matter as much as count.

## Classical counterpart

For any toy that fits in memory (tens of variables), exact classical methods are the reference answer.
