"""Credential-gated repeat of the optimization comparison on Classiq's own synthesis and executor.

NOT run by tests or CI. It needs `classiq.authenticate()` credentials, uses the Classiq synthesis service and the
Classiq "simulator" execution backend, and may incur cost. It refuses to start unless QMENTOR_ALLOW_REMOTE=1 is set after an
explicit human approval of provider, backend, and budget. Validation state of its output: target-validated only
after it has actually run; until then the Classiq-side numbers are `unverified`.

Run: QMENTOR_ALLOW_REMOTE=1 python run_remote.py
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
from classiq import ExecutionSession, synthesize
from scipy.optimize import minimize

import adapter
import main as harness

HERE = Path(__file__).resolve().parent


def cost_func(state) -> float:
    return adapter.canonical_energy([int(b) for b in state["v"]])


def run(p: int, quantile: float, seed: int) -> dict:
    qprog = synthesize(adapter.build_main(p))
    rng = np.random.default_rng(seed)
    with ExecutionSession(qprog, backend="simulator", num_shots=harness.SHOTS, random_seed=seed) as session:
        trace = []

        def objective(params):
            value = session.estimate_cost(cost_func, {"params": params.tolist()}, quantile=quantile)
            trace.append(value)
            return value

        res = minimize(objective, harness.initial_params(p, rng), method="COBYLA",
                       options={"maxiter": harness.MAX_EVALS})
        sample = session.sample({"params": res.x.tolist()})
    optimum = adapter.exact_ranking()[0][1]
    shots = sum(s.shots for s in sample.parsed_counts)
    hits = sum(s.shots for s in sample.parsed_counts if "".join(str(int(b)) for b in s.state["v"]) == optimum)
    return {"p": p, "quantile": quantile, "seed": seed, "evaluations": len(trace),
            "sampled_optimum_frequency": hits / shots, "params": res.x.tolist()}


if __name__ == "__main__":
    if os.environ.get("QMENTOR_ALLOW_REMOTE") != "1":
        print("refused: set QMENTOR_ALLOW_REMOTE=1 only after approving provider, backend and budget")
        sys.exit(2)
    results = [run(p, q, s) for p in (1, 2) for q in (1.0, harness.CVAR_ALPHA) for s in harness.SEEDS]
    (HERE / "remote_results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
