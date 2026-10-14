"""Gate -> photonic DV conversion (README-14 class C, conditional) through perceval-interop.

Source: Qiskit circuits (a 2-qubit QAOA layer for the A/C sub-problem of the six-bond data; a 3-qubit GHZ circuit).
Target: Perceval dual-rail Experiment from perceval_interop QiskitConverter (use_postselection=True), run on the
local SLOS processor with a perfect source.

Proof obligation for C: the logical output distribution CONDITIONAL on postselection/heralds equals the gate-model
distribution, and the UNCONDITIONAL success probability is reported next to it. A postselected match is never
reported as deterministic equivalence.

Version notes (observed 2026-10-14):
* perceval-interop 1.3.0 declares qiskit~=2.1.2 for its [qiskit] extra -> this fixture pins qiskit 2.1.2.
* `import perceval_interop` raises ImportError (MyQLMCommunicationLayer) when the optional myqlm extra is absent:
  the package __init__ re-exports a name its myqlm fallback never defines. load_converter() imports the Qiskit
  converter submodule without executing that __init__; test_upstream_import_defect_documented fails once
  upstream fixes it, so the workaround is then removed.
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import numpy as np  # noqa: E402
import perceval as pcvl  # noqa: E402
from qiskit import QuantumCircuit  # noqa: E402
from qiskit.quantum_info import Statevector  # noqa: E402

SUB = (0, 2)  # bonds A and C


def load_converter():
    if "perceval_interop" not in sys.modules:
        spec = importlib.util.find_spec("perceval_interop")
        pkg = types.ModuleType("perceval_interop")
        pkg.__path__ = list(spec.submodule_search_locations)
        sys.modules["perceval_interop"] = pkg
    from perceval_interop.qiskit import QiskitConverter
    return QiskitConverter


def sub_ising(problem: dict):
    data, par = problem["data"], problem["parameters"]
    i, j = SUB
    q, pen, sig = par["risk_aversion_q"], par["cardinality_penalty_A"], data["sigma"]
    linear = {0: q * sig[i][i] - data["mu"][i] - pen, 1: q * sig[j][j] - data["mu"][j] - pen}
    quad = {(0, 1): q * (sig[i][j] + sig[j][i]) + 2 * pen}
    return canonical.to_ising(linear, quad, pen)


def qaoa_circuit(problem: dict, gamma: float, beta: float) -> QuantumCircuit:
    h, J, _ = sub_ising(problem)
    s = max(abs(v) for v in list(h.values()) + list(J.values()))
    qc = QuantumCircuit(2)
    qc.h([0, 1])
    qc.rz(2 * gamma * h[0] / s, 0)
    qc.rz(2 * gamma * h[1] / s, 1)
    qc.cx(0, 1)
    qc.rz(2 * gamma * J[(0, 1)] / s, 1)
    qc.cx(0, 1)
    qc.rx(2 * beta, [0, 1])
    return qc


def ghz_circuit(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(0)
    for k in range(n - 1):
        qc.cx(k, k + 1)
    return qc


def gate_distribution(qc: QuantumCircuit) -> Dict[str, float]:
    """Probabilities keyed q0 q1 ... left to right (Qiskit labels are little-endian, so they are reversed)."""
    probs = Statevector(qc).probabilities_dict()
    return {label[::-1]: float(p) for label, p in probs.items() if p > 1e-15}


def decode(state) -> str:
    modes = list(state)
    out = []
    for q in range(len(modes) // 2):
        pair = modes[2 * q: 2 * q + 2]
        if pair == [1, 0]:
            out.append("0")
        elif pair == [0, 1]:
            out.append("1")
        else:
            raise ValueError(f"not a dual-rail logical state: {modes}")
    return "".join(out)


def photonic_distribution(qc: QuantumCircuit) -> Tuple[Dict[str, float], float, dict]:
    converter = load_converter()()
    experiment = converter.convert(qc, use_postselection=True)
    proc = pcvl.Processor("SLOS", experiment)
    proc.with_input(pcvl.LogicalState([0] * qc.num_qubits))
    proc.min_detected_photons_filter(qc.num_qubits)
    out = proc.probs()
    dist = {decode(s): float(p) for s, p in out["results"].items()}
    resources = {"modes": experiment.m, "heralded_modes": len(experiment.heralds),
                 "cnots": sum(1 for inst in qc.data if inst.operation.name == "cx")}
    return dist, float(out["global_perf"]), resources


def tvd(a: Dict[str, float], b: Dict[str, float]) -> float:
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys)


def validate_claim(record: dict) -> list:
    """Reject a conversion claim that hides postselection: class must be C and the success rate must be present."""
    problems = []
    if record.get("route_class") != "C":
        problems.append("postselected photonic conversion must be class C, not " + str(record.get("route_class")))
    rate = record.get("unconditional_success_probability")
    if rate is None:
        problems.append("unconditional success probability missing")
    elif not 0 < rate < 1:
        problems.append("success probability must be in (0, 1) for a postselected circuit")
    return problems


def energies(problem: dict) -> Dict[str, float]:
    h, J, off = sub_ising(problem)
    return {f"{a}{b}": canonical.ising_energy([1 - 2 * a, 1 - 2 * b], h, J, off) for a in (0, 1) for b in (0, 1)}


def angles_grid():
    return [(0.3, 0.2), (1.1, 0.7), (1.535, 1.19)]


def best_angles(problem: dict) -> Tuple[float, float]:
    e = energies(problem)
    grid = [(g, b) for g in np.linspace(0, np.pi, 25) for b in np.linspace(0, np.pi / 2, 13)]
    return min(grid, key=lambda gb: sum(p * e[k] for k, p in gate_distribution(qaoa_circuit(problem, *gb)).items()))
