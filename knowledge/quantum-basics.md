# Quantum basics

**Rule:** name the execution paradigm before discussing performance. Results from different paradigms are not interchangeable.

## Model
- A qubit state is `a|0> + b|1>` with `|a|^2 + |b|^2 = 1`; n qubits span `2^n` amplitudes, but measurement returns one n-bit string per shot.
- Gate-model programs apply unitary gates and measure; results are samples, so every statistic needs shots, seeds and confidence intervals.
- Noise (decoherence, gate and readout error) limits depth on current (NISQ) hardware; error correction trades many physical qubits for one logical qubit.

## Execution paradigms
| Paradigm | Example targets | What a result means |
|---|---|---|
| Statevector / shot simulator | Qiskit primitives, PennyLane `default.qubit` | Classical computation of an ideal or noise-modelled circuit |
| Gate-based hardware | IBM, IonQ, others via SDKs | Noisy samples from a physical device |
| Quantum annealer | D-Wave QPU | Low-energy samples of an Ising model after embedding |
| Hybrid solver | D-Wave hybrid, variational loops | Classical + quantum resources; not a pure-QPU benchmark |
| Analog neutral-atom | Pasqal via Pulser | Samples after pulse-driven Rydberg evolution; geometry sets couplings |

## Common misconception
"Quantum computers try every answer at once." Superposition does not give you all answers on readout; useful algorithms need interference that amplifies good answers, and many problems have no known exponential speed-up.

## Sources
Preskill 2018 (NISQ), Deutsch 1985 — see `sources.yml` (`preskill-2018`, `deutsch-1985`).
