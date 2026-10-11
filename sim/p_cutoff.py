"""Review comment MC1: validity of the ripple damage floor with the 0.5 K cut-off of the damage model.

The proof of Proposition 1 needs a convex damage function. The cut-off damage d_c(r) = d(r) 1[r >= 0.5 K] is not convex,
but h(r) = max(0, d(r) - d(0.5 K)) is convex, increasing and h <= d_c everywhere, so the bound evaluated with h is a valid
lower bound for the damage model actually simulated. The stored floor was evaluated with d_c(rho); the floor with h
differs from it by at most  Delta = sum over steps with rho >= 0.5 K of n_o d(0.5 K, T_w, t_on)  <=  sum over all steps
of n_o d(0.5 K, T_w, t_on). This script evaluates that upper bound of Delta for every variant, configuration and rule,
and its ratio to the stored floor.

python p_cutoff.py -> p_cutoff.md
"""
import os, json, importlib
import numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h, donhay
import tran_daodong as td

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = ['fvdr', 'fvdr75', 'fvdr_h2500', 'fvdr_h10000', 'fvdr_t10', 'fvdr_t30', 'fvdr_tw50', 'fvdr_tw60',
            'fvdr_tw65', 'fvdr_sic3k', 'fvdr_sic5k', 'fvdr_esw', 'fv', 'fvdr_par'] + \
           [f'fvdr_u{u}' for u in ('0.3', '0.4', '0.5', '0.6', '0.7')]
CFGS = ['Si-NPC', 'Si-ANPC', 'SiC-ANPC']

rows, worst = [], 0.0
for v in VARIANTS:
    for cfg in CFGS:
        fn = os.path.join(HERE, f'daodong_{v}_{cfg}.json')
        if not os.path.exists(fn):
            continue
        importlib.reload(th)                     # apply_variant changes module state (coolant temperature etc.)
        pf = 'hoso_50km_dr75.csv' if 'dr75' in v else ('hoso_50km_dr.csv' if 'dr' in v else 'hoso_50km.csv')
        prof = td.apply_variant(v, h.load_profile(os.path.join(HERE, pf)), cfg)
        t, fe = prof['t'], prof['fe']; dt = t[1] - t[0]
        Tw = th.T_WATER
        steps = np.array([i for i in range(len(t)) if prof['I'][i] > 0 and fe[i] >= h.F_EDGES[0]])
        n = fe[steps] * dt
        j = json.load(open(fn))
        for st in ('ton_clip', 'ton_free'):
            nf = donhay.nf_setting(st)
            delta = float(np.sum(n / nf(np.full(len(steps), tt.DT_MIN), Tw, 1.0 / (2 * fe[steps]))))
            floor = j['bounds_tw'][st]['D_bound_rip']
            q = delta / floor
            worst = max(worst, q)
            rows.append(f'| {v} | {cfg} | {st} | {n.sum():.0f} | {delta:.2e} | {floor:.2e} | {q:.1e} |')
out = ['# MC1: effect of the 0.5 K cut-off on the ripple damage floor', '',
       'Upper bound of the change of the floor when the convex minorant h(r) = max(0, d(r) - d(0.5 K)) replaces the',
       'cut-off damage in the bound (T_min = T_w, t_on = 1/(2 f_e), rule-specific clipping).', '',
       '| variant | config | rule | ripple cycles per run | max change | floor | ratio |', '|---|---|---|---|---|---|---|'] + rows + \
      ['', f'Largest ratio over all cases: {worst:.1e}']
open(os.path.join(HERE, 'p_cutoff.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out[-3:]))
