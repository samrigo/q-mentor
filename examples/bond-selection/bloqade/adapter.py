"""QuEra Bloqade (analog) adapter: capability check first, native analog program second.

1. Six-bond QUBO -> neutral-atom analog: refused as `unsupported-exact`. Rydberg couplings are
   U_ij = C6 / r_ij^6 > 0 and fixed by geometry: 15 independent couplings cannot be matched by 6 atoms in 2-D
   (2N - 3 = 9 geometric degrees of freedom). The best possible fit is measured, not assumed.
2. Native problem: a 5-atom chain whose classical final Hamiltonian (a maximum-independent-set style QUBO)
   E(n) = -delta_f * sum n_i + sum_{i<j} C6 / r_ij^6 n_i n_j is DEFINED by the geometry and the final detuning.
   An adiabatic sweep on the Bloqade emulator should concentrate probability on its classical ground state.

Conventions (tested):
* C6 = bloqade.analog.RB_C6 (rad um^6 / us); distances in um, time in us, rates in rad/us.
* Bloqade report bitstrings use '0' = Rydberg. This adapter reads the emulator state vector through
  `run_callback` and converts to the canonical convention '1' = Rydberg, atom k = character k.
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
from bloqade.analog import RB_C6, start  # noqa: E402
from scipy.optimize import minimize  # noqa: E402
from scipy.spatial.distance import pdist  # noqa: E402

SEED = 7
EXACT_REL_TOL = 0.01
SPACING_UM = 6.1
N_ATOMS = 5
OMEGA_MAX = 15.7          # rad/us
DELTA_START, DELTA_END = -16.0, 16.0  # rad/us
RAMP, SWEEP = 0.1, 3.8    # us


# ------------------------------------------------------------------ 1. six-bond capability report
def fit_geometry(target: np.ndarray, n: int, restarts: int = 20) -> Tuple[np.ndarray, float]:
    """Most generous 2-D embedding: free global scale, log-ratio least squares. Returns (coords, max rel error)."""
    rng = np.random.default_rng(SEED)
    iu = np.triu_indices(n, 1)
    log_t = np.log(target[iu])

    def loss(flat: np.ndarray) -> float:
        coords = flat[:-1].reshape(n, 2)
        log_u = np.log(RB_C6) - 6 * np.log(np.maximum(pdist(coords), 1e-6))
        return float(np.sum((log_u - (log_t + flat[-1])) ** 2))

    best = None
    for _ in range(restarts):
        res = minimize(loss, np.concatenate([rng.uniform(0, 15, 2 * n), [0.0]]), method="L-BFGS-B")
        if best is None or res.fun < best.fun:
            best = res
    coords = best.x[:-1].reshape(n, 2)
    u = RB_C6 / pdist(coords) ** 6
    scale = np.exp(best.x[-1])
    rel = np.abs(u - scale * target[iu]) / (scale * target[iu])
    return coords - coords.mean(axis=0), float(rel.max())


def capability_report(problem: dict) -> dict:
    linear, quad, _ = canonical.to_qubo(problem)
    n = len(linear)
    target = np.zeros((n, n))
    for (i, j), b in quad.items():
        target[i, j] = target[j, i] = b
    negative = [k for k, v in quad.items() if v <= 0]
    _, max_rel = fit_geometry(target, n) if not negative else (None, float("inf"))
    exact = not negative and max_rel <= EXACT_REL_TOL
    return {
        "schema": "qmentor.capability-report.v3",
        "problem_id": problem["id"],
        "target": {"provider": "QuEra", "sdk": "bloqade-analog 0.16.9", "backend": "bloqade python emulator / Aquila AHS",
                   "physical_family": "neutral-atom", "model": "analog", "support_level": "tested-local"},
        "status": "exact" if exact else "unsupported-exact",
        "checks": {
            "couplings_required": len(quad),
            "geometric_degrees_of_freedom_2d": 2 * n - 3,
            "non_positive_couplings": len(negative),
            "best_fit_max_relative_coupling_error": round(max_rel, 4),
            "exact_tolerance": EXACT_REL_TOL,
            "distinct_linear_terms": len({round(v, 9) for v in linear.values()}),
            "local_detuning": "site-dependent scale factors in [0, 1] times one global waveform (Aquila-style); "
                              "cannot fix the geometry mismatch",
        },
        "lost_semantics": ["15 independent pair couplings", "arbitrary coupling ratios"] if not exact else [],
        "alternatives": ["gate-model QAOA (Qiskit, Cirq, pytket) - exact energy mapping",
                         "D-Wave BQM (dimod) - exact energy model",
                         "a geometry-native problem on Bloqade (this folder's main.py)"],
    }


# ------------------------------------------------------------------ 2. native analog program
def positions() -> List[Tuple[float, float]]:
    return [(SPACING_UM * k, 0.0) for k in range(N_ATOMS)]


def native_qubo() -> Tuple[Dict[int, float], Dict[Tuple[int, int], float]]:
    """Classical final Hamiltonian in canonical QUBO form (constant 0)."""
    pos = np.array(positions())
    linear = {i: -DELTA_END for i in range(N_ATOMS)}
    quad = {(i, j): float(RB_C6 / np.linalg.norm(pos[i] - pos[j]) ** 6)
            for i, j in itertools.combinations(range(N_ATOMS), 2)}
    return linear, quad


def native_energy(x: Sequence[int]) -> float:
    linear, quad = native_qubo()
    return canonical.qubo_energy(x, linear, quad, 0.0)


def classical_ground_state() -> Tuple[str, float]:
    best = min(itertools.product((0, 1), repeat=N_ATOMS), key=native_energy)
    return canonical.bitstring(best), native_energy(best)


def program():
    durations = [RAMP, SWEEP, RAMP]
    return (start.add_position(positions())
            .rydberg.rabi.amplitude.uniform.piecewise_linear(durations, [0.0, OMEGA_MAX, OMEGA_MAX, 0.0])
            .detuning.uniform.piecewise_linear(durations, [DELTA_START, DELTA_START, DELTA_END, DELTA_END]))


def _collect(state, metadata, hamiltonian):
    probs = np.abs(state.data) ** 2
    rydberg = np.array([state.space.is_rydberg_at(k) for k in range(N_ATOMS)])  # shape (atoms, configs)
    out: Dict[str, float] = {}
    for c in range(probs.size):
        key = "".join("1" if rydberg[k, c] else "0" for k in range(N_ATOMS))
        out[key] = out.get(key, 0.0) + float(probs[c])
    return out


def exact_distribution() -> Dict[str, float]:
    """Final-state probabilities from the emulator, canonical convention ('1' = Rydberg)."""
    return program().bloqade.python().run_callback(_collect, atol=1e-10, rtol=1e-8)[0]


def sampled_counts(shots: int) -> Dict[str, int]:
    """Bloqade's own shot sampler (global numpy RNG, seeded), converted from its '0' = Rydberg convention."""
    np.random.seed(SEED)
    raw = program().bloqade.python().run(shots, atol=1e-10, rtol=1e-8).report().counts()[0]
    return {"".join("1" if ch == "0" else "0" for ch in key): int(v) for key, v in raw.items()}
