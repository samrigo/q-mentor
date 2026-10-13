# Pulser → Classiq conversion (through ProgramIR)

This is **not** a source-to-source rewrite. The pipeline is:

1. `extract_ir.py` (Pulser env) builds the source sequence and writes
   `program_ir.json` (register, device, Hamiltonian, controls, measurement,
   decoding, unsupported features) and `canonical_problem.json`.
2. A capability decision per semantic, recorded in `translation_record.json`.
3. `classiq/` — a complete project that reimplements the **shared QUBO** as a
   Classiq QAOA model and verifies the objective on all 16 assignments.

| Source semantic | Status |
|---|---|
| Geometry + C6/r⁶ couplings → QUBO pair terms | exact |
| Final detuning → uniform linear terms | exact |
| Analog adiabatic evolution Ω(t), δ(t) | **unsupported-exact** |
| Ground-rydberg measurement, bit order | exact |
| Device noise / SPAM | unsupported-exact |

Overall status: **reimplementation**. A Classiq QAOA result can be compared with the Pulser result only
on decoded solutions and canonical energy, never on success probability or runtime.

```bash
cd classiq && uv venv && uv pip sync requirements.lock && python -m pytest -q
```

Negative fixtures (stale API, missing import, undefined name, credential-required
synthesis, energy-changing target) live in `evals/conversion/`.
