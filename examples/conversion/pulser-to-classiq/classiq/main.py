"""Build the Classiq reimplementation offline and verify its cost on all 16 states.

Credentialed synthesis is not run here; the validation state is `imported`.
"""
import itertools
import json
from pathlib import Path

import classiq
from classiq import write_qmod

import adapter

HERE = Path(__file__).resolve().parent


def main() -> dict:
    model = adapter.build_model()
    write_qmod(adapter.main, "pulser_native_qaoa", directory=HERE, decimal_precision=12, symbolic_only=False)
    (HERE / "pulser_native_qaoa.synthesis_options.json").unlink(missing_ok=True)  # randomised seed; not an artifact
    qmod = (HERE / "pulser_native_qaoa.qmod").read_text()
    expr = qmod.split("phase (", 1)[1].rsplit(", gamma);", 1)[0]
    max_err = max(abs(adapter.evaluate_expression(expr, x) + adapter.CONSTANT - adapter.canonical_energy(x))
                  for x in itertools.product((0, 1), repeat=adapter.N))
    ranking = sorted((adapter.canonical_energy(x), "".join(map(str, x)))
                     for x in itertools.product((0, 1), repeat=adapter.N))
    record = {
        "schema": "qmentor.result-record.v2",
        "target": "classiq",
        "versions": {"classiq": classiq.__version__},
        "model_bytes": len(model),
        "native_qmod": "pulser_native_qaoa.qmod",
        "max_energy_error_all_states": max_err,
        "exact_optimum": {"bitstring": ranking[0][1], "energy": round(ranking[0][0], 6)},
        "validation_state": "imported (model created, native Qmod cost verified); synthesis unverified",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
