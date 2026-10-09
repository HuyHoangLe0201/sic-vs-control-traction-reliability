# P1-3: first-order scaling vs complete re-simulation (fvdr, baseline policy)

| config | s_R | s_P | rule | D re-simulated | D scaled | ratio scaled/re-simulated |
|---|---|---|---|---|---|---|
| Si-NPC | 1.1 | 1.1 | ton_clip | 3.15e-05 | 3.15e-05 | 1.001 |
| Si-NPC | 1.1 | 1.1 | ton_free | 9.32e-06 | 9.33e-06 | 1.001 |
| Si-NPC | 0.9 | 0.9 | ton_clip | 4.9e-06 | 4.89e-06 | 1.000 |
| Si-NPC | 0.9 | 0.9 | ton_free | 1.48e-06 | 1.48e-06 | 0.999 |
| Si-NPC | 1.1 | 0.9 | ton_clip | 1.24e-05 | 1.24e-05 | 1.000 |
| Si-NPC | 1.1 | 0.9 | ton_free | 3.71e-06 | 3.71e-06 | 1.000 |
| Si-NPC | 1.0 | 1.1 | ton_clip | 2.02e-05 | 2.02e-05 | 1.000 |
| Si-NPC | 1.0 | 1.1 | ton_free | 6.01e-06 | 6.01e-06 | 1.000 |
| SiC-ANPC | 1.1 | 1.1 | ton_clip | 2.39e-06 | 2.38e-06 | 0.995 |
| SiC-ANPC | 1.1 | 1.1 | ton_free | 3.84e-07 | 3.79e-07 | 0.986 |
| SiC-ANPC | 0.9 | 0.9 | ton_clip | 3.84e-07 | 3.85e-07 | 1.004 |
| SiC-ANPC | 0.9 | 0.9 | ton_free | 6.16e-08 | 6.23e-08 | 1.012 |
| SiC-ANPC | 1.1 | 0.9 | ton_clip | 9.54e-07 | 9.55e-07 | 1.000 |
| SiC-ANPC | 1.1 | 0.9 | ton_free | 1.53e-07 | 1.53e-07 | 1.001 |
| SiC-ANPC | 1.0 | 1.1 | ton_clip | 1.54e-06 | 1.54e-06 | 0.998 |
| SiC-ANPC | 1.0 | 1.1 | ton_free | 2.48e-07 | 2.46e-07 | 0.993 |
