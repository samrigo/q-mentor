"""Offline gates: six-bond refusal is measured, native QUBO matches its Hamiltonian, decode convention,
emulator concentrates on the classical ground state, smoke run."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())


def test_six_bond_is_refused_with_measured_error():
    report = adapter.capability_report(canonical.load_problem())
    assert report["status"] == "unsupported-exact"
    assert report["checks"]["couplings_required"] > report["checks"]["geometric_degrees_of_freedom_2d"]
    assert report["checks"]["best_fit_max_relative_coupling_error"] > EXPECTED["six_bond"]["min_fit_error"]


def test_native_qubo_matches_rydberg_hamiltonian_on_all_states():
    pos = np.array(adapter.positions())
    for x in itertools.product((0, 1), repeat=adapter.N_ATOMS):
        direct = -adapter.DELTA_END * sum(x) + sum(
            adapter.RB_C6 / np.linalg.norm(pos[i] - pos[j]) ** 6 * x[i] * x[j]
            for i, j in itertools.combinations(range(adapter.N_ATOMS), 2))
        assert abs(adapter.native_energy(x) - direct) < 1e-9


def test_classical_ground_state_is_the_independent_set():
    bits, energy = adapter.classical_ground_state()
    assert bits == EXPECTED["native"]["ground_state"]
    assert abs(energy - EXPECTED["native"]["ground_energy"]) < 1e-4


def test_rydberg_bit_convention():
    # Bloqade reports '0' for Rydberg; a single-atom pi pulse must decode to canonical '1'.
    from bloqade.analog import start
    prog = start.add_position((0, 0)).rydberg.rabi.amplitude.uniform.constant(value=np.pi / 0.2, duration=0.2)
    raw = prog.bloqade.python().run(50).report().counts()[0]
    assert set(raw) == {"0"}
    dist = prog.bloqade.python().run_callback(lambda s, m, h: float(np.abs(s.data[s.space.is_rydberg_at(0)]) @
                                                                       np.abs(s.data[s.space.is_rydberg_at(0)])))[0]
    assert dist > 0.999


def test_emulator_concentrates_on_ground_state():
    dist = adapter.exact_distribution()
    assert abs(sum(dist.values()) - 1) < 1e-6
    assert max(dist, key=dist.get) == EXPECTED["native"]["ground_state"]
    assert dist[EXPECTED["native"]["ground_state"]] > EXPECTED["native"]["min_ground_probability"]


def test_smoke_run():
    import main
    record = main.main()
    assert record["capability_report"]["status"] == "unsupported-exact"
    assert record["quantum"]["most_probable"] == EXPECTED["native"]["ground_state"]
