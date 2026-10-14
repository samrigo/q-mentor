"""Source gates: the Pulser program builds and validates on AnalogDevice, the extracted QUBO matches the physical
final Hamiltonian on all 32 states, the artifacts the Classiq side reads are current, and the source emulation runs."""
import itertools
import json
from pathlib import Path

import numpy as np

import adapter
import main

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())


def test_sequence_builds_on_device():
    seq = adapter.build_sequence(adapter.register())
    assert seq.device.name == "AnalogDevice"
    assert seq.get_duration() == adapter.DURATION_NS


def test_ten_pair_terms_match_c6_over_r6_on_all_states():
    reg = adapter.register()
    q = adapter.qubo(reg)
    assert len(q[1]) == 10 and all(b > 0 for b in q[1].values())
    pos = [reg.qubits[k].as_array() for k in reg.qubit_ids]
    for x in itertools.product((0, 1), repeat=5):
        direct = -adapter.DELTA_FINAL * sum(x) + sum(
            adapter.DEVICE.interaction_coeff / np.linalg.norm(pos[i] - pos[j]) ** 6 * x[i] * x[j]
            for i, j in itertools.combinations(range(5), 2))
        assert abs(adapter.energy(x, q) - direct) < 1e-9


def test_committed_artifacts_are_current():
    reg = adapter.register()
    q = adapter.qubo(reg)
    fresh = main.canonical_problem(reg, q)
    committed = json.loads((ROOT / "canonical_problem.json").read_text())
    assert fresh["sha256"] == committed["sha256"] == EXPECTED["objective_sha256"]


def test_unique_optimum_and_source_run():
    record = main.main()
    assert record["baseline"]["optimum"]["bitstring"] == EXPECTED["optimum"]
    assert record["baseline"]["runner_up"]["energy"] - record["baseline"]["optimum"]["energy"] > 0.1
    assert 0 < record["quantum"]["optimum_probability"] < 1
