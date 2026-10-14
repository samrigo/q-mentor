"""Pulser <-> Bloqade Hamiltonian translation fixture. Run: python main.py (local emulators only)."""
from __future__ import annotations

import importlib.metadata as md
import json

import numpy as np

import adapter

EXACT_TOL = 1e-3


def main() -> dict:
    p = adapter.pulser_distribution()
    matched = adapter.bloqade_distribution(matched=True)
    unmatched = adapter.bloqade_distribution(matched=False)
    d_matched, d_unmatched = adapter.tvd(p, matched), adapter.tvd(p, unmatched)
    u_p = adapter.interaction_matrix(adapter.pulser_positions(), adapter.C6_PULSER)
    u_b = adapter.interaction_matrix(adapter.bloqade_positions(True), adapter.C6_BLOQADE)
    record = {
        "schema": "qmentor.translation-record.v3",
        "edge_id": "pulser-to-bloqade-hamiltonian",
        "source": {"framework": "pulser", "version": md.version("pulser")},
        "target": {"framework": "bloqade-analog", "version": md.version("bloqade-analog")},
        "c6": {"pulser_AnalogDevice": adapter.C6_PULSER, "bloqade_RB_C6": adapter.C6_BLOQADE,
               "coordinate_scale_for_match": adapter.MATCH_SCALE},
        "interaction_max_abs_difference_matched": float(np.max(np.abs(u_p - u_b))),
        "matched": {"tvd": d_matched, "route_class": adapter.classify(d_matched, EXACT_TOL)},
        "unmatched_same_um_coordinates": {"tvd": d_unmatched, "route_class": adapter.classify(d_unmatched, EXACT_TOL)},
        "route_class": adapter.classify(d_matched, EXACT_TOL),
        "overall_status": "exact" if d_matched <= EXACT_TOL else "approximate",
        "pulser_distribution": {k: round(v, 6) for k, v in sorted(p.items())},
        "validation": {"observed_state": "locally-executed", "commands": ["python -m pytest -q"]},
    }
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
