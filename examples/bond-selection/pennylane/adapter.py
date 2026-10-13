"""Canonical six-bond model -> PennyLane cost Hamiltonian.

Wire k <-> variable k (A..F). PennyLane sample rows list wire 0 first, matching
the canonical left-to-right bit order (no reversal, unlike Qiskit).
Ising convention: x_k = (1 - z_k) / 2 with z_k the PauliZ eigenvalue (|0> -> +1),
identical to the canonical map. The constant offset is kept outside the
Hamiltonian and added back when reporting energies.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import pennylane as qml  # noqa: E402

DEVICE_NAME = "default.qubit"


def build_cost_hamiltonian(problem: dict) -> Tuple[qml.Hamiltonian, float]:
    h, J, offset = canonical.to_ising(*canonical.to_qubo(problem))
    coeffs, ops = [], []
    for i, value in h.items():
        coeffs.append(value)
        ops.append(qml.PauliZ(i))
    for (i, j), value in J.items():
        coeffs.append(value)
        ops.append(qml.PauliZ(i) @ qml.PauliZ(j))
    return qml.Hamiltonian(coeffs, ops), offset


def basis_energy(x: Sequence[int], hamiltonian, offset: float) -> float:
    """<x|H|x> + offset evaluated by PennyLane on default.qubit."""
    dev = qml.device(DEVICE_NAME, wires=len(x))

    @qml.qnode(dev)
    def circuit():
        qml.BasisState(list(x), wires=range(len(x)))
        return qml.expval(hamiltonian)

    return float(circuit()) + offset
