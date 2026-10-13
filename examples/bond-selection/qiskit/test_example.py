"""Offline gates: import, QUBO/Ising equivalence on all 64 states, decode, smoke run."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
TOL = EXPECTED["tolerances"]["energy_abs"]


def test_qubo_matches_canonical_on_all_states():
    problem = canonical.load_problem()
    qubo = adapter.build_qubo(problem)
    for x in itertools.product((0, 1), repeat=6):
        assert abs(qubo.objective.evaluate(list(x)) - canonical.direct_energy(x, problem)) < TOL


def test_ising_operator_matches_canonical_on_all_states():
    problem = canonical.load_problem()
    op, offset = adapter.build_ising(problem)
    assert op.num_qubits == 6
    for x in itertools.product((0, 1), repeat=6):
        assert abs(adapter.operator_energy(x, op, offset) - canonical.direct_energy(x, problem)) < TOL


def test_bit_order_round_trip():
    x = [1, 0, 1, 0, 1, 0]
    assert adapter.qiskit_label(x) == "010101"
    assert adapter.decode_qiskit_bitstring("010101") == x


def test_smoke_run_reproduces_baseline_and_decodes():
    import main
    record = main.main()
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]["bitstring"]
    assert abs(record["baseline"]["optimum"]["energy"] - EXPECTED["optimum"]["energy"]) < TOL
    best = record["quantum"]["best_sampled"]
    # QAOA is heuristic: it may not hit the optimum, but it can never beat it.
    assert best["energy"] >= EXPECTED["optimum"]["energy"] - TOL
    assert set(best) >= {"bitstring", "feasible", "energy"}
