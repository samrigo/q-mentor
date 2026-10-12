"""Classical baselines: exact enumeration and a seeded local-search heuristic."""

from __future__ import annotations

import time
from typing import Callable

import numpy as np

from .canonical import CanonicalQUBO, all_assignments, bits_to_str, is_feasible


def enumerate_exact(q: CanonicalQUBO, spec: dict | None = None, max_vars: int = 22) -> dict:
    """Exhaustive minimum. Refuses sizes where enumeration is not the right tool."""
    if q.n > max_vars:
        raise ValueError(f"{q.n} variables: use MIP/CP-SAT, not enumeration")
    t0 = time.perf_counter()
    rows = []
    for x in all_assignments(q.n):
        rows.append(
            {
                "bits": bits_to_str(x),
                "energy": q.energy(x),
                "feasible": is_feasible(spec, x) if spec else None,
            }
        )
    rows.sort(key=lambda r: r["energy"])
    elapsed = time.perf_counter() - t0
    best = rows[0]
    unique = len(rows) == 1 or rows[1]["energy"] - best["energy"] > 1e-9
    feasible_rows = [r for r in rows if r["feasible"]] if spec else rows
    return {
        "method": "exhaustive-enumeration",
        "n_states": len(rows),
        "best": best,
        "unique_optimum": unique,
        "runner_up_feasible": feasible_rows[1] if len(feasible_rows) > 1 else None,
        "all": rows,
        "wall_clock_s": elapsed,
    }


def penalty_separation(q: CanonicalQUBO, spec: dict) -> dict:
    """Prove on a small fixture that every infeasible state is worse than the best feasible one."""
    rows = enumerate_exact(q, spec)["all"]
    feas = [r["energy"] for r in rows if r["feasible"]]
    infeas = [r["energy"] for r in rows if not r["feasible"]]
    if not feas:
        return {"separates": False, "reason": "no feasible assignment"}
    margin = (min(infeas) - min(feas)) if infeas else float("inf")
    return {
        "separates": margin > 0,
        "best_feasible": min(feas),
        "best_infeasible": min(infeas) if infeas else None,
        "margin": margin,
    }


def simulated_annealing(
    q: CanonicalQUBO, seed: int, sweeps: int = 300, t_start: float = 20.0, t_end: float = 0.01
) -> dict:
    """Seeded simulated annealing with single-flip AND pair-swap moves.

    Swap moves keep cardinality, so the heuristic is not trapped by large
    penalty barriers; this gives the classical comparator fair tuning effort.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, q.n)
    e = q.energy(x)
    best_x, best_e = x.copy(), e
    t0 = time.perf_counter()
    for T in np.geomspace(t_start, t_end, sweeps):
        for _ in range(q.n):
            ones, zeros = np.flatnonzero(x == 1), np.flatnonzero(x == 0)
            if len(ones) and len(zeros) and rng.random() < 0.5:
                flip = [rng.choice(ones), rng.choice(zeros)]
            else:
                flip = [rng.integers(q.n)]
            x[flip] ^= 1
            e_new = q.energy(x)
            if e_new <= e or rng.random() < np.exp(-(e_new - e) / T):
                e = e_new
                if e < best_e:
                    best_x, best_e = x.copy(), e
            else:
                x[flip] ^= 1
    return {
        "method": "simulated-annealing (flip + swap moves)",
        "seed": seed,
        "sweeps": sweeps,
        "bits": bits_to_str(best_x),
        "energy": float(best_e),
        "wall_clock_s": time.perf_counter() - t0,
    }


def summarize_samples(
    samples: dict[str, int], energy: Callable[[str], float], feasible: Callable[[str], bool], optimum: float
) -> dict:
    """Metrics for any sampler: feasibility rate, best/median energy, optimality gap."""
    shots = sum(samples.values())
    energies = []
    n_feasible = 0
    for bits, count in samples.items():
        energies.extend([energy(bits)] * count)
        if feasible(bits):
            n_feasible += count
    energies_arr = np.array(energies)
    best = float(energies_arr.min())
    p_opt = sum(c for b, c in samples.items() if abs(energy(b) - optimum) < 1e-9) / shots
    # Wilson 95% interval for the probability of sampling the optimum
    z = 1.96
    denom = 1 + z**2 / shots
    centre = (p_opt + z**2 / (2 * shots)) / denom
    half = z * np.sqrt(p_opt * (1 - p_opt) / shots + z**2 / (4 * shots**2)) / denom
    return {
        "shots": shots,
        "feasibility_rate": n_feasible / shots,
        "best_energy": best,
        "median_energy": float(np.median(energies_arr)),
        "optimality_gap": best - optimum,
        "p_optimum": p_opt,
        "p_optimum_ci95": [float(max(0.0, centre - half)), float(min(1.0, centre + half))],
    }
