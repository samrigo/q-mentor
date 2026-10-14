"""Offline gates: half-turn conventions, energy diagonal on all 64 states, pre/post-compilation semantics,
resource comparison, bit order, smoke run."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from pytket import Circuit

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
TOL = EXPECTED["tolerances"]["energy_abs"]


def test_half_turn_conventions():
    c = Circuit(1)
    c.Rx(2 * 0.3 / math.pi, 0)  # mixer for beta = 0.3
    x = np.array([[0, 1], [1, 0]])
    assert np.allclose(c.get_unitary(), np.cos(0.3) * np.eye(2) - 1j * np.sin(0.3) * x)


def test_cost_layer_equals_exp_minus_i_gamma_energy_on_all_states():
    problem = canonical.load_problem()
    scale = adapter.coefficient_scale(problem)
    gamma = 0.21
    c = Circuit(adapter.N)
    adapter.add_cost_layer(c, problem, gamma * scale, scale)
    u = c.get_unitary()
    assert np.allclose(u, np.diag(np.diag(u)))  # diagonal in the computational basis
    phases = np.angle(np.diag(u) / np.exp(-1j * gamma * adapter.all_energies(problem)))
    assert np.allclose(phases, phases[0], atol=1e-9)  # equal up to one global phase -> all 64 energies match


def test_energy_table_matches_canonical_order():
    problem = canonical.load_problem()
    energies = adapter.all_energies(problem)
    for index, value in enumerate(energies):
        assert abs(value - canonical.direct_energy(adapter.decode_index(index), problem)) < TOL


def test_compilation_preserves_semantics_and_keeps_cheaper_pass():
    problem = canonical.load_problem()
    source = adapter.qaoa_circuit(problem, [0.3, 0.7], [0.4, 0.2])
    compiled, report = adapter.compile_circuit(source)
    assert adapter.unitary_error_up_to_phase(source, compiled) < 1e-8
    assert report["chosen"] == "rebase"
    assert report["peephole"]["two_qubit_gates"] > report["rebase"]["two_qubit_gates"]  # observed, not assumed


def test_bit_order_ilo_be():
    c = Circuit(adapter.N)
    for k, bit in enumerate([1, 0, 1, 0, 1, 0]):
        if bit:
            c.X(k)
    assert int(np.argmax(np.abs(c.get_statevector()))) == int("101010", 2)
    assert adapter.decode_index(int("101010", 2)) == [1, 0, 1, 0, 1, 0]


def test_smoke_run_reproduces_baseline_and_decodes():
    import main
    record = main.main()
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]["bitstring"]
    assert record["quantum"]["best_sampled"]["energy"] >= EXPECTED["optimum"]["energy"] - TOL
    assert record["quantum"]["optimum_probability"] > EXPECTED["quantum"]["min_optimum_probability"]
