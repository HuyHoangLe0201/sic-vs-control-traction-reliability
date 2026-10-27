"""Size and solve time of the linear programs (for the computational-implementation paragraph of the CAEE version).

At mission operating points of the base case (variant fvdr), the min-max ripple program of the ripple-aware law and the
mean-temperature program are built and solved as in tran_daodong.RippleCache and tonhao, and their size (variables,
constraints, non-zeros) and wall-clock time are recorded.
python p_lp_timing.py -> p_lp_timing.md
"""
import os, time, json
import numpy as np
import tonhao as th, hanhtrinh as h, tran_daodong as td, dao_dong as dd

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
    prof = td.apply_variant('fvdr', h.load_profile(os.path.join(HERE, 'hoso_50km_dr.csv')), cfg)
    I, M, C, FE = prof['I'], prof['m'], prof['c'], prof['fe']
    base = h.OpCache(cfg)
    tp = base.tp
    idx = [i for i in range(len(I)) if I[i] > 0 and FE[i] >= td.F_EDGES[0]]
    pick = [idx[int(q * (len(idx) - 1))] for q in (0.05, 0.3, 0.6, 0.95)]
    for i in pick:
        t0 = time.perf_counter()
        d0 = base.get(I[i], M[i], C[i], FE[i])
        t_base = time.perf_counter() - t0                 # loss tables + mean-temperature LP (T*) at this point
        k = base.key(I[i], M[i], C[i], FE[i])
        r = d0['r']
        LT = th.at_temp(r['L'], r['Tb'])
        G = dd.ripple_map(tp, LT, td.F_MID[k[4]])
        Aeq, beq, nv = dd.eq_constraints(tp, r['inpb'], k[3])
        t0 = time.perf_counter()
        rstar, x, rr, st, dual = dd.ripple_lp(tp, G, Aeq, beq, npc=r['npc'])
        t_lp = time.perf_counter() - t0
        rows.append(dict(cfg=cfg, I=float(I[i]), fe=float(FE[i]), n_policy=int(nv), n_angles=int(G.shape[1]),
                         n_eq=int(Aeq.shape[0]), t_point=t_base, t_ripple_lp=t_lp, status=int(st)))
        print(rows[-1], flush=True)
json.dump(rows, open(os.path.join(HERE, 'p_lp_timing.json'), 'w'), indent=1)
L = ['| config | I (A) | f_e (Hz) | policy variables | angles | equality rows | point set-up incl. T* LP (s) | min-max ripple LP (s) |',
     '|---|---|---|---|---|---|---|---|']
L += [f"| {x['cfg']} | {x['I']:.0f} | {x['fe']:.1f} | {x['n_policy']} | {x['n_angles']} | {x['n_eq']} | {x['t_point']:.2f} | {x['t_ripple_lp']:.2f} |" for x in rows]
open(os.path.join(HERE, 'p_lp_timing.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
