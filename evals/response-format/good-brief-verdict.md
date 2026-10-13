Status: complete

Result
**Classical now; quantum teaching PoC only.** Score 31/100. Exhaustive enumeration of all 64 assignments returns A, C, E (energy −9.3725) in microseconds, so no quantum method can add value at this size (fact). A 2-layer QAOA run is useful only to learn the encoding (assumption: the goal is learning).

Validation
Enumeration run locally (`python scripts/validate_math.py`); hard gate "baseline" passes, "advantage hypothesis" fails.

Next
Revisit only if the selection grows past ~40 assets with constraints a MIP solver cannot meet in time.
