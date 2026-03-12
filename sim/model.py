import numpy as np
from numpy.typing import NDArray
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_V, u_mOhm, u_ms, u_uH, u_us

from sim.constants import (
    BUS_VOLTAGE,
    CABLE_INDUCTANCE,
    CABLE_RESISTANCE,
    FAULT_RESISTANCE,
    FUSE_RESISTANCE,
    SOURCE_RESISTANCE,
    ureg,
)


def build_circuit() -> Circuit:
    """Build DC bus fault circuit netlist.

    Topology: V_bus -> R_source -> R_fuse -> L_cable + R_cable -> R_fault -> GND

    Returns:
        PySpice Circuit ready for simulation
    """
    circuit = Circuit("DC Bus Fault")

    # Reason: voltage source provides bus voltage and lets us measure total current via branch
    v_bus = BUS_VOLTAGE.magnitude
    circuit.V(1, "bus", circuit.gnd, v_bus @ u_V)

    r_src = SOURCE_RESISTANCE.to(ureg.mohm).magnitude.nominal_value
    circuit.R("source", "bus", "post_source", r_src @ u_mOhm)

    r_fuse = FUSE_RESISTANCE.to(ureg.mohm).magnitude
    circuit.R("fuse", "post_source", "post_fuse", r_fuse @ u_mOhm)

    l_cable = CABLE_INDUCTANCE.to(ureg.uH).magnitude.nominal_value
    circuit.L("cable", "post_fuse", "post_inductor", l_cable @ u_uH)

    r_cable = CABLE_RESISTANCE.to(ureg.mohm).magnitude.nominal_value
    circuit.R("cable", "post_inductor", "fault_point", r_cable @ u_mOhm)

    r_fault = FAULT_RESISTANCE.to(ureg.mohm).magnitude
    circuit.R("fault", "fault_point", circuit.gnd, r_fault @ u_mOhm)

    return circuit


def simulate() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Run transient fault simulation.

    Returns:
        Tuple of (time_ms, fault_current_kA) arrays
    """
    circuit = build_circuit()
    simulator = circuit.simulator()

    # Reason: use_initial_condition=True skips DC operating point so inductor starts at zero current
    analysis = simulator.transient(
        step_time=1 @ u_us,
        end_time=10 @ u_ms,
        use_initial_condition=True,
    )

    time_s = np.array([float(t) for t in analysis.time])
    # Reason: current through V1 is negative by SPICE convention (current into + terminal)
    current_a = np.array([-float(i) for i in analysis["v1"]])

    time_ms = time_s * 1e3
    current_ka = current_a / 1e3

    return time_ms, current_ka
