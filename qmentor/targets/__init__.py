"""Execution-target adapters.

Every adapter exposes:

* ``capability(q)`` -> CapabilityReport dict (status: exact | approximate |
  unsupported-exact | unknown) produced BEFORE any code or job.
* ``energy_table(q)`` -> {bitstring_in_canonical_order: energy} computed from
  the target's own native representation, so equivalence is tested against
  the target encoding rather than against our own algebra.

Provider SDKs are imported lazily; a missing SDK raises TargetUnavailable,
which tests turn into an explicit skip (never a silent pass).
"""

from __future__ import annotations

from ..canonical import CanonicalQUBO, all_assignments, bits_to_str


class TargetUnavailable(RuntimeError):
    """Optional SDK not installed for this target."""


def check_equivalence(q: CanonicalQUBO, table: dict[str, float], tol: float = 1e-9) -> dict:
    """Compare a target's energy for every assignment with the canonical energy."""
    worst = 0.0
    mismatches = []
    for x in all_assignments(q.n):
        b = bits_to_str(x)
        if b not in table:
            mismatches.append({"bits": b, "reason": "missing"})
            continue
        diff = abs(table[b] - q.energy(x))
        worst = max(worst, diff)
        if diff > tol:
            mismatches.append({"bits": b, "canonical": q.energy(x), "target": table[b]})
    return {
        "states_checked": 2**q.n,
        "max_abs_diff": worst,
        "equivalent": not mismatches,
        "mismatches": mismatches[:5],
    }


def require(module: str):
    import importlib

    try:
        return importlib.import_module(module)
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise TargetUnavailable(f"optional dependency '{module}' is not installed") from exc
