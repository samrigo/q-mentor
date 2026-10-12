"""Ground truth for the six-bond demo (README-04)."""
import pytest

from qmentor.baseline import enumerate_exact, penalty_separation, simulated_annealing, summarize_samples
from qmentor.canonical import is_feasible, str_to_bits


def test_enumeration_reproduces_unique_optimum(spec, qubo, expected):
    r = enumerate_exact(qubo, spec)
    assert r["n_states"] == expected["n_states"] == 64
    assert r["unique_optimum"]
    assert r["best"]["bits"] == expected["optimum"]["bits"]
    assert r["best"]["energy"] == pytest.approx(expected["optimum"]["energy"], abs=1e-9)
    assert r["best"]["feasible"]


def test_runner_up_and_gap(spec, qubo, expected):
    r = enumerate_exact(qubo, spec)
    ru = r["runner_up_feasible"]
    assert ru["bits"] == expected["runner_up_feasible"]["bits"]
    assert ru["energy"] - r["best"]["energy"] == pytest.approx(expected["gap"], abs=1e-9)


def test_optimum_business_metrics(spec, expected):
    import numpy as np
    x = np.array(str_to_bits(expected["optimum"]["bits"]), dtype=float)
    o = spec["objective"]
    assert np.dot(o["expected_return"], x) == pytest.approx(11.9)
    assert x @ np.asarray(o["risk_matrix"]) @ x == pytest.approx(1.67)
    assert sum(v["duration"] * b for v, b in zip(spec["variables"], x)) == pytest.approx(14.7)


def test_penalty_separates_feasible_from_infeasible(spec, qubo):
    s = penalty_separation(qubo, spec)
    assert s["separates"] and s["margin"] > 0


def test_enumeration_refuses_large_instances(qubo):
    import numpy as np
    from qmentor.canonical import CanonicalQUBO
    big = CanonicalQUBO(Q=np.zeros((30, 30)), constant=0, variables=tuple(map(str, range(30))))
    with pytest.raises(ValueError, match="MIP/CP-SAT"):
        enumerate_exact(big)


@pytest.mark.parametrize("seed", range(5))
def test_heuristic_baseline_is_seeded_and_strong(qubo, expected, seed):
    a, b = simulated_annealing(qubo, seed), simulated_annealing(qubo, seed)
    assert a["bits"] == b["bits"]
    assert a["energy"] == pytest.approx(expected["optimum"]["energy"])


def test_sample_decoding_marks_feasibility(spec, qubo, expected):
    samples = {"101010": 3, "111111": 1}
    m = summarize_samples(samples, lambda b: qubo.energy(str_to_bits(b)),
                          lambda b: is_feasible(spec, str_to_bits(b)), expected["optimum"]["energy"])
    assert m["feasibility_rate"] == pytest.approx(0.75)
    assert m["optimality_gap"] == pytest.approx(0)
    lo, hi = m["p_optimum_ci95"]
    assert lo < 0.75 < hi
