"""Canonical six-bond model -> dimod BinaryQuadraticModel.

Labels are the variable ids 'A'..'F'; canonical order is A..F left to right.
Coefficient convention: dimod BINARY linear biases = canonical a_i, quadratic
biases = canonical upper-triangular b_ij (each pair once), offset = c.

Sign convention warning: dimod's SPIN vartype uses x = (s + 1) / 2, the opposite
of the canonical x = (1 - s) / 2. Hence s_dimod = -s_canonical; tests check this.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
import dimod  # noqa: E402


def labels(problem: dict) -> List[str]:
    return [v["id"] for v in problem["variables"]]


def build_bqm(problem: dict) -> dimod.BinaryQuadraticModel:
    names = labels(problem)
    linear, quad, const = canonical.to_qubo(problem)
    return dimod.BinaryQuadraticModel(
        {names[i]: a for i, a in linear.items()},
        {(names[i], names[j]): b for (i, j), b in quad.items()},
        const,
        dimod.BINARY,
    )


def sample_to_vector(sample: Dict[str, int], problem: dict) -> List[int]:
    return [int(sample[name]) for name in labels(problem)]


def qpu_sampler_guarded():
    """Return a D-Wave QPU sampler ONLY with explicit opt-in.

    Requires QMENTOR_ALLOW_REMOTE=1, QMENTOR_CONFIRM_COST=yes, a Leap token in the
    approved secret store, and the optional `dwave-system` package. Never called by
    the default tests or by main.py.
    """
    if os.environ.get("QMENTOR_ALLOW_REMOTE") != "1" or os.environ.get("QMENTOR_CONFIRM_COST") != "yes":
        raise PermissionError("Remote D-Wave execution needs QMENTOR_ALLOW_REMOTE=1 and QMENTOR_CONFIRM_COST=yes.")
    from dwave.system import DWaveSampler, EmbeddingComposite  # optional dependency
    return EmbeddingComposite(DWaveSampler())
