"""Monte Carlo B10 lifetime (procedure of Reigosa et al. 2016) on the saved mission simulations.

Per sample: thermal-resistance factor s_R and loss factor s_P (normal, +-10 % at 90 % confidence) scale the
junction rise above coolant, T' = T_w + s_R s_P (T - T_w) (first order; this transform keeps the rainflow
extrema, so cycles are counted once); CIPS08 beta1 +-5 %, beta2 +-20 % (90 % confidence); SiC capability kappa
log-normal with 5-95 % range 0.25-0.6. Lifetime = 1 / (worst-chip damage per trip x trips per year).
Usage: 500 000 km/year, 50 km station spacing -> 10 000 trips/year (assumption).
The CIPS08 constant and current/voltage/wire terms make absolute years indicative; ratios are the result.

python mc_b10.py fv   -> mc_b10_fv.md, mc_b10_fv.png
python mc_b10.py fvdr free -> heating times not clipped below 1 s (alternative rule), mc_b10_fvdr_free.md

Review item P1-3: an independent per-chip factor (normal, +-5 % at 90 %) is added to the common s_R s_P, 95 %
bootstrap intervals of the percentiles are reported, and the probabilities that SiC substitution / SiC with the
ripple-aware law yields the lower damage than Si-ANPC with the ripple-aware law are given.
"""
import os, sys, numpy as np
import tonhao as th, tonthuong as tt

HERE = os.path.dirname(os.path.abspath(__file__))
NS = 4000
TRIPS_PER_YEAR = 10_000
Z90 = 1.645
rng = np.random.default_rng(2026)


def cycles_of(T, t):
    T2 = T.copy(); k = int(np.argmin(T2))
    Tc = np.r_[T2[k:], T2[:k + 1]]; tc = np.r_[t[k:], t[:k + 1] + t[-1] + (t[1] - t[0])]
    cyc = [(r, m - r / 2, c, d) for r, m, c, d in tt.rainflow(Tc, tc) if r >= tt.DT_MIN]
    return np.array(cyc).reshape(-1, 4)


def nf_samples(dT, Tmin, ton, b1, b2):
    """CIPS08 with sampled beta1, beta2: dT, Tmin, ton [m]; b1, b2 [S] -> N_f [S, m]."""
    p = tt.CIPS
    ton = np.clip(ton, *tt.TON_RANGE)
    base = p['K'] * np.power(ton, p['b3']) * p['I_wire'] ** p['b4'] * p['V100'] ** p['b5'] * p['D_um'] ** p['b6']
    return base[None, :] * np.power(dT[None, :], b1[:, None]) * np.exp(b2[:, None] / (Tmin[None, :] + 273.15))


def chip_damage_samples(Tj, rip, fe, t, s, b1, b2, Tw):
    dt = t[1] - t[0]
    cyc = cycles_of(Tj, t)
    D = np.zeros(len(s))
    if len(cyc):
        dT = s[:, None] * cyc[None, :, 0]
        Tmin = Tw + s[:, None] * (cyc[None, :, 1] - Tw)
        for i in range(len(s)):   # loop over samples keeps memory low; vectorised over cycles
            D[i] = np.sum(cyc[:, 2] / nf_samples(dT[i], Tmin[i], cyc[:, 3], b1[i:i + 1], b2[i:i + 1])[0])
    m = (rip >= tt.DT_MIN) & (fe >= 0.5)
    if np.any(m):
        n = fe[m] * dt; r0 = rip[m]; Tm0 = Tj[m]; ton = 1.0 / (2 * fe[m])
        for i in range(len(s)):
            r = s[i] * r0; Tmin = Tw + s[i] * (Tm0 - r0 / 2 - Tw)
            D[i] += np.sum(n / nf_samples(r, Tmin, ton, b1[i:i + 1], b2[i:i + 1])[0])
    return D


def main(variant, rule='clip'):
    if rule == 'free':
        tt.TON_RANGE = (1e-4, 15.0)
    Tw = th.T_WATER
    sR = 1 + rng.normal(0, 0.10 / Z90, NS); sP = 1 + rng.normal(0, 0.10 / Z90, NS); s = sR * sP
    b1 = tt.CIPS['b1'] * (1 + rng.normal(0, 0.05 / Z90, NS))
    b2 = tt.CIPS['b2'] * (1 + rng.normal(0, 0.20 / Z90, NS))
    lk_lo, lk_hi = np.log(0.25), np.log(0.6)
    kappa = np.exp(rng.normal((lk_lo + lk_hi) / 2, (lk_hi - lk_lo) / (2 * Z90), NS))
    res = {}
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        d = np.load(os.path.join(HERE, f'mophong_{variant}_{cfg}.npz'))
        t, fe = d['t'], d['fe']
        for tag in ('base', 'ha', 'har'):
            Tj, rip = d[f'{tag}_Tj'], d[f'{tag}_rip']
            # nominal damage per chip to pick candidates for the worst chip
            nom = [chip_damage_samples(Tj[:, k], rip[:, k], fe, t, np.ones(1), np.array([tt.CIPS['b1']]),
                                       np.array([tt.CIPS['b2']]), Tw)[0] for k in range(Tj.shape[1])]
            cand = np.argsort(nom)[-3:]
            Dk = np.stack([chip_damage_samples(Tj[:, k], rip[:, k], fe, t,
                                               s * (1 + rng.normal(0, 0.05 / Z90, NS)), b1, b2, Tw) for k in cand])
            Dw = Dk.max(0)
            if cfg.startswith('SiC'):
                Dw = Dw / kappa
            life = 1.0 / (Dw * TRIPS_PER_YEAR)
            bs = [np.percentile(rng.choice(life, len(life)), 10) for _ in range(300)]
            res[(cfg, tag)] = dict(B1=np.percentile(life, 1), B10=np.percentile(life, 10), B50=np.percentile(life, 50),
                                   B10lo=np.percentile(bs, 2.5), B10hi=np.percentile(bs, 97.5), life=life, Dw=Dw)
            print(cfg, tag, {k: round(float(v), 1) for k, v in res[(cfg, tag)].items() if k not in ('life', 'Dw')}, flush=True)
    ref = res[('Si-NPC', 'base')]['B10']
    suf = '' if rule == 'clip' else '_free'
    with open(os.path.join(HERE, f'mc_b10_{variant}{suf}.md'), 'w', encoding='utf-8') as f:
        f.write(f'Monte Carlo, {NS} samples, {TRIPS_PER_YEAR} trips/year; SiC includes kappa ~ logN(5-95 %: 0.25-0.6)\n\n')
        f.write(f'rule: {rule}\n\n| config | law | B1 (years) | B10 (years) | B50 (years) | B10 / B10(Si-NPC base) | '
                '95 % bootstrap CI of the ratio |\n|---|---|---|---|---|---|---|\n')
        for (cfg, tag), v in res.items():
            f.write(f"| {cfg} | {tag} | {v['B1']:.3g} | {v['B10']:.3g} | {v['B50']:.3g} | {v['B10']/ref:.3g} | "
                    f"{v['B10lo']/ref:.3g}-{v['B10hi']/ref:.3g} |\n")
        Da = res[('Si-ANPC', 'har')]['Dw']
        f.write(f"\nP(SiC substitution better than Si-ANPC + ripple law) = {np.mean(res[('SiC-ANPC', 'base')]['Dw'] < Da):.3f}\n")
        f.write(f"P(SiC + ripple law better than Si-ANPC + ripple law) = {np.mean(res[('SiC-ANPC', 'har')]['Dw'] < Da):.3f}\n")
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for (cfg, tag), v in res.items():
        x = np.sort(v['life']); y = np.arange(1, len(x) + 1) / len(x)
        ax.semilogx(x, y, ls={'base': ':', 'ha': '--', 'har': '-'}[tag],
                    color={'Si-NPC': 'C0', 'Si-ANPC': 'C1', 'SiC-ANPC': 'C2'}[cfg], label=f'{cfg} {tag}')
    ax.axhline(0.10, color='k', lw=0.6); ax.set_xlabel('lifetime (years, indicative)'); ax.set_ylabel('unreliability F(t)')
    ax.grid(alpha=.3, which='both'); ax.legend(fontsize=7, ncol=3); fig.tight_layout()
    fig.savefig(os.path.join(HERE, f'mc_b10_{variant}{suf}.png'), dpi=110)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'fv', sys.argv[2] if len(sys.argv) > 2 else 'clip')
