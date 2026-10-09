# P0-7 / P0-9 / P0-13 post-processing

## P0-7: kappa-bar with a common lifetime kernel for both technologies (u = 0.77, fvdr)

| kernel | sub vs NPC+har | sub vs ANPC+har | both vs ANPC | har gain ANPC | u at kappa 0.25 | u at kappa 0.6 |
|---|---|---|---|---|---|---|
| ton_clip | 0.88 | 1.15 | 0.291 | 12.8 | 0.50 | 0.66 |
| ton_free | 0.294 | 0.384 | 0.0825 | 8.07 | 0.70 | > 0.77 |
| clip+elastic(-10) | 0.00677 | 0.0104 | 0.00148 | 19 | > 0.77 | > 0.77 |
| free+elastic(-10) | 0.00263 | 0.00402 | 0.00148 | 8.15 | > 0.77 | > 0.77 |
| clip+elastic(-4) | 0.889 | 1.16 | 0.296 | 12.6 | 0.50 | 0.66 |
| free+elastic(-4) | 0.3 | 0.392 | 0.0843 | 8.05 | 0.70 | > 0.77 |
| LESIT | 0.414 | 0.595 | 0.112 | 68.7 | 0.63 | > 0.77 |

## P0-9: damage share of the worst chip by heating time (baseline policy, fvdr)

| config | rule | < 20 ms | 20-50 ms | 50-500 ms | > 0.5 s |
|---|---|---|---|---|---|
| Si-NPC | ton_clip | 0.10 | 0.43 | 0.41 | 0.07 |
| Si-NPC | ton_free | 0.05 | 0.30 | 0.44 | 0.21 |
| Si-ANPC | ton_clip | 0.10 | 0.43 | 0.41 | 0.07 |
| Si-ANPC | ton_free | 0.05 | 0.30 | 0.44 | 0.21 |
| SiC-ANPC | ton_clip | 0.62 | 0.27 | 0.09 | 0.02 |
| SiC-ANPC | ton_free | 0.36 | 0.34 | 0.16 | 0.14 |

## P0-13: baseplate solder, N ~ dTc^-n

| variant | n | SiC base / Si-ANPC har | Si-ANPC har / base |
|---|---|---|---|
| fvdr | 2.00 | 0.318 (x3.1) | 0.862 |
| fvdr | 2.26 | 0.281 (x3.6) | 0.862 |
| fvdr | 3.00 | 0.198 (x5.0) | 0.810 |
| fvdr | 4.00 | 0.122 (x8.2) | 0.744 |
| fvdr | 5.00 | 0.0742 (x13.5) | 0.686 |
| fvdr_par | 2.00 | 0.115 (x8.7) | 0.798 |
| fvdr_par | 2.26 | 0.0892 (x11.2) | 0.795 |
| fvdr_par | 3.00 | 0.0437 (x22.9) | 0.795 |
| fvdr_par | 4.00 | 0.0162 (x61.6) | 0.759 |
| fvdr_par | 5.00 | 0.00594 (x168.4) | 0.703 |
| fvdr_u0.3 | 2.00 | 0.0816 (x12.2) | 0.761 |
| fvdr_u0.3 | 2.26 | 0.0622 (x16.1) | 0.750 |
| fvdr_u0.3 | 3.00 | 0.0282 (x35.5) | 0.729 |
| fvdr_u0.3 | 4.00 | 0.00926 (x107.9) | 0.709 |
| fvdr_u0.3 | 5.00 | 0.00297 (x336.9) | 0.649 |
