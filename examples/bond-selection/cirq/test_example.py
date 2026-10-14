"""Offline gates: Hamiltonian energy on all 64 states, cost-unitary phase convention, bit order, smoke run."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import cirq
import numpy as np

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
TOL = EXPECTED["tolerances"]["energy_abs"]


def test_hamiltonian_matches_canonical_on_all_states():
    problem = canonical.load_problem()
    ham = adapter.cost_hamiltonian(problem)
    for x in itertools.product((0, 1), repeat=6):
        assert abs(adapter.hamiltonian_energy(x, ham) - canonical.direct_energy(x, problem)) < TOL


def test_cost_layer_is_exp_minus_i_gamma_energy_up_to_global_phase():
    problem = canonical.load_problem()
    gamma, scale = 0.137, adapter.coefficient_scale(problem)
    unitary = cirq.Circuit(adapter.cost_layer(problem, gamma * scale, scale)).unitary(qubit_order=adapter.QUBITS)
    energies = np.array([canonical.direct_energy([int(b) for b in format(k, "06b")], problem) for k in range(64)])
    target = np.diag(np.exp(-1j * gamma * energies))
    assert cirq.allclose_up_to_global_phase(unitary, target, atol=1e-9)


def test_mixer_convention_rx_two_beta():
    beta = 0.3
    u = cirq.unitary(cirq.rx(2 * beta))
    x = np.array([[0, 1], [1, 0]])
    assert np.allclose(u, np.cos(beta) * np.eye(2) - 1j * np.sin(beta) * x)


def test_bit_order_big_endian():
    x = [1, 0, 1, 0, 1, 0]
    state = adapter.basis_state(x)
    assert int(np.argmax(np.abs(state))) == int("101010", 2)
    assert adapter.decode_measurement(np.array(x)) == x


def test_smoke_run_reproduces_baseline_and_decodes():
    import main
    record = main.main()
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]["bitstring"]
    assert abs(record["baseline"]["optimum"]["energy"] - EXPECTED["optimum"]["energy"]) < TOL
    best = record["quantum"]["best_sampled"]
    assert best["energy"] >= EXPECTED["optimum"]["energy"] - TOL
    assert record["quantum"]["optimum_probability"] > EXPECTED["quantum"]["min_optimum_probability"]
