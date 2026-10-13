"""Offline gates: Hamiltonian energy equivalence on all 64 basis states, wire order, smoke run."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
TOL = 1e-8


def test_hamiltonian_matches_canonical_on_all_states():
    problem = canonical.load_problem()
    ham, offset = adapter.build_cost_hamiltonian(problem)
    for x in itertools.product((0, 1), repeat=6):
        assert abs(adapter.basis_energy(x, ham, offset) - canonical.direct_energy(x, problem)) < TOL


def test_wire_order_is_left_to_right():
    problem = canonical.load_problem()
    ham, offset = adapter.build_cost_hamiltonian(problem)
    assert abs(adapter.basis_energy([1, 0, 1, 0, 1, 0], ham, offset) - EXPECTED["optimum"]["energy"]) < TOL
    assert abs(adapter.basis_energy([0, 1, 0, 1, 0, 1], ham, offset) - EXPECTED["optimum"]["energy"]) > 1.0


def test_smoke_run():
    import main
    record = main.main()
    assert record["device"] == "default.qubit"
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]["bitstring"]
    assert record["quantum"]["best_sampled"]["energy"] >= EXPECTED["optimum"]["energy"] - TOL
