"""Pasqal/Pulser example, offline.

1. Capability report for the canonical six-bond QUBO -> expected `unsupported-exact`
   (written to capability_report.json). No six-bond sequence is generated.
2. Supported geometry-native QUBO: 4 atoms on AnalogDevice, quantum adiabatic
   algorithm (QAA) sequence, run on the local QutipBackendV2 emulator noiselessly and with a
   SPAM noise model. Samples are decoded and scored with the canonical energy.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pulser
from pulser import InterpolatedWaveform, NoiseModel, Pulse, Sequence
from pulser.backend import BitStrings
from pulser_simulation import QutipBackendV2, QutipConfig

import adapter
import canonical

HERE = Path(__file__).resolve().parent
SEED = 7
SHOTS = 2000
DURATION_NS = 4000


def build_qaa_sequence(register: pulser.Register) -> Sequence:
    seq = Sequence(register, adapter.DEVICE)
    seq.declare_channel("ising", "rydberg_global")
    amplitude = InterpolatedWaveform(DURATION_NS, [1e-9, adapter.OMEGA_MAX, 1e-9])
    detuning = InterpolatedWaveform(DURATION_NS, [-adapter.DELTA_FINAL, 0.0, adapter.DELTA_FINAL])
    seq.add(Pulse(amplitude, detuning, 0), "ising")
    seq.measure("ground-rydberg")
    return seq


def run(seq: Sequence, qubo, noise: NoiseModel | None, trajectories: int = 1) -> dict:
    np.random.seed(SEED)  # Pulser samples bitstrings through NumPy's global RNG
    options = {"noise_model": noise, "n_trajectories": trajectories} if noise is not None else {}
    config = QutipConfig(observables=[BitStrings(evaluation_times=[1.0], num_shots=SHOTS)], **options)
    results = QutipBackendV2(seq, config=config).run()
    assert list(results.atom_order) == list(seq.register.qubit_ids), "unexpected bit order"
    counts = results.final_bitstrings
    total = sum(counts.values())
    ranking = adapter.native_ranking(qubo)
    optimum = ranking[0][1]
    decoded = sorted(({"bitstring": b, "count": int(c),
                       "energy": round(adapter.native_energy(canonical.parse_bitstring(b), qubo), 6)}
                      for b, c in counts.items()), key=lambda d: d["energy"])
    return {
        "optimum_bitstring": optimum,
        "total_shots": int(total),
        "optimum_probability": round(counts.get(optimum, 0) / total, 4),
        "top_states": sorted(decoded, key=lambda d: -d["count"])[:5],
        "best_sampled": decoded[0],
    }


def main() -> dict:
    problem = canonical.load_problem()
    report = adapter.capability_report(problem)
    (HERE / "capability_report.json").write_text(json.dumps(report, indent=2) + "\n")

    register = adapter.native_register()
    qubo = adapter.native_qubo(register)
    seq = build_qaa_sequence(register)
    spam = NoiseModel(state_prep_error=0.005, p_false_pos=0.01, p_false_neg=0.05)
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "pasqal-pulser",
        "versions": {"pulser": pulser.__version__},
        "six_bond_capability": report["status"],
        "baseline": {"method": "exhaustive enumeration of the 16 native assignments",
                     "optimum": dict(zip(("energy", "bitstring"), adapter.native_ranking(qubo)[0]))},
        "native_problem": {
            "device": adapter.DEVICE.name, "atoms": adapter.N_NATIVE, "spacing_um": adapter.SPACING_UM,
            "delta_final_rad_per_us": adapter.DELTA_FINAL, "omega_max_rad_per_us": round(adapter.OMEGA_MAX, 6),
            "duration_ns": DURATION_NS, "exact_ranking": adapter.native_ranking(qubo)[:4],
        },
        "noiseless_emulation": run(seq, qubo, None),
        "spam_noise_emulation": dict(run(seq, qubo, spam, trajectories=20),
                                     noise={"state_prep_error": 0.005, "p_false_pos": 0.01,
                                            "p_false_neg": 0.05, "trajectories": 20}),
        "seed": SEED, "shots": SHOTS,
        "evidence_level": "executable on a local emulator; geometry-native toy only; not quantum advantage",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
