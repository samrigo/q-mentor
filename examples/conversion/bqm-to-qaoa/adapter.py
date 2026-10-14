"""BQM/anneal -> gate: the SAME objective, a DIFFERENT algorithm (README-14 class R).

The canonical six-bond QUBO becomes a dimod BinaryQuadraticModel (class E as an energy model, offset included) and
a Qiskit Ising operator for QAOA. Every bitstring's energy agrees, yet annealing samples and QAOA samples come from
different algorithms with different schedules, distributions, and costs, so the route is a reimplementation.
Dropping the BQM offset silently shifts every energy; that is rejected, not tolerated.

Conventions: dimod variable k = canonical bit k; Qiskit Ising x = (1 - z)/2 with little-endian labels reversed.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import List, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import dimod  # noqa: E402
from qiskit.quantum_info import SparsePauliOp, Statevector  # noqa: E402

N = 6


def to_bqm(problem: dict, keep_offset: bool = True) -> dimod.BinaryQuadraticModel:
    linear, quad, const = canonical.to_qubo(problem)
    return dimod.BinaryQuadraticModel(linear, quad, const if keep_offset else 0.0, dimod.BINARY)


def to_qiskit_operator(problem: dict):
    """Ising operator with offset from the canonical map, labels little-endian (qubit 0 rightmost)."""
    h, J, off = canonical.to_ising(*canonical.to_qubo(problem))
    terms = []
    for i, v in h.items():
        label = ["I"] * N
        label[N - 1 - i] = "Z"
        terms.append(("".join(label), v))
    for (i, j), v in J.items():
        label = ["I"] * N
        label[N - 1 - i] = "Z"
        label[N - 1 - j] = "Z"
        terms.append(("".join(label), v))
    return SparsePauliOp.from_list(terms), off


def operator_energy(x: Sequence[int], op: SparsePauliOp, off: float) -> float:
    label = "".join(str(b) for b in reversed(x))
    return float(Statevector.from_label(label).expectation_value(op).real) + off


def classify(source_algorithm: str, target_algorithm: str, energies_equal: bool, decode_equal: bool) -> str:
    """README-14: E only for the same computation; same objective + different algorithm is R; else U."""
    if not (energies_equal and decode_equal):
        return "U"
    return "E" if source_algorithm == target_algorithm else "R"


def all_states() -> List[tuple]:
    return list(itertools.product((0, 1), repeat=N))


def max_error(problem: dict, energy_fn) -> float:
    return max(abs(energy_fn(x) - canonical.direct_energy(x, problem)) for x in all_states())


def exact_samples(bqm: dimod.BinaryQuadraticModel) -> dimod.SampleSet:
    return dimod.ExactSolver().sample(bqm)


def lowest(sampleset: dimod.SampleSet) -> str:
    best = sampleset.first.sample
    return "".join(str(int(best[k])) for k in range(N))

