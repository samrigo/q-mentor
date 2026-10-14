# Gate → photonic DV conversion (README-14 class C, conditional)

- **Pins:** `perceval-quandela==1.3.1`, `perceval-interop[qiskit]==1.3.0`, `qiskit==2.1.2`, `scipy==1.16.3`;
  CPython 3.13, x86_64 Linux. perceval-interop 1.3.0 declares `qiskit~=2.1.2`, so this fixture uses the
  bridge-matched Qiskit, not the 2.5.2 pinned elsewhere.
- **Route:** Qiskit gate circuit → Perceval dual-rail `Experiment` via `QiskitConverter().convert(qc, use_postselection=True)`
  → local `Processor("SLOS")`, perfect source.

| Circuit | Conditional match (TVD vs gate model) | Unconditional success | Modes (heralded) |
|---|---|---|---|
| QAOA layer, bonds A/C (2 CNOTs on one pair) | 7 × 10⁻¹⁶ | 0.0082 (2/27 × 1/9) | 4 (+4) |
| Bell (1 CNOT) | 1 × 10⁻¹⁶ | 0.111 (1/9) | 4 (+2) |
| GHZ-3 (2 CNOTs) | 1 × 10⁻¹⁶ | 0.0123 (1/81) | 6 (+4) |

The conditional distribution is exact; execution is not deterministic. A report that shows the match without the
success rate, or labels the route `E`, is rejected by `adapter.validate_claim` (tested).

**Upstream defect (observed 2026-10-14):** `import perceval_interop` raises `ImportError: cannot import name
'MyQLMCommunicationLayer'` unless the optional `myqlm` extra is installed — the package `__init__` re-exports a name
its fallback branch never defines. `adapter.load_converter` imports the Qiskit converter submodule without running
that `__init__`; `test_upstream_import_defect_documented` fails once upstream fixes it, signalling removal of the
workaround. Check https://github.com/Quandela/Perceval_Interop/issues before the next release.

```bash
uv venv && uv pip sync requirements.lock && python -m pytest -q
```

Sources: https://perceval.quandela.net/interopdocs/, https://github.com/Quandela/Perceval_Interop
