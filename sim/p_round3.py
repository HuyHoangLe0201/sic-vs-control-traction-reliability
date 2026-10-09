"""External comments (2026-10-09), major concerns 1, 3, 4.

MC1  Frozen-loss ripple bound: for random admissible policies (vertices of X(o) and mixtures) and for chip temperatures
     between T_w and 150 C (uniform levels and random per chip), compare the ripple r_k(x;T) with the frozen value
     r_k(x;T_w); also compare the pair bounds rho_o(w) evaluated at T with those at T_w. Also report the spread of the
     relative temperature coefficient over the period, the sufficient condition for exact conservativeness.
MC3  Asymmetry of the ripple waveform: true minimum of the periodic component versus -r/2, and the resulting factor on the
     CIPS08 damage of that cycle.
MC4  Rate of zero-level-path changes in the carrier-period realisation of the ripple-aware law.

python p_round3.py -> p_round3.md
"""
import os, numpy as np
from scipy.optimize import linprog
from scipy import sparse
import tonhao as th, dao_dong as dd, tonthuong as tt, xung_policy as xp

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(3)
POINTS = [('start-up 5 Hz', 340.8, 0.040, 0.95, 4.75), ('10 Hz', 455.2, 0.082, 0.95, 9.7), ('20 Hz', 462.0, 0.167, 0.95, 19.7),
          ('30 Hz', 462.0, 0.253, 0.95, 29.8), ('60 Hz', 462.0, 0.49, 0.95, 57.1), ('150 Hz', 462.0, 0.95, 0.95, 147.1),
          ('brake 20 Hz', 382.8, 0.171, -0.95, 20.2)]
NV = 40   # random vertices per point


def polytope(tp, r):
    Aeq, beq, nv = dd.eq_constraints(tp, r['inpb'], r['g'])
    A_ub, b_ub = (r['npc'] if r['npc'] is not None else (None, None))
    return Aeq, beq, nv, A_ub, b_ub


def vertices(Aeq, beq, nv, A_ub, b_ub, n):
    out = []
    for _ in range(n):
        res = linprog(rng.normal(size=nv), A_eq=Aeq, b_eq=beq, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * nv, method='highs')
        if res.status == 0:
            out.append(res.x)
    return out


def ranges(G, x):
    w = G @ x
    return w.max(1) - w.min(1), w.min(1)


def main():
    th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
    L = ['# Round-3 checks (external comments MC1, MC3, MC4)\n']
    L1 = ['## MC1: ripple at temperature T relative to the frozen ripple at T_w (chips with r(T_w) > 0.5 K)\n',
          '| config | point | policies | min ratio r(T)/r(T_w) over T in {T_b, 125, 150, random} | share of cases < 1 | '
          'min ratio of pair bounds rho_T / rho_Tw | spread of relative tempco over the period (max chip) |',
          '|---|---|---|---|---|---|---|']
    L3 = ['\n## MC3: asymmetry of the ripple waveform (worst chip per policy)\n',
          '| config | point | policy | r (K) | min of periodic part (K) | -r/2 (K) | damage factor true/approx (T_min) |',
          '|---|---|---|---|---|---|---|']
    L4 = ['\n## MC4: zero-level path changes per second in the realised ripple-aware law (per leg)\n',
          '| config | point | path changes per s | carrier periods per s | share of zero-level time in both-paths state |',
          '|---|---|---|---|---|']
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        for lab, I, m, c, fe in POINTS:
            r = th.analyse_point(cfg, I, m, c, 1500.0, fe=fe)
            tp = r['tp']; nc = tp['nchip']
            Aeq, beq, nv, A_ub, b_ub = polytope(tp, r)
            V = vertices(Aeq, beq, nv, A_ub, b_ub, NV)
            X = V + [np.mean([V[i] for i in rng.choice(len(V), 4, replace=False)], axis=0) for _ in range(NV)]
            Gw = dd.ripple_map(tp, th.at_temp(r['L'], np.full(nc, th.T_WATER)), fe)
            temps = [r['Tb'], np.full(nc, 125.0), np.full(nc, 150.0)] + [rng.uniform(th.T_WATER, 150.0, nc) for _ in range(3)]
            Gs = [dd.ripple_map(tp, th.at_temp(r['L'], T), fe) for T in temps]
            ratios = []
            for x in X:
                r0, _ = ranges(Gw, x)
                m0 = r0 > 0.5
                for G in Gs:
                    r1, _ = ranges(G, x)
                    ratios.extend((r1[m0] / r0[m0]).tolist())
            ratios = np.array(ratios)
            # pair bounds at T_b and 150 C versus T_w
            pr = []
            for G in Gs[:3]:
                for nm, w in dd.orbits(tp):
                    a = dd.ripple_lp(tp, Gw, Aeq, beq, w, npc=r['npc'])[0]
                    if a > 0.5:
                        pr.append(dd.ripple_lp(tp, G, Aeq, beq, w, npc=r['npc'])[0] / a)
            # spread of the relative temperature coefficient of the chip loss over the period (baseline policy)
            Lb = th.bin_avg(r['L'])                                     # [NOFF,NOT,NBIN,nchip,3]
            p25 = np.einsum('bro,robk->bk', r['wb'], Lb[..., 0]); p125 = np.einsum('bro,robk->bk', r['wb'], Lb[..., 1])
            cc = np.where(p25 > 1e-3 * p25.max(0), (p125 / np.maximum(p25, 1e-9) - 1) / 100.0, np.nan)
            spread = np.nanmax([np.nanmax(cc[:, k]) - np.nanmin(cc[:, k]) for k in range(nc) if np.isfinite(cc[:, k]).any()])
            L1.append(f'| {cfg} | {lab} | {len(X)} | {ratios.min():.3f} | {np.mean(ratios < 1):.3f} | '
                      f'{min(pr) if pr else float("nan"):.3f} | {spread * 1e3:.2f}e-3 /K |')
            print(L1[-1], flush=True)
            # MC3 on the three policies at the baseline temperatures
            Gb = dd.ripple_map(tp, th.at_temp(r['L'], r['Tb']), fe)
            rs, xh, _, _, _ = dd.ripple_lp(tp, Gb, Aeq, beq, npc=r['npc'])
            for nm, x in (('base', r['wb'].reshape(-1)), ('ha', r['w_eq'].reshape(-1)), ('har', xh)):
                rr, mn = ranges(Gb, x)
                k = int(np.argmax(rr))
                Tm = r['Tb'][k] + 273.15
                b2 = tt.CIPS['b2']
                fac = np.exp(b2 / (Tm - rr[k] / 2) - b2 / (Tm + mn[k]))   # d_true / d_approx = N_approx / N_true
                L3.append(f'| {cfg} | {lab} | {nm} | {rr[k]:.2f} | {mn[k]:.2f} | {-rr[k] / 2:.2f} | {fac:.3f} |')
            # MC4 path changes (ANPC only)
            if tp['topo'] == 'ANPC':
                w = xh.reshape(th.NBIN, th.NOFF, len(tp['otypes']))
                n = 4 if fe < 40 else 12
                t = np.arange(int(n / fe * xp.FSW)) / xp.FSW
                thc = (2 * np.pi * fe * (t + 0.5 / xp.FSW)) % (2 * np.pi)
                bc = np.minimum((thc / (2 * np.pi) * th.NBIN).astype(int), th.NBIN - 1)
                kc = np.arange(len(t))
                pos = (kc * 0.6180339887498949) % 1.0
                wf = w.reshape(th.NBIN, -1); cum = np.cumsum(wf, 1); cum = cum / cum[:, -1:]
                ch = np.minimum(np.array([np.searchsorted(cum[b], p, side='right') for b, p in zip(bc, pos)]), wf.shape[1] - 1)
                path = ch % len(tp['otypes'])
                changes = np.sum(path[1:] != path[:-1]) / (len(t) / xp.FSW)
                shareB = w[:, :, 2].sum() / w.sum()
                L4.append(f'| {cfg} | {lab} | {changes:.0f} | {xp.FSW:.0f} | {shareB:.2f} |')
    out = '\n'.join(L + L1 + L3 + L4) + '\n'
    open(os.path.join(HERE, 'p_round3.md'), 'w', encoding='utf-8').write(out)
    print(out)


if __name__ == '__main__':
    main()
