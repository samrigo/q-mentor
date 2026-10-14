"""Pasqal/Pulser -> Classiq optimization regression gates (README-10).

Semantics: cost expression == canonical QUBO on all 32 states; phase sign and RX convention; named layers and
parameter slicing; @qfunc/@qperm behaviour on the pinned SDK; quantile semantics of the installed SDK.
Fairness: identical objective hash, budget, seeds, decode across variants; CVaR never compared with mean energy;
"improved" only on the predeclared metric beyond the baseline interval and within the resource cap.
"""
import itertools
import json
from pathlib import Path

import numpy as np
import pytest
from classiq.interface.exceptions import ClassiqError
from classiq.interface.executor.estimate_cost import estimate_quantile_cost

import adapter
import main

HERE = Path(__file__).resolve().parent
EXPECTED = json.loads((HERE / "expected.json").read_text())


@pytest.fixture(scope="module")
def record():
    return main.main()


def test_canonical_problem_has_five_variables_and_ten_pair_terms():
    assert adapter.N == 5 and len(adapter.QUAD) == 10
    assert adapter.objective_hash() == EXPECTED["objective_hash"]


def test_exported_cost_matches_canonical_on_all_states(record):
    for p, check in record["model_checks"].items():
        assert check["max_energy_error_all_32_states"] < 1e-9, p
        assert check["named_layers"] and check["param_slicing"], p


def test_reference_cost_layer_is_exp_minus_i_gamma_energy():
    gamma = 0.37
    psi0 = np.full(32, 1 / np.sqrt(32), dtype=complex)
    psi = np.exp(1j * gamma * (-adapter.COSTS)) * psi0
    target = np.exp(-1j * gamma * (adapter.ENERGIES - adapter.CONSTANT) / adapter.SCALE) * psi0
    assert np.allclose(psi, target)


def test_rx_convention_and_beta_relabelling():
    beta = 0.41
    x = np.array([[0, 1], [1, 0]])
    assert np.allclose(adapter.rx(beta), np.cos(beta / 2) * np.eye(2) - 1j * np.sin(beta / 2) * x)
    # RX(2 b) = exp(-i b X): the same mixer under the other convention needs beta doubled, never reused as-is
    assert np.allclose(adapter.rx(2 * beta), np.cos(beta) * np.eye(2) - 1j * np.sin(beta) * x)
    assert not np.allclose(adapter.rx(beta), adapter.rx(2 * beta))


def test_decorators_on_pinned_sdk():
    assert adapter.build_model(1, "qfunc", "qfunc")
    assert adapter.build_model(1, "qperm", "qfunc")          # accepted: phase-only layer
    with pytest.raises(ClassiqError, match="Non-permutation"):
        adapter.build_model(1, "qfunc", "qperm")             # rejected: RX is not a permutation


def test_installed_quantile_keeps_the_lowest_fraction():
    costs, shots = np.array([1.0, 2.0, 3.0, 10.0]), np.array([3, 3, 2, 2])
    # quantile=0.3 averages the lowest 30 % of the 10 samples = three samples of cost 1.0
    assert estimate_quantile_cost(costs, shots, quantile=0.3) == pytest.approx(1.0)
    assert estimate_quantile_cost(costs, shots, quantile=0.6) == pytest.approx(1.5)


def test_variants_share_objective_budget_and_decode(record):
    assert record["objective_hash"] == adapter.objective_hash()
    for v in record["variants"]:
        assert v["shots_per_evaluation"] * v["max_evaluations"] == record["budget"]["total_shots_per_seed"]
        assert [s["seed"] for s in v["per_seed"]] == record["budget"]["seeds"]
        assert v["best_feasible_energy"] >= record["exact_optimum"]["energy"] - 1e-9


def test_depth_comparison_and_stage_rule(record):
    ps = {v["p"] for v in record["variants"]}
    assert {1, 2} <= ps
    assert (4 in ps) == record["budget"]["stage2_run"]
    assert any(v["objective_mode"] == "cvar" for v in record["variants"])
    assert any(v["objective_mode"] == "mean" for v in record["variants"])


def test_selection_rule_is_honest(record):
    base = next(v for v in record["variants"] if v["id"] == record["baseline_variant"])
    sel = next(v for v in record["variants"] if v["id"] == record["selected"])
    if record["status"] == "improved":
        assert sel["optimum_probability"]["ci95"][0] > base["optimum_probability"]["ci95"][1]
        assert sel["two_qubit_gates"] <= main.RESOURCE_CAP_TWO_QUBIT
    else:
        assert record["status"] == "not-improved" and record["selected"] == record["baseline_variant"]
    assert record["status"] == EXPECTED["status"]
    assert record["execution"]["target_sdk_execution"] == "unverified-credential-required"


def test_four_layers_not_assumed_to_reach_optimum(record):
    for v in record["variants"]:
        if v["p"] == 4:
            assert v["optimum_probability"]["mean"] < 0.99  # observed, recorded; p=4 is a candidate, not a guarantee


def test_bit_order_round_trip():
    for x in itertools.product((0, 1), repeat=adapter.N):
        k = int("".join(map(str, x)), 2)
        assert adapter.STATES[k] == x
