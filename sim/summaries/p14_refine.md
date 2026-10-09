# P1-4: LP discretisation, default (36 bins, 5 offsets, 36 angles) vs refined (72, 9, 72)

| config | point | T* default / refined (C) | r* default / refined (K) | largest pair bound default / refined (K) | max relative change of pair bounds |
|---|---|---|---|---|---|
| Si-NPC | start-up | 66.87 / 66.86 | 18.84 / 18.84 | 17.48 / 17.52 | 0.178 |
| Si-NPC | acceleration | 67.50 / 67.48 | 8.26 / 8.27 | 8.26 / 8.27 | 0.008 |
| Si-NPC | braking | 60.86 / 60.30 | 6.37 / 6.30 | 4.25 / 3.89 | 0.183 |
| Si-NPC | high speed | 69.72 / 69.72 | 3.80 / 3.84 | 3.78 / 3.81 | 0.008 |
| Si-ANPC | start-up | 61.19 / 61.02 | 13.95 / 13.70 | 7.80 / 6.41 | 0.178 |
| Si-ANPC | acceleration | 59.90 / 59.90 | 4.85 / 4.87 | 3.01 / 3.04 | 0.020 |
| Si-ANPC | braking | 57.92 / 57.88 | 6.04 / 6.00 | 4.09 / 3.43 | 0.160 |
| Si-ANPC | high speed | 68.49 / 68.49 | 3.56 / 3.57 | 3.35 / 3.35 | 0.007 |
| SiC-ANPC | start-up | 47.71 / 47.71 | 4.10 / 4.09 | 4.01 / 3.97 | 0.030 |
| SiC-ANPC | acceleration | 49.22 / 49.12 | 2.45 / 2.40 | 2.03 / 2.01 | 0.011 |
| SiC-ANPC | braking | 45.71 / 45.58 | 1.31 / 1.23 | 1.21 / 1.19 | 0.149 |
| SiC-ANPC | high speed | 55.71 / 55.71 | 3.77 / 3.79 | 3.69 / 3.71 | 0.008 |
