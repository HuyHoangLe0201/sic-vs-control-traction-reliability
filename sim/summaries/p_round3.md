# Round-3 checks (external comments MC1, MC3, MC4)

## MC1: ripple at temperature T relative to the frozen ripple at T_w (chips with r(T_w) > 0.5 K)

| config | point | policies | min ratio r(T)/r(T_w) over T in {T_b, 125, 150, random} | share of cases < 1 | min ratio of pair bounds rho_T / rho_Tw | spread of relative tempco over the period (max chip) |
|---|---|---|---|---|---|---|
| Si-NPC | start-up 5 Hz | 80 | 0.953 | 0.534 | 0.976 | 1.56e-3 /K |
| Si-NPC | 10 Hz | 80 | 0.978 | 0.151 | 0.995 | 1.80e-3 /K |
| Si-NPC | 20 Hz | 80 | 0.967 | 0.097 | 0.996 | 1.82e-3 /K |
| Si-NPC | 30 Hz | 80 | 0.960 | 0.155 | 0.998 | 1.82e-3 /K |
| Si-NPC | 60 Hz | 80 | 0.932 | 0.209 | 0.998 | 1.82e-3 /K |
| Si-NPC | 150 Hz | 80 | 0.976 | 0.250 | 0.978 | 1.82e-3 /K |
| Si-NPC | brake 20 Hz | 80 | 0.958 | 0.534 | 0.980 | 1.21e-3 /K |
| Si-ANPC | start-up 5 Hz | 80 | 0.936 | 0.464 | 1.017 | 1.56e-3 /K |
| Si-ANPC | 10 Hz | 80 | 0.962 | 0.240 | 1.029 | 1.80e-3 /K |
| Si-ANPC | 20 Hz | 80 | 0.963 | 0.231 | 1.031 | 1.82e-3 /K |
| Si-ANPC | 30 Hz | 80 | 0.956 | 0.243 | 1.034 | 1.82e-3 /K |
| Si-ANPC | 60 Hz | 80 | 0.932 | 0.299 | 1.041 | 1.82e-3 /K |
| Si-ANPC | 150 Hz | 80 | 0.916 | 0.338 | 1.051 | 1.82e-3 /K |
| Si-ANPC | brake 20 Hz | 80 | 0.949 | 0.469 | 0.980 | 1.21e-3 /K |
| SiC-ANPC | start-up 5 Hz | 80 | 1.001 | 0.000 | 1.047 | 5.33e-3 /K |
| SiC-ANPC | 10 Hz | 80 | 1.030 | 0.000 | 1.041 | 5.19e-3 /K |
| SiC-ANPC | 20 Hz | 80 | 1.032 | 0.000 | 1.046 | 5.19e-3 /K |
| SiC-ANPC | 30 Hz | 80 | 1.017 | 0.000 | 1.052 | 5.19e-3 /K |
| SiC-ANPC | 60 Hz | 80 | 1.024 | 0.000 | 1.068 | 5.11e-3 /K |
| SiC-ANPC | 150 Hz | 80 | 1.019 | 0.000 | 1.095 | 4.96e-3 /K |
| SiC-ANPC | brake 20 Hz | 80 | 1.019 | 0.000 | 1.035 | 5.31e-3 /K |

## MC3: asymmetry of the ripple waveform (worst chip per policy)

| config | point | policy | r (K) | min of periodic part (K) | -r/2 (K) | damage factor true/approx (T_min) |
|---|---|---|---|---|---|---|
| Si-NPC | start-up 5 Hz | base | 33.39 | -12.93 | -16.69 | 1.045 |
| Si-NPC | start-up 5 Hz | ha | 23.09 | -6.92 | -11.55 | 1.054 |
| Si-NPC | start-up 5 Hz | har | 12.53 | -4.19 | -6.27 | 1.027 |
| Si-NPC | 10 Hz | base | 34.03 | -14.05 | -17.02 | 1.033 |
| Si-NPC | 10 Hz | ha | 23.16 | -7.89 | -11.58 | 1.040 |
| Si-NPC | 10 Hz | har | 13.39 | -5.03 | -6.69 | 1.017 |
| Si-NPC | 20 Hz | base | 20.72 | -9.09 | -10.36 | 1.014 |
| Si-NPC | 20 Hz | ha | 14.60 | -5.57 | -7.30 | 1.018 |
| Si-NPC | 20 Hz | har | 9.20 | -3.70 | -4.60 | 1.011 |
| Si-NPC | 30 Hz | base | 14.51 | -6.42 | -7.25 | 1.009 |
| Si-NPC | 30 Hz | ha | 10.78 | -4.33 | -5.39 | 1.011 |
| Si-NPC | 30 Hz | har | 7.81 | -3.47 | -3.90 | 1.005 |
| Si-NPC | 60 Hz | base | 7.36 | -3.25 | -3.68 | 1.005 |
| Si-NPC | 60 Hz | ha | 7.79 | -3.03 | -3.90 | 1.010 |
| Si-NPC | 60 Hz | har | 6.32 | -2.97 | -3.16 | 1.002 |
| Si-NPC | 150 Hz | base | 4.43 | -1.86 | -2.22 | 1.004 |
| Si-NPC | 150 Hz | ha | 3.98 | -1.67 | -1.99 | 1.003 |
| Si-NPC | 150 Hz | har | 3.85 | -1.65 | -1.93 | 1.003 |
| Si-NPC | brake 20 Hz | base | 14.16 | -6.13 | -7.08 | 1.011 |
| Si-NPC | brake 20 Hz | ha | 9.79 | -3.59 | -4.90 | 1.015 |
| Si-NPC | brake 20 Hz | har | 6.33 | -2.67 | -3.17 | 1.005 |
| Si-ANPC | start-up 5 Hz | base | 33.44 | -12.80 | -16.72 | 1.047 |
| Si-ANPC | start-up 5 Hz | ha | 15.10 | -4.60 | -7.55 | 1.034 |
| Si-ANPC | start-up 5 Hz | har | 9.44 | -4.52 | -4.72 | 1.003 |
| Si-ANPC | 10 Hz | base | 34.11 | -13.90 | -17.06 | 1.035 |
| Si-ANPC | 10 Hz | ha | 12.54 | -4.76 | -6.27 | 1.016 |
| Si-ANPC | 10 Hz | har | 9.99 | -4.10 | -4.99 | 1.010 |
| Si-ANPC | 20 Hz | base | 20.81 | -9.01 | -10.41 | 1.015 |
| Si-ANPC | 20 Hz | ha | 7.83 | -3.29 | -3.91 | 1.006 |
| Si-ANPC | 20 Hz | har | 6.47 | -2.78 | -3.23 | 1.005 |
| Si-ANPC | 30 Hz | base | 14.58 | -6.35 | -7.29 | 1.010 |
| Si-ANPC | 30 Hz | ha | 5.79 | -2.48 | -2.89 | 1.004 |
| Si-ANPC | 30 Hz | har | 4.91 | -2.25 | -2.46 | 1.002 |
| Si-ANPC | 60 Hz | base | 7.41 | -3.21 | -3.71 | 1.006 |
| Si-ANPC | 60 Hz | ha | 3.93 | -1.57 | -1.97 | 1.005 |
| Si-ANPC | 60 Hz | har | 3.57 | -1.39 | -1.78 | 1.005 |
| Si-ANPC | 150 Hz | base | 4.43 | -1.86 | -2.22 | 1.004 |
| Si-ANPC | 150 Hz | ha | 3.70 | -1.55 | -1.85 | 1.003 |
| Si-ANPC | 150 Hz | har | 3.61 | -1.51 | -1.80 | 1.003 |
| Si-ANPC | brake 20 Hz | base | 16.94 | -7.40 | -8.47 | 1.012 |
| Si-ANPC | brake 20 Hz | ha | 7.72 | -3.51 | -3.86 | 1.004 |
| Si-ANPC | brake 20 Hz | har | 6.00 | -2.61 | -3.00 | 1.005 |
| SiC-ANPC | start-up 5 Hz | base | 11.85 | -3.80 | -5.92 | 1.028 |
| SiC-ANPC | start-up 5 Hz | ha | 3.24 | -1.23 | -1.62 | 1.005 |
| SiC-ANPC | start-up 5 Hz | har | 1.98 | -1.09 | -0.99 | 0.999 |
| SiC-ANPC | 10 Hz | base | 16.55 | -5.82 | -8.27 | 1.031 |
| SiC-ANPC | 10 Hz | ha | 3.90 | -1.80 | -1.95 | 1.002 |
| SiC-ANPC | 10 Hz | har | 2.74 | -1.44 | -1.37 | 0.999 |
| SiC-ANPC | 20 Hz | base | 12.10 | -4.50 | -6.05 | 1.019 |
| SiC-ANPC | 20 Hz | ha | 3.67 | -1.49 | -1.84 | 1.004 |
| SiC-ANPC | 20 Hz | har | 2.20 | -1.22 | -1.10 | 0.999 |
| SiC-ANPC | 30 Hz | base | 9.72 | -3.76 | -4.86 | 1.014 |
| SiC-ANPC | 30 Hz | ha | 3.56 | -1.44 | -1.78 | 1.004 |
| SiC-ANPC | 30 Hz | har | 2.18 | -1.25 | -1.09 | 0.998 |
| SiC-ANPC | 60 Hz | base | 6.72 | -2.67 | -3.36 | 1.008 |
| SiC-ANPC | 60 Hz | ha | 3.30 | -1.41 | -1.65 | 1.003 |
| SiC-ANPC | 60 Hz | har | 2.47 | -1.28 | -1.23 | 0.999 |
| SiC-ANPC | 150 Hz | base | 4.35 | -1.57 | -2.18 | 1.007 |
| SiC-ANPC | 150 Hz | ha | 4.04 | -1.45 | -2.02 | 1.007 |
| SiC-ANPC | 150 Hz | har | 3.80 | -1.37 | -1.90 | 1.006 |
| SiC-ANPC | brake 20 Hz | base | 7.86 | -3.09 | -3.93 | 1.011 |
| SiC-ANPC | brake 20 Hz | ha | 2.98 | -1.04 | -1.49 | 1.006 |
| SiC-ANPC | brake 20 Hz | har | 1.30 | -0.57 | -0.65 | 1.001 |

## MC4: zero-level path changes per second in the realised ripple-aware law (per leg)

| config | point | path changes per s | carrier periods per s | share of zero-level time in both-paths state |
|---|---|---|---|---|
| Si-ANPC | start-up 5 Hz | 671 | 1500 | 0.57 |
| Si-ANPC | 10 Hz | 549 | 1500 | 0.56 |
| Si-ANPC | 20 Hz | 434 | 1500 | 0.66 |
| Si-ANPC | 30 Hz | 336 | 1500 | 0.73 |
| Si-ANPC | 60 Hz | 838 | 1500 | 0.55 |
| Si-ANPC | 150 Hz | 971 | 1500 | 0.27 |
| Si-ANPC | brake 20 Hz | 859 | 1500 | 0.35 |
| SiC-ANPC | start-up 5 Hz | 321 | 1500 | 0.59 |
| SiC-ANPC | 10 Hz | 218 | 1500 | 0.61 |
| SiC-ANPC | 20 Hz | 365 | 1500 | 0.51 |
| SiC-ANPC | 30 Hz | 530 | 1500 | 0.35 |
| SiC-ANPC | 60 Hz | 805 | 1500 | 0.12 |
| SiC-ANPC | 150 Hz | 467 | 1500 | 0.03 |
| SiC-ANPC | brake 20 Hz | 414 | 1500 | 0.55 |
