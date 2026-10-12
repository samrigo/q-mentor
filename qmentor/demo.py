"""Run the six-bond demo end to end, offline, and write result records.

    python -m qmentor.demo [--out demo/bond-selection/results] [--skip-quantum]

The executive brief is generated ONLY from the written records.
"""

from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from . import __version__
from .baseline import enumerate_exact, penalty_separation, simulated_annealing, summarize_samples
from .canonical import build_mean_variance_qubo, is_feasible, load_problem, str_to_bits
from .targets import TargetUnavailable, check_equivalence
from .targets import classiq_target, dwave_target, pennylane_target, pulser_target, qiskit_target
from .verdict import score

ROOT = Path(__file__).resolve().parent.parent
PROBLEM = ROOT / "demo" / "bond-selection" / "problem.json"


def run(out: Path, skip_quantum: bool = False) -> dict:
    spec = load_problem(PROBLEM)
    q = build_mean_variance_qubo(spec)
    exact = enumerate_exact(q, spec)
    sep = penalty_separation(q, spec)
    sa = [simulated_annealing(q, seed=s) for s in range(5)]

    targets = {}
    for mod in (qiskit_target, pennylane_target, classiq_target, dwave_target):
        entry = {"capability": mod.capability(q)}
        try:
            entry["equivalence"] = check_equivalence(q, mod.energy_table(q))
        except TargetUnavailable as exc:
            entry["equivalence"] = {"equivalent": None, "skipped": str(exc)}
        targets[mod.TARGET] = entry
    targets[pulser_target.TARGET] = {"capability": pulser_target.capability(q)}

    optimum = exact["best"]["energy"]
    energy = lambda b: q.energy(str_to_bits(b))  # noqa: E731
    feasible = lambda b: is_feasible(spec, str_to_bits(b))  # noqa: E731
    runs = []
    if not skip_quantum:
        for mod in (qiskit_target, pennylane_target):
            try:
                r = mod.run_qaoa_local(q)
            except TargetUnavailable as exc:
                runs.append({"target": mod.TARGET, "skipped": str(exc)})
                continue
            r["metrics"] = summarize_samples(r.pop("samples"), energy, feasible, optimum)
            runs.append(r)

    best = exact["best"]
    sel = [v for v, b in zip(q.variables, best["bits"]) if b == "1"]
    x = np.array(str_to_bits(best["bits"]), dtype=float)
    obj = spec["objective"]
    result = {
        "schema": "ResultRecord/1",
        "problem": spec["name"],
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": {"qmentor": __version__, "python": platform.python_version(), "numpy": np.__version__},
        "data_class": spec["provenance"]["data_class"],
        "bit_order": "index0-leftmost",
        "exact_baseline": {
            "method": exact["method"],
            "n_states": exact["n_states"],
            "bits": best["bits"],
            "selected": sel,
            "energy": best["energy"],
            "unique_optimum": exact["unique_optimum"],
            "runner_up_feasible": exact["runner_up_feasible"],
            "yield_score": float(np.dot(obj["expected_return"], x)),
            "risk": float(x @ np.asarray(obj["risk_matrix"]) @ x),
            "duration": float(sum(v["duration"] * b for v, b in zip(spec["variables"], x))),
            "wall_clock_s": exact["wall_clock_s"],
        },
        "penalty_separation": sep,
        "heuristic_baseline": {
            "method": "simulated-annealing",
            "seeds": [r["seed"] for r in sa],
            "hit_optimum": sum(abs(r["energy"] - optimum) < 1e-9 for r in sa),
            "runs": sa,
        },
        "targets": targets,
        "quantum_runs": runs,
        "evidence_level": "competitive-on-a-toy" if any(
            r.get("metrics", {}).get("optimality_gap", 1) < 1e-9 for r in runs
        ) else ("executable" if runs else "formulated"),
        "advantage_claimed": False,
    }
    verdict = score(
        {
            "problem_structure": 0.6,
            "formulation_quality": 0.9,
            "classical_comparison": 0.0,  # exact enumeration solves it instantly
            "input_output_fit": 0.5,
            "resource_fit": 0.6,
            "evidence": 0.2,
        },
        {"no_classical_baseline": False, "unsupported_advantage_claim": False},
    )
    result["verdict"] = verdict
    out.mkdir(parents=True, exist_ok=True)
    (out / "result-record.json").write_text(json.dumps(result, indent=2, default=float) + "\n")
    (out / "executive-brief.md").write_text(brief(result))
    return result


def brief(r: dict) -> str:
    """One-page brief built strictly from a ResultRecord."""
    e = r["exact_baseline"]
    lines = [
        "# Executive brief - six-bond selection (synthetic)",
        "",
        f"_Generated from `result-record.json` ({r['generated']}). Synthetic data; not investment advice._",
        "",
        f"**Decision:** {r['verdict']['verdict']} (score {r['verdict']['score']}/100, band {r['verdict']['score_band']}"
        + (f"; capped: {', '.join(r['verdict']['caps_applied'])}" if r['verdict'].get('caps_applied') else "")
        + "). "
        "Use exact classical enumeration; keep quantum as a teaching exercise.",
        "",
        "## Evidence",
        f"- Exact enumeration of {e['n_states']} states found {', '.join(e['selected'])} "
        f"(bits `{e['bits']}`), energy {e['energy']:.4f}, in {e['wall_clock_s']*1000:.1f} ms.",
        f"- Seeded simulated annealing reached the optimum in {r['heuristic_baseline']['hit_optimum']}"
        f"/{len(r['heuristic_baseline']['seeds'])} seeds.",
    ]
    for name, t in r["targets"].items():
        eq = t.get("equivalence", {})
        status = t["capability"]["status"]
        if eq.get("equivalent") is True:
            lines.append(f"- {name}: {status}; energies match on all {eq['states_checked']} states.")
        elif eq.get("skipped"):
            lines.append(f"- {name}: {status}; equivalence not run ({eq['skipped']}).")
        elif "equivalence" in t:
            lines.append(f"- {name}: {status}; equivalence FAILED.")
        else:
            lines.append(f"- {name}: {status}; " + "; ".join(t["capability"]["failures"]) + ".")
    for q in r["quantum_runs"]:
        if "skipped" in q:
            lines.append(f"- {q['target']} QAOA: skipped ({q['skipped']}).")
            continue
        m = q["metrics"]
        lines.append(
            f"- {q['target']} QAOA ({q.get('backend', q.get('device'))}, seed {q['seed']}, {m['shots']} shots): "
            f"feasible {m['feasibility_rate']:.0%}, best gap {m['optimality_gap']:.4f}, "
            f"P(optimum) {m['p_optimum']:.3f} (95% CI {m['p_optimum_ci95'][0]:.3f}-{m['p_optimum_ci95'][1]:.3f})."
        )
    lines += [
        "",
        f"## Evidence level\n{r['evidence_level']}. Matching a 64-state toy optimum is **not** quantum advantage.",
        "",
        "## Limits",
        "- Toy mean-variance model: no prices, lots, liquidity, turnover, taxes, or estimation error.",
        "- Simulators are noiseless; no hardware, queue time, or provider cost measured.",
        "",
        "## Next gate",
        "Revisit only with a problem class where a tuned classical solver (MIP/CP-SAT) measurably struggles "
        "and an end-to-end benchmark plan is approved.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", default=str(ROOT / "demo" / "bond-selection" / "results"))
    p.add_argument("--skip-quantum", action="store_true", help="skip local QAOA simulation runs")
    args = p.parse_args()
    r = run(Path(args.out), args.skip_quantum)
    print(json.dumps({"optimum": r["exact_baseline"]["bits"], "energy": r["exact_baseline"]["energy"],
                      "verdict": r["verdict"]["verdict"], "out": args.out}, indent=2))


if __name__ == "__main__":
    main()
