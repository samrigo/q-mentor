"""Offline gates: optical conventions, sub-problem energies, conditional distribution == ideal gate model,
unconditional success rate reported, six-bond resource refusal, decode, smoke run."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import perceval as pcvl
import pytest
from perceval.components import BS

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())


def test_rx_and_rz_conventions():
    t = 0.6
    assert np.allclose(np.asarray(BS.Rx(theta=-t).compute_unitary()), adapter._rx(t))
    exp = pcvl.Experiment(2)
    adapter._add_rz(exp, 0, t)
    assert np.allclose(np.asarray(exp.unitary_circuit().compute_unitary()), adapter._rz(t))


def test_sub_problem_energy_matches_direct_objective():
    problem = canonical.load_problem()
    sub = adapter.sub_problem(problem)
    for x in adapter.all_states():
        assert abs(adapter.sub_energy(x, sub) - adapter.sub_energy_direct(x, problem)) < 1e-9


def test_conditional_distribution_equals_ideal_and_success_is_reported():
    sub = adapter.sub_problem(canonical.load_problem())
    for gamma, beta in [(0.3, 0.2), (1.1, 0.7), (1.535, 1.19)]:
        photonic, success = adapter.photonic_distribution(sub, gamma, beta, 15.0)
        ideal = adapter.reference_distribution(sub, gamma, beta, 15.0)
        assert 0.5 * sum(abs(photonic.get(k, 0) - ideal[k]) for k in ideal) < 1e-9
        assert success == pytest.approx(adapter.HERALDED_CNOT_SUCCESS * adapter.POSTSELECTED_CNOT_SUCCESS, rel=1e-6)


def test_decode_rejects_non_logical_states():
    assert adapter.decode_state(pcvl.BasicState([1, 0, 0, 1])) == "01"
    with pytest.raises(ValueError):
        adapter.decode_state(pcvl.BasicState([2, 0, 0, 0]))


def test_six_bond_is_conditional_but_impractical():
    report = adapter.six_bond_report(canonical.load_problem())
    assert report["status"] == "conditional-impractical"
    assert report["checks"]["unconditional_success_probability"] < EXPECTED["six_bond"]["max_success_probability"]


def test_smoke_run():
    import main
    record = main.main()
    q = record["quantum"]
    assert q["total_variation_distance"] < 1e-9
    assert q["unconditional_success_probability"] < 1  # postselected fidelity is never reported as deterministic
    assert record["baseline"]["sub_problem"]["optimum"] == EXPECTED["sub_problem"]["optimum"]
