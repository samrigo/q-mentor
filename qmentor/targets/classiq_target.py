"""Classiq target: high-level model -> synthesis -> execution.

Offline path is MODEL VALIDATION ONLY. We build the Pyomo model that Classiq's
combinatorial-optimization workflow accepts and evaluate it on every
assignment. Synthesis and execution need a Classiq account (authentication),
so they are never run by default; the plan records what must be captured
when a user approves them (synthesis constraints, width/depth, backend).

The penalised canonical objective is passed directly (no Pyomo constraint) so
Classiq does not choose its own penalty and change the objective silently.
"""

from __future__ import annotations

from ..canonical import CanonicalQUBO, all_assignments, bits_to_str
from . import require

TARGET = "classiq"


def capability(q: CanonicalQUBO) -> dict:
    return {
        "target": TARGET,
        "role": "high-level modeling and synthesis platform",
        "status": "exact",
        "status_scope": "model level; synthesized circuit not produced offline",
        "mapping": "Pyomo ConcreteModel (binary vars, penalised quadratic objective) -> Classiq QAOA workflow",
        "requires": [
            "Classiq authentication for synthesis/execution (explicit approval)",
            "record synthesis preferences/constraints, circuit width and depth, execution backend",
        ],
        "lost_semantics": [
            "If hard constraints are passed as Pyomo constraints instead, Classiq applies its own penalty; "
            "re-run equivalence before comparing energies"
        ],
        "resources": {"logical_qubits_expected": q.n},
        "remote_execution": "not performed",
    }


def to_pyomo(q: CanonicalQUBO):
    pyo = require("pyomo.environ")
    m = pyo.ConcreteModel(name="canonical_qubo")
    idx = list(range(q.n))
    m.x = pyo.Var(idx, domain=pyo.Binary)
    expr = q.constant
    for i in idx:
        expr += float(q.Q[i, i]) * m.x[i]
        for j in idx:
            if j > i and q.Q[i, j]:
                expr += float(2 * q.Q[i, j]) * m.x[i] * m.x[j]
    m.cost = pyo.Objective(expr=expr, sense=pyo.minimize)
    return m


def energy_table(q: CanonicalQUBO) -> dict[str, float]:
    pyo = require("pyomo.environ")
    m = to_pyomo(q)
    table = {}
    for x in all_assignments(q.n):
        for i, b in enumerate(x):
            m.x[i].set_value(b)
        table[bits_to_str(x)] = float(pyo.value(m.cost))
    return table


CODE_TEMPLATE = '''\
# Generated plan - requires explicit approval before running (Classiq account needed).
# Pin: classiq==<tested version>; record synthesis width/depth and backend in the ResultRecord.
from classiq import *                       # noqa: F401,F403
from qmentor.canonical import build_mean_variance_qubo, load_problem
from qmentor.targets.classiq_target import to_pyomo

qubo = build_mean_variance_qubo(load_problem("demo/bond-selection/problem.json"))
model = to_pyomo(qubo)
# Follow the Classiq combinatorial-optimization guide for the pinned version:
# build the QAOA problem from `model`, synthesize with explicit constraints,
# execute on a simulator first, decode with variable 0 leftmost.
'''


def plan() -> dict:
    return {"target": TARGET, "code_template": CODE_TEMPLATE, "authenticate_called": False}
