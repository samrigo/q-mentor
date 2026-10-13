# Examples

All examples solve or analyse the same synthetic six-bond `CanonicalProblem`
(`demo/bond-selection/problem.json`). Each target directory is a complete,
offline project: `README.md`, `requirements.in` + `requirements.lock`, `main.py`,
`adapter.py`, `test_example.py`, `expected.json`.

| Target | Role | Offline path | Mapping status | Highest observed validation state |
|---|---|---|---|---|
| [Qiskit](bond-selection/qiskit/) | Gate-model SDK | `StatevectorSampler` | exact | `locally-executed` |
| [PennyLane](bond-selection/pennylane/) | Framework (not a provider) | `default.qubit` | exact | `locally-executed` |
| [D-Wave Ocean](bond-selection/dwave/) | BQM / annealing stack | `ExactSolver`, local SA | exact | `locally-executed` |
| [Classiq](bond-selection/classiq/) | Modeling + synthesis platform | local `create_model`, native Qmod export | exact (objective) | `imported` — synthesis needs credentials, **unverified** |
| [Pasqal/Pulser](bond-selection/pasqal-pulser/) | Neutral-atom pulse programs | capability report + QutipBackendV2 | six-bond: **unsupported-exact**; geometry-native toy: exact | `locally-executed` (native toy only) |
| [Pulser → Classiq](conversion/pulser-to-classiq/) | Conversion through ProgramIR | as above | **reimplementation**; analog schedule unsupported-exact | `imported` |

Validation states follow README-03 of the build kit: `draft` < `syntax-checked`
< `imported` < `locally-executed` < `target-validated`. Nothing here is
`target-validated`: no hardware, cloud simulator or credential was used.

Run everything in clean, per-target environments:

```bash
python scripts/validate_examples.py            # creates fresh venvs from the locks, runs every test
python scripts/validate_examples.py --static   # placeholder/undefined-name/stale-API scan only
```

Locks were compiled for CPython 3.13 on x86_64 Linux. Re-run
`uv pip compile requirements.in -o requirements.lock` for other platforms and
record the result in `registry/compatibility.yml`.

The [cross-target matrix](conversion/MATRIX.md) classifies all 25 source→target cells.
