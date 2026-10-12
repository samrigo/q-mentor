# Knowledge index

Read **only** the pack a skill links. Each pack answers one question, stays under ~1,000 tokens, and cites entries in [sources.yml](sources.yml).

| Pack | Question it answers | Typical skills |
|---|---|---|
| [quantum-basics](quantum-basics.md) | What are qubits, gates, measurement, noise, and the hardware paradigms? | learn |
| [optimization-math](optimization-math.md) | How do QUBO, Ising, penalties, QAOA, and annealing work under our conventions? | learn, frame, design, translate, implement, test, review |
| [quantum-fit](quantum-fit.md) | When is a problem worth a quantum experiment, and how is evidence levelled? | brainstorm, verdict, evaluate, review, exec |
| [research-method](research-method.md) | How are research claims graded into evidence cards? | research, evaluate, improve |
| [providers-qiskit](providers-qiskit.md) | How does the canonical model map to Qiskit (gate model)? | design, translate, implement |
| [providers-classiq](providers-classiq.md) | How does it map to Classiq (high-level modeling and synthesis)? | translate |
| [providers-dwave](providers-dwave.md) | How does it map to D-Wave Ocean (BQM, annealing, hybrid)? | translate |
| [providers-pasqal-pulser](providers-pasqal-pulser.md) | What can Pasqal/Pulser neutral-atom programs represent exactly? | translate |
| [framework-pennylane](framework-pennylane.md) | How does it map to PennyLane (differentiable framework + device)? | design, translate, implement |
| [pqc](pqc.md) | Which cryptography is quantum-exposed, and what does NIST standardize? | learn, pqc-scan |

Domain packs live in [`../domains/`](../domains/). Execution-target packs are optional at install time (`scripts/deploy_repo_local.py --targets`).
