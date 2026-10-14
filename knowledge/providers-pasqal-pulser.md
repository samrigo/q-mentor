# Pasqal / Pulser adapter

Tested: `pulser==1.9.1` (last_verified 2026-10-13).

**Rule:** emit a CapabilityReport before any code. Pulser is not a generic QUBO compiler.

## Physics constraints
- Interaction `U_ij = C6 / r_ij^6` is always positive and fixed by atom positions; negative or independent couplings are not available.
- N atoms in 2D give 2N − 3 geometric degrees of freedom versus N(N−1)/2 couplings; dense QUBOs generally cannot be embedded exactly for N ≥ 4.
- Global channels apply one detuning to all atoms; distinct linear terms need local addressing or a DMM, if the device has one.
- Device limits: minimum atom distance, maximum radial distance, max amplitude/detuning (`AnalogDevice`: C6 = 865723.02, ≥ 5 µm, ≤ 38 µm, global channel only).

## Statuses
`exact` only when every check passes. `approximate` requires a stated error bound and a separate result label. Otherwise `unsupported-exact` plus alternatives: gate-model or annealing target, geometry-native reformulation, DMM-capable device.

## Code
`Register.from_coordinates`, `Sequence(register, device)`, `declare_channel("ising", "rydberg_global")`, `Pulse(InterpolatedWaveform(...), InterpolatedWaveform(...), 0)`, `measure("ground-rydberg")`. Emulate with `pulser_simulation.QutipBackendV2` + `QutipConfig(observables=[BitStrings(...)])`; `QutipEmulator` is deprecated (1.9). Noise: `NoiseModel(...)` plus `n_trajectories` in the config.

Worked example and refusal: `examples/bond-selection/pasqal-pulser/`.

v3 notes (2026-10-14): `AnalogDevice.interaction_coeff` = 865 723 rad·µm⁶/µs, while Bloqade's `RB_C6` = 5 420 441 — the same coordinates are different Hamiltonians across SDKs (`examples/conversion/pulser-to-bloqade/`). Exact final-state probabilities: `QutipConfig(observables=[StateResult(evaluation_times=[1.0])])` then `results.final_state.probabilities()` (keys use `r`/`g`). Pulser → Classiq optimization regression: `examples/conversion/pulser-to-classiq-qaoa/`.
