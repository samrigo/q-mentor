"""Pasqal/Pulser adapter: capability check first, code second.

Two problems live here:

1. The canonical six-bond QUBO. Before any sequence is built we test whether a
   neutral-atom register on `pulser.devices.AnalogDevice` can represent it
   exactly. Rydberg interactions are U_ij = C6 / r_ij^6 (always positive) and
   are fixed by geometry; the device exposes only a global Rydberg channel, so
   every atom sees the same detuning. The six-bond QUBO needs 15 independent
   couplings (only 2N-3 = 9 geometric degrees of freedom in 2D) and six
   different linear terms, so the exact mapping is refused.

2. A *geometry-native* 4-atom QUBO whose couplings are DEFINED by a register on
   the same device (U_ij = C6/r_ij^6, uniform linear term -delta). This is the
   supported example: canonical energy and physical Hamiltonian agree by
   construction, and the adapter recomputes them from Pulser's device data.

Bit order: register qubit k <-> bitstring character k; '1' = Rydberg state.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
from scipy.optimize import minimize
from scipy.spatial.distance import pdist, squareform

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "demo" / "bond-selection"))

import canonical  # noqa: E402
from pulser import Register  # noqa: E402
from pulser.devices import AnalogDevice  # noqa: E402

DEVICE = AnalogDevice
EXACT_REL_TOL = 0.01      # 1 % coupling error still counts as "exact"
APPROX_REL_TOL = 0.10     # beyond 10 % we do not even offer a labelled approximation
SEED = 7


# --------------------------------------------------------------------------- #
# 1. Capability report for the canonical six-bond QUBO
# --------------------------------------------------------------------------- #
def _fit_geometry(target: np.ndarray, n: int, restarts: int = 20) -> Tuple[np.ndarray, float]:
    """Best 2D positions so that C6/r^6 is proportional to target couplings.

    Minimises squared log-ratio error with a free global scale, i.e. the most
    generous possible embedding (device distance limits are checked afterwards).
    """
    rng = np.random.default_rng(SEED)
    iu = np.triu_indices(n, 1)
    log_t = np.log(target[iu])

    def loss(flat: np.ndarray) -> float:
        coords = flat[:-1].reshape(n, 2)
        log_scale = flat[-1]
        d = pdist(coords)
        log_u = np.log(DEVICE.interaction_coeff) - 6 * np.log(np.maximum(d, 1e-6))
        return float(np.sum((log_u - (log_t + log_scale)) ** 2))

    best_x, best_f = None, np.inf
    for _ in range(restarts):
        x0 = np.concatenate([rng.uniform(0, 15, 2 * n), [0.0]])
        res = minimize(loss, x0, method="L-BFGS-B")
        if res.fun < best_f:
            best_x, best_f = res.x, res.fun
    coords = best_x[:-1].reshape(n, 2)
    coords -= coords.mean(axis=0)
    u_pairs = DEVICE.interaction_coeff / pdist(coords) ** 6   # pdist order == triu order
    scale = np.exp(best_x[-1])
    rel = np.abs(u_pairs - scale * target[iu]) / (scale * target[iu])
    return coords, float(rel.max())


def capability_report(problem: dict) -> dict:
    linear, quad, const = canonical.to_qubo(problem)
    n = len(linear)
    target = np.zeros((n, n))
    for (i, j), b in quad.items():
        target[i, j] = target[j, i] = b
    couplings = np.array(list(quad.values()))
    lin = np.array(list(linear.values()))
    coords, max_rel_err = _fit_geometry(target, n)
    min_dist = float(pdist(coords).min())
    max_radius = float(np.linalg.norm(coords, axis=1).max())
    has_local_detuning = bool(getattr(DEVICE, "dmm_channels", {})) or any(
        ch.addressing == "Local" for ch in DEVICE.channels.values())

    checks = [
        {"check": "coupling sign", "required": "all b_ij > 0 (Rydberg repulsion)",
         "observed": f"min b_ij = {couplings.min():.4f}", "pass": bool(couplings.min() > 0)},
        {"check": "geometric degrees of freedom",
         "required": f"{n * (n - 1) // 2} independent couplings",
         "observed": f"2D register offers {2 * n - 3} (rigid-motion-free) coordinates",
         "pass": n * (n - 1) // 2 <= 2 * n - 3},
        {"check": "best-fit embedding error",
         "required": f"max relative coupling error <= {EXACT_REL_TOL:.0%}",
         "observed": f"{max_rel_err:.1%}", "pass": max_rel_err <= EXACT_REL_TOL},
        {"check": "device distance limits",
         "required": f"min distance >= {DEVICE.min_atom_distance} um, radius <= {DEVICE.max_radial_distance} um",
         "observed": f"best-fit min distance {min_dist:.2f} um, radius {max_radius:.2f} um",
         "pass": bool(min_dist >= DEVICE.min_atom_distance and max_radius <= DEVICE.max_radial_distance)},
        {"check": "per-qubit linear terms",
         "required": "local detuning or DMM to realise 6 distinct a_i",
         "observed": f"a_i spread {lin.min():.2f}..{lin.max():.2f}; device local detuning available: {has_local_detuning}",
         "pass": bool(has_local_detuning or np.ptp(lin) < 1e-9)},
    ]
    exact = all(c["pass"] for c in checks)
    approx_ok = max_rel_err <= APPROX_REL_TOL and has_local_detuning
    return {
        "schema": "qmentor.capability-report.v2",
        "problem_id": problem["id"],
        "target": "pasqal-pulser",
        "device": DEVICE.name,
        "device_facts": {"interaction_coeff_C6": DEVICE.interaction_coeff,
                         "min_atom_distance_um": DEVICE.min_atom_distance,
                         "max_radial_distance_um": DEVICE.max_radial_distance,
                         "channels": sorted(DEVICE.channels)},
        "status": "exact" if exact else ("approximate" if approx_ok else "unsupported-exact"),
        "checks": checks,
        "lost_semantics": [] if exact else [
            "independent pairwise couplings (geometry fixes all 15 from 12 coordinates)",
            "per-asset linear terms (global channel applies one detuning to all atoms)",
        ],
        "approximation_offered": approx_ok,
        "alternatives": [
            "Run the same canonical QUBO on a gate-model target (Qiskit, Classiq, PennyLane) or D-Wave BQM; see sibling examples.",
            "Reformulate toward a geometry-native problem (e.g. weighted independent set on a register) and re-run this report.",
            "Use a device with local detuning (DMM) and re-check the coupling-fit error; any result must be labelled approximate with this bound.",
            "Check docs.pasqal.com for a higher-level QUBO workflow; record its version before relying on it.",
        ],
    }


# --------------------------------------------------------------------------- #
# 2. Geometry-native supported QUBO (4 atoms on a line)
# --------------------------------------------------------------------------- #
SPACING_UM = 6.0
N_NATIVE = 4
DELTA_FINAL = 6.0          # rad/us; uniform linear term is -DELTA_FINAL
OMEGA_MAX = 2.0 * np.pi * 0.8   # rad/us, below AnalogDevice max amplitude


def native_register() -> Register:
    coords = np.array([[k * SPACING_UM, 0.0] for k in range(N_NATIVE)])
    coords -= coords.mean(axis=0)
    return Register.from_coordinates(coords, prefix="q")


def native_qubo(register: Register) -> Tuple[Dict[int, float], Dict[Tuple[int, int], float], float]:
    """Canonical QUBO defined by the register: E(x) = sum U_ij x_i x_j - delta * sum x_i."""
    pos = np.array([register.qubits[q].as_array() for q in register.qubit_ids], dtype=float)
    dist = squareform(pdist(pos))
    linear = {i: -DELTA_FINAL for i in range(len(pos))}
    quad = {(i, j): float(DEVICE.interaction_coeff / dist[i, j] ** 6)
            for i in range(len(pos)) for j in range(i + 1, len(pos))}
    return linear, quad, 0.0


def native_energy(x: Sequence[int], qubo) -> float:
    return canonical.qubo_energy(x, *qubo)


def native_ranking(qubo) -> List[Tuple[float, str]]:
    n = len(qubo[0])
    return sorted((native_energy(x, qubo), canonical.bitstring(x)) for x in itertools.product((0, 1), repeat=n))


def rydberg_hamiltonian_diagonal(x: Sequence[int], register: Register) -> float:
    """Diagonal of the final Rydberg Hamiltonian H/hbar = sum_{i<j} U_ij n_i n_j - delta sum n_i,
    computed independently from Pulser's device coefficient and register distances."""
    ids = register.qubit_ids
    energy = -DELTA_FINAL * sum(x)
    for i, j in itertools.combinations(range(len(ids)), 2):
        r = np.linalg.norm(register.qubits[ids[i]].as_array() - register.qubits[ids[j]].as_array())
        energy += DEVICE.interaction_coeff / float(r) ** 6 * x[i] * x[j]
    return float(energy)


if __name__ == "__main__":
    print(json.dumps(capability_report(canonical.load_problem()), indent=2))
