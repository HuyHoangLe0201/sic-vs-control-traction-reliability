# Amplitude correction versus rainflow counting, extended set of points (review round 5)

ratio = rainflow damage of the pulse-resolved waveform / damage of the single corrected cycle
(below 1: the mission correction overstates the damage).

| network | rule | policy | n | min | median | max |
|---|---|---|---|---|---|---|
| nominal | ton_clip | baseline | 36 | 0.83 | 0.97 | 1.06 |
| nominal | ton_clip | mean-temperature law | 36 | 0.36 | 0.68 | 1.19 |
| nominal | ton_clip | ripple-aware law | 36 | 0.24 | 0.68 | 2.16 |
| nominal | ton_free | baseline | 36 | 1.01 | 1.29 | 1.47 |
| nominal | ton_free | mean-temperature law | 36 | 0.57 | 1.00 | 1.55 |
| nominal | ton_free | ripple-aware law | 36 | 0.46 | 0.95 | 1.66 |
| no us term | ton_clip | baseline | 36 | 0.83 | 0.97 | 1.02 |
| no us term | ton_clip | mean-temperature law | 36 | 0.40 | 0.78 | 1.00 |
| no us term | ton_clip | ripple-aware law | 36 | 0.35 | 0.78 | 1.59 |
| no us term | ton_free | baseline | 36 | 1.03 | 1.30 | 1.48 |
| no us term | ton_free | mean-temperature law | 36 | 0.70 | 1.13 | 1.44 |
| no us term | ton_free | ripple-aware law | 36 | 0.58 | 1.14 | 1.71 |

Points with r_p >= 1 K only (smaller cycles contribute negligibly).

| config | I | fe | cos | policy | chip | network | rule | r_a | r_p | ratio |
|---|---|---|---|---|---|---|---|---|---|---|
| Si-NPC | 460 | 19 | +0.95 | baseline | D6 | nominal | ton_clip | 21.87 | 23.33 | 1.01 |
| Si-NPC | 460 | 19 | +0.95 | baseline | D6 | nominal | ton_free | 21.87 | 23.33 | 1.43 |
| Si-NPC | 460 | 19 | +0.95 | baseline | D6 | no us term | ton_clip | 21.99 | 22.26 | 1.00 |
| Si-NPC | 460 | 19 | +0.95 | baseline | D6 | no us term | ton_free | 21.99 | 22.26 | 1.42 |
| Si-NPC | 460 | 19 | +0.95 | mean-temperature law | D6 | nominal | ton_clip | 15.91 | 17.70 | 1.00 |
| Si-NPC | 460 | 19 | +0.95 | mean-temperature law | D6 | nominal | ton_free | 15.91 | 17.70 | 1.29 |
| Si-NPC | 460 | 19 | +0.95 | mean-temperature law | D6 | no us term | ton_clip | 15.92 | 16.80 | 0.99 |
| Si-NPC | 460 | 19 | +0.95 | mean-temperature law | D6 | no us term | ton_free | 15.92 | 16.80 | 1.29 |
| Si-NPC | 460 | 19 | +0.95 | ripple-aware law | D5 | nominal | ton_clip | 10.18 | 12.53 | 1.03 |
| Si-NPC | 460 | 19 | +0.95 | ripple-aware law | D5 | nominal | ton_free | 10.18 | 12.53 | 1.32 |
| Si-NPC | 460 | 19 | +0.95 | ripple-aware law | D5 | no us term | ton_clip | 10.19 | 11.49 | 0.92 |
| Si-NPC | 460 | 19 | +0.95 | ripple-aware law | D5 | no us term | ton_free | 10.19 | 11.49 | 1.21 |
| Si-NPC | 460 | 46 | +0.95 | baseline | D6 | nominal | ton_clip | 9.39 | 11.28 | 1.02 |
| Si-NPC | 460 | 46 | +0.95 | baseline | D6 | nominal | ton_free | 9.39 | 11.28 | 1.35 |
| Si-NPC | 460 | 46 | +0.95 | baseline | D6 | no us term | ton_clip | 9.52 | 10.00 | 0.98 |
| Si-NPC | 460 | 46 | +0.95 | baseline | D6 | no us term | ton_free | 9.52 | 10.00 | 1.38 |
| Si-NPC | 460 | 46 | +0.95 | mean-temperature law | D6 | nominal | ton_clip | 9.35 | 14.35 | 0.47 |
| Si-NPC | 460 | 46 | +0.95 | mean-temperature law | D6 | nominal | ton_free | 9.35 | 14.35 | 0.83 |
| Si-NPC | 460 | 46 | +0.95 | mean-temperature law | D6 | no us term | ton_clip | 9.19 | 13.22 | 0.40 |
| Si-NPC | 460 | 46 | +0.95 | mean-temperature law | D6 | no us term | ton_free | 9.19 | 13.22 | 0.77 |
| Si-NPC | 460 | 46 | +0.95 | ripple-aware law | D6 | nominal | ton_clip | 7.23 | 14.17 | 0.51 |
| Si-NPC | 460 | 46 | +0.95 | ripple-aware law | D6 | nominal | ton_free | 7.23 | 14.17 | 0.91 |
| Si-NPC | 460 | 46 | +0.95 | ripple-aware law | D6 | no us term | ton_clip | 7.27 | 11.71 | 0.45 |
| Si-NPC | 460 | 46 | +0.95 | ripple-aware law | D6 | no us term | ton_free | 7.27 | 11.71 | 0.80 |
| Si-NPC | 460 | 92 | +0.95 | baseline | T4 | nominal | ton_clip | 5.10 | 7.50 | 1.06 |
| Si-NPC | 460 | 92 | +0.95 | baseline | T4 | nominal | ton_free | 5.10 | 7.50 | 1.35 |
| Si-NPC | 460 | 92 | +0.95 | baseline | T4 | no us term | ton_clip | 5.17 | 5.46 | 0.98 |
| Si-NPC | 460 | 92 | +0.95 | baseline | T4 | no us term | ton_free | 5.17 | 5.46 | 1.32 |
| Si-NPC | 460 | 92 | +0.95 | mean-temperature law | T3 | nominal | ton_clip | 4.87 | 5.66 | 0.57 |
| Si-NPC | 460 | 92 | +0.95 | mean-temperature law | T3 | nominal | ton_free | 4.87 | 5.66 | 0.84 |
| Si-NPC | 460 | 92 | +0.95 | mean-temperature law | T3 | no us term | ton_clip | 4.94 | 4.95 | 0.98 |
| Si-NPC | 460 | 92 | +0.95 | mean-temperature law | T3 | no us term | ton_free | 4.94 | 4.95 | 1.36 |
| Si-NPC | 460 | 92 | +0.95 | ripple-aware law | T3 | nominal | ton_clip | 4.87 | 5.66 | 0.57 |
| Si-NPC | 460 | 92 | +0.95 | ripple-aware law | T3 | nominal | ton_free | 4.87 | 5.66 | 0.84 |
| Si-NPC | 460 | 92 | +0.95 | ripple-aware law | T3 | no us term | ton_clip | 4.94 | 4.95 | 0.98 |
| Si-NPC | 460 | 92 | +0.95 | ripple-aware law | T3 | no us term | ton_free | 4.94 | 4.95 | 1.36 |
| Si-NPC | 460 | 135 | +0.95 | baseline | T4 | nominal | ton_clip | 4.73 | 7.11 | 0.96 |
| Si-NPC | 460 | 135 | +0.95 | baseline | T4 | nominal | ton_free | 4.73 | 7.11 | 1.14 |
| Si-NPC | 460 | 135 | +0.95 | baseline | T4 | no us term | ton_clip | 4.77 | 4.97 | 0.95 |
| Si-NPC | 460 | 135 | +0.95 | baseline | T4 | no us term | ton_free | 4.77 | 4.97 | 1.29 |
| Si-NPC | 460 | 135 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 4.27 | 9.10 | 0.36 |
| Si-NPC | 460 | 135 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 4.27 | 9.10 | 0.62 |
| Si-NPC | 460 | 135 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 4.32 | 4.90 | 0.89 |
| Si-NPC | 460 | 135 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 4.32 | 4.90 | 1.15 |
| Si-NPC | 460 | 135 | +0.95 | ripple-aware law | T4 | nominal | ton_clip | 4.21 | 9.35 | 0.42 |
| Si-NPC | 460 | 135 | +0.95 | ripple-aware law | T4 | nominal | ton_free | 4.21 | 9.35 | 0.65 |
| Si-NPC | 460 | 135 | +0.95 | ripple-aware law | T4 | no us term | ton_clip | 4.24 | 5.05 | 0.81 |
| Si-NPC | 460 | 135 | +0.95 | ripple-aware law | T4 | no us term | ton_free | 4.24 | 5.05 | 1.27 |
| Si-NPC | 460 | 184 | +0.95 | baseline | T4 | nominal | ton_clip | 3.83 | 6.28 | 0.90 |
| Si-NPC | 460 | 184 | +0.95 | baseline | T4 | nominal | ton_free | 3.83 | 6.28 | 1.24 |
| Si-NPC | 460 | 184 | +0.95 | baseline | T4 | no us term | ton_clip | 3.81 | 4.09 | 0.89 |
| Si-NPC | 460 | 184 | +0.95 | baseline | T4 | no us term | ton_free | 3.81 | 4.09 | 1.28 |
| Si-NPC | 460 | 184 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 3.38 | 7.62 | 0.45 |
| Si-NPC | 460 | 184 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 3.38 | 7.62 | 0.72 |
| Si-NPC | 460 | 184 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 3.34 | 4.05 | 0.81 |
| Si-NPC | 460 | 184 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 3.34 | 4.05 | 1.15 |
| Si-NPC | 460 | 184 | +0.95 | ripple-aware law | T4 | nominal | ton_clip | 3.38 | 7.62 | 0.45 |
| Si-NPC | 460 | 184 | +0.95 | ripple-aware law | T4 | nominal | ton_free | 3.38 | 7.62 | 0.72 |
| Si-NPC | 460 | 184 | +0.95 | ripple-aware law | T4 | no us term | ton_clip | 3.34 | 4.05 | 0.81 |
| Si-NPC | 460 | 184 | +0.95 | ripple-aware law | T4 | no us term | ton_free | 3.34 | 4.05 | 1.15 |
| Si-NPC | 460 | 230 | +0.95 | baseline | T4 | nominal | ton_clip | 3.25 | 5.80 | 0.83 |
| Si-NPC | 460 | 230 | +0.95 | baseline | T4 | nominal | ton_free | 3.25 | 5.80 | 1.20 |
| Si-NPC | 460 | 230 | +0.95 | baseline | T4 | no us term | ton_clip | 3.18 | 3.48 | 0.83 |
| Si-NPC | 460 | 230 | +0.95 | baseline | T4 | no us term | ton_free | 3.18 | 3.48 | 1.23 |
| Si-NPC | 460 | 230 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 2.87 | 6.92 | 0.50 |
| Si-NPC | 460 | 230 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 2.87 | 6.92 | 0.57 |
| Si-NPC | 460 | 230 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 2.79 | 3.42 | 0.78 |
| Si-NPC | 460 | 230 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 2.79 | 3.42 | 1.23 |
| Si-NPC | 460 | 230 | +0.95 | ripple-aware law | T4 | nominal | ton_clip | 2.87 | 6.92 | 0.50 |
| Si-NPC | 460 | 230 | +0.95 | ripple-aware law | T4 | nominal | ton_free | 2.87 | 6.92 | 0.57 |
| Si-NPC | 460 | 230 | +0.95 | ripple-aware law | T4 | no us term | ton_clip | 2.79 | 3.42 | 0.78 |
| Si-NPC | 460 | 230 | +0.95 | ripple-aware law | T4 | no us term | ton_free | 2.79 | 3.42 | 1.23 |
| Si-NPC | 380 | 19 | -0.95 | baseline | D6 | nominal | ton_clip | 15.35 | 15.63 | 0.99 |
| Si-NPC | 380 | 19 | -0.95 | baseline | D6 | nominal | ton_free | 15.35 | 15.63 | 1.20 |
| Si-NPC | 380 | 19 | -0.95 | baseline | D6 | no us term | ton_clip | 15.44 | 15.63 | 0.98 |
| Si-NPC | 380 | 19 | -0.95 | baseline | D6 | no us term | ton_free | 15.44 | 15.63 | 1.20 |
| Si-NPC | 380 | 19 | -0.95 | mean-temperature law | D6 | nominal | ton_clip | 10.37 | 13.06 | 0.93 |
| Si-NPC | 380 | 19 | -0.95 | mean-temperature law | D6 | nominal | ton_free | 10.37 | 13.06 | 1.10 |
| Si-NPC | 380 | 19 | -0.95 | mean-temperature law | D6 | no us term | ton_clip | 10.34 | 11.77 | 0.91 |
| Si-NPC | 380 | 19 | -0.95 | mean-temperature law | D6 | no us term | ton_free | 10.34 | 11.77 | 1.10 |
| Si-NPC | 380 | 19 | -0.95 | ripple-aware law | D1 | nominal | ton_clip | 7.07 | 10.24 | 0.85 |
| Si-NPC | 380 | 19 | -0.95 | ripple-aware law | D1 | nominal | ton_free | 7.07 | 10.24 | 1.12 |
| Si-NPC | 380 | 19 | -0.95 | ripple-aware law | D6 | no us term | ton_clip | 7.07 | 8.86 | 0.89 |
| Si-NPC | 380 | 19 | -0.95 | ripple-aware law | D6 | no us term | ton_free | 7.07 | 8.86 | 1.14 |
| Si-NPC | 380 | 46 | -0.95 | baseline | D6 | nominal | ton_clip | 6.57 | 7.18 | 0.96 |
| Si-NPC | 380 | 46 | -0.95 | baseline | D6 | nominal | ton_free | 6.57 | 7.18 | 1.04 |
| Si-NPC | 380 | 46 | -0.95 | baseline | D6 | no us term | ton_clip | 6.66 | 7.03 | 0.97 |
| Si-NPC | 380 | 46 | -0.95 | baseline | D6 | no us term | ton_free | 6.66 | 7.03 | 1.15 |
| Si-NPC | 380 | 46 | -0.95 | mean-temperature law | D6 | nominal | ton_clip | 7.15 | 9.36 | 0.61 |
| Si-NPC | 380 | 46 | -0.95 | mean-temperature law | D6 | nominal | ton_free | 7.15 | 9.36 | 0.90 |
| Si-NPC | 380 | 46 | -0.95 | mean-temperature law | D6 | no us term | ton_clip | 7.26 | 9.32 | 0.57 |
| Si-NPC | 380 | 46 | -0.95 | mean-temperature law | D6 | no us term | ton_free | 7.26 | 9.32 | 0.89 |
| Si-NPC | 380 | 46 | -0.95 | ripple-aware law | D5 | nominal | ton_clip | 4.92 | 7.65 | 0.71 |
| Si-NPC | 380 | 46 | -0.95 | ripple-aware law | D5 | nominal | ton_free | 4.92 | 7.65 | 1.10 |
| Si-NPC | 380 | 46 | -0.95 | ripple-aware law | D6 | no us term | ton_clip | 4.93 | 7.96 | 0.40 |
| Si-NPC | 380 | 46 | -0.95 | ripple-aware law | D6 | no us term | ton_free | 4.93 | 7.96 | 0.75 |
| Si-NPC | 370 | 92 | -0.95 | baseline | D1 | nominal | ton_clip | 5.73 | 7.09 | 1.03 |
| Si-NPC | 370 | 92 | -0.95 | baseline | D1 | nominal | ton_free | 5.73 | 7.09 | 1.40 |
| Si-NPC | 370 | 92 | -0.95 | baseline | D1 | no us term | ton_clip | 5.78 | 6.07 | 0.95 |
| Si-NPC | 370 | 92 | -0.95 | baseline | D1 | no us term | ton_free | 5.78 | 6.07 | 1.16 |
| Si-NPC | 370 | 92 | -0.95 | mean-temperature law | D1 | nominal | ton_clip | 5.26 | 8.22 | 0.74 |
| Si-NPC | 370 | 92 | -0.95 | mean-temperature law | D1 | nominal | ton_free | 5.26 | 8.22 | 1.00 |
| Si-NPC | 370 | 92 | -0.95 | mean-temperature law | D1 | no us term | ton_clip | 5.31 | 6.47 | 0.65 |
| Si-NPC | 370 | 92 | -0.95 | mean-temperature law | D1 | no us term | ton_free | 5.31 | 6.47 | 0.92 |
| Si-NPC | 370 | 92 | -0.95 | ripple-aware law | D1 | nominal | ton_clip | 5.01 | 7.75 | 0.73 |
| Si-NPC | 370 | 92 | -0.95 | ripple-aware law | D1 | nominal | ton_free | 5.01 | 7.75 | 1.11 |
| Si-NPC | 370 | 92 | -0.95 | ripple-aware law | D1 | no us term | ton_clip | 5.06 | 6.40 | 0.63 |
| Si-NPC | 370 | 92 | -0.95 | ripple-aware law | D1 | no us term | ton_free | 5.06 | 6.40 | 1.10 |
| Si-NPC | 400 | 159 | -0.95 | baseline | D1 | nominal | ton_clip | 5.45 | 6.77 | 0.91 |
| Si-NPC | 400 | 159 | -0.95 | baseline | D1 | nominal | ton_free | 5.45 | 6.77 | 1.31 |
| Si-NPC | 400 | 159 | -0.95 | baseline | D1 | no us term | ton_clip | 5.43 | 5.70 | 0.92 |
| Si-NPC | 400 | 159 | -0.95 | baseline | D1 | no us term | ton_free | 5.43 | 5.70 | 1.28 |
| Si-NPC | 400 | 159 | -0.95 | mean-temperature law | D4 | nominal | ton_clip | 5.17 | 7.57 | 0.59 |
| Si-NPC | 400 | 159 | -0.95 | mean-temperature law | D4 | nominal | ton_free | 5.17 | 7.57 | 0.90 |
| Si-NPC | 400 | 159 | -0.95 | mean-temperature law | D4 | no us term | ton_clip | 5.17 | 5.70 | 0.78 |
| Si-NPC | 400 | 159 | -0.95 | mean-temperature law | D4 | no us term | ton_free | 5.17 | 5.70 | 1.16 |
| Si-NPC | 400 | 159 | -0.95 | ripple-aware law | D4 | nominal | ton_clip | 5.17 | 7.57 | 0.59 |
| Si-NPC | 400 | 159 | -0.95 | ripple-aware law | D4 | nominal | ton_free | 5.17 | 7.57 | 0.90 |
| Si-NPC | 400 | 159 | -0.95 | ripple-aware law | D4 | no us term | ton_clip | 5.17 | 5.70 | 0.78 |
| Si-NPC | 400 | 159 | -0.95 | ripple-aware law | D4 | no us term | ton_free | 5.17 | 5.70 | 1.16 |
| Si-NPC | 400 | 216 | -0.95 | baseline | D1 | nominal | ton_clip | 4.37 | 5.73 | 0.88 |
| Si-NPC | 400 | 216 | -0.95 | baseline | D1 | nominal | ton_free | 4.37 | 5.73 | 1.09 |
| Si-NPC | 400 | 216 | -0.95 | baseline | D1 | no us term | ton_clip | 4.27 | 4.57 | 0.94 |
| Si-NPC | 400 | 216 | -0.95 | baseline | D1 | no us term | ton_free | 4.27 | 4.57 | 1.20 |
| Si-NPC | 400 | 216 | -0.95 | mean-temperature law | D1 | nominal | ton_clip | 4.18 | 5.34 | 1.03 |
| Si-NPC | 400 | 216 | -0.95 | mean-temperature law | D1 | nominal | ton_free | 4.18 | 5.34 | 1.10 |
| Si-NPC | 400 | 216 | -0.95 | mean-temperature law | D4 | no us term | ton_clip | 4.12 | 4.70 | 0.84 |
| Si-NPC | 400 | 216 | -0.95 | mean-temperature law | D4 | no us term | ton_free | 4.12 | 4.70 | 1.31 |
| Si-NPC | 400 | 216 | -0.95 | ripple-aware law | D1 | nominal | ton_clip | 4.18 | 5.34 | 1.03 |
| Si-NPC | 400 | 216 | -0.95 | ripple-aware law | D1 | nominal | ton_free | 4.18 | 5.34 | 1.10 |
| Si-NPC | 400 | 216 | -0.95 | ripple-aware law | D4 | no us term | ton_clip | 4.12 | 4.70 | 0.84 |
| Si-NPC | 400 | 216 | -0.95 | ripple-aware law | D4 | no us term | ton_free | 4.12 | 4.70 | 1.31 |
| Si-NPC | 400 | 250 | -0.95 | baseline | D1 | nominal | ton_clip | 3.92 | 5.28 | 1.01 |
| Si-NPC | 400 | 250 | -0.95 | baseline | D1 | nominal | ton_free | 3.92 | 5.28 | 1.09 |
| Si-NPC | 400 | 250 | -0.95 | baseline | D4 | no us term | ton_clip | 3.78 | 4.17 | 1.00 |
| Si-NPC | 400 | 250 | -0.95 | baseline | D4 | no us term | ton_free | 3.78 | 4.17 | 1.39 |
| Si-NPC | 400 | 250 | -0.95 | mean-temperature law | D1 | nominal | ton_clip | 3.74 | 4.96 | 0.97 |
| Si-NPC | 400 | 250 | -0.95 | mean-temperature law | D1 | nominal | ton_free | 3.74 | 4.96 | 1.07 |
| Si-NPC | 400 | 250 | -0.95 | mean-temperature law | D4 | no us term | ton_clip | 3.65 | 4.16 | 0.96 |
| Si-NPC | 400 | 250 | -0.95 | mean-temperature law | D4 | no us term | ton_free | 3.65 | 4.16 | 1.38 |
| Si-NPC | 400 | 250 | -0.95 | ripple-aware law | D1 | nominal | ton_clip | 3.74 | 4.96 | 0.97 |
| Si-NPC | 400 | 250 | -0.95 | ripple-aware law | D1 | nominal | ton_free | 3.74 | 4.96 | 1.07 |
| Si-NPC | 400 | 250 | -0.95 | ripple-aware law | D4 | no us term | ton_clip | 3.65 | 4.16 | 0.96 |
| Si-NPC | 400 | 250 | -0.95 | ripple-aware law | D4 | no us term | ton_free | 3.65 | 4.16 | 1.38 |
| Si-ANPC | 460 | 19 | +0.95 | baseline | D6 | nominal | ton_clip | 21.95 | 23.41 | 1.01 |
| Si-ANPC | 460 | 19 | +0.95 | baseline | D6 | nominal | ton_free | 21.95 | 23.41 | 1.43 |
| Si-ANPC | 460 | 19 | +0.95 | baseline | D6 | no us term | ton_clip | 22.08 | 22.34 | 1.00 |
| Si-ANPC | 460 | 19 | +0.95 | baseline | D6 | no us term | ton_free | 22.08 | 22.34 | 1.43 |
| Si-ANPC | 460 | 19 | +0.95 | mean-temperature law | D6 | nominal | ton_clip | 8.25 | 9.68 | 0.96 |
| Si-ANPC | 460 | 19 | +0.95 | mean-temperature law | D6 | nominal | ton_free | 8.25 | 9.68 | 1.31 |
| Si-ANPC | 460 | 19 | +0.95 | mean-temperature law | D6 | no us term | ton_clip | 8.29 | 8.64 | 0.92 |
| Si-ANPC | 460 | 19 | +0.95 | mean-temperature law | D6 | no us term | ton_free | 8.29 | 8.64 | 1.28 |
| Si-ANPC | 460 | 19 | +0.95 | ripple-aware law | D6 | nominal | ton_clip | 7.17 | 9.76 | 0.81 |
| Si-ANPC | 460 | 19 | +0.95 | ripple-aware law | D6 | nominal | ton_free | 7.17 | 9.76 | 1.21 |
| Si-ANPC | 460 | 19 | +0.95 | ripple-aware law | D6 | no us term | ton_clip | 7.19 | 8.44 | 0.80 |
| Si-ANPC | 460 | 19 | +0.95 | ripple-aware law | D6 | no us term | ton_free | 7.19 | 8.44 | 1.22 |
| Si-ANPC | 460 | 46 | +0.95 | baseline | D6 | nominal | ton_clip | 9.44 | 11.33 | 1.02 |
| Si-ANPC | 460 | 46 | +0.95 | baseline | D6 | nominal | ton_free | 9.44 | 11.33 | 1.43 |
| Si-ANPC | 460 | 46 | +0.95 | baseline | D6 | no us term | ton_clip | 9.57 | 10.05 | 0.98 |
| Si-ANPC | 460 | 46 | +0.95 | baseline | D6 | no us term | ton_free | 9.57 | 10.05 | 1.41 |
| Si-ANPC | 460 | 46 | +0.95 | mean-temperature law | D2 | nominal | ton_clip | 4.19 | 5.68 | 0.56 |
| Si-ANPC | 460 | 46 | +0.95 | mean-temperature law | D2 | nominal | ton_free | 4.19 | 5.68 | 0.82 |
| Si-ANPC | 460 | 46 | +0.95 | mean-temperature law | D6 | no us term | ton_clip | 4.16 | 5.31 | 0.48 |
| Si-ANPC | 460 | 46 | +0.95 | mean-temperature law | D6 | no us term | ton_free | 4.16 | 5.31 | 0.70 |
| Si-ANPC | 460 | 46 | +0.95 | ripple-aware law | D2 | nominal | ton_clip | 4.12 | 5.72 | 0.56 |
| Si-ANPC | 460 | 46 | +0.95 | ripple-aware law | D2 | nominal | ton_free | 4.12 | 5.72 | 0.90 |
| Si-ANPC | 460 | 46 | +0.95 | ripple-aware law | T3 | no us term | ton_clip | 4.02 | 5.26 | 0.51 |
| Si-ANPC | 460 | 46 | +0.95 | ripple-aware law | T3 | no us term | ton_free | 4.02 | 5.26 | 0.88 |
| Si-ANPC | 460 | 92 | +0.95 | baseline | T4 | nominal | ton_clip | 5.10 | 7.50 | 1.06 |
| Si-ANPC | 460 | 92 | +0.95 | baseline | T4 | nominal | ton_free | 5.10 | 7.50 | 1.35 |
| Si-ANPC | 460 | 92 | +0.95 | baseline | T4 | no us term | ton_clip | 5.17 | 5.46 | 0.98 |
| Si-ANPC | 460 | 92 | +0.95 | baseline | T4 | no us term | ton_free | 5.17 | 5.46 | 1.32 |
| Si-ANPC | 460 | 92 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 4.23 | 7.27 | 0.86 |
| Si-ANPC | 460 | 92 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 4.23 | 7.27 | 1.06 |
| Si-ANPC | 460 | 92 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 4.29 | 5.01 | 0.76 |
| Si-ANPC | 460 | 92 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 4.29 | 5.01 | 1.09 |
| Si-ANPC | 460 | 92 | +0.95 | ripple-aware law | T3 | nominal | ton_clip | 4.01 | 9.63 | 0.31 |
| Si-ANPC | 460 | 92 | +0.95 | ripple-aware law | T3 | nominal | ton_free | 4.01 | 9.63 | 0.48 |
| Si-ANPC | 460 | 92 | +0.95 | ripple-aware law | T3 | no us term | ton_clip | 4.05 | 6.02 | 0.35 |
| Si-ANPC | 460 | 92 | +0.95 | ripple-aware law | T3 | no us term | ton_free | 4.05 | 6.02 | 0.58 |
| Si-ANPC | 460 | 135 | +0.95 | baseline | T4 | nominal | ton_clip | 4.73 | 7.11 | 0.96 |
| Si-ANPC | 460 | 135 | +0.95 | baseline | T4 | nominal | ton_free | 4.73 | 7.11 | 1.14 |
| Si-ANPC | 460 | 135 | +0.95 | baseline | T4 | no us term | ton_clip | 4.77 | 4.97 | 0.95 |
| Si-ANPC | 460 | 135 | +0.95 | baseline | T4 | no us term | ton_free | 4.77 | 4.97 | 1.29 |
| Si-ANPC | 460 | 135 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 3.97 | 6.28 | 0.67 |
| Si-ANPC | 460 | 135 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 3.97 | 6.28 | 1.00 |
| Si-ANPC | 460 | 135 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 3.98 | 4.47 | 0.76 |
| Si-ANPC | 460 | 135 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 3.98 | 4.47 | 0.95 |
| Si-ANPC | 460 | 135 | +0.95 | ripple-aware law | T4 | nominal | ton_clip | 3.93 | 6.27 | 0.66 |
| Si-ANPC | 460 | 135 | +0.95 | ripple-aware law | T4 | nominal | ton_free | 3.93 | 6.27 | 0.93 |
| Si-ANPC | 460 | 135 | +0.95 | ripple-aware law | T4 | no us term | ton_clip | 3.95 | 4.55 | 0.69 |
| Si-ANPC | 460 | 135 | +0.95 | ripple-aware law | T4 | no us term | ton_free | 3.95 | 4.55 | 0.99 |
| Si-ANPC | 460 | 184 | +0.95 | baseline | T4 | nominal | ton_clip | 3.83 | 6.28 | 0.90 |
| Si-ANPC | 460 | 184 | +0.95 | baseline | T4 | nominal | ton_free | 3.83 | 6.28 | 1.24 |
| Si-ANPC | 460 | 184 | +0.95 | baseline | T4 | no us term | ton_clip | 3.81 | 4.09 | 0.89 |
| Si-ANPC | 460 | 184 | +0.95 | baseline | T4 | no us term | ton_free | 3.81 | 4.09 | 1.28 |
| Si-ANPC | 460 | 184 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 3.25 | 5.69 | 0.58 |
| Si-ANPC | 460 | 184 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 3.25 | 5.69 | 0.95 |
| Si-ANPC | 460 | 184 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 3.22 | 3.76 | 0.71 |
| Si-ANPC | 460 | 184 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 3.22 | 3.76 | 1.12 |
| Si-ANPC | 460 | 184 | +0.95 | ripple-aware law | T4 | nominal | ton_clip | 3.20 | 8.17 | 0.27 |
| Si-ANPC | 460 | 184 | +0.95 | ripple-aware law | T4 | nominal | ton_free | 3.20 | 8.17 | 0.46 |
| Si-ANPC | 460 | 184 | +0.95 | ripple-aware law | T4 | no us term | ton_clip | 3.18 | 4.13 | 0.45 |
| Si-ANPC | 460 | 184 | +0.95 | ripple-aware law | T4 | no us term | ton_free | 3.18 | 4.13 | 0.60 |
| Si-ANPC | 460 | 230 | +0.95 | baseline | T4 | nominal | ton_clip | 3.25 | 5.80 | 0.83 |
| Si-ANPC | 460 | 230 | +0.95 | baseline | T4 | nominal | ton_free | 3.25 | 5.80 | 1.20 |
| Si-ANPC | 460 | 230 | +0.95 | baseline | T4 | no us term | ton_clip | 3.18 | 3.48 | 0.83 |
| Si-ANPC | 460 | 230 | +0.95 | baseline | T4 | no us term | ton_free | 3.18 | 3.48 | 1.23 |
| Si-ANPC | 460 | 230 | +0.95 | mean-temperature law | T4 | nominal | ton_clip | 2.76 | 4.89 | 0.74 |
| Si-ANPC | 460 | 230 | +0.95 | mean-temperature law | T4 | nominal | ton_free | 2.76 | 4.89 | 1.15 |
| Si-ANPC | 460 | 230 | +0.95 | mean-temperature law | T4 | no us term | ton_clip | 2.69 | 3.22 | 0.71 |
| Si-ANPC | 460 | 230 | +0.95 | mean-temperature law | T4 | no us term | ton_free | 2.69 | 3.22 | 1.15 |
| Si-ANPC | 460 | 230 | +0.95 | ripple-aware law | T4 | nominal | ton_clip | 2.71 | 6.90 | 0.24 |
| Si-ANPC | 460 | 230 | +0.95 | ripple-aware law | T4 | nominal | ton_free | 2.71 | 6.90 | 0.50 |
| Si-ANPC | 460 | 230 | +0.95 | ripple-aware law | T4 | no us term | ton_clip | 2.65 | 3.07 | 0.77 |
| Si-ANPC | 460 | 230 | +0.95 | ripple-aware law | T4 | no us term | ton_free | 2.65 | 3.07 | 1.04 |
| Si-ANPC | 380 | 19 | -0.95 | baseline | D2 | nominal | ton_clip | 18.26 | 18.26 | 0.98 |
| Si-ANPC | 380 | 19 | -0.95 | baseline | D2 | nominal | ton_free | 18.26 | 18.26 | 1.17 |
| Si-ANPC | 380 | 19 | -0.95 | baseline | D2 | no us term | ton_clip | 18.35 | 18.34 | 0.98 |
| Si-ANPC | 380 | 19 | -0.95 | baseline | D2 | no us term | ton_free | 18.35 | 18.34 | 1.18 |
| Si-ANPC | 380 | 19 | -0.95 | mean-temperature law | D2 | nominal | ton_clip | 8.20 | 8.60 | 0.92 |
| Si-ANPC | 380 | 19 | -0.95 | mean-temperature law | D2 | nominal | ton_free | 8.20 | 8.60 | 1.15 |
| Si-ANPC | 380 | 19 | -0.95 | mean-temperature law | D2 | no us term | ton_clip | 8.22 | 8.37 | 0.92 |
| Si-ANPC | 380 | 19 | -0.95 | mean-temperature law | D2 | no us term | ton_free | 8.22 | 8.37 | 1.21 |
| Si-ANPC | 380 | 19 | -0.95 | ripple-aware law | D2 | nominal | ton_clip | 6.66 | 8.92 | 0.86 |
| Si-ANPC | 380 | 19 | -0.95 | ripple-aware law | D2 | nominal | ton_free | 6.66 | 8.92 | 1.10 |
| Si-ANPC | 380 | 19 | -0.95 | ripple-aware law | D2 | no us term | ton_clip | 6.69 | 8.56 | 0.80 |
| Si-ANPC | 380 | 19 | -0.95 | ripple-aware law | D2 | no us term | ton_free | 6.69 | 8.56 | 1.16 |
| Si-ANPC | 380 | 46 | -0.95 | baseline | D2 | nominal | ton_clip | 10.50 | 10.49 | 0.97 |
| Si-ANPC | 380 | 46 | -0.95 | baseline | D2 | nominal | ton_free | 10.50 | 10.49 | 1.40 |
| Si-ANPC | 380 | 46 | -0.95 | baseline | D2 | no us term | ton_clip | 10.61 | 10.60 | 0.97 |
| Si-ANPC | 380 | 46 | -0.95 | baseline | D2 | no us term | ton_free | 10.61 | 10.60 | 1.40 |
| Si-ANPC | 380 | 46 | -0.95 | mean-temperature law | D6 | nominal | ton_clip | 6.39 | 9.00 | 0.56 |
| Si-ANPC | 380 | 46 | -0.95 | mean-temperature law | D6 | nominal | ton_free | 6.39 | 9.00 | 0.86 |
| Si-ANPC | 380 | 46 | -0.95 | mean-temperature law | D6 | no us term | ton_clip | 6.42 | 8.95 | 0.49 |
| Si-ANPC | 380 | 46 | -0.95 | mean-temperature law | D6 | no us term | ton_free | 6.42 | 8.95 | 0.81 |
| Si-ANPC | 380 | 46 | -0.95 | ripple-aware law | D2 | nominal | ton_clip | 4.69 | 7.11 | 0.68 |
| Si-ANPC | 380 | 46 | -0.95 | ripple-aware law | D2 | nominal | ton_free | 4.69 | 7.11 | 1.12 |
| Si-ANPC | 380 | 46 | -0.95 | ripple-aware law | D2 | no us term | ton_clip | 4.73 | 6.88 | 0.57 |
| Si-ANPC | 380 | 46 | -0.95 | ripple-aware law | D2 | no us term | ton_free | 4.73 | 6.88 | 1.04 |
| Si-ANPC | 370 | 92 | -0.95 | baseline | D2 | nominal | ton_clip | 6.95 | 6.89 | 0.98 |
| Si-ANPC | 370 | 92 | -0.95 | baseline | D2 | nominal | ton_free | 6.95 | 6.89 | 1.35 |
| Si-ANPC | 370 | 92 | -0.95 | baseline | D2 | no us term | ton_clip | 7.01 | 6.96 | 0.98 |
| Si-ANPC | 370 | 92 | -0.95 | baseline | D2 | no us term | ton_free | 7.01 | 6.96 | 1.36 |
| Si-ANPC | 370 | 92 | -0.95 | mean-temperature law | D2 | nominal | ton_clip | 5.50 | 5.95 | 0.81 |
| Si-ANPC | 370 | 92 | -0.95 | mean-temperature law | D2 | nominal | ton_free | 5.50 | 5.95 | 0.96 |
| Si-ANPC | 370 | 92 | -0.95 | mean-temperature law | D2 | no us term | ton_clip | 5.58 | 6.03 | 0.72 |
| Si-ANPC | 370 | 92 | -0.95 | mean-temperature law | D2 | no us term | ton_free | 5.58 | 6.03 | 1.16 |
| Si-ANPC | 370 | 92 | -0.95 | ripple-aware law | D2 | nominal | ton_clip | 4.91 | 7.03 | 0.75 |
| Si-ANPC | 370 | 92 | -0.95 | ripple-aware law | D2 | nominal | ton_free | 4.91 | 7.03 | 0.86 |
| Si-ANPC | 370 | 92 | -0.95 | ripple-aware law | D2 | no us term | ton_clip | 4.95 | 5.72 | 0.68 |
| Si-ANPC | 370 | 92 | -0.95 | ripple-aware law | D2 | no us term | ton_free | 4.95 | 5.72 | 1.15 |
| Si-ANPC | 400 | 159 | -0.95 | baseline | D2 | nominal | ton_clip | 5.55 | 5.55 | 0.95 |
| Si-ANPC | 400 | 159 | -0.95 | baseline | D2 | nominal | ton_free | 5.55 | 5.55 | 1.47 |
| Si-ANPC | 400 | 159 | -0.95 | baseline | D2 | no us term | ton_clip | 5.53 | 5.53 | 0.96 |
| Si-ANPC | 400 | 159 | -0.95 | baseline | D2 | no us term | ton_free | 5.53 | 5.53 | 1.48 |
| Si-ANPC | 400 | 159 | -0.95 | mean-temperature law | D1 | nominal | ton_clip | 5.10 | 8.04 | 0.60 |
| Si-ANPC | 400 | 159 | -0.95 | mean-temperature law | D1 | nominal | ton_free | 5.10 | 8.04 | 0.83 |
| Si-ANPC | 400 | 159 | -0.95 | mean-temperature law | D1 | no us term | ton_clip | 5.08 | 5.91 | 0.71 |
| Si-ANPC | 400 | 159 | -0.95 | mean-temperature law | D1 | no us term | ton_free | 5.08 | 5.91 | 0.96 |
| Si-ANPC | 400 | 159 | -0.95 | ripple-aware law | D1 | nominal | ton_clip | 5.09 | 8.04 | 0.66 |
| Si-ANPC | 400 | 159 | -0.95 | ripple-aware law | D1 | nominal | ton_free | 5.09 | 8.04 | 0.90 |
| Si-ANPC | 400 | 159 | -0.95 | ripple-aware law | D1 | no us term | ton_clip | 5.07 | 5.90 | 0.73 |
| Si-ANPC | 400 | 159 | -0.95 | ripple-aware law | D1 | no us term | ton_free | 5.07 | 5.90 | 0.99 |
| Si-ANPC | 400 | 216 | -0.95 | baseline | D2 | nominal | ton_clip | 4.45 | 4.39 | 1.01 |
| Si-ANPC | 400 | 216 | -0.95 | baseline | D2 | nominal | ton_free | 4.45 | 4.39 | 1.32 |
| Si-ANPC | 400 | 216 | -0.95 | baseline | D2 | no us term | ton_clip | 4.35 | 4.30 | 1.02 |
| Si-ANPC | 400 | 216 | -0.95 | baseline | D2 | no us term | ton_free | 4.35 | 4.30 | 1.36 |
| Si-ANPC | 400 | 216 | -0.95 | mean-temperature law | D4 | nominal | ton_clip | 4.13 | 6.46 | 0.63 |
| Si-ANPC | 400 | 216 | -0.95 | mean-temperature law | D4 | nominal | ton_free | 4.13 | 6.46 | 0.80 |
| Si-ANPC | 400 | 216 | -0.95 | mean-temperature law | D4 | no us term | ton_clip | 4.03 | 4.60 | 0.74 |
| Si-ANPC | 400 | 216 | -0.95 | mean-temperature law | D4 | no us term | ton_free | 4.03 | 4.60 | 0.93 |
| Si-ANPC | 400 | 216 | -0.95 | ripple-aware law | D2 | nominal | ton_clip | 4.05 | 4.41 | 0.90 |
| Si-ANPC | 400 | 216 | -0.95 | ripple-aware law | D2 | nominal | ton_free | 4.05 | 4.41 | 1.11 |
| Si-ANPC | 400 | 216 | -0.95 | ripple-aware law | D3 | no us term | ton_clip | 3.98 | 4.21 | 0.81 |
| Si-ANPC | 400 | 216 | -0.95 | ripple-aware law | D3 | no us term | ton_free | 3.98 | 4.21 | 1.10 |
| Si-ANPC | 400 | 250 | -0.95 | baseline | D2 | nominal | ton_clip | 3.99 | 3.99 | 0.97 |
| Si-ANPC | 400 | 250 | -0.95 | baseline | D2 | nominal | ton_free | 3.99 | 3.99 | 1.07 |
| Si-ANPC | 400 | 250 | -0.95 | baseline | D2 | no us term | ton_clip | 3.85 | 3.85 | 0.97 |
| Si-ANPC | 400 | 250 | -0.95 | baseline | D2 | no us term | ton_free | 3.85 | 3.85 | 1.10 |
| Si-ANPC | 400 | 250 | -0.95 | mean-temperature law | D4 | nominal | ton_clip | 3.70 | 6.26 | 1.00 |
| Si-ANPC | 400 | 250 | -0.95 | mean-temperature law | D4 | nominal | ton_free | 3.70 | 6.26 | 1.39 |
| Si-ANPC | 400 | 250 | -0.95 | mean-temperature law | D4 | no us term | ton_clip | 3.57 | 4.20 | 0.99 |
| Si-ANPC | 400 | 250 | -0.95 | mean-temperature law | D4 | no us term | ton_free | 3.57 | 4.20 | 1.38 |
| Si-ANPC | 400 | 250 | -0.95 | ripple-aware law | D2 | nominal | ton_clip | 3.63 | 5.20 | 0.39 |
| Si-ANPC | 400 | 250 | -0.95 | ripple-aware law | D2 | nominal | ton_free | 3.63 | 5.20 | 0.60 |
| Si-ANPC | 400 | 250 | -0.95 | ripple-aware law | D3 | no us term | ton_clip | 3.53 | 3.86 | 0.87 |
| Si-ANPC | 400 | 250 | -0.95 | ripple-aware law | D3 | no us term | ton_free | 3.53 | 3.86 | 1.28 |
| SiC-ANPC | 460 | 19 | +0.95 | baseline | S3 | nominal | ton_clip | 12.51 | 12.53 | 1.00 |
| SiC-ANPC | 460 | 19 | +0.95 | baseline | S3 | nominal | ton_free | 12.51 | 12.53 | 1.43 |
| SiC-ANPC | 460 | 19 | +0.95 | baseline | S3 | no us term | ton_clip | 12.55 | 12.57 | 1.01 |
| SiC-ANPC | 460 | 19 | +0.95 | baseline | S3 | no us term | ton_free | 12.55 | 12.57 | 1.43 |
| SiC-ANPC | 460 | 19 | +0.95 | mean-temperature law | S3 | nominal | ton_clip | 3.74 | 4.34 | 1.01 |
| SiC-ANPC | 460 | 19 | +0.95 | mean-temperature law | S3 | nominal | ton_free | 3.74 | 4.34 | 1.45 |
| SiC-ANPC | 460 | 19 | +0.95 | mean-temperature law | S3 | no us term | ton_clip | 3.76 | 4.03 | 1.00 |
| SiC-ANPC | 460 | 19 | +0.95 | mean-temperature law | S3 | no us term | ton_free | 3.76 | 4.03 | 1.44 |
| SiC-ANPC | 460 | 19 | +0.95 | ripple-aware law | S1 | nominal | ton_clip | 2.49 | 5.02 | 2.16 |
| SiC-ANPC | 460 | 19 | +0.95 | ripple-aware law | S1 | nominal | ton_free | 2.49 | 5.02 | 1.66 |
| SiC-ANPC | 460 | 19 | +0.95 | ripple-aware law | S1 | no us term | ton_clip | 2.50 | 3.51 | 1.59 |
| SiC-ANPC | 460 | 19 | +0.95 | ripple-aware law | S1 | no us term | ton_free | 2.50 | 3.51 | 1.71 |
| SiC-ANPC | 460 | 46 | +0.95 | baseline | S3 | nominal | ton_clip | 7.57 | 7.55 | 1.00 |
| SiC-ANPC | 460 | 46 | +0.95 | baseline | S3 | nominal | ton_free | 7.57 | 7.55 | 1.39 |
| SiC-ANPC | 460 | 46 | +0.95 | baseline | S3 | no us term | ton_clip | 7.64 | 7.62 | 1.00 |
| SiC-ANPC | 460 | 46 | +0.95 | baseline | S3 | no us term | ton_free | 7.64 | 7.62 | 1.39 |
| SiC-ANPC | 460 | 46 | +0.95 | mean-temperature law | S3 | nominal | ton_clip | 3.23 | 4.52 | 0.57 |
| SiC-ANPC | 460 | 46 | +0.95 | mean-temperature law | S3 | nominal | ton_free | 3.23 | 4.52 | 0.96 |
| SiC-ANPC | 460 | 46 | +0.95 | mean-temperature law | S3 | no us term | ton_clip | 3.27 | 4.38 | 0.56 |
| SiC-ANPC | 460 | 46 | +0.95 | mean-temperature law | S3 | no us term | ton_free | 3.27 | 4.38 | 0.92 |
| SiC-ANPC | 460 | 46 | +0.95 | ripple-aware law | S3 | nominal | ton_clip | 2.57 | 6.20 | 0.80 |
| SiC-ANPC | 460 | 46 | +0.95 | ripple-aware law | S3 | nominal | ton_free | 2.57 | 6.20 | 1.09 |
| SiC-ANPC | 460 | 46 | +0.95 | ripple-aware law | S3 | no us term | ton_clip | 2.55 | 4.92 | 0.69 |
| SiC-ANPC | 460 | 46 | +0.95 | ripple-aware law | S3 | no us term | ton_free | 2.55 | 4.92 | 1.00 |
| SiC-ANPC | 460 | 92 | +0.95 | baseline | S3 | nominal | ton_clip | 5.23 | 5.24 | 0.98 |
| SiC-ANPC | 460 | 92 | +0.95 | baseline | S3 | nominal | ton_free | 5.23 | 5.24 | 1.38 |
| SiC-ANPC | 460 | 92 | +0.95 | baseline | S3 | no us term | ton_clip | 5.32 | 5.33 | 0.98 |
| SiC-ANPC | 460 | 92 | +0.95 | baseline | S3 | no us term | ton_free | 5.32 | 5.33 | 1.37 |
| SiC-ANPC | 460 | 92 | +0.95 | mean-temperature law | S2 | nominal | ton_clip | 3.70 | 4.68 | 0.68 |
| SiC-ANPC | 460 | 92 | +0.95 | mean-temperature law | S2 | nominal | ton_free | 3.70 | 4.68 | 1.07 |
| SiC-ANPC | 460 | 92 | +0.95 | mean-temperature law | S2 | no us term | ton_clip | 3.75 | 4.72 | 0.62 |
| SiC-ANPC | 460 | 92 | +0.95 | mean-temperature law | S2 | no us term | ton_free | 3.75 | 4.72 | 1.00 |
| SiC-ANPC | 460 | 92 | +0.95 | ripple-aware law | S3 | nominal | ton_clip | 3.37 | 5.90 | 0.91 |
| SiC-ANPC | 460 | 92 | +0.95 | ripple-aware law | S3 | nominal | ton_free | 3.37 | 5.90 | 1.56 |
| SiC-ANPC | 460 | 92 | +0.95 | ripple-aware law | S3 | no us term | ton_clip | 3.42 | 4.52 | 0.81 |
| SiC-ANPC | 460 | 92 | +0.95 | ripple-aware law | S3 | no us term | ton_free | 3.42 | 4.52 | 1.57 |
| SiC-ANPC | 460 | 135 | +0.95 | baseline | S4 | nominal | ton_clip | 4.56 | 5.87 | 0.96 |
| SiC-ANPC | 460 | 135 | +0.95 | baseline | S4 | nominal | ton_free | 4.56 | 5.87 | 1.36 |
| SiC-ANPC | 460 | 135 | +0.95 | baseline | S4 | no us term | ton_clip | 4.65 | 4.84 | 0.91 |
| SiC-ANPC | 460 | 135 | +0.95 | baseline | S4 | no us term | ton_free | 4.65 | 4.84 | 1.28 |
| SiC-ANPC | 460 | 135 | +0.95 | mean-temperature law | S4 | nominal | ton_clip | 4.27 | 6.77 | 0.73 |
| SiC-ANPC | 460 | 135 | +0.95 | mean-temperature law | S4 | nominal | ton_free | 4.27 | 6.77 | 1.13 |
| SiC-ANPC | 460 | 135 | +0.95 | mean-temperature law | S4 | no us term | ton_clip | 4.34 | 4.79 | 0.86 |
| SiC-ANPC | 460 | 135 | +0.95 | mean-temperature law | S4 | no us term | ton_free | 4.34 | 4.79 | 1.09 |
| SiC-ANPC | 460 | 135 | +0.95 | ripple-aware law | S4 | nominal | ton_clip | 4.10 | 6.70 | 0.68 |
| SiC-ANPC | 460 | 135 | +0.95 | ripple-aware law | S4 | nominal | ton_free | 4.10 | 6.70 | 0.98 |
| SiC-ANPC | 460 | 135 | +0.95 | ripple-aware law | S4 | no us term | ton_clip | 4.16 | 4.79 | 0.76 |
| SiC-ANPC | 460 | 135 | +0.95 | ripple-aware law | S4 | no us term | ton_free | 4.16 | 4.79 | 0.92 |
| SiC-ANPC | 460 | 184 | +0.95 | baseline | S4 | nominal | ton_clip | 3.96 | 5.20 | 0.95 |
| SiC-ANPC | 460 | 184 | +0.95 | baseline | S4 | nominal | ton_free | 3.96 | 5.20 | 1.27 |
| SiC-ANPC | 460 | 184 | +0.95 | baseline | S4 | no us term | ton_clip | 4.02 | 4.17 | 0.95 |
| SiC-ANPC | 460 | 184 | +0.95 | baseline | S4 | no us term | ton_free | 4.02 | 4.17 | 1.32 |
| SiC-ANPC | 460 | 184 | +0.95 | mean-temperature law | S4 | nominal | ton_clip | 3.68 | 6.35 | 0.78 |
| SiC-ANPC | 460 | 184 | +0.95 | mean-temperature law | S4 | nominal | ton_free | 3.68 | 6.35 | 1.21 |
| SiC-ANPC | 460 | 184 | +0.95 | mean-temperature law | S4 | no us term | ton_clip | 3.74 | 4.34 | 0.82 |
| SiC-ANPC | 460 | 184 | +0.95 | mean-temperature law | S4 | no us term | ton_free | 3.74 | 4.34 | 1.26 |
| SiC-ANPC | 460 | 184 | +0.95 | ripple-aware law | S4 | nominal | ton_clip | 3.57 | 6.37 | 0.72 |
| SiC-ANPC | 460 | 184 | +0.95 | ripple-aware law | S4 | nominal | ton_free | 3.57 | 6.37 | 1.05 |
| SiC-ANPC | 460 | 184 | +0.95 | ripple-aware law | S4 | no us term | ton_clip | 3.63 | 4.33 | 0.77 |
| SiC-ANPC | 460 | 184 | +0.95 | ripple-aware law | S4 | no us term | ton_free | 3.63 | 4.33 | 1.22 |
| SiC-ANPC | 460 | 230 | +0.95 | baseline | S4 | nominal | ton_clip | 3.57 | 4.83 | 0.90 |
| SiC-ANPC | 460 | 230 | +0.95 | baseline | S4 | nominal | ton_free | 3.57 | 4.83 | 1.25 |
| SiC-ANPC | 460 | 230 | +0.95 | baseline | S4 | no us term | ton_clip | 3.61 | 3.77 | 0.91 |
| SiC-ANPC | 460 | 230 | +0.95 | baseline | S4 | no us term | ton_free | 3.61 | 3.77 | 1.34 |
| SiC-ANPC | 460 | 230 | +0.95 | mean-temperature law | S4 | nominal | ton_clip | 3.32 | 6.01 | 0.69 |
| SiC-ANPC | 460 | 230 | +0.95 | mean-temperature law | S4 | nominal | ton_free | 3.32 | 6.01 | 0.84 |
| SiC-ANPC | 460 | 230 | +0.95 | mean-temperature law | S4 | no us term | ton_clip | 3.36 | 3.90 | 0.80 |
| SiC-ANPC | 460 | 230 | +0.95 | mean-temperature law | S4 | no us term | ton_free | 3.36 | 3.90 | 0.96 |
| SiC-ANPC | 460 | 230 | +0.95 | ripple-aware law | S3 | nominal | ton_clip | 3.22 | 4.47 | 0.59 |
| SiC-ANPC | 460 | 230 | +0.95 | ripple-aware law | S3 | nominal | ton_free | 3.22 | 4.47 | 0.95 |
| SiC-ANPC | 460 | 230 | +0.95 | ripple-aware law | S4 | no us term | ton_clip | 3.25 | 3.88 | 0.72 |
| SiC-ANPC | 460 | 230 | +0.95 | ripple-aware law | S4 | no us term | ton_free | 3.25 | 3.88 | 1.13 |
| SiC-ANPC | 380 | 19 | -0.95 | baseline | S5 | nominal | ton_clip | 8.39 | 9.55 | 1.00 |
| SiC-ANPC | 380 | 19 | -0.95 | baseline | S5 | nominal | ton_free | 8.39 | 9.55 | 1.13 |
| SiC-ANPC | 380 | 19 | -0.95 | baseline | S5 | no us term | ton_clip | 8.40 | 8.61 | 0.97 |
| SiC-ANPC | 380 | 19 | -0.95 | baseline | S5 | no us term | ton_free | 8.40 | 8.61 | 1.13 |
| SiC-ANPC | 380 | 19 | -0.95 | mean-temperature law | S2 | nominal | ton_clip | 3.43 | 4.07 | 1.19 |
| SiC-ANPC | 380 | 19 | -0.95 | mean-temperature law | S2 | nominal | ton_free | 3.43 | 4.07 | 1.55 |
| SiC-ANPC | 380 | 19 | -0.95 | mean-temperature law | S2 | no us term | ton_clip | 3.43 | 3.77 | 0.80 |
| SiC-ANPC | 380 | 19 | -0.95 | mean-temperature law | S2 | no us term | ton_free | 3.43 | 3.77 | 1.28 |
| SiC-ANPC | 380 | 19 | -0.95 | ripple-aware law | S2 | nominal | ton_clip | 1.55 | 3.72 | 0.97 |
| SiC-ANPC | 380 | 19 | -0.95 | ripple-aware law | S2 | nominal | ton_free | 1.55 | 3.72 | 1.13 |
| SiC-ANPC | 380 | 19 | -0.95 | ripple-aware law | S2 | no us term | ton_clip | 1.55 | 2.71 | 1.21 |
| SiC-ANPC | 380 | 19 | -0.95 | ripple-aware law | S2 | no us term | ton_free | 1.55 | 2.71 | 1.35 |
| SiC-ANPC | 380 | 46 | -0.95 | baseline | S2 | nominal | ton_clip | 4.47 | 4.48 | 0.96 |
| SiC-ANPC | 380 | 46 | -0.95 | baseline | S2 | nominal | ton_free | 4.47 | 4.48 | 1.35 |
| SiC-ANPC | 380 | 46 | -0.95 | baseline | S2 | no us term | ton_clip | 4.50 | 4.51 | 0.96 |
| SiC-ANPC | 380 | 46 | -0.95 | baseline | S2 | no us term | ton_free | 4.50 | 4.51 | 1.35 |
| SiC-ANPC | 380 | 46 | -0.95 | mean-temperature law | S2 | nominal | ton_clip | 1.83 | 2.49 | 0.52 |
| SiC-ANPC | 380 | 46 | -0.95 | mean-temperature law | S2 | nominal | ton_free | 1.83 | 2.49 | 0.94 |
| SiC-ANPC | 380 | 46 | -0.95 | mean-temperature law | S2 | no us term | ton_clip | 1.84 | 2.38 | 0.55 |
| SiC-ANPC | 380 | 46 | -0.95 | mean-temperature law | S2 | no us term | ton_free | 1.84 | 2.38 | 0.99 |
| SiC-ANPC | 380 | 46 | -0.95 | ripple-aware law | S2 | nominal | ton_clip | 1.44 | 4.24 | 0.61 |
| SiC-ANPC | 380 | 46 | -0.95 | ripple-aware law | S2 | nominal | ton_free | 1.44 | 4.24 | 0.96 |
| SiC-ANPC | 380 | 46 | -0.95 | ripple-aware law | S2 | no us term | ton_clip | 1.43 | 2.64 | 0.94 |
| SiC-ANPC | 380 | 46 | -0.95 | ripple-aware law | S2 | no us term | ton_free | 1.43 | 2.64 | 1.35 |
| SiC-ANPC | 370 | 92 | -0.95 | baseline | S2 | nominal | ton_clip | 2.92 | 2.91 | 0.98 |
| SiC-ANPC | 370 | 92 | -0.95 | baseline | S2 | nominal | ton_free | 2.92 | 2.91 | 1.15 |
| SiC-ANPC | 370 | 92 | -0.95 | baseline | S2 | no us term | ton_clip | 2.96 | 2.94 | 0.98 |
| SiC-ANPC | 370 | 92 | -0.95 | baseline | S2 | no us term | ton_free | 2.96 | 2.94 | 1.16 |
| SiC-ANPC | 370 | 92 | -0.95 | mean-temperature law | S3 | nominal | ton_clip | 2.18 | 3.23 | 0.65 |
| SiC-ANPC | 370 | 92 | -0.95 | mean-temperature law | S3 | nominal | ton_free | 2.18 | 3.23 | 1.08 |
| SiC-ANPC | 370 | 92 | -0.95 | mean-temperature law | S3 | no us term | ton_clip | 2.22 | 2.64 | 0.67 |
| SiC-ANPC | 370 | 92 | -0.95 | mean-temperature law | S3 | no us term | ton_free | 2.22 | 2.64 | 1.13 |
| SiC-ANPC | 370 | 92 | -0.95 | ripple-aware law | S1 | nominal | ton_clip | 1.85 | 3.05 | 0.57 |
| SiC-ANPC | 370 | 92 | -0.95 | ripple-aware law | S1 | nominal | ton_free | 1.85 | 3.05 | 0.88 |
| SiC-ANPC | 370 | 92 | -0.95 | ripple-aware law | S1 | no us term | ton_clip | 1.82 | 2.63 | 0.65 |
| SiC-ANPC | 370 | 92 | -0.95 | ripple-aware law | S1 | no us term | ton_free | 1.82 | 2.63 | 0.75 |
| SiC-ANPC | 400 | 159 | -0.95 | baseline | S2 | nominal | ton_clip | 2.69 | 2.70 | 0.94 |
| SiC-ANPC | 400 | 159 | -0.95 | baseline | S2 | nominal | ton_free | 2.69 | 2.70 | 1.35 |
| SiC-ANPC | 400 | 159 | -0.95 | baseline | S2 | no us term | ton_clip | 2.73 | 2.73 | 0.95 |
| SiC-ANPC | 400 | 159 | -0.95 | baseline | S2 | no us term | ton_free | 2.73 | 2.73 | 1.36 |
| SiC-ANPC | 400 | 159 | -0.95 | mean-temperature law | S3 | nominal | ton_clip | 2.43 | 3.48 | 0.63 |
| SiC-ANPC | 400 | 159 | -0.95 | mean-temperature law | S3 | nominal | ton_free | 2.43 | 3.48 | 0.86 |
| SiC-ANPC | 400 | 159 | -0.95 | mean-temperature law | S3 | no us term | ton_clip | 2.47 | 2.75 | 0.77 |
| SiC-ANPC | 400 | 159 | -0.95 | mean-temperature law | S3 | no us term | ton_free | 2.47 | 2.75 | 0.98 |
| SiC-ANPC | 400 | 159 | -0.95 | ripple-aware law | S1 | nominal | ton_clip | 2.32 | 3.08 | 0.80 |
| SiC-ANPC | 400 | 159 | -0.95 | ripple-aware law | S1 | nominal | ton_free | 2.32 | 3.08 | 1.14 |
| SiC-ANPC | 400 | 159 | -0.95 | ripple-aware law | S1 | no us term | ton_clip | 2.34 | 2.70 | 0.84 |
| SiC-ANPC | 400 | 159 | -0.95 | ripple-aware law | S1 | no us term | ton_free | 2.34 | 2.70 | 0.97 |
| SiC-ANPC | 400 | 216 | -0.95 | baseline | S2 | nominal | ton_clip | 2.33 | 2.33 | 0.98 |
| SiC-ANPC | 400 | 216 | -0.95 | baseline | S2 | nominal | ton_free | 2.33 | 2.33 | 1.17 |
| SiC-ANPC | 400 | 216 | -0.95 | baseline | S2 | no us term | ton_clip | 2.36 | 2.35 | 0.98 |
| SiC-ANPC | 400 | 216 | -0.95 | baseline | S2 | no us term | ton_free | 2.36 | 2.35 | 1.19 |
| SiC-ANPC | 400 | 216 | -0.95 | mean-temperature law | S3 | nominal | ton_clip | 2.09 | 2.27 | 0.87 |
| SiC-ANPC | 400 | 216 | -0.95 | mean-temperature law | S3 | nominal | ton_free | 2.09 | 2.27 | 1.10 |
| SiC-ANPC | 400 | 216 | -0.95 | mean-temperature law | S3 | no us term | ton_clip | 2.12 | 2.31 | 0.82 |
| SiC-ANPC | 400 | 216 | -0.95 | mean-temperature law | S3 | no us term | ton_free | 2.12 | 2.31 | 1.06 |
| SiC-ANPC | 400 | 216 | -0.95 | ripple-aware law | S1 | nominal | ton_clip | 1.98 | 2.76 | 0.64 |
| SiC-ANPC | 400 | 216 | -0.95 | ripple-aware law | S1 | nominal | ton_free | 1.98 | 2.76 | 0.92 |
| SiC-ANPC | 400 | 216 | -0.95 | ripple-aware law | S1 | no us term | ton_clip | 2.00 | 2.38 | 0.75 |
| SiC-ANPC | 400 | 216 | -0.95 | ripple-aware law | S1 | no us term | ton_free | 2.00 | 2.38 | 1.02 |
| SiC-ANPC | 400 | 250 | -0.95 | baseline | S2 | nominal | ton_clip | 2.18 | 2.18 | 0.97 |
| SiC-ANPC | 400 | 250 | -0.95 | baseline | S2 | nominal | ton_free | 2.18 | 2.18 | 1.01 |
| SiC-ANPC | 400 | 250 | -0.95 | baseline | S2 | no us term | ton_clip | 2.19 | 2.19 | 0.97 |
| SiC-ANPC | 400 | 250 | -0.95 | baseline | S2 | no us term | ton_free | 2.19 | 2.19 | 1.03 |
| SiC-ANPC | 400 | 250 | -0.95 | mean-temperature law | S3 | nominal | ton_clip | 1.95 | 2.11 | 0.95 |
| SiC-ANPC | 400 | 250 | -0.95 | mean-temperature law | S3 | nominal | ton_free | 1.95 | 2.11 | 1.25 |
| SiC-ANPC | 400 | 250 | -0.95 | mean-temperature law | S3 | no us term | ton_clip | 1.98 | 2.14 | 0.95 |
| SiC-ANPC | 400 | 250 | -0.95 | mean-temperature law | S3 | no us term | ton_free | 1.98 | 2.14 | 1.25 |
| SiC-ANPC | 400 | 250 | -0.95 | ripple-aware law | S1 | nominal | ton_clip | 1.85 | 2.61 | 0.80 |
| SiC-ANPC | 400 | 250 | -0.95 | ripple-aware law | S1 | nominal | ton_free | 1.85 | 2.61 | 0.95 |
| SiC-ANPC | 400 | 250 | -0.95 | ripple-aware law | S1 | no us term | ton_clip | 1.87 | 2.23 | 0.88 |
| SiC-ANPC | 400 | 250 | -0.95 | ripple-aware law | S1 | no us term | ton_free | 1.87 | 2.23 | 1.04 |
