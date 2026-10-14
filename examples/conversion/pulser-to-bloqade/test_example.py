"""Analog <-> analog proof fixtures: same Hamiltonian -> same distribution; mismatched C6 -> approximation."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

import adapter

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())


@pytest.fixture(scope="module")
def pulser_dist():
    return adapter.pulser_distribution()


def test_c6_values_differ_and_scaling_matches_interactions():
    assert adapter.C6_BLOQADE / adapter.C6_PULSER > 5  # different device models, not a typo
    u_p = adapter.interaction_matrix(adapter.pulser_positions(), adapter.C6_PULSER)
    assert np.allclose(adapter.interaction_matrix(adapter.bloqade_positions(True), adapter.C6_BLOQADE), u_p)
    assert not np.allclose(adapter.interaction_matrix(adapter.bloqade_positions(False), adapter.C6_BLOQADE), u_p)


def test_waveforms_match_on_the_time_grid():
    seq = adapter.pulser_sequence()
    assert seq.get_duration() == 2 * adapter.RAMP_NS + adapter.HOLD_NS
    amplitude, detuning = adapter.pulser_waveforms()
    amp, det = amplitude.samples, detuning.samples
    assert len(amp) == len(det) == seq.get_duration()  # 1 ns grid in Pulser; Bloqade uses the same breakpoints in us
    assert amp[0] == pytest.approx(0.0, abs=1e-9) and max(amp) == pytest.approx(adapter.OMEGA)
    assert det[0] == pytest.approx(adapter.DELTA_START) and det[-1] == pytest.approx(adapter.DELTA_END)


def test_matched_hamiltonian_distributions_agree(pulser_dist):
    d = adapter.tvd(pulser_dist, adapter.bloqade_distribution(matched=True))
    assert d < EXPECTED["exact_tvd_tolerance"]
    assert adapter.classify(d, EXPECTED["exact_tvd_tolerance"]) == "E"


def test_unmatched_c6_is_approximation(pulser_dist):
    d = adapter.tvd(pulser_dist, adapter.bloqade_distribution(matched=False))
    assert d > 10 * EXPECTED["exact_tvd_tolerance"]
    assert adapter.classify(d, EXPECTED["exact_tvd_tolerance"]) == "A"


def test_sign_convention_positive_detuning_favours_rydberg(pulser_dist):
    # Final Delta > 0 with nearest-neighbour blockade: the independent set 101 dominates in both SDKs.
    assert max(pulser_dist, key=pulser_dist.get) == EXPECTED["most_probable"]
    b = adapter.bloqade_distribution(matched=True)
    assert max(b, key=b.get) == EXPECTED["most_probable"]


def test_smoke_run():
    import main
    record = main.main()
    assert record["route_class"] == "E" and record["unmatched_same_um_coordinates"]["route_class"] == "A"
