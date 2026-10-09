"""Review item P1-2: system-level (series) reliability of one inverter instead of the most damaged chip.

Each chip k of each of the three legs fails according to a Weibull distribution in the number of runs n with shape
beta_W and characteristic life proportional to 1/D_k (D_k: per-run damage). For a series system,
  -ln(1 - F_sys(n)) = sum_k (n D_k / c)^beta_W,
so the system B10 is proportional to (3 sum_k D_k^beta_W)^(-1/beta_W), and the break-even capability of SiC becomes
  kappa_sys = (sum_k D_SiC,k^beta_W / sum_k D_Si,k^beta_W)^(1/beta_W).

python p12_system.py  -> p12_system.md
"""
import os, numpy as np
import phantich_p0 as pp

HERE = os.path.dirname(os.path.abspath(__file__))
BETAS = (3.0, 5.0, 8.0)


def chip_D(v, c, tag, kn):
    d = pp.load(v, c)
    nf = pp.KERNELS[kn]
    t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    Tj, rip = d[f'{tag}_Tj'], d[f'{tag}_rip']
    return np.array([pp.tt.damage_lowfreq(Tj[:, k], t, nf)[0] + pp.tt.damage_ripple(Tj[:, k], rip[:, k], fe, dt, nf)
                     for k in range(Tj.shape[1])])


def main():
    L = ['# P1-2: system-level (series, three legs) vs worst-chip results, fvdr\n']
    for kn in ('ton_clip', 'ton_free'):
        D = {(c, tag): chip_D('fvdr', c, tag, kn) for c in pp.CFGS for tag in ('base', 'har')}
        L.append(f'## {kn}\n')
        L.append('| measure | worst chip | ' + ' | '.join(f'system, beta_W = {b:g}' for b in BETAS) + ' |')
        L.append('|---|---|' + '---|' * len(BETAS))
        sysD = lambda x, b: (3 * np.sum(x ** b)) ** (1 / b)
        ref = D[('Si-NPC', 'base')]
        for c in pp.CFGS:
            for tag in ('base', 'har'):
                x = D[(c, tag)]
                L.append(f'| B10 rel. to Si-NPC base: {c} {tag} | {ref.max() / x.max():.3g} | ' +
                         ' | '.join(f'{sysD(ref, b) / sysD(x, b):.3g}' for b in BETAS) + ' |')
        for lab, a, b_ in (('kappa sub vs Si-NPC+har', ('SiC-ANPC', 'base'), ('Si-NPC', 'har')),
                           ('kappa sub vs Si-ANPC+har', ('SiC-ANPC', 'base'), ('Si-ANPC', 'har')),
                           ('kappa both vs Si-ANPC', ('SiC-ANPC', 'har'), ('Si-ANPC', 'har'))):
            L.append(f'| {lab} | {D[a].max() / D[b_].max():.3g} | ' +
                     ' | '.join(f'{sysD(D[a], b) / sysD(D[b_], b):.3g}' for b in BETAS) + ' |')
        L.append('')
    open(os.path.join(HERE, 'p12_system.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
