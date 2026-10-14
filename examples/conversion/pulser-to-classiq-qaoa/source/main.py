"""Build the Pulser source, extract ProgramIR + CanonicalProblem, and run the source QAA on the local emulator.

Writes ../program_ir.json, ../canonical_problem.json and ../source_result.json (all committed; the Classiq side
reads only these artifacts, never the Pulser source text).
Run: python main.py   (inside the pinned Pulser environment)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pulser
from pulser.backend import StateResult
from pulser_simulation import QutipBackendV2, QutipConfig

import adapter

OUT = Path(__file__).resolve().parents[1]


def canonical_problem(reg, q) -> dict:
    linear, quad, const = q
    ids = list(reg.qubit_ids)
    payload = {"linear": [round(linear[i], 12) for i in range(len(ids))],
               "quadratic": [[i, j, round(b, 12)] for (i, j), b in quad.items()], "constant": const}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return {
        "schema": "qmentor.canonical-problem.v3",
        "id": "pulser-zigzag-5-atom",
        "description": "Final classical Hamiltonian of a 5-atom Rydberg register: 10 pair couplings, uniform detuning",
        "provenance": {"derived_from": "program_ir.json", "data_class": "synthetic"},
        "variables": [{"index": k, "id": q, "domain": "binary"} for k, q in enumerate(ids)],
        "bit_order": "character k = variable k (register order q0..q4); 1 = Rydberg",
        "objective": {"sense": "minimize", "expression": "E(x) = sum_i a_i x_i + sum_{i<j} b_ij x_i x_j + c"},
        "constraints": [],
        "qubo": payload,
        "qubo_convention": "each pair stored once (i<j); x in {0,1}; units rad/us",
        "sha256": digest,
    }


def program_ir(reg, seq, q) -> dict:
    ids = list(reg.qubit_ids)
    return {
        "schema": "qmentor.program-ir.v3",
        "source": {"framework": "pulser", "version": pulser.__version__,
                   "entry": "examples/conversion/pulser-to-classiq-qaoa/source/adapter.py::build_sequence",
                   "parse_status": "imported-and-built"},
        "paradigm": "analog neutral-atom (Rydberg) evolution",
        "register": {"device": seq.device.name, "qubit_order": ids,
                     "coordinates_um": {k: [round(float(v), 9) for v in reg.qubits[k].as_array()] for k in ids},
                     "interaction_coeff_C6": seq.device.interaction_coeff},
        "initial_state": "all atoms in ground state |g>",
        "hamiltonian": {"form": "H(t)/hbar = Omega(t)/2 sum_i sigma^x_i - delta(t) sum_i n_i + sum_{i<j} C6/r_ij^6 n_i n_j",
                        "interaction_terms": {f"{ids[i]}-{ids[j]}": round(b, 9) for (i, j), b in q[1].items()}},
        "controls": [{"channel": "rydberg_global", "addressing": "Global", "duration_ns": adapter.DURATION_NS,
                      "amplitude": {"waveform": "InterpolatedWaveform",
                                    "points_rad_per_us": [0.0, round(adapter.OMEGA_MAX, 9), 0.0]},
                      "detuning": {"waveform": "InterpolatedWaveform",
                                   "points_rad_per_us": [-adapter.DELTA_FINAL, 0.0, adapter.DELTA_FINAL]},
                      "phase": 0.0}],
        "gates": [],
        "measurement": {"basis": "ground-rydberg", "outcome_1_means": "Rydberg state |r>"},
        "decoding": {"bit_order": "register order q0..q4 = characters left to right",
                     "objective": "canonical QUBO energy of the decoded bitstring"},
        "unsupported_features_for_gate_targets": [
            "continuous-time analog evolution under Omega(t), delta(t) with always-on Rydberg interactions",
            "adiabatic schedule semantics (success depends on the spectral gap along the sweep, not on gate angles)",
            "device noise and SPAM model"],
    }


def run_source(seq, q) -> dict:
    cfg = QutipConfig(observables=[StateResult(evaluation_times=[1.0])])
    res = QutipBackendV2(seq, config=cfg).run()
    assert list(res.atom_order) == list(seq.register.qubit_ids)
    probs = {k.replace("r", "1").replace("g", "0"): float(v) for k, v in res.final_state.probabilities().items()}
    rank = adapter.ranking(q)
    optimum = rank[0][1]
    expected = sum(p * adapter.energy([int(c) for c in b], q) for b, p in probs.items())
    return {"algorithm": "QAA (adiabatic sweep), 4 us, global Rydberg channel", "backend": "QutipBackendV2 (noiseless)",
            "optimum_probability": round(probs.get(optimum, 0.0), 6), "expected_energy": round(expected, 6),
            "most_probable": max(probs, key=probs.get)}


def main() -> dict:
    reg = adapter.register()
    seq = adapter.build_sequence(reg)
    q = adapter.qubo(reg)
    problem, ir = canonical_problem(reg, q), program_ir(reg, seq, q)
    rank = adapter.ranking(q)
    result = {"schema": "qmentor.result-record.v3", "target": "pasqal-pulser (source)",
              "versions": {"pulser": pulser.__version__},
              "baseline": {"method": "exhaustive enumeration of 32 assignments",
                           "optimum": {"bitstring": rank[0][1], "energy": round(rank[0][0], 9)},
                           "runner_up": {"bitstring": rank[1][1], "energy": round(rank[1][0], 9)}},
              "quantum": run_source(seq, q),
              "evidence_level": "executable on a local emulator (level 2); not quantum advantage"}
    for name, data in (("canonical_problem.json", problem), ("program_ir.json", ir), ("source_result.json", result)):
        (OUT / name).write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
