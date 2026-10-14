"""Bloqade (QuEra analog): six-bond capability report + native 5-atom adiabatic program on the local emulator.

Run: python main.py   (from this directory, inside the pinned environment). No Braket/Aquila call is made.
"""
from __future__ import annotations

import importlib.metadata
import json
import time

import adapter
import canonical

SHOTS = 2000


def main() -> dict:
    problem = canonical.load_problem()
    start = time.perf_counter()
    report = adapter.capability_report(problem)
    ground, ground_energy = adapter.classical_ground_state()
    dist = adapter.exact_distribution()
    counts = adapter.sampled_counts(SHOTS)
    elapsed = time.perf_counter() - start
    top = max(dist, key=dist.get)
    record = {
        "schema": "qmentor.result-record.v3",
        "target": "bloqade",
        "versions": {"bloqade-analog": importlib.metadata.version("bloqade-analog"),
                     "numpy": importlib.metadata.version("numpy")},
        "baseline": {"six_bond": canonical.exact_baseline(problem)["optimum"],
                     "native_classical_ground_state": {"bitstring": ground, "energy": round(ground_energy, 6)}},
        "capability_report": report,
        "quantum": {
            "algorithm": "adiabatic sweep: Omega 0->15.7->0 rad/us, delta -16->+16 rad/us over 4.0 us",
            "backend": "bloqade.analog python emulator (local, noiseless)",
            "atoms": adapter.N_ATOMS,
            "spacing_um": adapter.SPACING_UM,
            "most_probable": top,
            "ground_state_probability": round(dist.get(ground, 0.0), 4),
            "shots": SHOTS,
            "sampled_ground_state_fraction": round(counts.get(ground, 0) / SHOTS, 4),
            "wall_clock_s": round(elapsed, 3),
        },
        "evidence_level": "executable (level 2) for the native problem; the six-bond QUBO is unsupported-exact here",
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
