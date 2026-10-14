# Knowledge index

Load one pack at a time. Each pack answers one question, stays under ~1,000 tokens,
and lists its sources in `sources.yml` with `last_verified` dates.

| Pack | Question it answers | Volatility |
|---|---|---|
| [quantum-basics.md](quantum-basics.md) | What are qubits, gates, measurement, and the execution paradigms? | stable |
| [optimization-math.md](optimization-math.md) | How do QUBO, Ising, penalties, QAOA and annealing fit together? | stable |
| [quantum-fit.md](quantum-fit.md) | When is quantum worth trying, and how is the verdict scored? | active |
| [research-method.md](research-method.md) | How are claims graded and promoted? | stable |
| [providers-qiskit.md](providers-qiskit.md) | How does the canonical model map to Qiskit? | volatile |
| [providers-classiq.md](providers-classiq.md) | How does the canonical model map to Classiq/Qmod? | volatile |
| [providers-dwave.md](providers-dwave.md) | How does the canonical model map to D-Wave Ocean? | volatile |
| [providers-pasqal-pulser.md](providers-pasqal-pulser.md) | When can a QUBO run on neutral atoms with Pulser? | volatile |
| [framework-pennylane.md](framework-pennylane.md) | How does the canonical model map to PennyLane? | volatile |
| [recent-research.md](recent-research.md) | Which recent papers are on the watchlist, and what do they not show? | active |
| [hardware-index.md](hardware-index.md) | Which family, model, SDK, backend and support level apply? | active |
| [hardware-superconducting.md](hardware-superconducting.md) | Gate, cat-qubit, and flux-annealer facts and evidence | active |
| [hardware-ions-atoms.md](hardware-ions-atoms.md) | Trapped ions and neutral atoms: questions, paths, evidence | active |
| [hardware-photonic-spin.md](hardware-photonic-spin.md) | Photonic DV/CV, silicon spin, diamond | active |
| [hardware-nmr-helium.md](hardware-nmr-helium.md) | NMR, electrons on helium, topological research limits | active |
| [conversion-atlas.md](conversion-atlas.md) | Which conversion class applies to a source/target pair, and what proves it? | volatile |
| [pqc.md](pqc.md) | What does a post-quantum crypto inventory look for? | active |

Domain packs live in `domains/<domain>/`. Organisation-specific lessons never go here.
