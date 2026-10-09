"""R6: mission thermal simulation and per-trip damage, baseline vs health-aware (LP law) control,
Si-NPC / Si-ANPC / SiC-ANPC, with fundamental-frequency ripple counted separately (Cougo 2026).

Usage: python hanhtrinh.py [hoso_50km.csv]
"""
import os, sys, time, json, numpy as np
import tonhao as th
import tonthuong as tt

HERE = os.path.dirname(os.path.abspath(__file__))
FSW = 1500.0
TAU_CS, TAU_HW = 1.0, 5.0     # s, module case-sink and sink-water time constants (assumption, FEM later)
NHARM = 12
F_EDGES = np.geomspace(0.5, 320.0, 17)          # output-frequency bands (ripple map, NP charge)
F_MID = np.sqrt(F_EDGES[:-1] * F_EDGES[1:])


def fband(fe):
    if fe is None or fe < F_EDGES[0]:
        return -1
    return int(np.clip(np.searchsorted(F_EDGES, fe) - 1, 0, len(F_MID) - 1))


def load_profile(fn):
    with open(fn) as f:
        head = f.readline().strip().split(',')
        rows = [l.strip().split(',') for l in f if l.strip()]
    col = {h: i for i, h in enumerate(head)}
    g = lambda k: np.array([float(r[col[k]]) for r in rows])
    return dict(t=g('t_s'), I=g('I_pk_A'), m=g('m'), c=g('cosphi'), fe=g('f_e_Hz'))


class OpCache:
    """Per operating point: policy-averaged chip losses at TEMPS, ripple harmonics, bound T*."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.tp = th.topology(cfg)
        self.Z = th.zmatrix(self.tp)
        self.data = {}

    def key(self, I, m, c, fe=None):
        """Operating-point key; includes the decision-interval grouping g set by fe (review P0-2) and the
        output-frequency band that scales the neutral-point charge (review P0-3)."""
        return (int(round(I / 10.0)) * 10, round(round(m / 0.02) * 0.02, 2), 1 if c >= 0 else -1,
                th.bin_group(fe, FSW), fband(fe))

    def get(self, I, m, c, fe=None):
        k = self.key(I, m, c, fe)
        if k in self.data:
            return self.data[k]
        Ik, mk, sk, g, fb = k
        if Ik <= 0:
            d = None
        else:
            # band-centre fe for the NP charge; g from the actual fe (lowest fe of the band is not needed:
            # the NP allowance is relative to the baseline at the same fe)
            fe_np = F_MID[fb] if fb >= 0 else None
            r = th.analyse_point(self.cfg, Ik, max(mk, 0.01), 0.95 * sk, FSW, fe=fe_np, g=g)
            d = dict(Tstar=r['Tstar'], Tb=r['Tb'].max(), Teq=r['Teq'].max(), r=r,
                     dV_base=r['dV_base'], dV_ha=r['dV_ha'])
            for tag, w, Tref in (('base', r['wb'], r['Tb']), ('ha', r['w_eq'], r['Teq'])):
                d[tag], d[tag + '_H'] = policy_tables(r['L'], w, Tref)
        self.data[k] = d
        return d


def policy_tables(L, w, Tref):
    """Policy-averaged chip losses at TEMPS [nchip,3] and loss harmonics at temperatures Tref."""
    Lb = th.bin_avg(L)                                               # [NOFF,NOT,NBIN,nchip,3]
    tab = np.einsum('bro,robkt->kt', w, Lb) / th.NBIN
    wth = w[th.BIN]                                                  # [NTH,NOFF,NOT]
    pth = np.einsum('qro,roqk->qk', wth, th.at_temp(L, Tref))        # [NTH, nchip]
    H = np.fft.rfft(pth, axis=0)[1:NHARM + 1] / th.NTH * 2
    return tab, H


def ripple_p2p(H, rth, foster, fe):
    """Peak-to-peak junction ripple from loss harmonics through the chip Foster network."""
    if fe < 0.5:
        return np.zeros(H.shape[1])
    R, tau = foster
    h = np.arange(1, H.shape[0] + 1)
    Zh = (R[None, :] / (1 + 1j * 2 * np.pi * fe * h[:, None] * tau[None, :])).sum(1)   # normalized
    th_ = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    E = np.exp(1j * np.outer(h, th_))                                                 # [nh, 72]
    T = np.real(np.einsum('hk,h,hq->qk', H, Zh, E)) * rth[None, :]
    return T.max(0) - T.min(0)


def simulate(cfg, prof, cache, tag):
    tp, Z = cache.tp, cache.Z
    t, dt = prof['t'], prof['t'][1] - prof['t'][0]
    n, nc, nm = len(t), tp['nchip'], tp['nmod']
    R, tau = tp['foster']
    aj = np.exp(-dt / tau)                                   # chip Foster decay
    am = np.exp(-dt / np.array([TAU_CS, TAU_HW]))
    Rm = np.array([tp['rcs'], th.R_HW])
    xj = np.zeros((nc, len(tau)))
    xm = np.zeros((nm, 2))
    sink = th.SINK
    if sink is not None:   # impulse responses of the folded heat-sink model at the simulation step
        tg = dt * np.arange(0, int(sink['t'][-1] / dt) + 1)
        Zs = np.stack([[np.interp(tg, np.r_[0, sink['t']], np.r_[0, sink['Zf'][:, a, b]]) for b in range(nm)]
                       for a in range(nm)])                     # [nm, nm, L+1]
        hk = np.diff(Zs, axis=2)[:, :, ::-1]                      # reversed impulse response, [nm, nm, L]
        L = hk.shape[2]
        Ph = np.zeros((n + L, nm))                               # module power history (zero-padded)
    Tj = np.zeros((n, nc)); Tc = np.zeros((n, nm)); rip = np.zeros((n, nc)); P = np.zeros((n, nc))
    Ts = np.array(th.TEMPS)
    T_now = np.full(nc, th.T_WATER)
    dV = np.zeros(n)
    for i in range(n):
        d = cache.get(prof['I'][i], prof['m'][i], prof['c'][i], prof['fe'][i])
        if d is None:
            p = np.zeros(nc)
        else:
            dV[i] = d.get('dV_' + tag) or 0.0
            tab = d[tag]
            j = (T_now > Ts[1]).astype(int)
            w = (T_now - Ts[j]) / (Ts[j + 1] - Ts[j])
            p = (1 - w) * tab[np.arange(nc), j] + w * tab[np.arange(nc), j + 1]
            rip[i] = ripple_p2p(d[tag + '_H'], tp['rth'], (R, tau), prof['fe'][i])
        pm = np.array([p[tp['mod_of'] == k].sum() for k in range(nm)])
        xj = aj[None, :] * xj + (tp['rth'][:, None] * R[None, :]) * (1 - aj[None, :]) * p[:, None]
        if sink is None:
            xm = am[None, :] * xm + Rm[None, :] * (1 - am[None, :]) * pm[:, None]
            Tc[i] = th.T_WATER + xm.sum(1)
        else:
            Ph[L + i] = pm
            win = Ph[i + 1:L + i + 1]                             # last L module powers, oldest first
            Tc[i] = th.T_WATER + tp['rcs'] * pm + np.einsum('abl,lb->a', hk, win)
        Tj[i] = Tc[i][tp['mod_of']] + xj.sum(1)
        T_now = Tj[i]
        P[i] = p
    return dict(Tj=Tj, Tc=Tc, rip=rip, P=P, dV=dV)


def damages(sim, prof, nf=tt.cips08_nf):
    t, dt, fe = prof['t'], prof['t'][1] - prof['t'][0], prof['fe']
    out = []
    for k in range(sim['Tj'].shape[1]):
        Dl, cyc = tt.damage_lowfreq(sim['Tj'][:, k], t, nf)
        Dr = tt.damage_ripple(sim['Tj'][:, k], sim['rip'][:, k], fe, dt, nf)
        big = max(cyc, key=lambda c: c[0]) if cyc else (0, 0, 0, 0, 0)
        out.append(dict(D_low=Dl, D_rip=Dr, D=Dl + Dr, dT_max=big[0], Tmin_dom=big[1], ton_dom=big[3],
                        rip_max=float(sim['rip'][:, k].max()), Tpeak=float(sim['Tj'][:, k].max())))
    sold = []
    for k in range(sim['Tc'].shape[1]):
        Ds, cyc = tt.damage_lowfreq(sim['Tc'][:, k], t, lambda d, Tm, on: tt.solder_nf_rel(d))
        sold.append(dict(D_rel=Ds, dTc_max=max((c[0] for c in cyc), default=0.0)))
    return out, sold


def main(fn):
    prof = load_profile(fn)
    res, caches = {}, {}
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        cache = OpCache(cfg); caches[cfg] = cache
        t0 = time.time()
        for tag in ('base', 'ha'):
            sim = simulate(cfg, prof, cache, tag)
            dj, ds = damages(sim, prof)
            res[(cfg, tag)] = dict(sim=sim, dj=dj, ds=ds)
            if cfg.startswith('SiC'):
                dh, _ = damages(sim, prof, nf=lambda d, Tm, on: tt.sic_nf_hoffmann(d, Tm))
                res[(cfg, tag)]['dj_hoff'] = dh
        print(f'{cfg}: {len(cache.data)} operating points, {time.time()-t0:.0f}s', flush=True)
    # mission-level ceiling for Si (dominant-cycle bound, Theorem/Corollary)
    summary = {}
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        Tstar_max = max(d['Tstar'] for d in caches[cfg].data.values() if d)
        base, ha = res[(cfg, 'base')], res[(cfg, 'ha')]
        kb = int(np.argmax([d['D'] for d in base['dj']])); kh = int(np.argmax([d['D'] for d in ha['dj']]))
        T_dw = float(base['sim']['Tj'][-1].min())
        ton_dom = base['dj'][kb]['ton_dom']
        D_ceil = 1.0 / tt.cips08_nf(Tstar_max - T_dw, T_dw, ton_dom)
        summary[cfg] = dict(
            hottest_base=caches[cfg].tp['names'][kb], D_base=base['dj'][kb]['D'], D_base_low=base['dj'][kb]['D_low'],
            D_base_rip=base['dj'][kb]['D_rip'], dT_base=base['dj'][kb]['dT_max'], Tpeak_base=base['dj'][kb]['Tpeak'],
            rip_base=max(d['rip_max'] for d in base['dj']),
            hottest_ha=caches[cfg].tp['names'][kh], D_ha=ha['dj'][kh]['D'], dT_ha=ha['dj'][kh]['dT_max'],
            Tpeak_ha=ha['dj'][kh]['Tpeak'], gain_ha=base['dj'][kb]['D'] / ha['dj'][kh]['D'],
            Tstar_max=Tstar_max, T_dw=T_dw, ton_dom=ton_dom, D_ceil=D_ceil,
            gain_ceil=base['dj'][kb]['D'] / D_ceil,
            solder_base=max(d['D_rel'] for d in base['ds']), solder_ha=max(d['D_rel'] for d in ha['ds']),
            dTc_base=max(d['dTc_max'] for d in base['ds']), dTc_ha=max(d['dTc_max'] for d in ha['ds']),
            P_inv_kWh=float(base['sim']['P'].sum(1).sum() * 3 * (prof['t'][1] - prof['t'][0]) / 3.6e6),
        )
        if cfg.startswith('SiC'):
            summary[cfg]['D_base_hoffmann'] = max(d['D'] for d in res[(cfg, 'base')]['dj_hoff'])
    sic = summary['SiC-ANPC']
    for si in ('Si-NPC', 'Si-ANPC'):
        s = summary[si]
        s['kappa_bar_bound'] = sic['D_base'] / s['D_ceil']        # Corollary (sufficient threshold)
        s['kappa_bar_LPlaw'] = sic['D_base'] / s['D_ha']          # against the simulated LP law
        s['kappa_implied_hoffmann'] = sic['D_base'] / sic['D_base_hoffmann']
        s['solder_ratio_SiC_vs_SiHA'] = sic['solder_base'] / s['solder_ha']
    tag = os.path.splitext(os.path.basename(fn))[0]
    with open(os.path.join(HERE, f'ketqua_{tag}.json'), 'w') as f:
        json.dump(summary, f, indent=1, default=float)
    for cfg, s in summary.items():
        print(cfg, json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()}))
    # figure: hottest-chip temperature for the three configurations
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    for a, cfg in zip(ax, ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')):
        for tagc, sty in (('base', '-'), ('ha', '--')):
            r = res[(cfg, tagc)]
            k = int(np.argmax([d['D'] for d in r['dj']]))
            a.plot(prof['t'], r['sim']['Tj'][:, k], sty, lw=1, label=f"{tagc}: {caches[cfg].tp['names'][k]}")
            a.fill_between(prof['t'], r['sim']['Tj'][:, k] - r['sim']['rip'][:, k] / 2,
                           r['sim']['Tj'][:, k] + r['sim']['rip'][:, k] / 2, alpha=.15)
        a.set_ylabel('T_j (degC)'); a.set_title(cfg); a.grid(alpha=.3); a.legend(fontsize=8)
    ax[-1].set_xlabel('t (s)')
    fig.tight_layout(); fig.savefig(os.path.join(HERE, f'ketqua_{tag}.png'), dpi=110)


if __name__ == '__main__':
    main(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'hoso_50km.csv'))
