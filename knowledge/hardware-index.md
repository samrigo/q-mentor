# Hardware index: family, model, SDK, support level

**Rule:** a recommendation names five things separately — physical family, computing model, SDK/package and version, concrete backend, and support level. A provider name alone never justifies code. Read the one matching record in `registry/backends.yml`; do not load the whole catalog.

## Support levels

| Level | Meaning | What Q-Mentor may emit |
|---|---|---|
| `tested-local` | A pinned offline example passes in a clean environment | Complete runnable code + tests |
| `profiled` | Documented capability + positive/negative fixture, no local adapter | Capability report and a link to a versioned official example; no runnable claim |
| `research-only` | No public, versioned, executable contract verified | Teaching and assessment only; executable conversion is `unsupported` |

## Families (README-11)

| Physical family | Computing model(s) | tested-local | profiled | research-only |
|---|---|---|---|---|
| Superconducting circuits | gate | Qiskit (IBM), Cirq (Google) | pyQuil (Rigetti), IQM client, OQC QAT | — |
| Superconducting bosonic/cat | gate (logical/physical cat) | — | Alice & Bob Qiskit provider emulators | AWS Ocelot |
| Superconducting flux annealer | anneal (BQM/CQM) | D-Wave Ocean local samplers | D-Wave QPU / Leap hybrid | — |
| Trapped ions | gate | pytket (Quantinuum compiler, local) | Quantinuum hardware via qnexus, IonQ, AQT | — |
| Neutral atoms | analog (Rydberg); gate | Pulser (Pasqal), Bloqade analog (QuEra) | Pasqal/QuEra/Atom gate backends | — |
| Photonics | photonic-DV; photonic-CV | Perceval (Quandela, DV) | PennyLane photonic device plugins | PsiQuantum, ORCA; Strawberry Fields is archived history |
| Silicon spin / quantum dots | gate | — | — | Diraq, Quantum Motion, Intel, SQC |
| Diamond / colour centres | gate (small register) | — | Qristal (Quantum Brilliance) | — |
| Liquid-state NMR | gate (2-3 qubit, education) | — | SpinQit simulator | — |
| Electrons on helium | gate (proposed) | — | — | EeroQ and research groups |
| Topological / Majorana | gate (proposed) | — | — | Microsoft topological program (Q# is a language, not a QPU) |

Access/programming layers — Amazon Braket, Azure Quantum, Classiq, PennyLane, CUDA-Q, Qiskit, pytket, Q# — are stored separately from backends. PennyLane `default.qubit`, Classiq synthesis, and every SDK simulator are simulators, never evidence of QPU support.

## Questions to ask before recommending

- Gate: native gates, coupling graph, dynamic circuits, calibration age, two-qubit error, depth.
- Anneal: QUBO/Ising convention, topology/embedding, chain strength, schedule, hybrid-solver boundary.
- Analog Rydberg: geometry, blockade, `C6/r^6` interaction sign, local addressing, pulse limits.
- Photonic: modes, photon number/loss, heralding/postselection rate, detector model, DV vs CV.
- Cat/NMR/diamond: physical vs logical qubit, noise bias, register size, operating conditions.
- Research-only: what was measured vs inferred; is there a programmable multi-qubit device at all?

Compare at most three suitable paths plus one classical path. Sources: `hw-ibm-utility-2023`, `hw-google-below-threshold-2025`, `hw-rydberg-weighted-graph-2025` in `sources.yml`.
