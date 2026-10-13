"""Six-bond selection in Classiq: Python-Qmod QAOA model + native Qmod export.

Offline (default): builds the model locally with `create_model`, exports native
Qmod (`bond_selection.qmod`) and checks the stored cost polynomial against the
canonical energy for all 64 states. No credentials, no network.

Remote (opt-in, UNVERIFIED in this repository's CI): with QMENTOR_ALLOW_REMOTE=1
and QMENTOR_CONFIRM_COST=yes after `classiq.authenticate()`, synthesizes the
model and samples it on Classiq's default simulator.
"""
import itertools
import json
import os
from pathlib import Path

import classiq
from classiq import ExecutionSession, synthesize, write_qmod

import adapter
import canonical

HERE = Path(__file__).resolve().parent
SEED = 7
SHOTS = 2048
# Fixed illustrative angles; the remote path is a smoke test, not a tuned QAOA.
PARAMS = [0.002, 0.6, 0.004, 0.3]


def offline_validation(problem: dict) -> dict:
    model_json = adapter.build_model()
    write_qmod(adapter.main, "bond_selection", directory=HERE, decimal_precision=10, symbolic_only=False)
    (HERE / "bond_selection.synthesis_options.json").unlink(missing_ok=True)  # randomised seed; not an artifact
    exprs = adapter.model_phase_expressions(model_json)
    max_err = 0.0
    for x in itertools.product((0, 1), repeat=adapter.N):
        value = adapter.evaluate_cost_text(exprs[0], x) + adapter.CONSTANT
        max_err = max(max_err, abs(value - canonical.direct_energy(x, problem)))
    return {"model_bytes": len(model_json), "phase_expressions_found": len(exprs),
            "max_energy_error_all_64_states": max_err, "native_qmod": "bond_selection.qmod"}


def remote_sample(problem: dict) -> dict:
    if os.environ.get("QMENTOR_ALLOW_REMOTE") != "1" or os.environ.get("QMENTOR_CONFIRM_COST") != "yes":
        return {"status": "not-run", "reason": "remote synthesis/execution requires explicit approval"}
    qprog = synthesize(adapter.main)
    with ExecutionSession(qprog, num_shots=SHOTS, random_seed=SEED) as session:
        frame = session.sample({"params": PARAMS})
    best = None
    for _, row in frame.iterrows():
        x = [int(v) for v in row["x"]]
        info = canonical.decode(x, problem)
        if best is None or info["energy"] < best["energy"]:
            best = info
    return {"status": "unverified-by-ci", "best_sampled": best}


def main() -> dict:
    problem = canonical.load_problem()
    record = {
        "schema": "qmentor.result-record.v2",
        "target": "classiq",
        "versions": {"classiq": classiq.__version__},
        "baseline": canonical.exact_baseline(problem),
        "offline_model_validation": offline_validation(problem),
        "remote": remote_sample(problem),
        "validation_state": "imported (model created and cost verified locally); synthesis unverified",
        "evidence_level": "formulated (level 1); no quantum hardware used; not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
