"""R3b on the mission: ripple-aware control law ('har') and the ripple ceiling (lower bound on the
worst-chip per-trip damage for any law acting through redundant states).

python tran_daodong.py <cfg>        -> daodong_<cfg>.json
"""
import os, sys, json, time, numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h, dao_dong as dd

HERE = os.path.dirname(os.path.abspath(__file__))
F_EDGES, F_MID = h.F_EDGES, h.F_MID
TIE_EPS = 0.02      # ripple slack of the two-stage tie-break (review P0-12)


class RippleCache:
    def __init__(self, cfg, base):
        self.base, self.tp, self.Z = base, base.tp, base.Z
        self.data = {}

    def get(self, I, m, c, fe=None):
        d0 = self.base.get(I, m, c, fe)
        if d0 is None:
            return None
        if fe is None or fe < F_EDGES[0]:
            return dict(har=d0['ha'], har_H=d0['ha_H'], rstar=None, dV_har=d0['dV_ha'])
        k = self.base.key(I, m, c, fe)
        fb = k[4]
        if k in self.data:
            return self.data[k]
        g = k[3]                                      # realisable decision-interval grouping (P0-2)
        r = d0['r']
        LT = th.at_temp(r['L'], r['Tb'])
        G = dd.ripple_map(self.tp, LT, F_MID[fb])
        Aeq, beq, nv = dd.eq_constraints(self.tp, r['inpb'], g)
        Lb = th.bin_avg(LT)                                                  # [NOFF,NOT,NBIN,nchip]
        Mp = np.transpose(Lb, (3, 2, 0, 1)).reshape(self.tp['nchip'], -1) / th.NBIN
        tie = (self.Z @ Mp, th.T_WATER, TIE_EPS)
        rstar, x, rr, st, dual = dd.ripple_lp(self.tp, G, Aeq, beq, npc=r['npc'], tie=tie)
        w = x.reshape(th.NBIN, th.NOFF, len(self.tp['otypes']))
        tab, H = h.policy_tables(r['L'], w, r['Tb'])
        xb = r['wb'].reshape(-1)
        rb = (G @ xb).max(1) - (G @ xb).min(1)
        pairs = {}
        for nm, wv in dd.orbits(self.tp):
            if wv @ rb < 0.3:
                pairs[nm] = float(wv @ rb)          # negligible: baseline value is an upper bound anyway
                continue
            pairs[nm] = float(dd.ripple_lp(self.tp, G, Aeq, beq, wv, npc=r['npc'])[0])
        dVh = None if r['Q'] is None else th.np_ripple(r['Q'], x)
        d = dict(har=tab, har_H=H, rstar=float(rstar), lp=int(st), dual=dual, pairs=pairs, w=w,
                 src=(I, m, c, fb, fe, g), rb_max=float(rb.max()), dV_har=dVh, Tpk_har=float((tie[0] @ x).max() + th.T_WATER))
        self.data[k] = d
        if len(self.data) % 10 == 0:
            print(f'  ripple points: {len(self.data)} (last I={I:.0f} m={m:.2f} fe={fe:.1f} g={g})', flush=True)
        return d

    def rho(self, d, wv):
        I, m, c, fb, fe, g = d['src']
        r = self.base.get(I, m, c, fe)['r']
        G = dd.ripple_map(self.tp, th.at_temp(r['L'], r['Tb']), F_MID[fb])
        Aeq, beq, _ = dd.eq_constraints(self.tp, r['inpb'], g)
        return float(dd.ripple_lp(self.tp, G, Aeq, beq, wv, npc=r['npc'])[0])


def apply_variant(variant, prof, cfg=None):
    import donhay, re
    if '_esw' in variant:  # review P1-8: Si switching energies below 125 C extrapolated linearly from the 125/150 C
        import linhkien as lk  # datasheet curves (floor at 50 % of the 125 C value) instead of being held at 125 C
        def ext(f):
            def g(i, T, V):
                if T >= 125:
                    return f(i, T, V)
                e125, e150 = f(i, 125.0, V), f(i, 150.0, V)
                return np.maximum(e125 + (e150 - e125) * (T - 125.0) / 25.0, 0.5 * e125)
            return g
        esw = ext(lambda i, T, V: lk.si_eon(i, T, V) + lk.si_eoff(i, T, V))
        th.TECH['Si']['eT'] = esw
        th.TECH['Si']['eD'] = ext(lk.si_err)
    mt = re.search(r'_tw(\d+)', variant)
    if mt:                 # coolant temperature variant on the final model (review P0-10)
        th.T_WATER = float(mt.group(1))
    ms = re.search(r'_sic(\d+(?:\.\d+)?)k', variant)
    if ms and cfg is not None and cfg.startswith('SiC'):   # SiC switching frequency (Si keeps 1.5 kHz)
        h.FSW = 1000.0 * float(ms.group(1))
    if variant == 'ilim':
        prof = donhay.limit_current(prof)
    elif variant == 'rhw5':
        th.R_HW = 5e-3
    elif variant == 'rhw20':
        th.R_HW = 20e-3
    elif variant == 'tw60':
        th.T_WATER = 60.0
    elif variant == 'sic5k':
        h.FSW = 5000.0
    if 'par' in variant:   # two modules in parallel per switch: each chip carries half the current
        prof = dict(prof); prof['I'] = prof['I'] / 2.0
    if '_u' in variant:    # utilisation sweep: peak current = u x 600 A rating, same module and heat sink
        u = float(variant.split('_u')[1])
        prof = dict(prof); prof['I'] = prof['I'] * u * 600.0 / 462.0
    if variant.startswith('fv'):   # finite-volume heat sink; suffix after '_' selects a sink variant file
        sub = variant.split('_', 1)[1] if '_' in variant else None
        if sub is not None and sub.startswith(('u', 'tw', 'sic', 'esw')):
            sub = None
        th.use_sink(os.path.join(HERE, 'tannhiet_step.npz' if sub is None else f'tannhiet_step_{sub}.npz'))
    return prof


def main(cfg, variant='base'):
    import donhay
    pf = 'hoso_50km_dr75.csv' if 'dr75' in variant else ('hoso_50km_dr.csv' if 'dr' in variant else 'hoso_50km.csv')
    prof = h.load_profile(os.path.join(HERE, pf))
    prof = apply_variant(variant, prof, cfg)
    t, dt, fe = prof['t'], prof['t'][1] - prof['t'][0], prof['fe']
    base = h.OpCache(cfg)
    rc = RippleCache(cfg, base)
    t0 = time.time()
    sims = {}
    for tag, cache in (('base', base), ('ha', base), ('har', rc)):
        sims[tag] = h.simulate(cfg, prof, cache, tag)
        print(cfg, tag, f'{time.time()-t0:.0f}s', len(rc.data), flush=True)
    settings = donhay.SETTINGS_SIC if cfg.startswith('SiC') else donhay.SETTINGS_SI
    res = {}
    for tag, sim in sims.items():
        for st in settings:
            dj, ds = h.damages(sim, prof, nf=donhay.nf_setting(st))
            k = int(np.argmax([x['D'] for x in dj]))
            res[f'{tag}|{st}'] = dict(chip=base.tp['names'][k], D=dj[k]['D'], D_low=dj[k]['D_low'],
                                      D_rip=dj[k]['D_rip'], rip_max=max(x['rip_max'] for x in dj),
                                      solder=max(x['D_rel'] for x in ds))
    # ---- ripple ceiling: candidate fixed weights = symmetric pairs + duals at the heaviest points
    steps = [i for i in range(len(t)) if prof['I'][i] > 0 and fe[i] >= F_EDGES[0]]
    dsteps = [rc.get(prof['I'][i], prof['m'][i], prof['c'][i], fe[i]) for i in steps]
    n = fe[steps] * dt
    Tw = th.T_WATER
    rhos = {}
    for nm in dd.orbits(base.tp):
        rhos['pair_' + nm[0]] = np.array([d['pairs'][nm[0]] for d in dsteps])
    # dual weights from the two points with the largest law ripple
    uniq = {}
    for d in dsteps:
        uniq[id(d)] = d
    top = sorted(uniq.values(), key=lambda d: -d['rstar'])[:2]
    for j, dtop in enumerate(top):
        wv = dtop['dual']
        memo = {}
        for d in uniq.values():                      # one LP per distinct operating point
            memo[id(d)] = rc.rho(d, wv)
        rhos[f'dual{j}'] = np.array([memo[id(d)] for d in dsteps])
    bounds = {}
    for st in ('ton_clip', 'ton_free'):
        f_nf = donhay.nf_setting(st)
        cand = {nm: float(np.sum(np.where(rho >= tt.DT_MIN, n / f_nf(np.maximum(rho, 1e-9), Tw, 1.0 / (2 * fe[steps])), 0)))
                for nm, rho in rhos.items()}
        bounds[st] = dict(candidates=cand, D_bound_rip=max(cand.values()))
    # neutral-point voltage ripple (V p-p, worst step) and inverter loss energy per trip (3 legs), review P0-3
    nps = {tag: dict(dV_max=float(sims[tag]['dV'].max()),
                     dV_p99=float(np.percentile(sims[tag]['dV'][sims[tag]['dV'] > 0], 99)) if (sims[tag]['dV'] > 0).any() else 0.0,
                     E_loss_MJ=float(3 * sims[tag]['P'].sum() * dt / 1e6)) for tag in sims}
    out = dict(cfg=cfg, variant=variant, sim=res, bounds=bounds, n_points=len(rc.data), np=nps,
               dv_spec=th.DV_NP_SPEC, c_np=th.C_NP, tie_eps=TIE_EPS)
    np.savez_compressed(os.path.join(HERE, f'mophong_{variant}_{cfg}.npz'), t=t, fe=fe,
                        **{f'{tag}_{k}': sims[tag][k] for tag in sims for k in ('Tj', 'Tc', 'rip', 'P', 'dV')},
                        names=np.array(base.tp['names']))
    with open(os.path.join(HERE, f'daodong_{variant}_{cfg}.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps(out, indent=1, default=lambda v: float(v)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'base')
