"""Offline gates: six-bond refusal, native QUBO == Rydberg Hamiltonian diagonal, sequence validity, emulator smoke run."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import adapter
import canonical

EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())
TOL = EXPECTED["tolerances"]["energy_abs"]


def test_six_bond_exact_mapping_is_refused_with_reasons():
    report = adapter.capability_report(canonical.load_problem())
    assert report["status"] == EXPECTED["six_bond"]["capability_status"]
    failing = {c["check"] for c in report["checks"] if not c["pass"]}
    assert set(EXPECTED["six_bond"]["failing_checks"]) <= failing
    assert report["approximation_offered"] is EXPECTED["six_bond"]["approximation_offered"]
    assert report["alternatives"] and report["lost_semantics"]


def test_native_qubo_equals_rydberg_hamiltonian_on_all_states():
    register = adapter.native_register()
    qubo = adapter.native_qubo(register)
    for x in itertools.product((0, 1), repeat=adapter.N_NATIVE):
        assert abs(adapter.native_energy(x, qubo) - adapter.rydberg_hamiltonian_diagonal(x, register)) < TOL


def test_native_optimum():
    ranking = adapter.native_ranking(adapter.native_qubo(adapter.native_register()))
    assert ranking[0][1] == EXPECTED["native_problem"]["optimum_bitstring"]
    assert abs(ranking[0][0] - EXPECTED["native_problem"]["optimum_energy_rad_per_us"]) < TOL
    assert ranking[1][0] - ranking[0][0] > 0.1


def test_sequence_respects_device_limits():
    import main
    seq = main.build_qaa_sequence(adapter.native_register())
    assert seq.device.name == EXPECTED["native_problem"]["device"]
    assert adapter.OMEGA_MAX <= seq.device.channels["rydberg_global"].max_amp
    assert adapter.DELTA_FINAL <= seq.device.channels["rydberg_global"].max_abs_detuning


def test_emulator_smoke_run():
    import main
    record = main.main()
    noiseless = record["noiseless_emulation"]
    assert noiseless["best_sampled"]["energy"] >= EXPECTED["native_problem"]["optimum_energy_rad_per_us"] - TOL
    good = {EXPECTED["native_problem"]["optimum_bitstring"], *EXPECTED["native_problem"]["runner_up_bitstrings"]}
    mass = sum(s["count"] for s in noiseless["top_states"] if s["bitstring"] in good) / noiseless["total_shots"]
    assert mass >= EXPECTED["native_problem"]["independent_set_mass_min_noiseless"]
    assert record["six_bond_capability"] == "unsupported-exact"
