"""Rydberg analog <-> Rydberg analog: translate the time-dependent Hamiltonian, not Python calls (README-14).

Canonical analog program (units rad/us, us, um):
    H(t) = Omega(t)/2 sum_i (|g><r| + |r><g|)_i - Delta(t) sum_i n_i + sum_{i<j} C6 / r_ij^6 n_i n_j
three atoms on a line, piecewise-linear Omega and Delta, all atoms start in |g>.

Pulser (AnalogDevice, C6 = 865723.02) and Bloqade (RB_C6 = 5.42e6) use different C6 values. The same coordinates in
um therefore describe DIFFERENT Hamiltonians. Matching the interaction requires scaling Bloqade coordinates by
(C6_bloqade / C6_pulser)^(1/6). With that match the route is class E (final distributions agree within ODE
tolerance); without it the route is at best class A with a measured error.

Pulser durations are in ns (integers, multiples of the device clock); Bloqade durations are in us.
Readout: canonical '1' = Rydberg; Pulser state labels 'r'/'g'; Bloqade state read through run_callback.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Tuple

import numpy as np
from bloqade.analog import RB_C6, start
from pulser import Pulse, Register, Sequence
from pulser.backend import StateResult
from pulser.devices import AnalogDevice
from pulser.waveforms import CompositeWaveform, ConstantWaveform, RampWaveform
from pulser_simulation import QutipBackendV2, QutipConfig

N = 3
SPACING_PULSER_UM = 7.0
OMEGA = 2 * np.pi * 0.6           # rad/us
DELTA_START, DELTA_END = -4.0, 4.0  # rad/us
RAMP_NS, HOLD_NS = 200, 1600
C6_PULSER = AnalogDevice.interaction_coeff
C6_BLOQADE = RB_C6
MATCH_SCALE = (C6_BLOQADE / C6_PULSER) ** (1 / 6)


def pulser_positions() -> List[Tuple[float, float]]:
    return [(SPACING_PULSER_UM * k, 0.0) for k in range(N)]


def bloqade_positions(matched: bool) -> List[Tuple[float, float]]:
    scale = MATCH_SCALE if matched else 1.0
    return [(x * scale, y * scale) for x, y in pulser_positions()]


def interaction_matrix(positions, c6: float) -> np.ndarray:
    pos = np.array(positions)
    out = np.zeros((N, N))
    for i, j in itertools.combinations(range(N), 2):
        out[i, j] = out[j, i] = c6 / np.linalg.norm(pos[i] - pos[j]) ** 6
    return out


def pulser_waveforms():
    amplitude = CompositeWaveform(RampWaveform(RAMP_NS, 0.0, OMEGA), ConstantWaveform(HOLD_NS, OMEGA),
                                  RampWaveform(RAMP_NS, OMEGA, 0.0))
    detuning = CompositeWaveform(ConstantWaveform(RAMP_NS, DELTA_START), RampWaveform(HOLD_NS, DELTA_START, DELTA_END),
                                 ConstantWaveform(RAMP_NS, DELTA_END))
    return amplitude, detuning


def pulser_sequence() -> Sequence:
    coords = np.array(pulser_positions())
    reg = Register.from_coordinates(coords - coords.mean(axis=0), prefix="q")
    seq = Sequence(reg, AnalogDevice)
    seq.declare_channel("rydberg", "rydberg_global")
    amplitude, detuning = pulser_waveforms()
    seq.add(Pulse(amplitude, detuning, 0.0), "rydberg")
    seq.measure("ground-rydberg")
    return seq


def pulser_distribution() -> Dict[str, float]:
    cfg = QutipConfig(observables=[StateResult(evaluation_times=[1.0])])
    res = QutipBackendV2(pulser_sequence(), config=cfg).run()
    return {k.replace("r", "1").replace("g", "0"): float(v) for k, v in res.final_state.probabilities().items()}


def bloqade_program(matched: bool):
    durations = [RAMP_NS / 1000, HOLD_NS / 1000, RAMP_NS / 1000]
    return (start.add_position(bloqade_positions(matched))
            .rydberg.rabi.amplitude.uniform.piecewise_linear(durations, [0.0, OMEGA, OMEGA, 0.0])
            .detuning.uniform.piecewise_linear(durations, [DELTA_START, DELTA_START, DELTA_END, DELTA_END]))


def _collect(state, metadata, hamiltonian):
    probs = np.abs(state.data) ** 2
    ryd = np.array([state.space.is_rydberg_at(k) for k in range(N)])
    out: Dict[str, float] = {}
    for c in range(probs.size):
        key = "".join("1" if ryd[k, c] else "0" for k in range(N))
        out[key] = out.get(key, 0.0) + float(probs[c])
    return out


def bloqade_distribution(matched: bool) -> Dict[str, float]:
    return bloqade_program(matched).bloqade.python().run_callback(_collect, atol=1e-10, rtol=1e-8)[0]


def tvd(a: Dict[str, float], b: Dict[str, float]) -> float:
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys)


def classify(distance: float, exact_tol: float) -> str:
    return "E" if distance <= exact_tol else "A"
