"""Canonical six-bond model -> pytket QAOA circuit, compilation pass, and semantic checks.

Conventions (tested in test_example.py):
* qubit k = variable k (A..F). pytket statevectors use ILO-BE (qubit 0 is the most significant bit), so
  basis index bits read A..F left to right.
* pytket angles are in HALF-TURNS: Rz(a) = exp(-i pi a Z / 2), Rx(a) = exp(-i pi a X / 2),
  ZZPhase(a) = exp(-i pi a Z Z / 2).
* cost U_C(gamma) = exp(-i gamma H_C / scale): Rz(2 gamma h / (pi scale)), ZZPhase(2 gamma J / (pi scale)).
* mixer U_M(beta) = exp(-i beta sum X) = Rx(2 beta / pi) on every qubit.
* compilation: two candidate pass sequences to an ion-native style gate set {ZZPhase, PhasedX, Rz}:
  "rebase" = AutoRebase + RemoveRedundancies, "peephole" = FullPeepholeOptimise + AutoRebase. Both must preserve
  the unitary up to global phase; the one with fewer two-qubit gates (then depth) is kept. On this circuit
  FullPeepholeOptimise routes through CX and doubles the ZZ count, so "rebase" is kept: a compiler pass is not an
  optimization until its resources are measured.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import numpy as np  # noqa: E402
from pytket import Circuit, OpType  # noqa: E402
from pytket.passes import AutoRebase, FullPeepholeOptimise, RemoveRedundancies, SequencePass  # noqa: E402

N = 6
TARGET_GATES = {OpType.ZZPhase, OpType.PhasedX, OpType.Rz}


def ising(problem: dict) -> Tuple[dict, dict, float]:
    return canonical.to_ising(*canonical.to_qubo(problem))


def coefficient_scale(problem: dict) -> float:
    h, J, _ = ising(problem)
    return max(abs(v) for v in list(h.values()) + list(J.values()))


def add_cost_layer(circuit: Circuit, problem: dict, gamma: float, scale: float) -> None:
    h, J, _ = ising(problem)
    for i, v in h.items():
        circuit.Rz(2 * gamma * v / (math.pi * scale), i)
    for (i, j), v in J.items():
        circuit.ZZPhase(2 * gamma * v / (math.pi * scale), i, j)


def add_mixer_layer(circuit: Circuit, beta: float) -> None:
    for q in range(N):
        circuit.Rx(2 * beta / math.pi, q)


def qaoa_circuit(problem: dict, gammas: Sequence[float], betas: Sequence[float]) -> Circuit:
    circuit = Circuit(N)
    for q in range(N):
        circuit.H(q)
    scale = coefficient_scale(problem)
    for gamma, beta in zip(gammas, betas):
        add_cost_layer(circuit, problem, gamma, scale)
        add_mixer_layer(circuit, beta)
    return circuit


PASSES = {
    "rebase": lambda: SequencePass([AutoRebase(TARGET_GATES), RemoveRedundancies()]),
    "peephole": lambda: SequencePass([FullPeepholeOptimise(), AutoRebase(TARGET_GATES)]),
}


def compile_with(circuit: Circuit, name: str) -> Circuit:
    compiled = circuit.copy()
    PASSES[name]().apply(compiled)
    return compiled


def resources(circuit: Circuit) -> dict:
    return {"gates": circuit.n_gates, "two_qubit_gates": circuit.n_2qb_gates(), "depth": circuit.depth(),
            "gate_types": sorted({str(c.op.type).replace("OpType.", "") for c in circuit.get_commands()})}


def unitary_error_up_to_phase(a: Circuit, b: Circuit) -> float:
    ua, ub = a.get_unitary(), b.get_unitary()
    phase = np.angle(np.vdot(ua.ravel(), ub.ravel()))
    return float(np.max(np.abs(ub - np.exp(1j * phase) * ua)))


def compile_circuit(circuit: Circuit) -> Tuple[Circuit, dict]:
    """Compile with every candidate pass, verify semantics, keep the cheapest. Returns (circuit, report)."""
    report = {}
    for name in PASSES:
        compiled = compile_with(circuit, name)
        report[name] = {**resources(compiled), "unitary_error": unitary_error_up_to_phase(circuit, compiled)}
    valid = [n for n in PASSES if report[n]["unitary_error"] < 1e-8]
    chosen = min(valid, key=lambda n: (report[n]["two_qubit_gates"], report[n]["depth"]))
    report["chosen"] = chosen
    return compile_with(circuit, chosen), report


def all_energies(problem: dict) -> np.ndarray:
    return np.array([canonical.direct_energy([int(b) for b in format(k, f"0{N}b")], problem) for k in range(2 ** N)])


def decode_index(index: int) -> list:
    return [int(b) for b in format(index, f"0{N}b")]
