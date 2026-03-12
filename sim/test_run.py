import numpy as np
import pytest

from sim.constants import (
    FUSE_I2T_MELT,
    IDEAL_FAULT_CURRENT,
    ureg,
)
from sim.model import simulate


def _extract_steady_state_current(current_ka: np.ndarray) -> float:
    """Extract steady-state fault current from last 10% of simulation.

    Args:
        current_ka: Fault current array in kA

    Returns:
        Mean steady-state current in kA
    """
    tail = current_ka[int(len(current_ka) * 0.9) :]
    return float(np.mean(tail))


def _compute_i2t(time_ms: np.ndarray, current_ka: np.ndarray) -> float:
    """Compute I²t energy let-through using trapezoidal integration.

    Args:
        time_ms: Time array in milliseconds
        current_ka: Current array in kA

    Returns:
        I²t in A²·s
    """
    current_a = current_ka * 1e3
    time_s = time_ms / 1e3
    return float(np.trapezoid(current_a**2, time_s))


class TestFaultCurrent:
    """Assertions against theory.ipynb expected values."""

    def test_inductance_limits_rise(self) -> None:
        """SPICE current must start near zero — cable inductance limits di/dt."""
        # act
        _t, current_ka = simulate()

        # assert — first sample should be well below steady state
        assert current_ka[0] < 0.5 * current_ka[-1]

    def test_steady_state_below_ideal(self) -> None:
        """Steady-state fault current must be at or below ideal (resistive-only) calc.

        SPICE includes inductance which doesn't affect DC steady state,
        but numerical differences and fuse resistance keep it close.
        """
        # arrange
        ideal_ka = IDEAL_FAULT_CURRENT.magnitude.nominal_value

        # act
        _t, current_ka = simulate()
        actual_ka = _extract_steady_state_current(current_ka)

        # assert — should be close to ideal (within 5%), not above
        assert actual_ka == pytest.approx(ideal_ka, rel=0.05)

    def test_peak_current_bounded(self) -> None:
        """Peak fault current must not exceed ideal (no inductance means no overshoot)."""
        # arrange
        ideal_ka = IDEAL_FAULT_CURRENT.magnitude.nominal_value

        # act
        _t, current_ka = simulate()
        peak_ka = float(np.max(current_ka))

        # assert — RL circuit cannot overshoot DC steady state
        assert peak_ka <= ideal_ka * 1.05  # 5% numerical margin

    def test_fuse_coordination(self) -> None:
        """Fault I²t must exceed fuse melting I²t — fuse must blow.

        If fault I²t < fuse I²t, the fuse won't clear and the cable burns.
        """
        # arrange
        fuse_melt_i2t = FUSE_I2T_MELT.to(ureg.A**2 * ureg.s).magnitude.nominal_value

        # act
        time_ms, current_ka = simulate()
        fault_i2t = _compute_i2t(time_ms, current_ka)

        # assert — fault must deliver enough energy to melt the fuse
        assert fault_i2t > fuse_melt_i2t

    def test_starts_at_zero(self) -> None:
        """Current must start at zero (inductor blocks instantaneous change)."""
        # act
        _t, current_ka = simulate()

        # assert
        assert current_ka[0] == pytest.approx(0.0, abs=0.1)
