"""Review item P0-4: effect of the pulse-resolved ripple correction on kappa-bar.
The ripple of every chip is scaled by the ratio pulsed/averaged found in xung_p04.py (worst chip, maximum of motoring
and braking at each output frequency, interpolated in log f_e), for both technologies and all policies.

python p04_kappa.py  -> p04_kappa.md
"""
import os, numpy as np
import phantich_p0 as pp

HERE = os.path.dirname(os.path.abspath(__file__))
F = np.array([4.8, 9.7, 20, 30, 57, 97, 150, 197, 250])
RATIO = {'Si': np.array([1.03, 1.04, 1.07, 1.11, 1.26, 1.45, 1.49, 1.63, 1.74]),
         'SiC': np.array([1.00, 1.09, 1.15, 1.00, 1.00, 1.22, 1.30, 1.35, 1.40])}


class Scaled(dict):
    pass


def scaled(v, c):
    d = pp.load(v, c)
    tech = 'SiC' if c.startswith('SiC') else 'Si'
    fac = np.interp(np.log(np.maximum(d['fe'], 1e-3)), np.log(F), RATIO[tech], left=RATIO[tech][0], right=RATIO[tech][-1])
    out = Scaled({k: d[k] for k in d.files})
    for tag in ('base', 'ha', 'har'):
        out[f'{tag}_rip'] = d[f'{tag}_rip'] * fac[:, None]
    return out


def kap(v, corrected, kn):
    nf = pp.KERNELS[kn]
    S = {c: (scaled(v, c) if corrected else pp.load(v, c)) for c in pp.CFGS}
    D = {(c, t): pp.worst_damage(S[c], t, nf)[0] for c in pp.CFGS for t in ('base', 'har')}
    return dict(sub_NPC=D[('SiC-ANPC', 'base')] / D[('Si-NPC', 'har')], sub_ANPC=D[('SiC-ANPC', 'base')] / D[('Si-ANPC', 'har')],
                both=D[('SiC-ANPC', 'har')] / D[('Si-ANPC', 'har')], D_SiC=D[('SiC-ANPC', 'base')], D_SiANPC=D[('Si-ANPC', 'har')])


def main():
    L = ['| rule | model | kappa sub vs NPC | kappa sub vs ANPC | both vs ANPC | D_SiC base | D_Si-ANPC har | u at 0.25 | u at 0.6 |',
         '|---|---|---|---|---|---|---|---|---|']
    us = np.array([u for _, u in pp.U_VARIANTS])
    for kn in ('ton_clip', 'ton_free'):
        for corr in (False, True):
            r = kap('fvdr', corr, kn)
            ks = np.array([kap(v, corr, kn)['sub_ANPC'] for v, _ in pp.U_VARIANTS])
            L.append(f"| {kn} | {'pulse-corrected' if corr else 'averaged'} | {r['sub_NPC']:.3g} | {r['sub_ANPC']:.3g} | "
                     f"{r['both']:.3g} | {r['D_SiC']:.3g} | {r['D_SiANPC']:.3g} | {pp.u_threshold(us, ks, 0.25)} | "
                     f"{pp.u_threshold(us, ks, 0.6)} |")
            print(L[-1], flush=True)
    open(os.path.join(HERE, 'p04_kappa.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
