"""Pasqal/Pulser must refuse exact mappings it cannot physically represent."""
import numpy as np

from qmentor.canonical import CanonicalQUBO
from qmentor.targets import pulser_target


def test_demo_qubo_is_unsupported_exact(qubo, expected):
    rep = pulser_target.capability(qubo)
    assert rep["status"] == expected["pulser_expected_status"] == "unsupported-exact"
    assert rep["failures"] and rep["alternatives"]
    assert not rep["checks"]["geometry"]["embeddable"]
    approx = rep["checks"]["geometry"]["approximation_option"]
    assert approx["label"].startswith("APPROXIMATE")


def test_negative_coupling_rejected():
    Q = np.array([[-1.0, -0.5], [-0.5, -1.0]])
    rep = pulser_target.capability(CanonicalQUBO(Q=Q, constant=0, variables=("a", "b")))
    assert rep["status"] == "unsupported-exact"
    assert not rep["checks"]["couplings_positive"]


def test_nonuniform_linear_terms_need_addressability():
    q = pulser_target.qubo_from_positions(np.array([[0, 0], [6, 0], [3, 5.2]]))
    Q = q.Q.copy(); Q[0, 0] = -3.0
    rep = pulser_target.capability(CanonicalQUBO(Q=Q, constant=0, variables=q.variables), "AnalogDevice")
    assert rep["status"] == "unsupported-exact"
    assert any("addressability" in f for f in rep["failures"])


def test_geometry_derived_qubo_is_exact():
    pos = np.array([[0.0, 0.0], [7.0, 0.0], [3.5, 6.0], [10.0, 6.0]])
    rep = pulser_target.capability(pulser_target.qubo_from_positions(pos))
    assert rep["status"] == "exact", rep["failures"]
    assert rep["checks"]["geometry"]["dimension_required"] == 2
