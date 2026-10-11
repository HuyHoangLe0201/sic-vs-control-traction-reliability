"""Review item P1-5: ripple bound with the losses evaluated at the coolant temperature T_w instead of the baseline
equilibrium temperatures, and with the ripple map evaluated at the upper edge of each output-frequency band instead of
its centre (the ripple decreases with f_e, so the band centre over-estimates the ripple of the faster steps). Losses that increase with temperature then make the frozen-loss ripple a lower estimate of the
ripple at any operating temperature, which removes the violation found at low utilisation for SiC.
Only the bound is recomputed; the simulations are reused.

python p15_bound.py <cfg> <variant>  -> adds 'bounds_tw' to daodong_<variant>_<cfg>.json
"""
import os, sys, json, time, numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h, dao_dong as dd, donhay
import tran_daodong as td

HERE = os.path.dirname(os.path.abspath(__file__))


def main(cfg, variant):
    pf = 'hoso_50km_dr75.csv' if 'dr75' in variant else ('hoso_50km_dr.csv' if 'dr' in variant else 'hoso_50km.csv')
    prof = td.apply_variant(variant, h.load_profile(os.path.join(HERE, pf)), cfg)
    t, fe = prof['t'], prof['fe']; dt = t[1] - t[0]
    base = h.OpCache(cfg)
    tp = base.tp
    Tw = th.T_WATER
    steps = [i for i in range(len(t)) if prof['I'][i] > 0 and fe[i] >= h.F_EDGES[0]]
    keys = [base.key(prof['I'][i], prof['m'][i], prof['c'][i], fe[i]) for i in steps]
    uniq = {}
    t0 = time.time()
    for i, k in zip(steps, keys):
        if k in uniq:
            continue
        r = base.get(prof['I'][i], prof['m'][i], prof['c'][i], fe[i])['r']
        LT = th.at_temp(r['L'], np.full(tp['nchip'], Tw))
        G = dd.ripple_map(tp, LT, h.F_EDGES[k[4] + 1])      # upper band edge: smallest ripple in the band
        Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], k[3])
        rs, x, rr, st, dual = dd.ripple_lp(tp, G, Aeq, beq, npc=r['npc'])
        pairs = {nm: float(dd.ripple_lp(tp, G, Aeq, beq, w, npc=r['npc'])[0]) for nm, w in dd.orbits(tp)}
        uniq[k] = dict(G=G, Aeq=Aeq, beq=beq, npc=r['npc'], rstar=rs, dual=dual, pairs=pairs)
        if len(uniq) % 20 == 0:
            print(f'  {len(uniq)} points {time.time() - t0:.0f}s', flush=True)
    rhos = {}
    for nm, _ in dd.orbits(tp):
        rhos['pair_' + nm] = np.array([uniq[k]['pairs'][nm] for k in keys])
    top = sorted(uniq.values(), key=lambda d: -d['rstar'])[:2]
    for j, dt_ in enumerate(top):
        memo = {kk: dd.ripple_lp(tp, d['G'], d['Aeq'], d['beq'], dt_['dual'], npc=d['npc'])[0] for kk, d in uniq.items()}
        rhos[f'dual{j}'] = np.array([memo[k] for k in keys])
    n = fe[steps] * dt
    bounds = {}
    for st in ('ton_clip', 'ton_free'):
        f_nf = donhay.nf_setting(st)
        ton = 1.0 / (2 * fe[steps])
        # previous evaluation with the cut-off damage d_c(rho) (not convex; kept for comparison)
        cand_cut = {nm: float(np.sum(np.where(rho >= tt.DT_MIN, n / f_nf(np.maximum(rho, 1e-9), Tw, ton), 0)))
                    for nm, rho in rhos.items()}
        # review MC1: convex minorant h(r) = max(0, d(r) - d(0.5 K)) <= d_c(r), so the bound is valid for the cut-off model
        d05 = n / f_nf(np.full(len(steps), tt.DT_MIN), Tw, ton)
        cand = {nm: float(np.sum(np.maximum(0.0, n / f_nf(np.maximum(rho, 1e-9), Tw, ton) - d05)))
                for nm, rho in rhos.items()}
        bounds[st] = dict(candidates=cand, D_bound_rip=max(cand.values()),
                          candidates_cut=cand_cut, D_bound_rip_cut=max(cand_cut.values()))
    fn = os.path.join(HERE, f'daodong_{variant}_{cfg}.json')
    j = json.load(open(fn))
    j['bounds_tb'] = j.get('bounds_tb', j['bounds'])
    j['bounds_tw'] = bounds
    json.dump(j, open(fn, 'w'), indent=1, default=float)
    for st in bounds:
        b = bounds[st]['D_bound_rip']
        print(cfg, variant, st, 'bound Tw', b, 'old', j['bounds_tb'][st]['D_bound_rip'],
              'har D_rip/bound', j['sim'][f'har|{st}']['D_rip'] / b, flush=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
