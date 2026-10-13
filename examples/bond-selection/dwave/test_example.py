"""Offline gates: BQM energies and offset vs canonical on all 64 states, spin sign, smoke run."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import dimod
import pytest

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
TOL = EXPECTED["tolerances"]["energy_abs"]


def test_exact_solver_energies_match_canonical():
    problem = canonical.load_problem()
    result = dimod.ExactSolver().sample(adapter.build_bqm(problem))
    assert len(result) == 64
    for sample, energy in result.data(["sample", "energy"]):
        x = adapter.sample_to_vector(sample, problem)
        assert abs(energy - canonical.direct_energy(x, problem)) < TOL


def test_spin_convention_is_negated_canonical_spin():
    problem = canonical.load_problem()
    bqm_spin = adapter.build_bqm(problem).change_vartype(dimod.SPIN, inplace=False)
    names = adapter.labels(problem)
    for x in itertools.product((0, 1), repeat=6):
        s_canonical = canonical.bits_to_spins(x)
        s_dimod = {names[i]: -s_canonical[i] for i in range(6)}
        assert abs(bqm_spin.energy(s_dimod) - canonical.direct_energy(x, problem)) < TOL


def test_offset_matches_canonical_constant():
    problem = canonical.load_problem()
    assert abs(adapter.build_bqm(problem).offset - canonical.to_qubo(problem)[2]) < TOL


def test_qpu_is_blocked_without_approval(monkeypatch):
    monkeypatch.delenv("QMENTOR_ALLOW_REMOTE", raising=False)
    with pytest.raises(PermissionError):
        adapter.qpu_sampler_guarded()


def test_smoke_run():
    import main
    record = main.main()
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]["bitstring"]
    assert abs(record["baseline"]["energy_from_bqm"] - EXPECTED["optimum"]["energy"]) < TOL
    assert record["heuristic"]["best"]["energy"] >= EXPECTED["optimum"]["energy"] - TOL
