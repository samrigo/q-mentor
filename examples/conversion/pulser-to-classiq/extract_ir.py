"""Extract ProgramIR + CanonicalProblem from the Pulser QAA source program.

Run in the Pulser environment. Reads the source sequence built by
examples/bond-selection/pasqal-pulser/main.py, never its text: the IR records
semantics (register, device, Hamiltonian, controls, measurement, decoding).
Outputs: program_ir.json, canonical_problem.json (both committed).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_DIR = HERE.parents[1] / "bond-selection" / "pasqal-pulser"
sys.path.insert(0, str(SOURCE_DIR))
sys.path.insert(0, str(HERE.parents[2] / "demo" / "bond-selection"))

import adapter as pulser_adapter  # noqa: E402
import main as pulser_main  # noqa: E402
import pulser  # noqa: E402


def extract() -> tuple[dict, dict]:
    register = pulser_adapter.native_register()
    seq = pulser_main.build_qaa_sequence(register)
    linear, quad, const = pulser_adapter.native_qubo(register)
    ids = list(register.qubit_ids)
    coords = {q: [round(float(v), 9) for v in register.qubits[q].as_array()] for q in ids}
    ir = {
        "schema": "qmentor.program-ir.v2",
        "source": {"framework": "pulser", "version": pulser.__version__,
                   "entry": "examples/bond-selection/pasqal-pulser/main.py::build_qaa_sequence",
                   "parse_status": "imported-and-built"},
        "paradigm": "analog neutral-atom (Rydberg) evolution",
        "register": {"device": seq.device.name, "qubit_order": ids, "coordinates_um": coords,
                     "interaction_coeff_C6": seq.device.interaction_coeff},
        "initial_state": "all atoms in ground state |g>",
        "hamiltonian": {
            "form": "H(t)/hbar = Omega(t)/2 sum_i sigma^x_i - delta(t) sum_i n_i + sum_{i<j} C6/r_ij^6 n_i n_j",
            "interaction_terms": {f"{ids[i]}-{ids[j]}": round(v, 9) for (i, j), v in quad.items()},
        },
        "controls": [{
            "channel": "rydberg_global", "addressing": "Global",
            "duration_ns": pulser_main.DURATION_NS,
            "amplitude": {"waveform": "InterpolatedWaveform", "points_rad_per_us": [0.0, round(pulser_adapter.OMEGA_MAX, 9), 0.0]},
            "detuning": {"waveform": "InterpolatedWaveform",
                         "points_rad_per_us": [-pulser_adapter.DELTA_FINAL, 0.0, pulser_adapter.DELTA_FINAL]},
            "phase": 0.0,
        }],
        "gates": [],
        "measurement": {"basis": "ground-rydberg", "outcome_1_means": "Rydberg state |r>"},
        "decoding": {"bit_order": "register qubit order q0..q3 = bitstring characters left to right",
                     "objective": "canonical QUBO energy of the decoded bitstring"},
        "unsupported_features_for_gate_targets": [
            "continuous-time analog evolution under Omega(t), delta(t) with always-on Rydberg interactions",
            "adiabatic schedule semantics (success depends on the gap along the sweep, not on gate angles)",
        ],
    }
    problem = {
        "schema": "qmentor.canonical-problem.v2",
        "id": "pulser-native-4-atom-line",
        "provenance": {"derived_from": "program_ir.json", "data_class": "synthetic"},
        "variables": [{"index": k, "id": q, "domain": "binary"} for k, q in enumerate(ids)],
        "bit_order": "character k = variable k (register order)",
        "qubo": {"linear": [linear[i] for i in range(len(ids))],
                 "quadratic": [[i, j, v] for (i, j), v in quad.items()],
                 "constant": const, "units": "rad/us"},
        "objective": {"sense": "minimize", "expression": "sum_i a_i x_i + sum_{i<j} b_ij x_i x_j + c"},
    }
    return ir, problem


if __name__ == "__main__":
    ir, problem = extract()
    (HERE / "program_ir.json").write_text(json.dumps(ir, indent=2) + "\n")
    (HERE / "canonical_problem.json").write_text(json.dumps(problem, indent=2) + "\n")
    print("wrote program_ir.json and canonical_problem.json")
