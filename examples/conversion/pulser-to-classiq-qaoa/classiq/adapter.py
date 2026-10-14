"""CanonicalProblem (from the Pulser ProgramIR) -> Classiq Qmod QAOA, plus a local reference simulator.

Route: Rydberg analog -> gate model = REIMPLEMENTATION (R) of the shared QUBO. The analog adiabatic schedule has no
exact circuit equivalent and is not carried over (see ../translation_record.json).

Structure follows the version-matched official example (Classiq/classiq-library
algorithms/search_and_optimization/QAOA/qaoa.ipynb at 9e5b7bed123716274150e1221addb03e51a785e7, 2026-10-14):
named `cost_layer`, `mixer_layer`, `qaoa_ansatz`; `gammas = params[0:p]`, `betas = params[p:2p]`;
cost layer `phase(-cost(v), gamma)`; mixer `RX(beta, q)`.

Conventions (tested in test_example.py):
* phase(expr, coefficient) multiplies |x> by exp(i * coefficient * expr(x)) (SDK docstring); with expr = -C(x)/s
  the cost layer is U_C(gamma) = exp(-i gamma C(x) / s), s = SCALE = max |QUBO coefficient|.
* RX(theta) = exp(-i theta X / 2) (SDK docstring). The mixer RX(beta) therefore equals exp(-i (beta/2) X):
  beta here spans [0, 2 pi) for the family that exp(-i beta' X) spans with beta' in [0, pi). Angles from a
  RX(2 beta) convention must be doubled before reuse; they are never compared directly.
* qubit v[k] = register atom k = bitstring character k; 1 = Rydberg.
* Decorator: @qfunc for the phase-only cost layer, as in the official example. In classiq 1.32.0 @qperm is
  accepted for the cost layer by create_model and rejected for the RX mixer ("Non-permutation operation used in a
  permutation function"); no synthesis-quality benefit of @qperm can be measured offline, so it is not adopted.
Note: no `from __future__ import annotations` -- Qmod reads real type objects.
"""
import hashlib
import itertools
import json
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np
from classiq import (RX, CArray, CReal, Output, QArray, QBit, allocate, apply_to_all, create_model,
                     hadamard_transform, phase, qfunc, qperm, repeat, write_qmod)
from classiq.interface.executor.estimate_cost import estimate_quantile_cost

HERE = Path(__file__).resolve().parent
PROBLEM = json.loads((HERE.parent / "canonical_problem.json").read_text())
LINEAR = {i: float(a) for i, a in enumerate(PROBLEM["qubo"]["linear"])}
QUAD = {(int(i), int(j)): float(b) for i, j, b in PROBLEM["qubo"]["quadratic"]}
CONSTANT = float(PROBLEM["qubo"]["constant"])
N = len(LINEAR)
SCALE = max(abs(v) for v in list(LINEAR.values()) + list(QUAD.values()))
DECORATORS = {"qfunc": qfunc, "qperm": qperm}


def objective_hash() -> str:
    return hashlib.sha256(json.dumps(PROBLEM["qubo"], sort_keys=True).encode()).hexdigest()


def canonical_energy(x: Sequence[int]) -> float:
    return CONSTANT + sum(a * x[i] for i, a in LINEAR.items()) + sum(b * x[i] * x[j] for (i, j), b in QUAD.items())


def cost(v):
    """Normalised cost C(x)/SCALE as a Qmod expression (also evaluates on plain lists)."""
    expr = 0
    for i, a in LINEAR.items():
        expr = expr + (a / SCALE) * v[i]
    for (i, j), b in QUAD.items():
        expr = expr + (b / SCALE) * v[i] * v[j]
    return expr


# ------------------------------------------------------------------ Qmod model
def build_main(p: int, cost_decorator: str = "qfunc", mixer_decorator: str = "qfunc") -> Callable:
    cost_dec, mixer_dec = DECORATORS[cost_decorator], DECORATORS[mixer_decorator]

    @cost_dec
    def cost_layer(gamma: CReal, v: QArray[QBit, N]):
        phase(-cost(v), gamma)

    @mixer_dec
    def mixer_layer(beta: CReal, v: QArray[QBit, N]):
        apply_to_all(lambda q: RX(beta, q), v)

    @qfunc
    def qaoa_ansatz(gammas: CArray[CReal], betas: CArray[CReal], v: QArray[QBit, N]):
        repeat(betas.len, lambda i: [cost_layer(gammas[i], v), mixer_layer(betas[i], v)])

    @qfunc
    def main(params: CArray[CReal, 2 * p], v: Output[QArray[QBit, N]]):
        allocate(v)
        hadamard_transform(v)
        qaoa_ansatz(params[0:p], params[p:2 * p], v)

    return main


def build_model(p: int, cost_decorator: str = "qfunc", mixer_decorator: str = "qfunc") -> str:
    return create_model(build_main(p, cost_decorator, mixer_decorator))


def export_qmod(p: int, directory: Path) -> Path:
    name = f"pulser_qaoa_p{p}"
    write_qmod(build_main(p), name, directory=directory, decimal_precision=12, symbolic_only=False)
    (directory / f"{name}.synthesis_options.json").unlink(missing_ok=True)  # randomised seed, not an artifact
    return directory / f"{name}.qmod"


def evaluate_expression(text: str, x: Sequence[int]) -> float:
    """Evaluate the cost expression exported in native Qmod (variables v[k]) on a bit vector."""
    return float(eval(text, {"__builtins__": {}}, {"v": list(x)}))  # noqa: S307 - generated numeric expression


# ------------------------------------------------------------------ reference simulator (same semantics)
STATES = [tuple(int(b) for b in format(k, f"0{N}b")) for k in range(2 ** N)]  # index bits = v[0]..v[N-1]
ENERGIES = np.array([canonical_energy(x) for x in STATES])
COSTS = np.array([cost(list(x)) for x in STATES])  # C/SCALE


def rx(theta: float) -> np.ndarray:
    return np.array([[np.cos(theta / 2), -1j * np.sin(theta / 2)], [-1j * np.sin(theta / 2), np.cos(theta / 2)]])


def _apply_single(state: np.ndarray, gate: np.ndarray, k: int) -> np.ndarray:
    psi = state.reshape([2] * N)
    psi = np.moveaxis(np.tensordot(gate, psi, axes=([1], [k])), 0, k)
    return psi.reshape(-1)


def statevector(params: Sequence[float], p: int) -> np.ndarray:
    gammas, betas = params[:p], params[p:2 * p]
    psi = np.full(2 ** N, 1 / np.sqrt(2 ** N), dtype=np.complex128)
    for gamma, beta in zip(gammas, betas):
        psi = np.exp(1j * gamma * (-COSTS)) * psi            # phase(-cost(v), gamma)
        gate = rx(beta)                                       # RX(beta, q) on every qubit
        for k in range(N):
            psi = _apply_single(psi, gate, k)
    return psi


def probabilities(params: Sequence[float], p: int) -> np.ndarray:
    return np.abs(statevector(params, p)) ** 2


def sampled_cost(params: Sequence[float], p: int, shots: int, quantile: float, rng: np.random.Generator) -> float:
    """What ExecutionSession.estimate_cost returns: sample, then the SDK's own quantile estimator."""
    probs = probabilities(params, p)
    counts = np.bincount(rng.choice(len(probs), size=shots, p=probs / probs.sum()), minlength=len(probs))
    nz = np.nonzero(counts)[0]
    if quantile == 1.0:
        return float(np.average(ENERGIES[nz], weights=counts[nz]))
    return float(estimate_quantile_cost(ENERGIES[nz], counts[nz], quantile=quantile))


# ------------------------------------------------------------------ resources (reference decomposition)
def resources(p: int) -> Dict[str, int]:
    """CX-RZ-CX per ZZ term; ZZ terms scheduled greedily into parallel rounds (edge colouring)."""
    pairs = [k for k, b in QUAD.items() if abs(b) > 0]
    rounds: List[List[Tuple[int, int]]] = []
    for pair in pairs:
        for r in rounds:
            if all(set(pair).isdisjoint(q) for q in r):
                r.append(pair)
                break
        else:
            rounds.append([pair])
    per_layer_depth = 3 * len(rounds) + 1 + 1          # ZZ rounds, local RZ, RX
    return {"two_qubit_gates": 2 * len(pairs) * p, "depth": 1 + per_layer_depth * p, "zz_rounds_per_layer": len(rounds)}


def exact_ranking() -> List[Tuple[float, str]]:
    return sorted((canonical_energy(x), "".join(map(str, x))) for x in itertools.product((0, 1), repeat=N))
