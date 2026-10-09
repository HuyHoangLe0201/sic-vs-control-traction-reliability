# P0-4: pulse-resolved vs carrier-averaged losses (baseline policy, f_sw = 1.5 kHz)

| config | point | pulse ratio | worst chip | ripple avg model (K) | ripple pulsed, mean / max over periods (K) | ratio max/avg | mean loss pulsed/avg |
|---|---|---|---|---|---|---|---|
| Si-NPC | motor 4.8 Hz | 315.8 | D6 / D6 | 33.51 | 34.62 / 34.68 | 1.03 | 1.000 |
| Si-NPC | motor 9.7 Hz | 154.6 | D6 / D6 | 34.36 | 35.54 / 35.67 | 1.04 | 1.000 |
| Si-NPC | motor 20 Hz | 76.1 | D6 / D6 | 20.98 | 22.37 / 22.45 | 1.07 | 1.000 |
| Si-NPC | motor 30 Hz | 50.3 | D6 / D6 | 14.73 | 16.28 / 16.36 | 1.11 | 1.000 |
| Si-NPC | brake 10 Hz | 145.8 | D6 / D6 | 23.93 | 23.94 / 24.12 | 1.01 | 1.000 |
| Si-NPC | brake 20 Hz | 74.3 | D6 / D6 | 14.53 | 14.72 / 14.82 | 1.02 | 1.000 |
| Si-NPC | motor 57 Hz | 26.3 | D6 / D6 | 7.49 | 9.38 / 9.41 | 1.26 | 1.000 |
| Si-NPC | motor 97 Hz | 15.4 | T4 / T4 | 5.18 | 7.46 / 7.52 | 1.45 | 1.000 |
| Si-NPC | motor 147 Hz | 10.2 | T4 / T4 | 4.47 | 6.57 / 6.66 | 1.49 | 0.999 |
| Si-NPC | motor 197 Hz | 7.6 | T4 / T1 | 3.64 | 5.72 / 5.94 | 1.63 | 1.000 |
| Si-NPC | motor 247 Hz | 6.1 | T4 / T4 | 3.08 | 5.10 / 5.34 | 1.74 | 1.001 |
| Si-NPC | brake 153 Hz | 9.8 | D1 / D1 | 5.63 | 6.74 / 6.97 | 1.24 | 1.000 |
| Si-NPC | brake 250 Hz | 6.0 | D1 / D4 | 3.95 | 5.34 / 5.35 | 1.36 | 1.001 |
| Si-ANPC | motor 4.8 Hz | 315.8 | D6 / D6 | 33.56 | 34.67 / 34.73 | 1.03 | 1.000 |
| Si-ANPC | motor 9.7 Hz | 154.6 | D6 / D6 | 34.45 | 35.62 / 35.75 | 1.04 | 1.000 |
| Si-ANPC | motor 20 Hz | 76.1 | D6 / D6 | 21.06 | 22.45 / 22.53 | 1.07 | 1.000 |
| Si-ANPC | motor 30 Hz | 50.3 | D6 / D6 | 14.80 | 16.35 / 16.43 | 1.11 | 1.000 |
| Si-ANPC | brake 10 Hz | 145.8 | D2 / D2 | 26.30 | 26.08 / 26.30 | 1.00 | 1.000 |
| Si-ANPC | brake 20 Hz | 74.3 | D2 / D2 | 17.51 | 17.35 / 17.51 | 1.00 | 1.000 |
| Si-ANPC | motor 57 Hz | 26.3 | D6 / D6 | 7.53 | 9.42 / 9.45 | 1.25 | 1.000 |
| Si-ANPC | motor 97 Hz | 15.4 | T4 / T4 | 5.18 | 7.46 / 7.52 | 1.45 | 1.000 |
| Si-ANPC | motor 147 Hz | 10.2 | T4 / T4 | 4.47 | 6.57 / 6.66 | 1.49 | 0.999 |
| Si-ANPC | motor 197 Hz | 7.6 | T4 / T1 | 3.64 | 5.72 / 5.94 | 1.63 | 1.000 |
| Si-ANPC | motor 247 Hz | 6.1 | T4 / T4 | 3.08 | 5.10 / 5.34 | 1.74 | 1.001 |
| Si-ANPC | brake 153 Hz | 9.8 | D2 / D1 | 5.79 | 6.74 / 6.97 | 1.20 | 1.000 |
| Si-ANPC | brake 250 Hz | 6.0 | D2 / D4 | 4.06 | 5.34 / 5.35 | 1.32 | 1.002 |
| SiC-ANPC | motor 4.8 Hz | 315.8 | S3 / S3 | 11.90 | 11.90 / 11.90 | 1.00 | 1.000 |
| SiC-ANPC | motor 9.7 Hz | 154.6 | S3 / S3 | 16.65 | 16.63 / 16.65 | 1.00 | 1.000 |
| SiC-ANPC | motor 20 Hz | 76.1 | S3 / S3 | 12.24 | 12.20 / 12.24 | 1.00 | 1.000 |
| SiC-ANPC | motor 30 Hz | 50.3 | S3 / S3 | 9.83 | 9.79 / 9.83 | 1.00 | 1.000 |
| SiC-ANPC | brake 10 Hz | 145.8 | S5 / S5 | 12.07 | 13.13 / 13.17 | 1.09 | 1.000 |
| SiC-ANPC | brake 20 Hz | 74.3 | S5 / S5 | 8.07 | 9.18 / 9.26 | 1.15 | 1.000 |
| SiC-ANPC | motor 57 Hz | 26.3 | S3 / S3 | 6.77 | 6.75 / 6.77 | 1.00 | 1.000 |
| SiC-ANPC | motor 97 Hz | 15.4 | S3 / S4 | 5.15 | 6.23 / 6.30 | 1.22 | 1.000 |
| SiC-ANPC | motor 147 Hz | 10.2 | S4 / S1 | 4.39 | 5.60 / 5.72 | 1.30 | 1.000 |
| SiC-ANPC | motor 197 Hz | 7.6 | S4 / S4 | 3.84 | 5.00 / 5.17 | 1.35 | 1.000 |
| SiC-ANPC | motor 247 Hz | 6.1 | S4 / S1 | 3.45 | 4.54 / 4.83 | 1.40 | 0.999 |
| SiC-ANPC | brake 153 Hz | 9.8 | S2 / S4 | 2.81 | 3.11 / 3.18 | 1.13 | 1.000 |
| SiC-ANPC | brake 250 Hz | 6.0 | S2 / S4 | 2.23 | 2.47 / 2.50 | 1.12 | 0.999 |
