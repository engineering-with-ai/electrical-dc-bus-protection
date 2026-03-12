# Fuse Selection Specification

## Requirements

| Parameter | Requirement | Basis |
|---|---|---|
| Rated voltage | >= 48 V DC | Bus voltage |
| Rated current | 400 A continuous | Load current rating |
| Melting I²t | <= 12,000 A²·s | Must clear before cable damage (fault I²t = 116,000 A²·s at 10 ms) |
| Interrupting capacity (AIC) | >= 5 kA DC | Peak fault current 3.40 kA + margin |
| Mounting | Bolted blade or stud | Bus bar installation |

## Selection Criteria

1. **Melting I²t** is the primary coordination parameter. The fuse must melt before the cable reaches damage temperature.
2. **Interrupting capacity** must exceed the prospective fault current. A fuse that melts but cannot interrupt the arc will fail catastrophically.
3. **DC rating** is mandatory. AC-rated fuses may not clear DC arcs due to lack of zero crossing.
4. **Cold resistance** should be ~1 mohm to match the simulation model.

## Candidate Fuse Classes

| Class | Typical I²t Range | AIC (DC) | Notes |
|---|---|---|---|
| NH / gG (IEC 60269) | 8,000 - 20,000 A²·s at 400 A | 50 kA+ | Industrial, widely available |
| Semiconductor (aR) | 2,000 - 8,000 A²·s at 400 A | 50 kA+ | Faster acting, higher cost |
| Automotive MEGA / MIDI | 5,000 - 15,000 A²·s | 2-10 kA | Compact, verify DC AIC |

## Notes

- Verify DC voltage rating and AIC on the actual fuse datasheet — many fuses are rated for AC only
- Derate continuous current by 20% for ambient temperatures above 40°C per UL 248
- The 9.7x margin between fault I²t and fuse melting I²t provides robust coordination even with tolerance stacking
