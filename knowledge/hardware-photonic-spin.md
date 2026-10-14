# Photonic, silicon-spin, and diamond hardware

**Rule:** photonic results are often *conditional* on detecting the right photons. Always report the unconditional success (heralding/postselection) rate next to any fidelity. Silicon-spin devices have no public versioned execution route here; diamond registers are small.

## Photonics (Quandela, Xanadu; PsiQuantum, ORCA)

- Ask: discrete-variable (DV, photons in modes) or continuous-variable (CV, squeezed light); modes per qubit (dual-rail = 2), photon and ancilla count, source brightness/indistinguishability, loss, detector model, feed-forward, postselection.
- `tested-local`: Perceval local processor (DV) — `examples/bond-selection/perceval/` and the gate→photonic fixture `examples/conversion/qiskit-to-perceval/`. `profiled`: PennyLane photonic device plugins. `research-only`: PsiQuantum, ORCA. Strawberry Fields (CV) is archived — historical reference only.
- A postselected dual-rail CNOT succeeds only part of the time; an n-gate circuit's success shrinks multiplicatively. Report it.
- Evidence: high-dimensional cluster states (`hw-photonic-cluster-states-2024`); manufacturable platform (`hw-photonic-manufacturable-2025`) — component benchmarks conditional on detection, excluding loss; boosted Bell measurements (`hw-photonic-boosted-bell-2025`).

## Silicon spin / quantum dots (Diraq, Quantum Motion, Intel, SQC)

- Ask: exchange gates, shuttling, control wiring, connectivity, readout, operating temperature.
- All `research-only` until a public provider SDK and backend contract are verified. No execution code.
- Evidence: pipeline architecture (`hw-silicon-pipeline-2024`, proposal); four-qubit Grover (`hw-silicon-grover-2025`, small demonstration); foundry unit cells > 99 % fidelity (`hw-silicon-foundry-2025`, fabrication and gate fidelity).

## Diamond / colour centres (Quantum Brilliance)

- Ask: register size, electron/nuclear-spin control, connectivity, noise, room-temperature claims.
- `profiled`: Qristal (`qristal-core`, C++/Python, local simulator) — not pip-installable as a pinned wheel at build time; promote after a clean build.
- Evidence: NV–photon teleportation (`hw-nv-teleportation-2024`), hybrid NV node with error correction (`hw-nv-network-node-2025`), room-temperature register benchmarking (`hw-nv-room-temperature-2025`) — network components and small-register characterisation.
