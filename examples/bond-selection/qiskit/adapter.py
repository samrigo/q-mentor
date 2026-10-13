"""Canonical six-bond model -> Qiskit Optimization QuadraticProgram -> QUBO -> Ising.

Bit/qubit convention: variable k (A..F) <-> qubit k. Qiskit bitstrings are
little-endian (qubit 0 is the RIGHTMOST character), so they are reversed before
decoding into the canonical left-to-right order.
Ising convention (Qiskit Optimization): x_k = (1 - z_k) / 2 with z_k the Pauli-Z
eigenvalue, identical to the canonical map in problem.json.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
from qiskit.quantum_info import SparsePauliOp, Statevector  # noqa: E402
from qiskit_optimization import QuadraticProgram  # noqa: E402
from qiskit_optimization.converters import QuadraticProgramToQubo  # noqa: E402


def build_quadratic_program(problem: dict) -> QuadraticProgram:
    """Objective without the cardinality penalty; cardinality as a hard constraint."""
    data, par = problem["data"], problem["parameters"]
    mu, dur, sigma = data["mu"], data["duration"], data["sigma"]
    q, w, target = par["risk_aversion_q"], par["duration_weight"], par["duration_target"]
    names = [v["id"] for v in problem["variables"]]
    n = len(names)
    qp = QuadraticProgram(name=problem["id"])
    for name in names:
        qp.binary_var(name)
    linear = {names[i]: q * sigma[i][i] - mu[i] + w * (dur[i] ** 2 - 2 * target * dur[i]) for i in range(n)}
    quadratic = {
        (names[i], names[j]): q * (sigma[i][j] + sigma[j][i]) + 2 * w * dur[i] * dur[j]
        for i in range(n) for j in range(i + 1, n)
    }
    qp.minimize(constant=w * target ** 2, linear=linear, quadratic=quadratic)
    qp.linear_constraint(linear={name: 1 for name in names}, sense="==",
                         rhs=par["budget_B"], name="cardinality")
    return qp


def build_qubo(problem: dict) -> QuadraticProgram:
    """Penalise the equality with the canonical penalty A (not Qiskit's auto value)."""
    penalty = problem["parameters"]["cardinality_penalty_A"]
    return QuadraticProgramToQubo(penalty=penalty).convert(build_quadratic_program(problem))


def build_ising(problem: dict) -> Tuple[SparsePauliOp, float]:
    operator, offset = build_qubo(problem).to_ising()
    return operator, float(offset)


def qiskit_label(x: Sequence[int]) -> str:
    """Canonical bit vector -> Qiskit little-endian basis label."""
    return "".join(str(int(b)) for b in reversed(x))


def decode_qiskit_bitstring(text: str) -> List[int]:
    return [int(ch) for ch in reversed(text)]


def operator_energy(x: Sequence[int], operator: SparsePauliOp, offset: float) -> float:
    state = Statevector.from_label(qiskit_label(x))
    return float(state.expectation_value(operator).real) + offset
