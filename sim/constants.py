from typing import Final

import pint
from uncertainties import ufloat

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

# --- Bus parameters ---
BUS_VOLTAGE: Final = 48.0 * ureg.V  # nominal DC bus, telecom/BESS standard

# --- Battery source ---
# Reason: internal resistance limits peak fault current from the source
SOURCE_RESISTANCE: Final = (
    ufloat(5.0, 0.5) * ureg.mohm
)  # battery pack internal resistance ±10%, per cell datasheet * series count

# --- Cable run (bus to load) ---
CABLE_RESISTANCE: Final = (
    ufloat(8.0, 0.8) * ureg.mohm
)  # 4 AWG copper, 3m run, ±10% per NEC Chapter 9 Table 8
CABLE_INDUCTANCE: Final = (
    ufloat(3.0, 0.6) * ureg.uH
)  # 3m run, ±20%, estimated from cable geometry

# --- Fuse (protecting the bus) ---
FUSE_RATING: Final = 400.0 * ureg.A  # rated continuous current
FUSE_I2T_MELT: Final = (
    ufloat(12000.0, 1200.0) * ureg.A**2 * ureg.s
)  # minimum melting I²t ±10%, per fuse datasheet
FUSE_RESISTANCE: Final = 1.0 * ureg.mohm  # cold resistance, per datasheet

# --- Fault ---
# Reason: bolted fault = zero impedance short at load terminals (worst case)
FAULT_RESISTANCE: Final = 0.1 * ureg.mohm  # near-zero, bolted short

# --- Derived: total loop impedance (hand calc, resistive only) ---
TOTAL_RESISTANCE: Final = (
    SOURCE_RESISTANCE + CABLE_RESISTANCE + FUSE_RESISTANCE + FAULT_RESISTANCE
).to(ureg.mohm)

# --- Ideal peak fault current (resistive, no inductance) ---
IDEAL_FAULT_CURRENT: Final = (BUS_VOLTAGE / TOTAL_RESISTANCE).to(ureg.kA)

# --- Ideal fault I²t at 10ms (for fuse coordination) ---
FAULT_DURATION: Final = 10.0 * ureg.ms  # assessment window
IDEAL_FAULT_I2T: Final = (IDEAL_FAULT_CURRENT**2 * FAULT_DURATION).to(
    ureg.A**2 * ureg.s
)
