# MC3: amplitude correction versus rainflow counting of the pulse-resolved history

Most loaded chip of each point (averaged model). r_a, r_p: averaged and pulse-resolved peak-to-peak ripple (K).
Ratio averaged: rainflow damage of the averaged waveform / single cycle of range r_a (check of the reference).
Ratio pulsed: rainflow damage of the pulse-resolved waveform / single cycle of range r_p (the mission correction).

| config | point | policy | chip | network | rule | r_a | r_p | ratio averaged | ratio pulsed |
|---|---|---|---|---|---|---|---|---|---|
| Si-ANPC | 462 A, 147 Hz | baseline | T4 | nominal | ton_clip | 4.47 | 6.64 | 0.99 | 1.03 |
| Si-ANPC | 462 A, 147 Hz | baseline | T4 | nominal | ton_free | 4.47 | 6.64 | 1.36 | 1.37 |
| Si-ANPC | 462 A, 147 Hz | baseline | T4 | no us term | ton_clip | 4.49 | 4.67 | 0.99 | 0.99 |
| Si-ANPC | 462 A, 147 Hz | baseline | T4 | no us term | ton_free | 4.49 | 4.67 | 1.36 | 1.42 |
| Si-ANPC | 462 A, 147 Hz | mean-temperature law | T4 | nominal | ton_clip | 3.76 | 5.96 | 0.99 | 0.74 |
| Si-ANPC | 462 A, 147 Hz | mean-temperature law | T4 | nominal | ton_free | 3.76 | 5.96 | 1.37 | 1.04 |
| Si-ANPC | 462 A, 147 Hz | mean-temperature law | T4 | no us term | ton_clip | 3.76 | 4.26 | 0.99 | 0.76 |
| Si-ANPC | 462 A, 147 Hz | mean-temperature law | T4 | no us term | ton_free | 3.76 | 4.26 | 1.36 | 1.15 |
| Si-ANPC | 273 A, 250 Hz | baseline | T4 | nominal | ton_clip | 1.56 | 3.09 | 0.99 | 1.08 |
| Si-ANPC | 273 A, 250 Hz | baseline | T4 | nominal | ton_free | 1.56 | 3.09 | 1.36 | 1.44 |
| Si-ANPC | 273 A, 250 Hz | baseline | T4 | no us term | ton_clip | 1.51 | 1.69 | 0.99 | 0.99 |
| Si-ANPC | 273 A, 250 Hz | baseline | T4 | no us term | ton_free | 1.51 | 1.69 | 1.36 | 1.36 |
| Si-ANPC | 273 A, 250 Hz | mean-temperature law | T4 | nominal | ton_clip | 1.25 | 2.60 | 0.99 | 0.56 |
| Si-ANPC | 273 A, 250 Hz | mean-temperature law | T4 | nominal | ton_free | 1.25 | 2.60 | 1.37 | 0.96 |
| Si-ANPC | 273 A, 250 Hz | mean-temperature law | T4 | no us term | ton_clip | 1.21 | 1.52 | 0.99 | 0.65 |
| Si-ANPC | 273 A, 250 Hz | mean-temperature law | T4 | no us term | ton_free | 1.21 | 1.52 | 1.36 | 1.08 |
| SiC-ANPC | 462 A, 147 Hz | baseline | S4 | nominal | ton_clip | 4.39 | 5.72 | 0.99 | 0.95 |
| SiC-ANPC | 462 A, 147 Hz | baseline | S4 | nominal | ton_free | 4.39 | 5.72 | 1.38 | 1.32 |
| SiC-ANPC | 462 A, 147 Hz | baseline | S4 | no us term | ton_clip | 4.47 | 4.68 | 1.00 | 0.90 |
| SiC-ANPC | 462 A, 147 Hz | baseline | S4 | no us term | ton_free | 4.47 | 4.68 | 1.38 | 1.26 |
| SiC-ANPC | 462 A, 147 Hz | mean-temperature law | S4 | nominal | ton_clip | 4.07 | 6.56 | 0.99 | 0.77 |
| SiC-ANPC | 462 A, 147 Hz | mean-temperature law | S4 | nominal | ton_free | 4.07 | 6.56 | 1.38 | 1.19 |
| SiC-ANPC | 462 A, 147 Hz | mean-temperature law | S1 | no us term | ton_clip | 4.14 | 4.72 | 1.01 | 0.85 |
| SiC-ANPC | 462 A, 147 Hz | mean-temperature law | S1 | no us term | ton_free | 4.14 | 4.72 | 1.10 | 1.29 |
| SiC-ANPC | 273 A, 250 Hz | baseline | S4 | nominal | ton_clip | 1.19 | 1.97 | 0.99 | 1.06 |
| SiC-ANPC | 273 A, 250 Hz | baseline | S4 | nominal | ton_free | 1.19 | 1.97 | 1.37 | 1.43 |
| SiC-ANPC | 273 A, 250 Hz | baseline | S4 | no us term | ton_clip | 1.20 | 1.28 | 0.99 | 0.99 |
| SiC-ANPC | 273 A, 250 Hz | baseline | S4 | no us term | ton_free | 1.20 | 1.28 | 1.36 | 1.39 |
| SiC-ANPC | 273 A, 250 Hz | mean-temperature law | S4 | nominal | ton_clip | 1.06 | 2.79 | 0.99 | 0.98 |
| SiC-ANPC | 273 A, 250 Hz | mean-temperature law | S4 | nominal | ton_free | 1.06 | 2.79 | 1.37 | 1.40 |
| SiC-ANPC | 273 A, 250 Hz | mean-temperature law | S4 | no us term | ton_clip | 1.07 | 1.36 | 0.99 | 0.95 |
| SiC-ANPC | 273 A, 250 Hz | mean-temperature law | S4 | no us term | ton_free | 1.07 | 1.36 | 1.36 | 1.39 |

- ton_clip, nominal: ratio pulsed 0.56--1.08
- ton_clip, no us term: ratio pulsed 0.65--0.99
- ton_free, nominal: ratio pulsed 0.96--1.44
- ton_free, no us term: ratio pulsed 1.08--1.42
