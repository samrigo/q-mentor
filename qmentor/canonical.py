"""Canonical problem representations: ProblemSpec -> CanonicalQUBO -> Ising.

Conventions (fixed across every adapter; see knowledge/optimization-math.md):

* Binary variables x_i in {0, 1}; variable 0 is the leftmost bit of a bitstring.
* E(x) = x^T Q x + c with Q stored as a FULL SYMMETRIC matrix, so an
  off-diagonal coupling appears twice (Q_ij and Q_ji) in the expansion.
* Ising spins use x_i = (1 - s_i) / 2, i.e. s_i = +1 <=> x_i = 0. This matches
  the Pauli-Z eigenvalue of |0> on gate-model targets. D-Wave dimod uses the
  opposite mapping (s = 2x - 1); its adapter converts explicitly.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np

SYMMETRY_TOL = 1e-12


@dataclass(frozen=True)
class CanonicalQUBO:
    Q: np.ndarray  # full symmetric matrix
    constant: float
    variables: tuple[str, ...]
    convention: str = "E(x)=x^T Q x + c; Q full symmetric; off-diagonals counted twice"
    bit_order: str = "index0-leftmost"
    penalties: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.Q.shape != (len(self.variables), len(self.variables)):
            raise ValueError("Q shape does not match variable count")
        if not np.allclose(self.Q, self.Q.T, atol=SYMMETRY_TOL):
            raise ValueError("Q must be symmetric under the canonical convention")

    @property
    def n(self) -> int:
        return len(self.variables)

    def energy(self, x: Iterable[int]) -> float:
        v = np.asarray(list(x), dtype=float)
        return float(v @ self.Q @ v + self.constant)


@dataclass(frozen=True)
class Ising:
    """E(s) = offset + sum_i h_i s_i + sum_{i<j} J_ij s_i s_j, with x = (1 - s)/2."""

    h: np.ndarray
    J: np.ndarray  # strictly upper triangular
    offset: float

    def energy(self, s: Iterable[int]) -> float:
        v = np.asarray(list(s), dtype=float)
        return float(self.offset + self.h @ v + v @ self.J @ v)


def all_assignments(n: int) -> list[tuple[int, ...]]:
    """All 2^n assignments, ordered as binary counting with variable 0 leftmost."""
    return list(itertools.product((0, 1), repeat=n))


def bits_to_str(x: Iterable[int]) -> str:
    return "".join(str(int(b)) for b in x)


def str_to_bits(s: str) -> tuple[int, ...]:
    if any(c not in "01" for c in s):
        raise ValueError(f"not a bitstring: {s!r}")
    return tuple(int(c) for c in s)


def x_to_s(x: Iterable[int]) -> tuple[int, ...]:
    return tuple(1 - 2 * int(b) for b in x)


def qubo_to_ising(q: CanonicalQUBO) -> Ising:
    n = q.n
    h = np.zeros(n)
    J = np.zeros((n, n))
    offset = q.constant
    for i in range(n):
        offset += q.Q[i, i] / 2
        h[i] -= q.Q[i, i] / 2
    for i in range(n):
        for j in range(i + 1, n):
            qij = q.Q[i, j]  # appears twice in x^T Q x
            offset += qij / 2
            h[i] -= qij / 2
            h[j] -= qij / 2
            J[i, j] += qij / 2
    return Ising(h=h, J=J, offset=float(offset))


# --------------------------------------------------------------------------
# Mean-variance selection with cardinality and target-sum penalties
# --------------------------------------------------------------------------


def load_problem(path: str | Path) -> dict:
    spec = json.loads(Path(path).read_text())
    validate_problem_spec(spec)
    return spec


def validate_problem_spec(spec: dict) -> None:
    required = {"name", "variables", "objective", "constraints", "provenance"}
    missing = required - spec.keys()
    if missing:
        raise ValueError(f"ProblemSpec missing fields: {sorted(missing)}")
    if spec["provenance"].get("data_class") not in {"synthetic", "public"}:
        raise ValueError("Only synthetic or public data is allowed by default")
    n = len(spec["variables"])
    obj = spec["objective"]
    sigma = np.asarray(obj["risk_matrix"], dtype=float)
    if sigma.shape != (n, n):
        raise ValueError("risk_matrix shape mismatch")
    if not np.allclose(sigma, sigma.T, atol=SYMMETRY_TOL):
        raise ValueError("risk_matrix must be symmetric")
    if np.linalg.eigvalsh(sigma).min() < -1e-12:
        raise ValueError("risk_matrix must be positive semidefinite")
    if obj["risk_aversion"] <= 0:
        raise ValueError("risk_aversion must be > 0")
    for key in ("expected_return",):
        if len(obj[key]) != n:
            raise ValueError(f"{key} length mismatch")


def build_mean_variance_qubo(spec: dict) -> CanonicalQUBO:
    """E(x) = q x^T S x - mu^T x + sum_k A_k (a_k^T x - b_k)^2.

    Each equality/target term (a^T x - b)^2 expands to x^T (a a^T) x - 2 b a^T x + b^2,
    and the linear part goes on the diagonal because x_i^2 = x_i.
    """
    variables = tuple(v["id"] for v in spec["variables"])
    obj = spec["objective"]
    S = np.asarray(obj["risk_matrix"], dtype=float)
    mu = np.asarray(obj["expected_return"], dtype=float)
    q = float(obj["risk_aversion"])

    Q = q * S - np.diag(mu)
    c = 0.0
    penalties = {}
    for con in spec["constraints"]:
        a = np.asarray(con["coefficients"], dtype=float)
        b = float(con["target"])
        A = float(con["penalty"])
        Q = Q + A * np.outer(a, a) - np.diag(2 * A * b * a)
        c += A * b * b
        penalties[con["name"]] = {"weight": A, "kind": con["kind"]}
    Q = (Q + Q.T) / 2  # remove floating asymmetry only
    return CanonicalQUBO(Q=Q, constant=c, variables=variables, penalties=penalties)


def direct_objective(spec: dict, x: Iterable[int]) -> float:
    """Evaluate the business objective straight from the spec, no QUBO algebra."""
    v = np.asarray(list(x), dtype=float)
    obj = spec["objective"]
    S = np.asarray(obj["risk_matrix"], dtype=float)
    mu = np.asarray(obj["expected_return"], dtype=float)
    e = obj["risk_aversion"] * v @ S @ v - mu @ v
    for con in spec["constraints"]:
        a = np.asarray(con["coefficients"], dtype=float)
        e += con["penalty"] * (a @ v - con["target"]) ** 2
    return float(e)


def is_feasible(spec: dict, x: Iterable[int]) -> bool:
    """Hard constraints are feasibility rules; soft targets are not."""
    v = np.asarray(list(x), dtype=float)
    for con in spec["constraints"]:
        if con["kind"] == "hard-equality":
            a = np.asarray(con["coefficients"], dtype=float)
            if abs(a @ v - con["target"]) > 1e-9:
                return False
    return True
