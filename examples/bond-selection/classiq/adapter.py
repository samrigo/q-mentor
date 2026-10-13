"""Canonical six-bond model -> Classiq Python-Qmod QAOA model.

Note: no `from __future__ import annotations` -- Qmod reads real type objects.

Qubit x[k] <-> variable k (A..F). The cost is the canonical QUBO polynomial
E(x) = sum a_k x_k + sum_{i<j} b_ij x_i x_j (+ constant c, which only adds a
global phase and is therefore omitted from the circuit and added back when
reporting). Measured QArray values are decoded per element, x[0] = A.
"""

import sys
from pathlib import Path
from typing import Dict, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
from classiq import (  # noqa: E402
    RX, CArray, CReal, Output, QArray, QBit, allocate, apply_to_all,
    create_model, hadamard_transform, phase, qfunc, repeat,
)

N = 6
LAYERS = 2


def qubo_terms(problem: dict) -> Tuple[Dict[int, float], Dict[Tuple[int, int], float], float]:
    return canonical.to_qubo(problem)


def cost_expression_text(problem: dict) -> str:
    """Human-readable polynomial with the exact coefficients used in the model."""
    linear, quad, _ = qubo_terms(problem)
    parts = [f"{a!r}*x[{i}]" for i, a in linear.items()]
    parts += [f"{b!r}*x[{i}]*x[{j}]" for (i, j), b in quad.items()]
    return " + ".join(parts)


def evaluate_cost_text(text: str, x: Sequence[int]) -> float:
    """Evaluate the generated polynomial for a bit vector (test helper, no builtins)."""
    return float(eval(text, {"__builtins__": {}}, {"x": list(x)}))  # noqa: S307 - generated, numeric only


PROBLEM = canonical.load_problem()
LINEAR, QUAD, CONSTANT = qubo_terms(PROBLEM)


def cost(x):
    """Canonical QUBO polynomial over the qubit array (constant omitted: global phase)."""
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


def build_model():
    """Return the serialized Qmod model; runs locally, no credentials."""
    return create_model(main)


def model_phase_expressions(model_json: str):
    """Return every phase-cost expression string stored in a serialized model."""
    import json
    import re

    text = json.dumps(json.loads(model_json))
    return [e for e in re.findall(r'"expr": "([^"]+)"', text) if "x[0] * x[1]" in e]
