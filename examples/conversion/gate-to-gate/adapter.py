"""Gate -> gate conversion fixtures (README-14 class E on a supported subset).

Source: a Qiskit QAOA layer for a 3-variable slice of the six-bond QUBO (bonds A, B, C), all parameters bound.
Targets and maintained bridges (checked 2026-10-14):
* pytket via pytket-qiskit 0.78.0 `qiskit_to_tk` (maintained).
* Cirq via OpenQASM 2 (`qiskit.qasm2.dumps` -> `cirq.contrib.qasm_import.circuit_from_qasm`), subset only.
Refused by default: pytket-cirq, pytket-pennylane, pytket-pyquil (Quantinuum lists them as unmaintained).

Semantics checked, not assumed:
* operator equality up to global phase after converting Qiskit's little-endian order to the targets' big-endian
  (ILO-BE) order;
* symbolic parameters: qiskit_to_tk raises on an unbound Parameter in 0.78.0, so parameters are bound first;
* dynamic circuits: OpenQASM 2 export raises on an `if_test` condition, so they are rejected for the Cirq route;
* implicit swaps: after mapping to a line architecture, equality holds only with the initial and final qubit maps.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import cirq  # noqa: E402
import numpy as np  # noqa: E402
from cirq.contrib.qasm_import import circuit_from_qasm  # noqa: E402
from pytket import Circuit  # noqa: E402
from pytket.architecture import Architecture  # noqa: E402
from pytket.extensions.qiskit import qiskit_to_tk  # noqa: E402
from pytket.passes import DefaultMappingPass  # noqa: E402
from pytket.predicates import CompilationUnit  # noqa: E402
from qiskit import QuantumCircuit, qasm2  # noqa: E402
from qiskit.quantum_info import Operator  # noqa: E402

SLICE = (0, 1, 2)
BRIDGES = {
    ("qiskit", "pytket"): {"bridge": "pytket-qiskit", "status": "maintained"},
    ("qiskit", "cirq"): {"bridge": "OpenQASM 2 subset (qiskit.qasm2 -> cirq.contrib.qasm_import)", "status": "maintained"},
    ("pytket", "cirq"): {"bridge": "pytket-cirq", "status": "unmaintained"},
    ("pytket", "pennylane"): {"bridge": "pytket-pennylane", "status": "unmaintained"},
    ("pytket", "pyquil"): {"bridge": "pytket-pyquil", "status": "unmaintained"},
}


class UnsupportedRoute(Exception):
    """Raised instead of emitting a conversion the route cannot guarantee."""


def choose_bridge(source: str, target: str) -> Dict[str, str]:
    info = BRIDGES.get((source, target))
    if info is None:
        raise UnsupportedRoute(f"no verified bridge for {source} -> {target}; build a capability report first")
    if info["status"] != "maintained":
        raise UnsupportedRoute(f"{info['bridge']} is {info['status']}; not used as a default bridge")
    return info


def slice_ising(problem: dict):
    linear, quad, const = canonical.to_qubo(problem)
    lin = {k: linear[i] for k, i in enumerate(SLICE)}
    qd = {(a, b): quad[(SLICE[a], SLICE[b])] for a in range(3) for b in range(a + 1, 3)}
    return canonical.to_ising(lin, qd, 0.0)


def qiskit_qaoa_layer(problem: dict, gamma: float, beta: float) -> QuantumCircuit:
    """exp(-i gamma H/s) then exp(-i beta sum X); Qiskit rzz(t) = exp(-i t ZZ/2), rz(t) = exp(-i t Z/2)."""
    h, J, _ = slice_ising(problem)
    s = max(abs(v) for v in list(h.values()) + list(J.values()))
    qc = QuantumCircuit(3)
    qc.h(range(3))
    for (a, b), v in J.items():
        qc.rzz(2 * gamma * v / s, a, b)
    for a, v in h.items():
        qc.rz(2 * gamma * v / s, a)
    qc.rx(2 * beta, range(3))
    return qc


def reverse_order(u: np.ndarray, n: int) -> np.ndarray:
    """Little-endian (Qiskit) operator -> big-endian (pytket ILO-BE / Cirq) operator."""
    perm = [int(format(i, f"0{n}b")[::-1], 2) for i in range(2 ** n)]
    return u[np.ix_(perm, perm)]


def qiskit_operator_big_endian(qc: QuantumCircuit) -> np.ndarray:
    return reverse_order(Operator(qc).data, qc.num_qubits)


def to_pytket(qc: QuantumCircuit) -> Circuit:
    choose_bridge("qiskit", "pytket")
    if qc.parameters:
        raise UnsupportedRoute(f"bind symbolic parameters first: {sorted(p.name for p in qc.parameters)}")
    return qiskit_to_tk(qc)


def to_cirq(qc: QuantumCircuit) -> cirq.Circuit:
    choose_bridge("qiskit", "cirq")
    try:
        text = qasm2.dumps(qc)
    except Exception as exc:  # qiskit.qasm2.QASM2ExportError for dynamic/unsupported features
        raise UnsupportedRoute(f"outside the OpenQASM 2 subset: {exc}") from exc
    return circuit_from_qasm(text)


def cirq_unitary(circuit: cirq.Circuit) -> np.ndarray:
    qubits = sorted(circuit.all_qubits(), key=lambda q: int(str(q).split("_")[-1]))
    return circuit.unitary(qubit_order=qubits)


def equal_up_to_phase(a: np.ndarray, b: np.ndarray, atol: float = 1e-9) -> bool:
    return cirq.allclose_up_to_global_phase(a, b, atol=atol)


def map_to_line(circuit: Circuit):
    """Route onto a 3-qubit line; return (mapped circuit, initial map, final map) as logical->physical indices."""
    cu = CompilationUnit(circuit.copy())
    DefaultMappingPass(Architecture([(0, 1), (1, 2)])).apply(cu)
    mapped = cu.circuit
    logical, physical = circuit.qubits, mapped.qubits
    init = {logical.index(q): physical.index(cu.initial_map[q]) for q in logical}
    final = {logical.index(q): physical.index(cu.final_map[q]) for q in logical}
    return mapped, init, final


def permutation(mapping: Dict[int, int], n: int) -> np.ndarray:
    mat = np.zeros((2 ** n, 2 ** n))
    for k in range(2 ** n):
        bits, out = format(k, f"0{n}b"), ["0"] * n
        for logical, physical in mapping.items():
            out[physical] = bits[logical]
        mat[int("".join(out), 2), k] = 1
    return mat


def gate_counts(circuit: Circuit) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for cmd in circuit.get_commands():
        name = str(cmd.op.type).replace("OpType.", "")
        counts[name] = counts.get(name, 0) + 1
    return counts


def slice_energies(problem: dict) -> List[float]:
    h, J, off = slice_ising(problem)
    out = []
    for k in range(8):
        s = [1 - 2 * int(b) for b in format(k, "03b")]
        out.append(canonical.ising_energy(s, h, J, off))
    return out
