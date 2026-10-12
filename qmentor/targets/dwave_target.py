"""D-Wave Ocean (dimod) target: BQM from the canonical QUBO, offline ExactSolver.

Convention differences handled explicitly:
* dimod quadratic biases multiply x_i x_j ONCE, so b_ij = 2 Q_ij for i<j.
* dimod SPIN uses s = 2x - 1 (s=+1 <=> x=1), the OPPOSITE of the canonical
  x = (1 - s)/2. ``to_canonical_ising`` flips the sign of h and leaves J alone.
"""

from __future__ import annotations

from ..canonical import CanonicalQUBO, bits_to_str
from . import require

TARGET = "dwave"


def capability(q: CanonicalQUBO) -> dict:
    return {
        "target": TARGET,
        "role": "BQM/CQM annealing and hybrid-solver stack",
        "status": "exact",
        "mapping": "BinaryQuadraticModel(BINARY): linear=Q_ii, quadratic=2*Q_ij (i<j), offset=c",
        "requires": [
            "QPU: minor-embedding into hardware graph (logical != physical qubits)",
            "chain strength choice and chain-break reporting on QPU",
        ],
        "lost_semantics": [],
        "resources": {"logical_variables": q.n},
        "offline_path": "dimod.ExactSolver (exhaustive, classical)",
        "remote_execution": "not performed; QPU or hybrid solvers need explicit approval, a token, and a cost estimate. "
        "A hybrid-solver result is not a pure-QPU benchmark.",
    }


def to_bqm(q: CanonicalQUBO):
    dimod = require("dimod")
    linear = {v: float(q.Q[i, i]) for i, v in enumerate(q.variables)}
    quadratic = {}
    for i in range(q.n):
        for j in range(i + 1, q.n):
            if q.Q[i, j]:
                quadratic[(q.variables[i], q.variables[j])] = float(2 * q.Q[i, j])
    return dimod.BinaryQuadraticModel(linear, quadratic, q.constant, dimod.BINARY)


def energy_table(q: CanonicalQUBO) -> dict[str, float]:
    dimod = require("dimod")
    bqm = to_bqm(q)
    sampleset = dimod.ExactSolver().sample(bqm)
    table = {}
    for rec in sampleset.data(["sample", "energy"]):
        x = [rec.sample[v] for v in q.variables]
        table[bits_to_str(x)] = float(rec.energy)
    return table


def to_canonical_ising(q: CanonicalQUBO) -> dict:
    """dimod Ising mapped into the canonical spin convention (s=+1 <=> x=0)."""
    h, J, offset = to_bqm(q).to_ising()
    return {
        "h": {v: -val for v, val in h.items()},
        "J": dict(J),
        "offset": offset,
    }


def sample_exact(q: CanonicalQUBO) -> dict:
    dimod = require("dimod")
    best = dimod.ExactSolver().sample(to_bqm(q)).first
    return {
        "target": TARGET,
        "versions": {"dimod": dimod.__version__},
        "sampler": "dimod.ExactSolver (local, classical, exhaustive)",
        "bits": bits_to_str([best.sample[v] for v in q.variables]),
        "energy": float(best.energy),
    }
