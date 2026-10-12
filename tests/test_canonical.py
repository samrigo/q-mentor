"""Deterministic formulation tests: symmetry, PSD, expansion, Ising conversion, bit order."""
import numpy as np
import pytest

from qmentor.canonical import (
    CanonicalQUBO, all_assignments, bits_to_str, direct_objective, qubo_to_ising,
    str_to_bits, validate_problem_spec, x_to_s,
)


def test_sigma_symmetric_positive_definite(spec):
    S = np.asarray(spec["objective"]["risk_matrix"])
    assert np.allclose(S, S.T)
    assert np.linalg.eigvalsh(S).min() > 0


def test_qubo_expansion_matches_direct_objective_on_all_states(spec, qubo):
    for x in all_assignments(6):
        assert qubo.energy(x) == pytest.approx(direct_objective(spec, x), abs=1e-9)


def test_ising_conversion_matches_on_all_states(qubo):
    ising = qubo_to_ising(qubo)
    for x in all_assignments(6):
        assert ising.energy(x_to_s(x)) == pytest.approx(qubo.energy(x), abs=1e-9)


def test_bit_order_is_leftmost_first():
    assert all_assignments(3)[1] == (0, 0, 1)
    assert bits_to_str((1, 0, 1, 0, 1, 0)) == "101010"
    assert str_to_bits("110") == (1, 1, 0)
    with pytest.raises(ValueError):
        str_to_bits("12")


def test_asymmetric_q_rejected():
    with pytest.raises(ValueError):
        CanonicalQUBO(Q=np.array([[0.0, 1.0], [0.0, 0.0]]), constant=0, variables=("a", "b"))


def test_prohibited_data_class_rejected(spec):
    bad = {**spec, "provenance": {"data_class": "client-confidential"}}
    with pytest.raises(ValueError, match="synthetic or public"):
        validate_problem_spec(bad)


def test_non_psd_risk_rejected(spec):
    obj = {**spec["objective"], "risk_matrix": (-np.eye(6)).tolist()}
    with pytest.raises(ValueError, match="positive semidefinite"):
        validate_problem_spec({**spec, "objective": obj})
