## Si-NPC
- base: worst chip D6, D = 1.3e-05 (t_on free 3.88e-06), ripple share 0.94 (free 0.80), max ripple 39.0 K, Tj peak 80.2 C, max mean-Tj rise above water 40.2 K, case swing max 19.3 K, solder rel 977
  band shares 0.5-2 Hz: 0.02, 2-5 Hz: 0.08, 5-10 Hz: 0.30, 10-30 Hz: 0.47, 30-100 Hz: 0.06, 100-300 Hz: 0.00, LF: 0.06
- ha: worst chip D5, D = 2.36e-06 (t_on free 6.98e-07), ripple share 0.93 (free 0.77), max ripple 34.0 K, Tj peak 68.5 C, max mean-Tj rise above water 36.6 K, case swing max 18.0 K, solder rel 839
  band shares 0.5-2 Hz: 0.04, 2-5 Hz: 0.09, 5-10 Hz: 0.22, 10-30 Hz: 0.38, 30-100 Hz: 0.20, 100-300 Hz: 0.00, LF: 0.07
- har: worst chip D1, D = 1.14e-06 (t_on free 5.45e-07), ripple share 0.60 (free 0.16), max ripple 16.1 K, Tj peak 76.6 C, max mean-Tj rise above water 36.6 K, case swing max 18.0 K, solder rel 840
  band shares 0.5-2 Hz: 0.00, 2-5 Hz: 0.02, 5-10 Hz: 0.06, 10-30 Hz: 0.11, 30-100 Hz: 0.05, 100-300 Hz: 0.36, LF: 0.40
- bound ton_clip: D_bound = 1.82e-07, best candidate pair_D1D4; ceiling = 71.4x, har gain = 11.4x, ha gain = 5.49x, har D_rip >= bound: True
- bound ton_free: D_bound = 2.59e-08, best candidate dual1; ceiling = 150x, har gain = 7.12x, ha gain = 5.56x, har D_rip >= bound: True
- operating points: 194
## Si-ANPC
- base: worst chip D6, D = 1.11e-05 (t_on free 3.37e-06), ripple share 0.94 (free 0.80), max ripple 38.9 K, Tj peak 79.9 C, max mean-Tj rise above water 39.9 K, case swing max 18.8 K, solder rel 873
  band shares 0.5-2 Hz: 0.03, 2-5 Hz: 0.10, 5-10 Hz: 0.29, 10-30 Hz: 0.46, 30-100 Hz: 0.06, 100-300 Hz: 0.00, LF: 0.06
- ha: worst chip D2, D = 9.64e-07 (t_on free 4.34e-07), ripple share 0.63 (free 0.18), max ripple 33.3 K, Tj peak 74.7 C, max mean-Tj rise above water 34.7 K, case swing max 17.3 K, solder rel 737
  band shares 0.5-2 Hz: 0.01, 2-5 Hz: 0.01, 5-10 Hz: 0.05, 10-30 Hz: 0.10, 30-100 Hz: 0.10, 100-300 Hz: 0.36, LF: 0.37
- har: worst chip D3, D = 8.7e-07 (t_on free 4.18e-07), ripple share 0.58 (free 0.12), max ripple 11.5 K, Tj peak 74.9 C, max mean-Tj rise above water 34.9 K, case swing max 17.4 K, solder rel 752
  band shares 0.5-2 Hz: 0.00, 2-5 Hz: 0.01, 5-10 Hz: 0.03, 10-30 Hz: 0.05, 30-100 Hz: 0.08, 100-300 Hz: 0.42, LF: 0.42
- bound ton_clip: D_bound = 1.5e-07, best candidate pair_D2D3; ceiling = 74x, har gain = 12.8x, ha gain = 11.5x, har D_rip >= bound: True
- bound ton_free: D_bound = 1.14e-08, best candidate pair_D2D3; ceiling = 296x, har gain = 8.07x, ha gain = 7.76x, har D_rip >= bound: True
- operating points: 194
## SiC-ANPC
- base: worst chip S2, D = 9.99e-07 (t_on free 1.6e-07), ripple share 0.98 (free 0.86), max ripple 17.0 K, Tj peak 58.4 C, max mean-Tj rise above water 18.4 K, case swing max 10.4 K, solder rel 211
  band shares 0.5-2 Hz: 0.00, 2-5 Hz: 0.01, 5-10 Hz: 0.08, 10-30 Hz: 0.32, 30-100 Hz: 0.25, 100-300 Hz: 0.32, LF: 0.02
- ha: worst chip S1, D = 2.87e-07 (t_on free 3.38e-08), ripple share 0.95 (free 0.55), max ripple 4.6 K, Tj peak 57.0 C, max mean-Tj rise above water 17.1 K, case swing max 9.6 K, solder rel 178
  band shares 0.5-2 Hz: 0.00, 2-5 Hz: 0.00, 5-10 Hz: 0.00, 10-30 Hz: 0.00, 30-100 Hz: 0.04, 100-300 Hz: 0.90, LF: 0.05
- har: worst chip S2, D = 2.53e-07 (t_on free 3.45e-08), ripple share 0.93 (free 0.45), max ripple 4.5 K, Tj peak 57.8 C, max mean-Tj rise above water 17.8 K, case swing max 9.8 K, solder rel 189
  band shares 0.5-2 Hz: 0.00, 2-5 Hz: 0.00, 5-10 Hz: 0.00, 10-30 Hz: 0.00, 30-100 Hz: 0.03, 100-300 Hz: 0.90, LF: 0.07
- bound ton_clip: D_bound = 7.5e-08, best candidate dual1; ceiling = 13.3x, har gain = 3.94x, ha gain = 3.48x, har D_rip >= bound: True
- bound ton_free: D_bound = 5.03e-09, best candidate dual1; ceiling = 31.9x, har gain = 4.66x, ha gain = 4.75x, har D_rip >= bound: True
- operating points: 194
