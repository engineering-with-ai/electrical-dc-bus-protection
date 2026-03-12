# dc-bus-protection

48V DC bus fault current analysis and fuse coordination — determines peak fault current during a bolted short circuit at the load terminals and verifies the selected fuse clears before cable damage.

The hand calc uses Ohm's law on the resistive loop (V_bus / R_total) to get the steady-state fault current. Cable inductance only slows the rise — it doesn't change the peak. The PySpice/ngspice transient simulation confirms the RL waveform matches the analytical solution and that the fault I²t exceeds the fuse melting I²t by ~10x.

## Schematic

```mermaid
graph LR
    V["V1<br/>48 V DC"] --> Rs["R_source<br/>5 mohm"]
    Rs --> Rf["R_fuse<br/>1 mohm"]
    Rf --> L["L_cable<br/>3 uH"]
    L --> Rc["R_cable<br/>8 mohm"]
    Rc --> Rfault["R_fault<br/>0.1 mohm"]
    Rfault --> GND["GND"]

    style V fill:#4a9,stroke:#333
    style Rs fill:#49a,stroke:#333
    style Rf fill:#a94,stroke:#333
    style L fill:#94a,stroke:#333
    style Rc fill:#49a,stroke:#333
    style Rfault fill:#a44,stroke:#333
    style GND fill:#666,stroke:#333
```

## Key Results

| Quantity | Value |
|---|---|
| Total loop resistance | 14.1 +/- 0.94 mohm |
| Peak fault current | 3.40 +/- 0.23 kA |
| L/R time constant | ~213 us |
| Fault I²t at 10 ms | ~116,000 A²·s |
| Fuse melting I²t | 12,000 A²·s |
| Fuse clears? | Yes (9.7x margin) |

## Workflow

```
theory.ipynb (hand calc + expected values) -> sim/ (PySpice/ngspice transient) -> pytest (assert sim matches theory)
```

1. `theory.ipynb` derives I_fault = V_bus / R_total symbolically, plugs in actual values with pint + uncertainties, plots analytical RL response
2. `sim/model.py` builds the RL fault circuit netlist and runs a 10 ms transient simulation
3. `sim/test_run.py` asserts: starts at zero, rises with L/R tau, reaches ~3.4 kA, fuse I²t coordination passes

## Quick Start

```bash
uv sync
uv run poe checks
uv run poe notebook
uv run poe sim
```

## Structure

- `theory.ipynb` — sympy derivation, pint + uncertainties, matplotlib verification plot
- `sim/constants.py` — bus voltage, resistances, inductance, fuse I²t with units and tolerances
- `sim/model.py` — PySpice circuit netlist and transient simulation
- `sim/test_run.py` — 5 pytest assertions: rise time, steady state, peak bound, fuse coordination, zero start
- `cad/dc_bus_fault.kicad_sch` — KiCad schematic (0 ERC violations)
- `cad/drawings/` — exported SVG and PDF
- `spec/protection_coordination.md` — system parameters, derived values, coordination check
- `spec/fuse_spec.md` — fuse selection requirements and candidate classes
- `spec/bom.md` — bill of materials
