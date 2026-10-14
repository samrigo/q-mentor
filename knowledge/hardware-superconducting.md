# Superconducting hardware: gate, cat, and flux annealing

**Rule:** three different machines share the word "superconducting". Gate processors (IBM, Google, Rigetti, IQM, OQC) run circuits; bosonic/cat-qubit devices (Alice & Bob; AWS Ocelot research) trade one error type for another; D-Wave flux annealers sample a binary quadratic model. Never move a claim from one to another.

## Gate circuits

- Ask: native gates, coupling graph, dynamic circuits (mid-circuit measure/reset/feed-forward), calibration age, two-qubit error, depth after transpilation.
- `tested-local`: Qiskit `StatevectorSampler` (`examples/bond-selection/qiskit/`), Cirq `Simulator` (`examples/bond-selection/cirq/`). `profiled`: pyQuil (Rigetti), `iqm-client[qiskit]` (the old `qiskit-on-iqm` repo is archived), OQC QAT.
- Evidence: the IBM utility experiment (`hw-ibm-utility-2023`) is about error-mitigated expectation values compared with specific classical methods at that date; it is not an optimization advantage, and its classical comparison must be rechecked against later classical work before citing. Google's below-threshold surface-code memory (`hw-google-below-threshold-2025`, corrected in 2026 `hw-google-below-threshold-correction-2026`) shows logical-memory scaling, not application speedup.

## Bosonic / cat qubits

- Ask: physical versus logical cat qubit, noise bias (bit-flip suppressed, phase-flip not), bias-preserving gate set, emulator versus QPU.
- `profiled`: Alice & Bob `qiskit-alice-bob-provider` local emulators — pending a clean pinned build; a logical emulator is not QPU evidence. AWS Ocelot: `research-only`.
- Evidence: protected cat-qubit control (`hw-cat-qubit-control-2024`, with an axis-unit correction) — bit-flip protection under control, not universal fault tolerance; concatenated bosonic memory (`hw-concatenated-bosonic-memory-2025`); LDPC-cat codes (`hw-ldpc-cat-codes-2025`) are a theoretical resource estimate.

## Flux annealing (D-Wave)

- Ask: QUBO/Ising sign convention and offset, Pegasus/Zephyr topology and embedding, chain strength and chain breaks, anneal schedule, reads, and whether a *hybrid* solver (classical + QPU) produced the answer.
- `tested-local`: dimod `ExactSolver` and `dwave-samplers` simulated annealing (`examples/bond-selection/dwave/`). `profiled`: QPU and Leap hybrid (credentialed, paid).
- Evidence: annealing applications versus classical solvers (`hw-annealing-vs-classical-2025`) stresses benchmark design; annealing error mitigation (`hw-annealing-error-mitigation-2025`) has hardware-model assumptions; the end-to-end portfolio preprint (`rr-portfolio-annealing-e2e-2025`) mixes classical allocation and quantum selection — separate them before citing.
