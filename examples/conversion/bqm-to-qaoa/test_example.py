"""BQM -> QAOA proof fixtures: identical energies on all 64 states, class R (never E), offset never dropped."""
from __future__ import annotations

import json
from pathlib import Path

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
PROBLEM = canonical.load_problem()


def test_bqm_energy_model_is_exact_with_offset():
    bqm = adapter.to_bqm(PROBLEM)
    assert adapter.max_error(PROBLEM, lambda x: bqm.energy(dict(enumerate(x)))) < 1e-9
    assert adapter.lowest(adapter.exact_samples(bqm)) == EXPECTED["optimum"]


def test_offset_dropped_is_rejected():
    bqm = adapter.to_bqm(PROBLEM, keep_offset=False)
    err = adapter.max_error(PROBLEM, lambda x: bqm.energy(dict(enumerate(x))))
    assert err > 1.0  # every energy shifts by the constant: not an equivalent model
    assert adapter.lowest(adapter.exact_samples(bqm)) == EXPECTED["optimum"]  # argmin survives, energies do not


def test_qiskit_operator_matches_canonical_on_all_states():
    op, off = adapter.to_qiskit_operator(PROBLEM)
    assert adapter.max_error(PROBLEM, lambda x: adapter.operator_energy(x, op, off)) < 1e-9


def test_reimplementation_not_labelled_exact():
    assert adapter.classify("quantum annealing / BQM sampling", "QAOA", True, True) == "R"
    assert adapter.classify("QAOA", "QAOA", True, True) == "E"
    assert adapter.classify("quantum annealing / BQM sampling", "QAOA", False, True) == "U"


def test_smoke_run():
    import main
    record = main.main()
    assert record["route_class"] == EXPECTED["route_class"]
