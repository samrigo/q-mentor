"""Offline gates: model creation, stored cost polynomial == canonical energy, native Qmod export."""
import itertools
import json
from pathlib import Path

import adapter
import canonical

HERE = Path(__file__).parent
EXPECTED = json.loads((HERE / "expected.json").read_text())
TOL = 1e-8


def test_model_cost_polynomial_matches_canonical():
    problem = canonical.load_problem()
    exprs = adapter.model_phase_expressions(adapter.build_model())
    assert exprs, "phase cost expression missing from the serialized model"
    for x in itertools.product((0, 1), repeat=6):
        value = adapter.evaluate_cost_text(exprs[0], x) + adapter.CONSTANT
        assert abs(value - canonical.direct_energy(x, problem)) < TOL


def test_generated_text_polynomial_matches_canonical():
    problem = canonical.load_problem()
    text = adapter.cost_expression_text(problem)
    for x in itertools.product((0, 1), repeat=6):
        assert abs(adapter.evaluate_cost_text(text, x) + adapter.CONSTANT - canonical.direct_energy(x, problem)) < TOL


def test_smoke_run_writes_native_qmod_without_remote_calls(monkeypatch):
    monkeypatch.delenv("QMENTOR_ALLOW_REMOTE", raising=False)
    import main
    record = main.main()
    assert record["remote"]["status"] == "not-run"
    assert record["offline_model_validation"]["max_energy_error_all_64_states"] < TOL
    qmod = (HERE / "bond_selection.qmod").read_text()
    assert "qfunc qaoa_layer" in qmod and "phase (" in qmod
    # Native Qmod must carry the same cost polynomial as the canonical model.
    expr = qmod.split("phase (", 1)[1].rsplit(", gamma);", 1)[0]
    problem = canonical.load_problem()
    for x in itertools.product((0, 1), repeat=6):
        value = adapter.evaluate_cost_text(expr, x) + adapter.CONSTANT
        assert abs(value - canonical.direct_energy(x, problem)) < TOL
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]["bitstring"]
