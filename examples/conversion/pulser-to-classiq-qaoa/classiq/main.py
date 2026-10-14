"""Pasqal/Pulser -> Classiq optimization regression (README-10): build, verify, and compare QAOA variants fairly.

1. Build the Classiq Qmod model offline for p = 1, 2, 4 (create_model + native Qmod export); verify the exported
   cost expression equals the canonical QUBO on all 32 assignments.
2. Compare variants at a FIXED budget on the identical objective, feasible set, initial state and decode:
   depth p in {1, 2} first, p = 4 only if the best stage-1 optimum probability is below STAGE2_THRESHOLD;
   optimizer modes "mean" (estimate_cost quantile=1.0 + SciPy COBYLA, the documented pattern) and "cvar"
   (estimate_cost quantile=0.3, i.e. the mean of the LOWEST 30 % of sampled costs, as implemented by the
   installed SDK) + COBYLA; shot-budget split 1000 shots x 60 evaluations or 4000 x 15 (same 60 000 shots per
   seed); seeds 7, 11, 13.
3. Select by a predeclared primary metric (exact optimum probability at the final angles) under a resource cap.
   A candidate is "improved" only if its 95 % interval lies above the baseline's; otherwise "not-improved".

Classiq synthesis and execution need credentials and are NOT run; every variant is evaluated on
adapter.statevector, a local reference simulator of the identical ansatz. run_remote.py repeats the comparison on
Classiq's executor only with QMENTOR_ALLOW_REMOTE=1 and explicit approval.
Run: python main.py   (inside the pinned Classiq environment)
"""
import json
import time
from pathlib import Path

import classiq
import numpy as np
from scipy import stats
from scipy.optimize import minimize

import adapter

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
SEEDS = [7, 11, 13]
SHOTS = 1000
MAX_EVALS = 60
FINAL_SHOTS = 1000
CVAR_ALPHA = 0.3
STAGE2_THRESHOLD = 0.5
RESOURCE_CAP_TWO_QUBIT = 80
PRIMARY_METRIC = "optimum_probability (exact, at the final angles; mean over seeds)"


def initial_params(p: int, rng: np.random.Generator) -> np.ndarray:
    """Official pattern: gammas linspace(0, 1), betas linspace(1, 0); seeded jitter separates the starts."""
    base = np.concatenate((np.linspace(0, 1, p), np.linspace(1, 0, p)))
    return base + rng.uniform(-0.1, 0.1, 2 * p)


TOTAL_SHOTS_PER_SEED = SHOTS * MAX_EVALS


def interval(values, lo=None, hi=None):
    """Mean and two-sided 95 % t-interval over seeds (clipped to [lo, hi] for probabilities)."""
    values = np.asarray(values, dtype=float)
    mean = float(values.mean())
    if len(values) < 2 or values.std(ddof=1) == 0:
        return {"mean": round(mean, 6), "ci95": [round(mean, 6), round(mean, 6)]}
    half = float(stats.t.ppf(0.975, len(values) - 1) * values.std(ddof=1) / np.sqrt(len(values)))
    low, high = mean - half, mean + half
    low = max(low, lo) if lo is not None else low
    high = min(high, hi) if hi is not None else high
    return {"mean": round(mean, 6), "ci95": [round(low, 6), round(high, 6)]}


def run_variant(p: int, mode: str, optimum: str, optimum_energy: float, shots: int = SHOTS,
                max_evals: int = MAX_EVALS) -> dict:
    assert shots * max_evals == TOTAL_SHOTS_PER_SEED, "every variant gets the same total shot budget"
    quantile = 1.0 if mode == "mean" else CVAR_ALPHA
    per_seed = []
    start = time.perf_counter()
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        evals = {"n": 0}

        def objective(params):
            evals["n"] += 1
            return adapter.sampled_cost(params, p, shots, quantile, rng)

        res = minimize(objective, initial_params(p, rng), method="COBYLA", options={"maxiter": max_evals})
        probs = adapter.probabilities(res.x, p)
        sample = np.bincount(rng.choice(len(probs), size=FINAL_SHOTS, p=probs / probs.sum()), minlength=len(probs))
        best_idx = min(np.nonzero(sample)[0], key=lambda k: adapter.ENERGIES[k])
        per_seed.append({
            "seed": seed,
            "evaluations": int(evals["n"]),
            "optimum_probability": float(probs[int(optimum, 2)]),
            "expected_energy": float(probs @ adapter.ENERGIES),
            "feasible_probability": 1.0,
            "best_sampled": "".join(map(str, adapter.STATES[best_idx])),
            "best_sampled_energy": float(adapter.ENERGIES[best_idx]),
            "params": [round(float(v), 6) for v in res.x],
        })
    elapsed = time.perf_counter() - start
    res_count = adapter.resources(p)
    best_e = min(s["best_sampled_energy"] for s in per_seed)
    return {
        "id": f"p{p}-{mode}" + ("" if shots == SHOTS else f"-{shots}x{max_evals}"),
        "p": p,
        "optimizer": f"SciPy COBYLA maxiter={max_evals} on estimate_cost(quantile={quantile}), {shots} shots/evaluation",
        "shots_per_evaluation": shots,
        "max_evaluations": max_evals,
        "objective_mode": "mean" if mode == "mean" else "cvar",
        "best_feasible_energy": round(best_e, 9),
        "gap_to_optimum": round(best_e - optimum_energy, 9),
        "feasible_probability": interval([s["feasible_probability"] for s in per_seed], 0.0, 1.0),
        "expected_energy": interval([s["expected_energy"] for s in per_seed]),
        "optimum_probability": interval([s["optimum_probability"] for s in per_seed], 0.0, 1.0),
        "evaluations": int(sum(s["evaluations"] for s in per_seed)),
        "depth": res_count["depth"],
        "two_qubit_gates": res_count["two_qubit_gates"],
        "wall_time_s": round(elapsed, 3),
        "per_seed": per_seed,
    }


def select(variants: list, baseline_id: str) -> tuple:
    base = next(v for v in variants if v["id"] == baseline_id)
    winners = [v for v in variants if v["id"] != baseline_id and v["two_qubit_gates"] <= RESOURCE_CAP_TWO_QUBIT
               and v["optimum_probability"]["ci95"][0] > base["optimum_probability"]["ci95"][1]]
    if not winners:
        return baseline_id, "not-improved", (
            f"No variant's 95% interval for the primary metric lies above the baseline {baseline_id} "
            f"({base['optimum_probability']['mean']:.3f}); the simpler variant is kept.")
    best = max(winners, key=lambda v: (v["optimum_probability"]["mean"], -v["two_qubit_gates"]))
    return best["id"], "improved", (
        f"{best['id']} raises the primary metric from {base['optimum_probability']['mean']:.3f} to "
        f"{best['optimum_probability']['mean']:.3f} (95% intervals disjoint) within the cap of "
        f"{RESOURCE_CAP_TWO_QUBIT} two-qubit gates ({best['two_qubit_gates']}).")


def verify_model() -> dict:
    out = {}
    for p in (1, 2, 4):
        model = adapter.build_model(p)
        path = adapter.export_qmod(p, HERE)
        text = path.read_text()
        # The SDK simplifies the exported expression (e.g. 1.0 * v[i] * v[j] -> (v[i] and v[j])); evaluate what it
        # actually wrote. phase_expr = -C(x)/s, so energy = -phase_expr * s + c.
        expr = text.split("phase (", 1)[1].rsplit(", gamma);", 1)[0]
        err = max(abs(-adapter.evaluate_expression(expr, x) * adapter.SCALE + adapter.CONSTANT - adapter.canonical_energy(x))
                  for x in adapter.STATES)
        out[f"p{p}"] = {"model_bytes": len(model), "native_qmod": path.name, "max_energy_error_all_32_states": err,
                        "named_layers": all(f"qfunc {n}" in text for n in ("cost_layer", "mixer_layer", "qaoa_ansatz")),
                        "param_slicing": f"params[0:{p}]" in text and f"params[{p}:{2 * p}]" in text}
    return out


def main() -> dict:
    ranking = adapter.exact_ranking()
    t0 = time.perf_counter()
    optimum_energy, optimum = adapter.exact_ranking()[0]
    enum_time = time.perf_counter() - t0
    model_checks = verify_model()
    variants = [run_variant(p, mode, optimum, optimum_energy) for p in (1, 2) for mode in ("mean", "cvar")]
    variants.append(run_variant(2, "mean", optimum, optimum_energy, shots=4000, max_evals=15))
    best_stage1 = max(v["optimum_probability"]["mean"] for v in variants)
    stage2 = best_stage1 < STAGE2_THRESHOLD
    if stage2:
        variants += [run_variant(4, mode, optimum, optimum_energy) for mode in ("mean", "cvar")]
    selected, status, reason = select(variants, "p1-mean")
    record = {
        "schema": "qmentor.optimization-record.v3",
        "problem_id": adapter.PROBLEM["id"],
        "objective_hash": adapter.objective_hash(),
        "feasible_set": "all 32 assignments (unconstrained QUBO from the Pulser register); feasible probability is 1 by construction",
        "exact_optimum": {"bitstring": optimum, "energy": round(optimum_energy, 9),
                          "runner_up": {"bitstring": ranking[1][1], "energy": round(ranking[1][0], 9)}},
        "classical_baseline": {"method": "exhaustive enumeration (32 states)", "best_energy": round(optimum_energy, 9),
                               "wall_time_s": round(enum_time, 6)},
        "primary_metric": PRIMARY_METRIC,
        "resource_cap": f"two-qubit gates <= {RESOURCE_CAP_TWO_QUBIT} (reference CX-RZ-CX decomposition)",
        "budget": {"shots_per_evaluation": SHOTS, "max_evaluations": MAX_EVALS, "seeds": SEEDS,
                   "total_shots_per_seed": TOTAL_SHOTS_PER_SEED,
                   "final_sample_shots": FINAL_SHOTS,
                   "stage_rule": f"p in {{1,2}} first; p=4 only if best stage-1 optimum probability < {STAGE2_THRESHOLD}",
                   "stage2_run": stage2},
        "conventions": {
            "cost_unitary": "phase(-cost(v), gamma) = exp(-i gamma C(x)/s), s = max |coefficient| = %.9f" % adapter.SCALE,
            "mixer_unitary": "RX(beta, q) on every qubit = exp(-i (beta/2) X) per qubit",
            "rx_convention": "RX(theta) = exp(-i theta X / 2) (classiq 1.32.0 docstring); RX(beta) and RX(2 beta) label the same family with different ranges",
            "angle_bounds": "unbounded COBYLA; gammas start linspace(0,1,p), betas linspace(1,0,p), +/-0.1 seeded jitter",
            "phase_decorator": "@qfunc (official example). @qperm accepted for the cost layer by create_model, rejected for the RX mixer; no offline synthesis benefit measurable, not adopted",
            "cvar_alpha": CVAR_ALPHA,
        },
        "variants": variants,
        "baseline_variant": "p1-mean",
        "selected": selected,
        "status": status,
        "selection_reason": reason,
        "execution": {
            "engine": "adapter.statevector: local reference simulator of the identical Qmod ansatz (numpy)",
            "validation_state": "imported (Classiq model built offline for p=1,2,4); variants locally-executed on the reference simulator",
            "target_sdk_execution": "unverified-credential-required",
        },
        "model_checks": model_checks,
        "versions": {"classiq": classiq.__version__, "numpy": np.__version__},
        "source_reference": json.loads((OUT / "source_result.json").read_text())["quantum"],
    }
    (OUT / "optimization_record.json").write_text(json.dumps(record, indent=2) + "\n")
    summary = {v["id"]: {"p_opt": v["optimum_probability"], "E": v["expected_energy"]["mean"],
                         "2q": v["two_qubit_gates"]} for v in variants}
    print(json.dumps({"selected": selected, "status": status, "reason": reason, "variants": summary}, indent=2))
    return record


if __name__ == "__main__":
    main()
