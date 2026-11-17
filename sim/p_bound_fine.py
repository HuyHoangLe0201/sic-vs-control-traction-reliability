"""Tightened damage floor (CAEE editor point c), base case.

The published floor (p15_bound.py, 'bounds_tw') evaluates the ripple map at the upper edge of 16 output-frequency bands
(band ratio 1.5). Here the map is evaluated at the smallest point of a fine geometric grid (ratio RATIO) that is not
below the actual output frequency of each step; since the ripple decreases with f_e, the floor stays valid and the
frequency slack falls from a factor 1.5 to RATIO. Everything else is unchanged (losses at the coolant temperature,
cycle minimum at the coolant temperature, convex minorant of the cut-off damage, NP and decision-interval constraints).

Chip weighting: rho_w(t) = min_x w.r(x) is concave in w, so for a mixture w = sum a_j w_j of candidate weightings
rho_w(t) >= sum a_j rho_wj(t); the floor is therefore also maximised over mixtures of the candidates (pairs + duals)
with the per-step value replaced by the mixture of the candidate values, which remains a valid floor.

python p_bound_fine.py <cfg> [variant]  -> p_bound_fine_<variant>_<cfg>.json / .npz (per-step rho of each candidate)
"""
import os, sys, json, time, itertools
import numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h, dao_dong as dd, donhay
import tran_daodong as td

HERE = os.path.dirname(os.path.abspath(__file__))
RATIO = 1.02


def floors(rhos, n, Tw, ton, f_nf):
    d05 = n / f_nf(np.full(len(n), tt.DT_MIN), Tw, ton)
    hfun = lambda rho: float(np.sum(np.maximum(0.0, n / f_nf(np.maximum(rho, 1e-9), Tw, ton) - d05)))
    cand = {nm: hfun(rho) for nm, rho in rhos.items()}
    names = [k for k in rhos if cand[k] > 0]
    best, arg = max(cand.values()), max(cand, key=cand.get)
    # mixtures of two and three candidates on a grid of weights 0.05
    grid = np.linspace(0, 1, 21)
    for a, b in itertools.combinations(names, 2):
        for al in grid[1:-1]:
            v = hfun(al * rhos[a] + (1 - al) * rhos[b])
            if v > best:
                best, arg = v, f'{al:.2f}*{a}+{1 - al:.2f}*{b}'
    for a, b, c in itertools.combinations(names, 3):
        for al in grid[1:-1]:
            for be in grid[1:-1]:
                if al + be >= 1:
                    continue
                v = hfun(al * rhos[a] + be * rhos[b] + (1 - al - be) * rhos[c])
                if v > best:
                    best, arg = v, f'{al:.2f}*{a}+{be:.2f}*{b}+{1 - al - be:.2f}*{c}'
    return cand, best, arg


def main(cfg, variant='fvdr'):
    pf = 'hoso_50km_dr75.csv' if 'dr75' in variant else ('hoso_50km_dr.csv' if 'dr' in variant else 'hoso_50km.csv')
    prof = td.apply_variant(variant, h.load_profile(os.path.join(HERE, pf)), cfg)
    t, fe = prof['t'], prof['fe']; dt = t[1] - t[0]
    base = h.OpCache(cfg)
    tp = base.tp
    Tw = th.T_WATER
    grid = 0.5 * RATIO ** np.arange(0, 400)
    steps = [i for i in range(len(t)) if prof['I'][i] > 0 and fe[i] >= h.F_EDGES[0]]
    keys = [base.key(prof['I'][i], prof['m'][i], prof['c'][i], fe[i]) + (int(np.searchsorted(grid, fe[i])),)
            for i in steps]
    uniq = {}
    t0 = time.time()

    def setup(k, i):
        r = base.get(prof['I'][i], prof['m'][i], prof['c'][i], fe[i])['r']
        LT = th.at_temp(r['L'], np.full(tp['nchip'], Tw))
        G = dd.ripple_map(tp, LT, grid[k[5]])          # grid point >= f_e: ripple not above the true one
        Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], k[3])
        return G, Aeq, beq, r['npc']

    def rho_w(k, i, w):
        G, Aeq, beq, npc = setup(k, i)
        return float(dd.ripple_lp(tp, G, Aeq, beq, w, npc=npc)[0])
    for i, k in zip(steps, keys):
        if k in uniq:
            continue
        r = base.get(prof['I'][i], prof['m'][i], prof['c'][i], fe[i])['r']
        LT = th.at_temp(r['L'], np.full(tp['nchip'], Tw))
        G = dd.ripple_map(tp, LT, grid[k[5]])          # grid point >= f_e: ripple not above the true one
        Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], k[3])
        rs, x, rr, st, dual = dd.ripple_lp(tp, G, Aeq, beq, npc=r['npc'])
        pairs = {nm: float(dd.ripple_lp(tp, G, Aeq, beq, w, npc=r['npc'])[0]) for nm, w in dd.orbits(tp)}
        uniq[k] = dict(i=i, rstar=rs, dual=dual, pairs=pairs)     # G not stored (about 4 MB per point)
        if len(uniq) % 25 == 0:
            print(f'  {len(uniq)} points {time.time() - t0:.0f}s', flush=True)
    rhos = {}
    for nm, _ in dd.orbits(tp):
        rhos['pair_' + nm] = np.array([uniq[k]['pairs'][nm] for k in keys])
    top = sorted(uniq.values(), key=lambda d: -d['rstar'])[:2]
    for j, dt_ in enumerate(top):
        memo = {kk: rho_w(kk, d['i'], dt_['dual']) for kk, d in uniq.items()}
        rhos[f'dual{j}'] = np.array([memo[k] for k in keys])
    n = fe[steps] * dt
    ton = 1.0 / (2 * fe[steps])
    old = json.load(open(os.path.join(HERE, f'daodong_{variant}_{cfg}.json')))
    out = dict(cfg=cfg, variant=variant, ratio=RATIO, n_points=len(uniq), time_s=time.time() - t0, bounds={})
    for st in ('ton_clip', 'ton_free'):
        cand, best, arg = floors(rhos, n, Tw, ton, donhay.nf_setting(st))
        out['bounds'][st] = dict(candidates=cand, D_floor_pairs=max(cand.values()), D_floor=best, argmax=arg,
                                 D_floor_published=old['bounds_tw'][st]['D_bound_rip'])
        print(cfg, st, out['bounds'][st], flush=True)
    np.savez_compressed(os.path.join(HERE, f'p_bound_fine_{variant}_{cfg}.npz'), steps=np.array(steps), **rhos)
    json.dump(out, open(os.path.join(HERE, f'p_bound_fine_{variant}_{cfg}.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'fvdr')
