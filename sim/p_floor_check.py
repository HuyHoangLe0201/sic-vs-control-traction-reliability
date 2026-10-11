"""Review comment MC1, after the rerun of p15_bound.py: floor with the convex minorant of the cut-off damage
(D_bound_rip) versus the previous cut-off evaluation (D_bound_rip_cut); smallest ratio of simulated ripple damage to
the floor over all variants, configurations, policies and rules (the floor must never exceed a simulated policy).

python p_floor_check.py -> p_floor_check.md
"""
import os, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = ['fvdr', 'fvdr75', 'fvdr_h2500', 'fvdr_h10000', 'fvdr_t10', 'fvdr_t30', 'fvdr_tw50', 'fvdr_tw60',
            'fvdr_tw65', 'fvdr_sic3k', 'fvdr_sic5k', 'fvdr_esw', 'fv', 'fvdr_par'] + \
           [f'fvdr_u{u}' for u in ('0.3', '0.4', '0.5', '0.6', '0.7')]
rows, ratios, changes, n = [], [], [], 0
for v in VARIANTS:
    for c in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        j = json.load(open(os.path.join(HERE, f'daodong_{v}_{c}.json')))
        for st in ('ton_clip', 'ton_free'):
            b = j['bounds_tw'][st]
            fl, cut = b['D_bound_rip'], b.get('D_bound_rip_cut', float('nan'))
            changes.append(fl / cut)
            ceil_new, ceil_old = j['sim'][f'base|{st}']['D'] / fl, j['sim'][f'base|{st}']['D'] / cut
            for pol in ('base', 'ha', 'har'):
                ratios.append(j['sim'][f'{pol}|{st}']['D_rip'] / fl); n += 1
            rows.append(f'| {v} | {c} | {st} | {cut:.3e} | {fl:.3e} | {fl / cut:.4f} | {ceil_old:.1f} | {ceil_new:.1f} |')
out = ['# MC1 after the rerun: floor with the convex minorant h of the cut-off damage', '',
       '| variant | config | rule | floor (cut-off) | floor (h) | ratio | ceiling old | ceiling new |',
       '|---|---|---|---|---|---|---|---|'] + rows + ['',
       f'floor(h)/floor(cut-off): {min(changes):.4f} -- {max(changes):.4f}',
       f'smallest simulated ripple damage / floor over {n} cases: {min(ratios):.2f}']
open(os.path.join(HERE, 'p_floor_check.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out[-2:]))
