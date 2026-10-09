"""Post-processing for review items P0-7 (common lifetime kernels), P0-9 (damage share vs heating time) and
P0-13 (baseplate-solder exponent), on the stored mission simulations (mophong_<variant>_<cfg>.npz).

python phantich_p0.py   -> phantich_p0.md, phantich_p0.json
"""
import os, json, numpy as np
import tonthuong as tt, donhay

HERE = os.path.dirname(os.path.abspath(__file__))
CFGS = ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')
U_VARIANTS = [('fvdr_u0.3', 0.3), ('fvdr_u0.4', 0.4), ('fvdr_u0.5', 0.5), ('fvdr_u0.6', 0.6), ('fvdr_u0.7', 0.7),
              ('fvdr', 0.77)]
R_GAS = 8.314


def lesit_nf(d, Tm_min, on):
    """LESIT (Held 1997): N = 640 dT^-5 exp(Q/(R Tm)), Q = 78 kJ/mol, Tm = mean temperature of the cycle."""
    Tm = Tm_min + d / 2.0 + 273.15
    return 640.0 * np.power(d, -5.0) * np.exp(7.8e4 / (R_GAS * Tm))


def two_slope(beta_e, base, T_knee=60.0, b1=-4.416):
    """CIPS08 with the elastic low-dT term of Cougo (2026) in the form used for SiC by Hoffmann/Cougo:
    N = N_CIPS * (1 + (-beta_e/50) (dT/T_knee)^(beta_e - b1)), applied identically to both technologies."""
    def f(d, Tm, on):
        return base(d, Tm, on) * (1.0 + (-beta_e / 50.0) * np.power(np.maximum(d, 1e-6) / T_knee, beta_e - b1))
    return f


KERNELS = {
    'ton_clip': donhay.nf_setting('ton_clip'),
    'ton_free': donhay.nf_setting('ton_free'),
    'clip+elastic(-10)': two_slope(-10.0, donhay.nf_setting('ton_clip')),
    'free+elastic(-10)': two_slope(-10.0, donhay.nf_setting('ton_free')),
    'clip+elastic(-4)': two_slope(-4.0, donhay.nf_setting('ton_clip')),
    'free+elastic(-4)': two_slope(-4.0, donhay.nf_setting('ton_free')),
    'LESIT': lesit_nf,
}


def load(v, c):
    return np.load(os.path.join(HERE, f'mophong_{v}_{c}.npz'))


def worst_damage(d, tag, nf):
    t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    Tj, rip = d[f'{tag}_Tj'], d[f'{tag}_rip']
    best = None
    for k in range(Tj.shape[1]):
        Dl, cyc = tt.damage_lowfreq(Tj[:, k], t, nf)
        Dr = tt.damage_ripple(Tj[:, k], rip[:, k], fe, dt, nf)
        if best is None or Dl + Dr > best[0]:
            best = (Dl + Dr, k, cyc)
    return best


def kappa_table(v):
    S = {c: load(v, c) for c in CFGS}
    out = {}
    for kn, nf in KERNELS.items():
        D = {(c, tag): worst_damage(S[c], tag, nf)[0] for c in CFGS for tag in ('base', 'har')}
        out[kn] = dict(sub_NPC=D[('SiC-ANPC', 'base')] / D[('Si-NPC', 'har')],
                       sub_ANPC=D[('SiC-ANPC', 'base')] / D[('Si-ANPC', 'har')],
                       both_ANPC=D[('SiC-ANPC', 'har')] / D[('Si-ANPC', 'har')],
                       gain_har_ANPC=D[('Si-ANPC', 'base')] / D[('Si-ANPC', 'har')])
    return out


def u_threshold(us, ks, kappa):
    """Largest u in the sweep at which kappa-bar(u) <= kappa (linear interpolation in log kappa-bar)."""
    lk = np.log(ks)
    if ks[0] > kappa:
        return '< 0.3'
    for i in range(len(us) - 1):
        if ks[i] <= kappa < ks[i + 1]:
            return f'{us[i] + (us[i + 1] - us[i]) * (np.log(kappa) - lk[i]) / (lk[i + 1] - lk[i]):.2f}'
    return '> 0.77'


def ton_shares(v, c, tag='base'):
    """Damage share of the worst chip by heating time of the damaging cycle, under both t_on rules."""
    d = load(v, c)
    t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    edges = [0, 0.02, 0.05, 0.5, 1e9]
    res = {}
    for kn in ('ton_clip', 'ton_free'):
        nf = KERNELS[kn]
        Dtot, k, cyc = worst_damage(d, tag, nf)
        Tj, rip = d[f'{tag}_Tj'][:, k], d[f'{tag}_rip'][:, k]
        sh = np.zeros(len(edges) - 1)
        for rng, Tmin, cnt, dur, dd in cyc:                       # slow cycles
            sh[np.searchsorted(edges, dur, side='right') - 1] += dd
        m = rip >= tt.DT_MIN
        ton = 1.0 / (2.0 * np.maximum(fe, 1e-3))
        dr = np.where(m, fe * dt / nf(np.maximum(rip, 1e-6), Tj - rip / 2, ton), 0.0)
        for i in range(len(edges) - 1):
            sh[i] += dr[(ton >= edges[i]) & (ton < edges[i + 1])].sum()
        res[kn] = (sh / sh.sum()).round(3).tolist()
    return res


def solder(v, n_list=(2.0, 1 / 0.442, 3.0, 4.0, 5.0)):
    """Baseplate-solder damage ratios for N ~ dTc^-n: SiC (baseline) / Si-ANPC (ripple-aware law), and the
    control effect on Si-ANPC (har/base)."""
    S = {c: load(v, c) for c in ('Si-ANPC', 'SiC-ANPC')}
    out = {}
    for n in n_list:
        nf = lambda d, Tm, on, n=n: np.power(d, -n)
        def dmax(c, tag):
            Tc, t = S[c][f'{tag}_Tc'], S[c]['t']
            return max(tt.damage_lowfreq(Tc[:, k], t, nf)[0] for k in range(Tc.shape[1]))
        out[f'{n:.2f}'] = dict(ratio=dmax('SiC-ANPC', 'base') / dmax('Si-ANPC', 'har'),
                               control=dmax('Si-ANPC', 'har') / dmax('Si-ANPC', 'base'))
    return out


def main():
    J, L = {}, ['# P0-7 / P0-9 / P0-13 post-processing\n']
    # P0-7: kernels at the reference point and over the utilisation sweep
    K = {v: kappa_table(v) for v, _ in U_VARIANTS}
    J['kappa'] = K
    L.append('## P0-7: kappa-bar with a common lifetime kernel for both technologies (u = 0.77, fvdr)\n')
    L.append('| kernel | sub vs NPC+har | sub vs ANPC+har | both vs ANPC | har gain ANPC | u at kappa 0.25 | u at kappa 0.6 |')
    L.append('|---|---|---|---|---|---|---|')
    us = np.array([u for _, u in U_VARIANTS])
    for kn in KERNELS:
        ks = np.array([K[v][kn]['sub_ANPC'] for v, _ in U_VARIANTS])
        r = K['fvdr'][kn]
        L.append(f"| {kn} | {r['sub_NPC']:.3g} | {r['sub_ANPC']:.3g} | {r['both_ANPC']:.3g} | {r['gain_har_ANPC']:.3g} | "
                 f"{u_threshold(us, ks, 0.25)} | {u_threshold(us, ks, 0.6)} |")
    # P0-9
    L.append('\n## P0-9: damage share of the worst chip by heating time (baseline policy, fvdr)\n')
    L.append('| config | rule | < 20 ms | 20-50 ms | 50-500 ms | > 0.5 s |')
    L.append('|---|---|---|---|---|---|')
    J['ton'] = {}
    for c in CFGS:
        s = ton_shares('fvdr', c)
        J['ton'][c] = s
        for kn, sh in s.items():
            L.append(f'| {c} | {kn} | ' + ' | '.join(f'{x:.2f}' for x in sh) + ' |')
    # P0-13
    L.append('\n## P0-13: baseplate solder, N ~ dTc^-n\n')
    L.append('| variant | n | SiC base / Si-ANPC har | Si-ANPC har / base |')
    L.append('|---|---|---|---|')
    J['solder'] = {}
    for v in ('fvdr', 'fvdr_par', 'fvdr_u0.3'):
        s = solder(v)
        J['solder'][v] = s
        for n, r in s.items():
            L.append(f"| {v} | {n} | {r['ratio']:.3g} (x{1 / r['ratio']:.1f}) | {r['control']:.3f} |")
    open(os.path.join(HERE, 'phantich_p0.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    json.dump(J, open(os.path.join(HERE, 'phantich_p0.json'), 'w'), indent=1, default=float)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
