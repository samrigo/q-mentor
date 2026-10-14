"""Quandela Perceval (discrete-variable photonics) adapter.

1. Six-bond QUBO -> photonic dual-rail QAOA: route class `conditional` in principle, but every two-qubit gate is
   probabilistic. One QAOA layer needs 15 ZZ terms = 30 CNOTs: 29 heralded (success 2/27 each, two ancilla
   photons) and one postselected (1/9). The unconditional success probability is computed, not hand-waved; it is
   far too small to run, so the six-bond example is reported as `conditional-impractical`, with no code.
2. Native program: a two-variable sub-problem of the same data (choose exactly one of bonds A and C), QAOA p=1 on
   two dual-rail qubits with one heralded CNOT and one postselected CNOT. The postselected (conditional) logical
   distribution must equal the ideal gate-model distribution, and the unconditional success rate is reported.

Conventions (tested):
* dual rail: logical |0> = photon in the first mode of the pair, |1> = photon in the second mode.
* Perceval BS.Rx(theta) = [[cos t/2, i sin t/2], [i sin t/2, cos t/2]] = standard RX(-theta); so the standard
  RX(theta) = exp(-i theta X / 2) is built as BS.Rx(theta=-theta). Mixer U_M(beta) = RX(2 beta).
* RZ(theta) = diag(e^{-i theta/2}, e^{i theta/2}) = PS(-theta/2) on mode 0 and PS(theta/2) on mode 1.
* ZZ(gamma J) = exp(-i gamma J Z Z) = CNOT . (I x RZ(2 gamma J)) . CNOT.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import numpy as np  # noqa: E402
import perceval as pcvl  # noqa: E402
from perceval.components import BS, PS  # noqa: E402

HERALDED_CNOT_SUCCESS = 2 / 27
POSTSELECTED_CNOT_SUCCESS = 1 / 9
SUB = (0, 2)  # bonds A and C


# ------------------------------------------------------------------ 1. six-bond resource report
def six_bond_report(problem: dict, layers: int = 1) -> dict:
    _, quad, _ = canonical.to_qubo(problem)
    n = len(problem["variables"])
    cnots = 2 * len(quad) * layers
    success = HERALDED_CNOT_SUCCESS ** (cnots - 1) * POSTSELECTED_CNOT_SUCCESS
    return {
        "schema": "qmentor.capability-report.v3",
        "problem_id": problem["id"],
        "target": {"provider": "Quandela", "sdk": "perceval-quandela 1.3.1", "backend": "Processor SLOS (local)",
                   "physical_family": "photonic", "model": "photonic-DV", "support_level": "tested-local"},
        "status": "conditional-impractical",
        "checks": {
            "logical_qubits": n,
            "dual_rail_modes": 2 * n,
            "zz_terms_per_layer": len(quad),
            "cnots": cnots,
            "heralded_cnots": cnots - 1,
            "ancilla_photons": 2 * (cnots - 1),
            "ancilla_modes": 4 * (cnots - 1) + 2,
            "unconditional_success_probability": success,
        },
        "lost_semantics": ["deterministic execution: only a postselected/heralded fraction of runs succeeds"],
        "alternatives": ["gate-model QAOA on a local simulator (Qiskit, Cirq, pytket)", "D-Wave BQM (dimod)",
                         "the two-variable photonic program in this folder"],
    }


# ------------------------------------------------------------------ 2. native two-variable sub-problem
def sub_problem(problem: dict) -> dict:
    """Choose exactly one of bonds A and C: 1.5 x^T Sigma x - mu^T x + A (x0 + x1 - 1)^2 (same data and A)."""
    data, par = problem["data"], problem["parameters"]
    i, j = SUB
    q, pen = par["risk_aversion_q"], par["cardinality_penalty_A"]
    sig = data["sigma"]
    linear = {0: q * sig[i][i] - data["mu"][i] - pen, 1: q * sig[j][j] - data["mu"][j] - pen}
    quad = {(0, 1): q * (sig[i][j] + sig[j][i]) + 2 * pen}
    return {"linear": linear, "quad": quad, "const": pen, "labels": [problem["variables"][i]["id"],
                                                                      problem["variables"][j]["id"]]}


def sub_energy(x: Sequence[int], sub: dict) -> float:
    return canonical.qubo_energy(x, sub["linear"], sub["quad"], sub["const"])


def sub_energy_direct(x: Sequence[int], problem: dict) -> float:
    data, par = problem["data"], problem["parameters"]
    idx = SUB
    risk = sum(data["sigma"][idx[a]][idx[b]] * x[a] * x[b] for a in range(2) for b in range(2))
    ret = sum(data["mu"][idx[a]] * x[a] for a in range(2))
    return par["risk_aversion_q"] * risk - ret + par["cardinality_penalty_A"] * (sum(x) - 1) ** 2


def ising(sub: dict) -> Tuple[dict, dict, float]:
    return canonical.to_ising(sub["linear"], sub["quad"], sub["const"])


# ---- ideal gate-model reference (numpy), standard conventions
def _rx(t):
    return np.array([[np.cos(t / 2), -1j * np.sin(t / 2)], [-1j * np.sin(t / 2), np.cos(t / 2)]])


def _rz(t):
    return np.diag([np.exp(-1j * t / 2), np.exp(1j * t / 2)])


H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])


def reference_unitary(sub: dict, gamma: float, beta: float, scale: float) -> np.ndarray:
    h, J, _ = ising(sub)
    g = gamma / scale
    u = np.kron(H1, H1)
    u = np.kron(_rz(2 * g * h[0]), _rz(2 * g * h[1])) @ u
    u = CNOT @ np.kron(np.eye(2), _rz(2 * g * J[(0, 1)])) @ CNOT @ u
    u = np.kron(_rx(2 * beta), _rx(2 * beta)) @ u
    return u


def reference_distribution(sub: dict, gamma: float, beta: float, scale: float) -> Dict[str, float]:
    psi = reference_unitary(sub, gamma, beta, scale)[:, 0]
    return {f"{k:02b}": float(abs(psi[k]) ** 2) for k in range(4)}


# ---- photonic circuit
def _add_rz(exp: pcvl.Experiment, qubit: int, theta: float) -> None:
    exp.add(2 * qubit, PS(-theta / 2))
    exp.add(2 * qubit + 1, PS(theta / 2))


def _add_rx(exp: pcvl.Experiment, qubit: int, theta: float) -> None:
    exp.add(2 * qubit, BS.Rx(theta=-theta))


def photonic_experiment(sub: dict, gamma: float, beta: float, scale: float) -> pcvl.Experiment:
    h, J, _ = ising(sub)
    g = gamma / scale
    exp = pcvl.Experiment(4)
    exp.add(0, BS.H())
    exp.add(2, BS.H())
    _add_rz(exp, 0, 2 * g * h[0])
    _add_rz(exp, 1, 2 * g * h[1])
    exp.add(0, pcvl.catalog["heralded cnot"].build_experiment())
    _add_rz(exp, 1, 2 * g * J[(0, 1)])
    exp.add(0, pcvl.catalog["postprocessed cnot"].build_experiment())
    _add_rx(exp, 0, 2 * beta)
    _add_rx(exp, 1, 2 * beta)
    return exp


def decode_state(state) -> str:
    """Dual-rail |1,0> -> '0', |0,1> -> '1' per qubit (heralded modes already removed by Perceval)."""
    modes = list(state)
    bits = []
    for q in range(2):
        pair = modes[2 * q: 2 * q + 2]
        if pair == [1, 0]:
            bits.append("0")
        elif pair == [0, 1]:
            bits.append("1")
        else:
            raise ValueError(f"not a dual-rail logical state: {modes}")
    return "".join(bits)


def photonic_distribution(sub: dict, gamma: float, beta: float, scale: float) -> Tuple[Dict[str, float], float]:
    proc = pcvl.Processor("SLOS", photonic_experiment(sub, gamma, beta, scale))
    proc.with_input(pcvl.BasicState([1, 0, 1, 0]))
    proc.min_detected_photons_filter(2)
    out = proc.probs()
    dist = {decode_state(state): float(p) for state, p in out["results"].items()}
    return dist, float(out["global_perf"])


def all_states() -> List[Tuple[int, int]]:
    return list(itertools.product((0, 1), repeat=2))
