"""Global (Sobol) sensitivity of the parametric uncertainties, Saltelli sampling with the Jansen (total) and
Saltelli-2010 (first-order) estimators, implemented directly.

Factors (independent, uniform over the 90 % ranges used in mc_b10.py):
  sR_Si, sP_Si, sR_SiC, sP_SiC  thermal-resistance and loss factors per technology  [0.9, 1.1]
  b1f, b2f                       CIPS08 beta1, beta2 relative factors                 [0.95, 1.05], [0.8, 1.2]
  lnk                            ln kappa of SiC                                       [ln 0.25, ln 0.6]
Outputs: log10 per-trip worst-chip damage of Si-NPC+har, Si-ANPC+har, SiC base (with kappa), and the decision
ratio log10(D_SiC,base / D_Si-ANPC,har) (SiC wins if < 0).
Structural assumptions (current limit, heat sink, t_on rule, lifetime-model form) are covered by the one-at-a-time
variants, not here.

Extended for review item P0-7: beta3 (heating-time exponent, relative factor 0.65-1.3) and the lower clip of
the heating time t_floor (log-uniform 1 ms - 1 s; t_floor = 1 s is the reference rule, 1e-4 s the alternative),
so that the heating-time treatment enters as a continuous structural factor.

python sobol2.py fvdr  -> sobol2_fvdr.md
"""
import os, sys, numpy as np
import tonhao as th, tonthuong as tt
from mc_b10 import cycles_of


def nf_one(dT, Tmin, ton, b1, b2, b3, tfl):
    p = tt.CIPS
    ton = np.clip(ton, tfl, tt.TON_RANGE[1])
    return (p['K'] * np.power(ton, b3) * p['I_wire'] ** p['b4'] * p['V100'] ** p['b5'] * p['D_um'] ** p['b6']
            * np.power(dT, b1) * np.exp(b2 / (Tmin + 273.15)))

HERE = os.path.dirname(os.path.abspath(__file__))
N = 1024
F = [('sR_Si', 0.9, 1.1), ('sP_Si', 0.9, 1.1), ('sR_SiC', 0.9, 1.1), ('sP_SiC', 0.9, 1.1),
     ('b1f', 0.95, 1.05), ('b2f', 0.8, 1.2), ('b3f', 0.65, 1.3), ('lntf', np.log(1e-3), np.log(1.0)),
     ('lnk', np.log(0.25), np.log(0.6))]
rng = np.random.default_rng(7)


class ChipModel:
    """Precomputed cycles of one chip history; damage for vectors of (s, b1, b2)."""

    def __init__(self, Tj, rip, fe, t, Tw):
        self.cyc = cycles_of(Tj, t)
        m = (rip >= tt.DT_MIN) & (fe >= 0.5)
        dt = t[1] - t[0]
        self.n, self.r0, self.Tm0, self.ton = fe[m] * dt, rip[m], Tj[m], 1.0 / (2 * fe[m])
        self.Tw = Tw

    def damage(self, s, b1, b2, b3, tfl):
        D = np.zeros(len(s)); c = self.cyc; Tw = self.Tw
        for i in range(len(s)):
            if len(c):
                D[i] += np.sum(c[:, 2] / nf_one(s[i] * c[:, 0], Tw + s[i] * (c[:, 1] - Tw), c[:, 3],
                                                b1[i], b2[i], b3[i], tfl[i]))
            if len(self.n):
                r = s[i] * self.r0
                D[i] += np.sum(self.n / nf_one(r, Tw + s[i] * (self.Tm0 - self.r0 / 2 - Tw), self.ton,
                                               b1[i], b2[i], b3[i], tfl[i]))
        return D


def worst_models(variant, cfg, tag, Tw):
    d = np.load(os.path.join(HERE, f'mophong_{variant}_{cfg}.npz'))
    Tj, rip, t, fe = d[f'{tag}_Tj'], d[f'{tag}_rip'], d['t'], d['fe']
    ms = [ChipModel(Tj[:, k], rip[:, k], fe, t, Tw) for k in range(Tj.shape[1])]
    one = np.ones(1)
    nom = [m.damage(one, np.array([tt.CIPS['b1']]), np.array([tt.CIPS['b2']]), np.array([tt.CIPS['b3']]),
                    np.array([1.0]))[0] for m in ms]
    return [ms[k] for k in np.argsort(nom)[-3:]]


def model(X, mods):
    sR_Si, sP_Si, sR_SiC, sP_SiC, b1f, b2f, b3f, lntf, lnk = X.T
    b1 = tt.CIPS['b1'] * b1f; b2 = tt.CIPS['b2'] * b2f; b3 = tt.CIPS['b3'] * b3f; tfl = np.exp(lntf)
    sSi, sSiC = sR_Si * sP_Si, sR_SiC * sP_SiC
    D = {}
    for key, ms in mods.items():
        s = sSiC if key.startswith('SiC') else sSi
        D[key] = np.max([m.damage(s, b1, b2, b3, tfl) for m in ms], axis=0)
    D['SiC-ANPC|base'] = D['SiC-ANPC|base'] / np.exp(lnk)
    Y = {'log10 D Si-NPC+har': np.log10(D['Si-NPC|har']), 'log10 D Si-ANPC+har': np.log10(D['Si-ANPC|har']),
         'log10 D SiC base': np.log10(D['SiC-ANPC|base']),
         'log10 D_SiC/D_Si-ANPC+har': np.log10(D['SiC-ANPC|base'] / D['Si-ANPC|har'])}
    return Y


def main(variant):
    Tw = th.T_WATER
    mods = {'Si-NPC|har': worst_models(variant, 'Si-NPC', 'har', Tw),
            'Si-ANPC|har': worst_models(variant, 'Si-ANPC', 'har', Tw),
            'SiC-ANPC|base': worst_models(variant, 'SiC-ANPC', 'base', Tw)}
    k = len(F)
    lo = np.array([f[1] for f in F]); hi = np.array([f[2] for f in F])
    A = lo + (hi - lo) * rng.random((N, k)); B = lo + (hi - lo) * rng.random((N, k))
    YA, YB = model(A, mods), model(B, mods)
    mu = {y: np.mean(np.r_[YA[y], YB[y]]) for y in YA}          # centring stabilises the first-order estimator
    YA = {y: v - mu[y] for y, v in YA.items()}; YB = {y: v - mu[y] for y, v in YB.items()}
    S1 = {y: [] for y in YA}; ST = {y: [] for y in YA}
    for i in range(k):
        ABi = A.copy(); ABi[:, i] = B[:, i]
        YABi = {y: v - mu[y] for y, v in model(ABi, mods).items()}
        for y in YA:
            V = np.var(np.r_[YA[y], YB[y]])
            S1[y].append(np.mean(YB[y] * (YABi[y] - YA[y])) / V)
            ST[y].append(0.5 * np.mean((YA[y] - YABi[y]) ** 2) / V)
        print('factor', F[i][0], 'done', flush=True)
    with open(os.path.join(HERE, f'sobol2_{variant}.md'), 'w', encoding='utf-8') as f:
        f.write(f'Sobol indices, N = {N} (Saltelli; {N * (k + 2)} model evaluations), variant {variant}\n\n')
        f.write('| output | ' + ' | '.join(f'{n} S1 / ST' for n, _, _ in F) + ' |\n|' + '---|' * (k + 1) + '\n')
        for y in YA:
            f.write(f'| {y} | ' + ' | '.join(f'{s1:.2f} / {st:.2f}' for s1, st in zip(S1[y], ST[y])) + ' |\n')
        y = 'log10 D_SiC/D_Si-ANPC+har'
        f.write('\nP(SiC substitution beats Si-ANPC + ripple law) = '
                f"{np.mean(np.r_[YA[y], YB[y]] + mu[y] < 0):.3f}\n")
    print(open(os.path.join(HERE, f'sobol2_{variant}.md'), encoding='utf-8').read())


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'fvdr')
