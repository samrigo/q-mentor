# Trapped ions and neutral atoms

**Rule:** ions and atoms are both "atomic" but program differently. Ions run gate circuits with high connectivity; neutral atoms run either analog Rydberg Hamiltonians (geometry-defined interactions) or gate circuits. An arbitrary dense QUBO is not an analog Rydberg program.

## Trapped ions (Quantinuum, IonQ, AQT)

- Ask: native entangler (MS/ZZ), all-to-all versus shuttling, mid-circuit measurement and reuse, shot time and cost per circuit.
- `tested-local`: pytket circuits and compilation passes (`examples/bond-selection/pytket/`). `profiled`: Quantinuum hardware via `qnexus` (device submission moved out of `pytket-quantinuum` at 0.56.0), IonQ (`qiskit-ionq`), AQT (`qiskit-aqt-provider`).
- Evidence: four logical qubits beyond break-even (`hw-ions-four-logical-qubits-2024`; listed as a preprint in the brief, now Phys. Rev. Lett. 133, 180601; postselected); fault-tolerant code switching (`hw-ions-code-switching-2025`); Helios 98-qubit system (`hw-helios-98-qubit-2026`, Publisher Correction 2026-07-07) — architecture benchmarks, not an optimization advantage.

## Neutral atoms (Pasqal, QuEra, Atom Computing)

- Ask: register geometry and minimum spacing, blockade radius, interaction `C6/r^6` (positive, distance-fixed; device-specific C6), global versus local addressing (detuning maps), atom movement, pulse limits, measurement basis, noise.
- `tested-local`: Pulser + pulser-simulation (`examples/bond-selection/pasqal-pulser/`), Bloqade analog emulator (`examples/bond-selection/bloqade/`). `profiled`: gate-mode backends (Pasqal, QuEra, Atom Computing).
- Representability: a QUBO maps exactly only if every coupling is positive and realisable as `C6/r^6` by some 2-D layout within device limits and the linear terms are implementable (uniform detuning, or local detuning where available). The six-bond QUBO is `unsupported-exact` (15 couplings, 9 geometric degrees of freedom).
- Evidence: reconfigurable-array logical processor (`hw-atoms-logical-processor-2023`); weighted-graph optimization with local light shifts (`hw-rydberg-weighted-graph-2025`) — hardware-specific encoding, small graphs; logical magic-state distillation (`hw-atoms-magic-state-2025`) is a fault-tolerance component, not QUBO execution.
