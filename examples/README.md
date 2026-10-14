# Examples

Two groups, both offline and credential-free by default:

- `bond-selection/<target>/` — the nine `tested-local` reference paths of `registry/backends.yml`, each anchored on
  the synthetic six-bond `CanonicalProblem` (`demo/bond-selection/problem.json`). They are reference
  implementations, not nine interchangeable hardware backends.
- `conversion/<route>/` — README-14 conversion fixtures: one representative route per class, plus the mandatory
  Pasqal/Pulser → Classiq optimization regression. Negative fixtures live in `evals/conversion/`.

Every folder is a complete project: `README.md`, `requirements.in` + `requirements.lock`, `main.py`, `adapter.py`,
`test_example.py`, `expected.json` (no notebooks, ellipses, `TODO`, wildcard pins, credentials, or network calls).

| Target | Family / model | Offline backend | Six-bond mapping | Highest observed state |
|---|---|---|---|---|
| [Qiskit](bond-selection/qiskit/) | superconducting / gate | `StatevectorSampler` | exact | `locally-executed` |
| [Cirq](bond-selection/cirq/) | superconducting / gate | `cirq.Simulator` | exact | `locally-executed` |
| [pytket](bond-selection/pytket/) | trapped-ion compiler / gate | exact statevector + compiler passes | exact (compiled unitary checked) | `locally-executed` |
| [PennyLane](bond-selection/pennylane/) | framework / gate | `default.qubit` | exact | `locally-executed` |
| [Classiq](bond-selection/classiq/) | programming + synthesis layer / gate | `create_model`, native Qmod | exact (objective) | `imported` — synthesis needs credentials, **unverified** |
| [D-Wave Ocean](bond-selection/dwave/) | flux annealer / anneal | `ExactSolver`, local SA | exact (BQM energy) | `locally-executed` |
| [Pasqal/Pulser](bond-selection/pasqal-pulser/) | neutral atom / analog | capability report + `QutipBackendV2` | **unsupported-exact**; geometry-native toy instead | `locally-executed` (native toy) |
| [Bloqade](bond-selection/bloqade/) | neutral atom / analog | bloqade python emulator | **unsupported-exact**; native 5-atom program instead | `locally-executed` (native program) |
| [Perceval](bond-selection/perceval/) | photonic / DV | `Processor("SLOS")` | **conditional-impractical** (success 1.8e-34); native 2-qubit program instead | `locally-executed` (native program) |

| Conversion fixture | Route | Class |
|---|---|---|
| [gate-to-gate](conversion/gate-to-gate/) | Qiskit → pytket (pytket-qiskit), Qiskit → Cirq (OpenQASM 2) | exact |
| [qiskit-to-perceval](conversion/qiskit-to-perceval/) | Qiskit → Perceval dual-rail (perceval-interop) | conditional |
| [pulser-to-bloqade](conversion/pulser-to-bloqade/) | Pulser ↔ Bloqade analog Hamiltonian | exact after C6 matching; approximate otherwise |
| [pulser-to-classiq-qaoa](conversion/pulser-to-classiq-qaoa/) | Pulser (5 atoms, 10 couplings) → Classiq QAOA with `OptimizationRecord` | reimplementation |
| [pulser-to-classiq](conversion/pulser-to-classiq/) | v2 four-atom ProgramIR walk-through | reimplementation |
| `evals/conversion/test_bqm_vs_qaoa.py` | D-Wave BQM → Qiskit QAOA | reimplementation (never "exact") |

Validation states: `draft` < `syntax-checked` < `imported` < `locally-executed` < `target-validated`. Nothing here is
`target-validated`: no hardware, cloud simulator, or credential was used.

```bash
python scripts/validate_examples.py              # fresh venv per folder from its lock; compileall + pytest
python scripts/validate_examples.py --only cirq  # one target
python scripts/validate_examples.py --static     # placeholder / undefined-name / stale-API / network scan only
```

Locks are compiled for CPython 3.13 on x86_64 Linux (`uv pip compile`). Re-lock for other platforms and record the
result in `registry/compatibility.yml`.
