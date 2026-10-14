# Compatibility matrix — Q-Mentor 3.1.1 (checked 2026-10-14)

Machine-readable source: `registry/compatibility.yml`. "Observed" means a command actually ran and passed here;
"unverified" means not run — never assume it passed.

## Packaging and clients

| Surface | Version | Check | Result |
|---|---|---|---|
| Agent Plugins manifest | schema 1.0.0 | offline validation against vendored schema | observed pass |
| Copilot CLI (plugin mode) | 1.0.97 | install, `skill list --json` (17), agent file shipped, disable/enable, uninstall | observed pass |
| Copilot CLI (repository mode) | 1.0.97 | `skill list --json` from `.github/skills` (17 project skills) | observed pass |
| Copilot CLI agent invocation, routing, behaviour evals | — | 52 live cases in `evals/behavior/cases.yml` | **unverified** (needs a licensed session) |
| Copilot cloud agent / app, VS Code agent mode | — | repository-local deployment | **unverified** |
| `gh skill publish --dry-run` | gh 2.89.0 | command not available | **unavailable** |

## Execution targets (all offline, CPython 3.13, x86_64 Linux)

| Target | Family / model | Pins | Tag SHA | Highest state |
|---|---|---|---|---|
| Qiskit | superconducting / gate | qiskit 2.5.2, qiskit-optimization 0.7.0 | `c1c01ada` | locally-executed |
| Cirq | superconducting / gate | cirq-core 1.7.0 | `de651a78` | locally-executed |
| pytket | trapped-ion compiler / gate | pytket 2.18.5 | `4a554cbc` | locally-executed |
| PennyLane | framework / gate | pennylane 0.45.1 | `5f61ce25` | locally-executed |
| Classiq | programming layer / gate | classiq 1.32.0 | (library ref `9e5b7bed`) | imported; synthesis unverified |
| D-Wave Ocean | flux annealer / anneal | dimod 0.12.22, dwave-samplers 1.8.0 | `3ecf9cc2`, `6bb7f674` | locally-executed |
| Pulser | neutral atom / analog | pulser 1.9.1 | `12891850` | locally-executed |
| Bloqade | neutral atom / analog | bloqade-analog 0.16.9, numpy 2.2.6 | `fd7f87e6` | locally-executed |
| Perceval | photonic / DV | perceval-quandela 1.3.1 | `64ed82f9` | locally-executed |

## Conversion bridges

| Route | Bridge | Status | Class |
|---|---|---|---|
| Qiskit → pytket | pytket-qiskit 0.78.0 (`6d0c2a01`) | maintained; symbols must be bound | E |
| Qiskit → Cirq | OpenQASM 2 subset (cirq-core 1.7.0 + ply 3.11) | maintained; dynamic circuits rejected | E |
| Qiskit → Perceval | perceval-interop 1.3.0 (`49480e97`) with qiskit 2.1.2 | maintained; package-import defect worked around | C |
| Pulser ↔ Bloqade | canonical Hamiltonian | C6 must be matched | E (matched) / A |
| BQM → Qiskit QAOA | canonical QUBO | — | R |
| Pulser → Classiq | canonical QUBO via ProgramIR | analog schedule not converted | R |
| pytket-cirq, pytket-pennylane, pytket-pyquil | — | unmaintained | refused |
| Qadence → Pulser | qadence 1.11.5 | "not actively maintained" (README, HEAD `cc314806`) | refused as default |
| Gate → CV photonics, electrons on helium, topological, silicon spin | — | no executable contract | U |

## Known issues

- bloqade-analog 0.16.9 fails at run time with numpy ≥ 2.3 → numpy 2.2.6.
- perceval-interop 1.3.0 package import fails without the `myqlm` extra → submodule import; detector test.
- pytket-qiskit 0.78.0 rejects unbound `Parameter`s → bind first.
- Copilot CLI direct plugin installs are deprecated in favour of marketplace installs.
