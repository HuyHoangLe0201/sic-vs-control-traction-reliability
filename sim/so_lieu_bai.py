"""Numbers quoted in the manuscript (baseline variant fvdr). python so_lieu_bai.py -> so_lieu_bai.md"""
import os, json, numpy as np
import tonthuong as tt

HERE = os.path.dirname(os.path.abspath(__file__))
V = 'fvdr'
CFGS = ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')
bands = [(0.5, 2), (2, 5), (5, 10), (10, 30), (30, 100), (100, 300)]
out = []
for cfg in CFGS:
    j = json.load(open(os.path.join(HERE, f'daodong_{V}_{cfg}.json')))
    d = np.load(os.path.join(HERE, f'mophong_{V}_{cfg}.npz'))
    t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    out.append(f'## {cfg}')
    for tag in ('base', 'ha', 'har'):
        s = j['sim'][f'{tag}|ton_clip']; sf = j['sim'][f'{tag}|ton_free']
        Tj = d[f'{tag}_Tj']; rip = d[f'{tag}_rip']; Tc = d[f'{tag}_Tc']
        k = list(d['names']).index(s['chip'])
        sh = []
        for lo, hi in bands:
            m = (fe >= lo) & (fe < hi)
            sh.append(tt.damage_ripple(Tj[:, k], np.where(m, rip[:, k], 0), fe, dt) / s['D'])
        out.append(f"- {tag}: worst chip {s['chip']}, D = {s['D']:.3g} (t_on free {sf['D']:.3g}), ripple share "
                   f"{s['D_rip']/s['D']:.2f} (free {sf['D_rip']/sf['D']:.2f}), max ripple {s['rip_max']:.1f} K, "
                   f"Tj peak {Tj[:, k].max():.1f} C, max mean-Tj rise above water {Tj.max() - 40:.1f} K, "
                   f"case swing max {(Tc.max(0) - Tc.min(0)).max():.1f} K, solder rel {s['solder']:.3g}")
        out.append('  band shares ' + ', '.join(f'{lo}-{hi} Hz: {x:.2f}' for (lo, hi), x in zip(bands, sh))
                   + f', LF: {1 - s["D_rip"]/s["D"]:.2f}')
    for st in ('ton_clip', 'ton_free'):
        b = j.get('bounds_tw', j['bounds'])[st]
        out.append(f"- bound {st}: D_bound = {b['D_bound_rip']:.3g}, best candidate "
                   f"{max(b['candidates'], key=b['candidates'].get)}; ceiling = {j['sim']['base|'+st]['D']/b['D_bound_rip']:.3g}x, "
                   f"har gain = {j['sim']['base|'+st]['D']/j['sim']['har|'+st]['D']:.3g}x, ha gain = "
                   f"{j['sim']['base|'+st]['D']/j['sim']['ha|'+st]['D']:.3g}x, har D_rip >= bound: "
                   f"{j['sim']['har|'+st]['D_rip'] >= b['D_bound_rip']}")
    out.append(f"- operating points: {j['n_points']}")
open(os.path.join(HERE, 'so_lieu_bai.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
