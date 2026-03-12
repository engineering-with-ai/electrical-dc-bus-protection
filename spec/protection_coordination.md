# DC Bus Fault Protection Coordination

## System Parameters

| Parameter | Value | Source |
|---|---|---|
| Bus voltage | 48 V DC | Telecom/BESS standard |
| Source resistance | 5.0 +/- 0.5 mohm | Battery pack internal, per cell datasheet x series count |
| Cable resistance | 8.0 +/- 0.8 mohm | 4 AWG copper, 3m run, per NEC Chapter 9 Table 8 |
| Cable inductance | 3.0 +/- 0.6 uH | 3m run, estimated from cable geometry |
| Fuse resistance (cold) | 1.0 mohm | Fuse datasheet |
| Fault resistance | 0.1 mohm | Bolted short (worst case) |

## Derived Values

| Quantity | Value | Method |
|---|---|---|
| Total loop resistance | 14.1 +/- 0.94 mohm | Sum of series resistances, uncertainty propagated |
| Peak fault current (resistive) | 3.40 +/- 0.23 kA | V_bus / R_total, no inductance |
| L/R time constant | ~213 us | L_cable / R_total |
| Fault I²t at 10 ms | ~116,000 A²·s | I_fault² x t, resistive model |

## Fuse Coordination

| Check | Requirement | Result |
|---|---|---|
| Fault I²t > Fuse melting I²t | 116,000 A²·s > 12,000 A²·s | PASS — 9.7x margin |
| Fuse interrupting capacity > Peak fault current | Must exceed 3.40 kA | Select fuse with AIC >= 5 kA |
| Fuse continuous rating < cable ampacity | 400 A < 4 AWG ampacity (per NEC 310.16) | PASS |

## Conclusion

The 400 A fuse with 12,000 A²·s melting I²t will clear a bolted fault within milliseconds. The fault delivers ~10x the energy needed to melt the fuse element, providing adequate coordination margin even under worst-case tolerance stacking.

## Assumptions

- Bolted fault (zero impedance short at load terminals)
- Constant bus voltage (no source droop under fault)
- Cold fuse resistance (pre-fault)
- No arc resistance (worst case)
- Sea level, 25°C (no altitude or temperature derating)
- Cable inductance neglected for steady-state calc (included in SPICE transient)

## Validation

- Hand calc (resistive model) verified against SPICE transient simulation
- SPICE confirms: current starts at 0, rises with L/R tau ~213 us, reaches ~3.4 kA steady state
- 5 pytest assertions pass (see `sim/test_run.py`)
