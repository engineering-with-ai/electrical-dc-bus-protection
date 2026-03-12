# Bill of Materials — DC Bus Fault Protection

| Item | Reference | Description         | Value                             | Qty | Notes                                   |
|------|-----------|---------------------|-----------------------------------|-----|-----------------------------------------|
| 1    | V1        | DC bus source       | 48 V                              | 1   | Battery pack, R_internal = 5 mohm       |
| 2    | R_fuse    | Bus fuse            | 400 A, I²t <= 12,000 A²·s         | 1   | See fuse_spec.md for selection criteria |
| 3    | —         | Bus cable           | 4 AWG copper, 3 m                 | 1   | R = 8 mohm, L = 3 uH per NEC Ch9 T8     |
| 4    | —         | Fuse holder         | Match fuse class (NH, MEGA, etc.) | 1   | Rated for >= 400 A continuous           |
| 5    | —         | Bus bar / terminals | Rated for 5 kA fault              | 2   | Source and load connection points       |

## Notes

- R_fault (0.1 mohm) represents the bolted short — not a purchased component
- R_source (5 mohm) is internal to the battery pack — not a discrete component
- Cable length and gauge determine both R_cable and L_cable — verify against NEC Chapter 9 Table 8 for the actual installation
