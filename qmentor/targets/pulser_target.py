"""Pasqal / Pulser neutral-atom target: CAPABILITY GATE FIRST.

Pulser is not a generic QUBO compiler. In the Rydberg Hamiltonian the pair
interaction between atoms i and j is U_ij = C6 / r_ij^6, which is always
POSITIVE, never zero at finite distance, and fixed by GEOMETRY. Linear QUBO
terms map to detunings; non-uniform linear terms need LOCAL addressability.

Exact representability of a canonical QUBO therefore requires:

1. every off-diagonal Q_ij > 0 (sign and non-zero);
2. distances r_ij = (C6 / (k * Q_ij))^(1/6) that exist as points in the
   device's dimension (2D or 3D) for some global scale k > 0. A global scale
   multiplies all squared distances equally, so this reduces to a classical
   multidimensional-scaling test: B = -1/2 J D^2 J must be positive
   semidefinite with rank <= dimension. This test is deterministic;
3. uniform diagonal, or a device with local detuning addressability;
4. the distance dynamic range fits the device's minimum spacing and radius.

Anything failing returns ``unsupported-exact`` with alternatives. A
least-squares embedding may be offered, but only as a separately labeled
``approximate`` option with its coupling error.
"""

from __future__ import annotations

import numpy as np

from ..canonical import CanonicalQUBO

TARGET = "pasqal-pulser"
RANK_TOL = 1e-9

# Fallback device envelope used when pulser is not installed. Values are
# copied from pulser-core 1.9.1 AnalogDevice and must be re-verified on upgrade.
FALLBACK_DEVICE = {
    "name": "AnalogDevice (pulser-core 1.9.1 snapshot)",
    "dimensions": 2,
    "min_atom_distance_um": 5.0,
    "max_radial_distance_um": 38.0,
    "local_detuning": False,
}


def device_envelope(device_name: str = "AnalogDevice") -> dict:
    try:
        import pulser.devices as devices  # optional
    except ImportError:
        return dict(FALLBACK_DEVICE, source="fallback snapshot; pulser not installed")
    dev = getattr(devices, device_name)
    return {
        "name": dev.name,
        "dimensions": int(dev.dimensions),
        "min_atom_distance_um": float(dev.min_atom_distance),
        "max_radial_distance_um": None if dev.max_radial_distance is None else float(dev.max_radial_distance),
        "local_detuning": bool(getattr(dev, "dmm_objects", ())),
        "source": f"pulser {__import__('pulser').__version__}",
    }


def _mds(D2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = D2.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    w, V = np.linalg.eigh(B)
    order = np.argsort(w)[::-1]
    return w[order], V[:, order]


def capability(q: CanonicalQUBO, device_name: str = "AnalogDevice") -> dict:
    dev = device_envelope(device_name)
    n = q.n
    off = np.array([q.Q[i, j] for i in range(n) for j in range(i + 1, n)])
    failures, checks = [], {}

    checks["couplings_positive"] = bool(np.all(off > 0))
    if not checks["couplings_positive"]:
        failures.append(
            f"{int(np.sum(off <= 0))} off-diagonal coupling(s) are zero or negative; "
            "Rydberg interactions C6/r^6 are strictly positive"
        )

    diag = np.diag(q.Q)
    checks["uniform_linear_terms"] = bool(np.allclose(diag, diag[0]))
    if not checks["uniform_linear_terms"] and not dev["local_detuning"]:
        failures.append("non-uniform linear terms need local detuning addressability, which this device lacks")

    geometry = {"dimension_required": None, "embeddable": False}
    if checks["couplings_positive"]:
        r = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                r[i, j] = r[j, i] = q.Q[i, j] ** (-1 / 6)  # up to a global scale
        D2 = r**2
        w, V = _mds(D2)
        scale = max(abs(w).max(), 1e-300)
        rel = w / scale
        neg = rel < -RANK_TOL
        rank = int(np.sum(rel > RANK_TOL))
        geometry.update(
            {
                "mds_eigenvalues_relative": [float(v) for v in rel],
                "euclidean": bool(not neg.any()),
                "dimension_required": rank if not neg.any() else None,
            }
        )
        geometry["embeddable"] = bool(not neg.any() and rank <= dev["dimensions"])
        if not geometry["embeddable"]:
            failures.append(
                f"required interaction distances are not realisable in {dev['dimensions']}D "
                f"(MDS rank {rank}, negative eigenvalues: {bool(neg.any())})"
            )
            k = dev["dimensions"]
            pos = V[:, :k] * np.sqrt(np.clip(w[:k], 0, None))
            approx_r = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=-1)
            mask = ~np.eye(n, dtype=bool)
            with np.errstate(divide="ignore"):
                approx_U = np.where(mask, np.where(mask, approx_r, 1.0) ** (-6.0), 0.0)
            r_safe = np.where(mask, r, 1.0)
            target_U = np.where(mask, r_safe ** (-6.0), 0.0)
            ok = np.isfinite(approx_U) & mask
            # Scale-free comparison: best least-squares scale between couplings
            a = (approx_U[ok] @ target_U[ok]) / (approx_U[ok] @ approx_U[ok]) if ok.any() else 0
            err = np.abs(a * approx_U[ok] - target_U[ok]) / target_U[ok]
            geometry["approximation_option"] = {
                "label": "APPROXIMATE - not equivalent",
                "method": f"classical MDS projection to {k}D",
                "max_relative_coupling_error": float(err.max()) if err.size else None,
                "median_relative_coupling_error": float(np.median(err)) if err.size else None,
            }
        else:
            ratio = float(r[np.triu_indices(n, 1)].max() / r[np.triu_indices(n, 1)].min())
            geometry["distance_dynamic_range"] = ratio
            if dev["max_radial_distance_um"]:
                limit = 2 * dev["max_radial_distance_um"] / dev["min_atom_distance_um"]
                if ratio > limit:
                    failures.append(f"distance dynamic range {ratio:.2f} exceeds device limit {limit:.2f}")
    checks["geometry"] = geometry

    status = "exact" if not failures else "unsupported-exact"
    return {
        "target": TARGET,
        "role": "neutral-atom pulse/analog provider ecosystem (not a generic QUBO compiler)",
        "status": status,
        "device": dev,
        "checks": checks,
        "failures": failures,
        "lost_semantics": failures,
        "alternatives": []
        if status == "exact"
        else [
            "Reformulate so couplings follow a realisable geometry (e.g. sparse/unit-disk structure)",
            "Use a higher-level Pasqal workflow that performs its own embedding and report its approximation",
            "Use a digital (gate-based) route on Qiskit/PennyLane where the QUBO maps exactly",
            "Use D-Wave or a classical exact solver for this instance",
            "Accept the labeled approximation only with its coupling error reported in every result",
        ],
        "offline_path": "capability analysis only; local emulation is allowed only after status == exact",
        "remote_execution": "not performed",
    }


def qubo_from_positions(positions: np.ndarray, linear: float = -1.0) -> CanonicalQUBO:
    """Build a QUBO that IS exactly representable (positive fixture for tests)."""
    n = len(positions)
    Q = np.zeros((n, n))
    for i in range(n):
        Q[i, i] = linear
        for j in range(i + 1, n):
            Q[i, j] = Q[j, i] = np.linalg.norm(positions[i] - positions[j]) ** -6
    return CanonicalQUBO(Q=Q, constant=0.0, variables=tuple(f"a{i}" for i in range(n)))
