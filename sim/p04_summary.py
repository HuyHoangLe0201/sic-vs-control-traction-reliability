"""Summary of the policy-aware pulse correction (p04m_*.json) -> p04_summary.md"""
import json, numpy as np, phantich_p0 as pp
V = [('fvdr_u0.3', .3), ('fvdr_u0.4', .4), ('fvdr_u0.5', .5), ('fvdr_u0.6', .6), ('fvdr_u0.7', .7), ('fvdr', .77)]
J = {v: {c: json.load(open(f'p04m_{v}_{c}.json'))['D'] for c in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')} for v, _ in V}
us = np.array([u for _, u in V])
L = ['| rule | model | gain har Si-NPC / Si-ANPC / SiC (u=0.77) | gain ha Si-NPC / Si-ANPC / SiC | kappa sub vs Si-ANPC+har | kappa both | u limit kappa 0.25 / 0.6 | gain har Si range over u |',
     '|---|---|---|---|---|---|---|---|']
for st in ('ton_clip', 'ton_free'):
    for m, lab in (('averaged', 'carrier-averaged'), ('no_us_term', 'pulse-resolved, without us term'), ('nominal', 'pulse-resolved, with us term')):
        D = lambda v, c, t: J[v][c][t][m][st]
        g = lambda v, c, t: D(v, c, 'base') / D(v, c, t)
        ks = np.array([D(v, 'SiC-ANPC', 'base') / D(v, 'Si-ANPC', 'har') for v, _ in V])
        gs = [g(v, c, 'har') for v, _ in V for c in ('Si-NPC', 'Si-ANPC')]
        L.append(f"| {st} | {lab} | {g('fvdr','Si-NPC','har'):.1f} / {g('fvdr','Si-ANPC','har'):.1f} / {g('fvdr','SiC-ANPC','har'):.1f} | "
                 f"{g('fvdr','Si-NPC','ha'):.1f} / {g('fvdr','Si-ANPC','ha'):.1f} / {g('fvdr','SiC-ANPC','ha'):.1f} | {ks[-1]:.2f} | "
                 f"{D('fvdr','SiC-ANPC','har') / D('fvdr','Si-ANPC','har'):.2f} | {pp.u_threshold(us, ks, 0.25)} / {pp.u_threshold(us, ks, 0.6)} | {min(gs):.1f}-{max(gs):.1f} |")
open('p04_summary.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
