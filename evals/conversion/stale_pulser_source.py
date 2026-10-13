"""Negative fixture: outdated Pulser source (pre-1.0 API). Conversion must reject, not port."""
import numpy as np
from pulser import Pulse, Register, Sequence
from pulser.devices import AnalogDevice
from pulser.waveforms import RampWaveform
from pulser_simulation import Simulation

reg = Register.from_coordinates(np.array([[0.0, 0.0], [6.0, 0.0]]), prefix="q")
seq = Sequence(reg, AnalogDevice)
seq.declare_channel("ising", "rydberg_global")
seq.add(Pulse.ConstantDetuning(RampWaveform(1000, 0.0, 6.0), 0.0, 0.0), "ising")
result = Simulation(seq).run()
