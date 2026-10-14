"""Canonical six-bond model -> Cirq cost Hamiltonian and QAOA circuit.

Conventions (tested in test_example.py):
* qubit k = cirq.LineQubit(k) = variable k (A..F). Cirq state vectors and measurement
  results are big-endian in qubit order, so bitstrings read left to right = canonical order.
* Ising map x_k = (1 - s_k) / 2 with s_k the Z eigenvalue, identical to problem.json.
* cost unitary U_C(gamma) = exp(-i gamma H_C / scale) with scale = max |Ising coefficient| (angles stay O(1));
  single-Z terms use cirq.rz(2 gamma h)
  (cirq.rz(t) = exp(-i t Z / 2)) and ZZ terms use ZZPowGate(exponent=2 gamma J / pi,
  global_shift=-0.5) = exp(-i gamma J Z Z).
* mixer U_M(beta) = exp(-i beta sum X) = cirq.rx(2 beta) on every qubit.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import cirq  # noqa: E402
import numpy as np  # noqa: E402

N = 6
QUBITS = cirq.LineQubit.range(N)


def ising(problem: dict) -> Tuple[dict, dict, float]:
    return canonical.to_ising(*canonical.to_qubo(problem))


def cost_hamiltonian(problem: dict) -> cirq.PauliSum:
    h, J, offset = ising(problem)
    ham = cirq.PauliSum.from_pauli_strings([cirq.PauliString({}, coefficient=offset)])
    for i, v in h.items():
        ham += v * cirq.Z(QUBITS[i])
    for (i, j), v in J.items():
        ham += v * cirq.Z(QUBITS[i]) * cirq.Z(QUBITS[j])
    return ham


def basis_state(x: Sequence[int]) -> np.ndarray:
    index = int("".join(str(int(b)) for b in x), 2)
    vec = np.zeros(2 ** N, dtype=np.complex128)
    vec[index] = 1.0
    return vec


def hamiltonian_energy(x: Sequence[int], ham: cirq.PauliSum) -> float:
    qubit_map = {q: k for k, q in enumerate(QUBITS)}
    return float(ham.expectation_from_state_vector(basis_state(x), qubit_map).real)


def coefficient_scale(problem: dict) -> float:
    h, J, _ = ising(problem)
    return max(abs(v) for v in list(h.values()) + list(J.values()))


def cost_layer(problem: dict, gamma: float, scale: float = 1.0) -> List[cirq.Operation]:
    """exp(-i gamma H_C / scale) up to the global phase of the constant offset."""
    h, J, _ = ising(problem)
    gamma = gamma / scale
    ops = [cirq.rz(2 * gamma * v).on(QUBITS[i]) for i, v in h.items()]
    ops += [cirq.ZZPowGate(exponent=2 * gamma * v / math.pi, global_shift=-0.5).on(QUBITS[i], QUBITS[j])
            for (i, j), v in J.items()]
    return ops


def mixer_layer(beta: float) -> List[cirq.Operation]:
    return [cirq.rx(2 * beta).on(q) for q in QUBITS]


def qaoa_circuit(problem: dict, gammas: Sequence[float], betas: Sequence[float], measure: bool = True) -> cirq.Circuit:
    circuit = cirq.Circuit(cirq.H.on_each(*QUBITS))
    scale = coefficient_scale(problem)
    for gamma, beta in zip(gammas, betas):
        circuit.append(cost_layer(problem, gamma, scale))
        circuit.append(mixer_layer(beta))
    if measure:
        circuit.append(cirq.measure(*QUBITS, key="x"))
    return circuit


def decode_measurement(row: Sequence[int]) -> List[int]:
    """Measurement key "x" returns bits in qubit order = canonical order (no reversal)."""
    return [int(b) for b in row]
