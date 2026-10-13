"""CanonicalProblem (derived from the Pulser ProgramIR) -> Classiq Qmod QAOA.

This is a REIMPLEMENTATION of the same optimisation objective, not a conversion
of the Pulser pulse sequence: the analog adiabatic schedule has no exact gate
equivalent (see ../translation_record.json). Qubit x[k] <-> register atom k;
|1> <-> Rydberg state |r>.

Note: no `from __future__ import annotations` -- Qmod reads real type objects.
"""
import json
from pathlib import Path
from typing import Sequence

from classiq import (
    RX, CArray, CReal, Output, QArray, QBit, allocate, apply_to_all,
    create_model, hadamard_transform, phase, qfunc, repeat,
)

HERE = Path(__file__).resolve().parent
PROBLEM = json.loads((HERE.parent / "canonical_problem.json").read_text())
LINEAR = {i: float(a) for i, a in enumerate(PROBLEM["qubo"]["linear"])}
QUAD = {(int(i), int(j)): float(b) for i, j, b in PROBLEM["qubo"]["quadratic"]}
CONSTANT = float(PROBLEM["qubo"]["constant"])
N = len(LINEAR)
LAYERS = 2


def canonical_energy(x: Sequence[int]) -> float:
    return (CONSTANT + sum(a * x[i] for i, a in LINEAR.items())
            + sum(b * x[i] * x[j] for (i, j), b in QUAD.items()))


def cost(x):
    expr = 0
    for i, a in LINEAR.items():
        expr = expr + a * x[i]
    for (i, j), b in QUAD.items():
        expr = expr + b * x[i] * x[j]
    return expr


@qfunc
def qaoa_layer(gamma: CReal, beta: CReal, x: QArray[QBit, N]):
    phase(cost(x), gamma)
    apply_to_all(lambda q: RX(beta, q), x)


@qfunc
def main(params: CArray[CReal, 2 * LAYERS], x: Output[QArray[QBit, N]]):
    allocate(x)
    hadamard_transform(x)
    repeat(LAYERS, lambda k: qaoa_layer(params[2 * k], params[2 * k + 1], x))


def build_model() -> str:
    return create_model(main)


def evaluate_expression(text: str, x: Sequence[int]) -> float:
    return float(eval(text, {"__builtins__": {}}, {"x": list(x)}))  # noqa: S307 - numeric, generated
