# NMR, electrons on helium, and topological research

**Rule:** these paths are for teaching and assessment. NMR desktops are 2-3-qubit education devices; electron-on-helium and topological devices have no public programmable multi-qubit backend. None receives optimization code from Q-Mentor.

## Liquid-state NMR (SpinQ; academic tabletop systems)

- Ask: molecule and ensemble encoding (pseudo-pure states), polarization, pulse calibration, coherence, register size, which OS/backends the SDK supports.
- `profiled`: SpinQit simulator (`spinqit` on PyPI; docs label 0.2.4 while PyPI lists 0.3.0 — resolve before pinning). Gate → NMR is `E` only for a tiny verified gate set after a clean local build; until then capability report only.
- Evidence: NMR quantum computer for education (`hw-nmr-education-2024`) and desk-device reliability (`hw-nmr-desk-reliability-2025`) characterise small devices; neither establishes scalable optimization.

## Electrons on helium (EeroQ; research groups)

- Ask: charge versus spin encoding, electron shuttling, microwave coupling and readout, any measured two-qubit gate.
- `research-only`. The spin-qubit blueprint (`hw-helium-blueprint-2023`, preprint) proposes gates and readout; charge–photon strong coupling (`hw-helium-charge-photon-2026`) is device-level readout/control evidence. Do not infer programmable two-qubit computation.

## Topological / Majorana (Microsoft research program)

- Ask: what was measured (parity readout) versus inferred (topological protection); do programmable qubits exist?
- `research-only`. Q# and Azure Quantum are a language and access layer, not proof of a topological QPU.
- Evidence: interferometric parity measurement (`hw-topological-parity-2025`) and single-shot Kitaev-chain parity readout (`hw-kitaev-chain-readout-2026`) are device-level results; independent scrutiny (`hw-topological-scrutiny-commentary-2025`) is commentary, not a primary paper.

## How to answer

Return a capability report: family, computing model, what exists publicly, support level, the nearest `tested-local` path for learning (e.g., Qiskit simulator for gate logic), and the evidence boundary. A conversion request to these targets is `unsupported` with a negative fixture (`evals/hardware/cases.yml`).
