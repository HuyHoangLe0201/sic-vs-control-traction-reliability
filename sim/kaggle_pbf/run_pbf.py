"""Kaggle runner for p_bound_fine.py (tightened floor, CAEE point c): the same computation, with the operating points
distributed over all CPU cores. VARIANTS and CFG are set by the build script; output p_bound_fine_<variant>_<cfg>.json/.npz
in /kaggle/working (D_floor_published is filled in locally by gop_bound_fine.py)."""
import os, sys, glob, json, shutil, time, multiprocessing as mp

VARIANTS = ['__VARIANT__']
CFG = '__CFG__'
SRC = glob.glob('/kaggle/input/*/') or glob.glob('/kaggle/input/*/*/')
RUN = '/kaggle/working/run'
os.makedirs(RUN, exist_ok=True)
for d in SRC:
    for f in glob.glob(os.path.join(d, '**', '*'), recursive=True):
        if os.path.isfile(f) and f.endswith(('.py', '.csv', '.npz')):
            shutil.copy(f, RUN)
os.chdir(RUN); sys.path.insert(0, RUN)
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import numpy as np
import tonhao as th, hanhtrinh as h, dao_dong as dd, tran_daodong as td, donhay
from p_bound_fine import floors, RATIO

G_ = {}


def setup(k, i):
    prof, base, tp, Tw, grid, fe = G_['prof'], G_['base'], G_['tp'], G_['Tw'], G_['grid'], G_['fe']
    r = base.get(prof['I'][i], prof['m'][i], prof['c'][i], fe[i])['r']
    LT = th.at_temp(r['L'], np.full(tp['nchip'], Tw))
    G = dd.ripple_map(tp, LT, grid[k[5]])
    Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], k[3])
    return G, Aeq, beq, r['npc']


def phase_a(arg):
    k, i = arg
    G, Aeq, beq, npc = setup(k, i)
    tp = G_['tp']
    rs, x, rr, st, dual = dd.ripple_lp(tp, G, Aeq, beq, npc=npc)
    pairs = {nm: float(dd.ripple_lp(tp, G, Aeq, beq, w, npc=npc)[0]) for nm, w in dd.orbits(tp)}
    return k, dict(i=i, rstar=float(rs), dual=np.asarray(dual), pairs=pairs)


def phase_b(arg):
    k, i, w = arg
    G, Aeq, beq, npc = setup(k, i)
    return k, float(dd.ripple_lp(G_['tp'], G, Aeq, beq, w, npc=npc)[0])


def main(cfg, variant):
    pf = 'hoso_50km_dr75.csv' if 'dr75' in variant else ('hoso_50km_dr.csv' if 'dr' in variant else 'hoso_50km.csv')
    prof = td.apply_variant(variant, h.load_profile(os.path.join(RUN, pf)), cfg)
    t, fe = prof['t'], prof['fe']; dt = t[1] - t[0]
    base = h.OpCache(cfg)
    tp = base.tp
    Tw = th.T_WATER
    grid = 0.5 * RATIO ** np.arange(0, 400)
    G_.update(prof=prof, base=base, tp=tp, Tw=Tw, grid=grid, fe=fe)
    steps = [i for i in range(len(t)) if prof['I'][i] > 0 and fe[i] >= h.F_EDGES[0]]
    keys = [base.key(prof['I'][i], prof['m'][i], prof['c'][i], fe[i]) + (int(np.searchsorted(grid, fe[i])),)
            for i in steps]
    first = {}
    for i, k in zip(steps, keys):
        first.setdefault(k, i)
    t0 = time.time()
    with mp.get_context('fork').Pool(mp.cpu_count()) as pool:
        uniq = dict(pool.map(phase_a, list(first.items()), chunksize=1))
        print(f'{variant} {cfg}: phase A {len(uniq)} points {time.time() - t0:.0f}s', flush=True)
        rhos = {}
        for nm, _ in dd.orbits(tp):
            rhos['pair_' + nm] = np.array([uniq[k]['pairs'][nm] for k in keys])
        top = sorted(uniq.values(), key=lambda d: -d['rstar'])[:2]
        for j, dt_ in enumerate(top):
            memo = dict(pool.map(phase_b, [(k, d['i'], dt_['dual']) for k, d in uniq.items()], chunksize=1))
            rhos[f'dual{j}'] = np.array([memo[k] for k in keys])
            print(f'  dual{j} {time.time() - t0:.0f}s', flush=True)
    n = fe[steps] * dt
    ton = 1.0 / (2 * fe[steps])
    out = dict(cfg=cfg, variant=variant, ratio=RATIO, n_points=len(uniq), time_s=time.time() - t0,
               cpus=mp.cpu_count(), host='kaggle', bounds={})
    for st in ('ton_clip', 'ton_free'):
        cand, best, arg = floors(rhos, n, Tw, ton, donhay.nf_setting(st))
        out['bounds'][st] = dict(candidates=cand, D_floor_pairs=max(cand.values()), D_floor=best, argmax=arg,
                                 D_floor_published=None)
        print(cfg, variant, st, best, arg, flush=True)
    np.savez_compressed(f'/kaggle/working/p_bound_fine_{variant}_{cfg}.npz', steps=np.array(steps), **rhos)
    json.dump(out, open(f'/kaggle/working/p_bound_fine_{variant}_{cfg}.json', 'w'), indent=1, default=float)


if __name__ == '__main__':
    for v in VARIANTS:
        main(CFG, v)
