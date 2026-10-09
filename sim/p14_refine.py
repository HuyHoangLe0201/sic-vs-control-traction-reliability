"""Review item P1-4: discretisation of the ripple LP. The single-point min-max ripple r* and the symmetric-pair bounds
rho_o(w) are recomputed with 72 bins, 9 offset levels and 72 angle samples and compared with the default 36/5/36.
A finer grid enlarges the admissible set, so the refined values are the more conservative (lower) bounds.

python p14_refine.py  -> p14_refine.md
"""
import os, numpy as np
import tonhao as th, dao_dong as dd

HERE = os.path.dirname(os.path.abspath(__file__))
POINTS = [('start-up', 462.0, 0.10, 0.95, 5.0), ('acceleration', 462.0, 0.30, 0.95, 30.0),
          ('braking', 383.0, 0.17, -0.95, 20.0), ('high speed', 462.0, 0.95, 0.95, 150.0)]


def setgrid(nbin, noff, nq):
    th.NBIN, th.NOFF, dd.NQ = nbin, noff, nq
    th.BIN = (np.arange(th.NTH) * th.NBIN) // th.NTH


def point(cfg, I, m, c, fe):
    r = th.analyse_point(cfg, I, m, c, 1500.0, fe=fe)
    tp = r['tp']
    LT = th.at_temp(r['L'], r['Tb'])
    G = dd.ripple_map(tp, LT, fe)
    Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], r['g'])
    rstar = dd.ripple_lp(tp, G, Aeq, beq, npc=r['npc'])[0]
    pairs = {nm: dd.ripple_lp(tp, G, Aeq, beq, w, npc=r['npc'])[0] for nm, w in dd.orbits(tp)}
    return rstar, pairs, r['Tstar']


def main():
    th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
    L = ['# P1-4: LP discretisation, default (36 bins, 5 offsets, 36 angles) vs refined (72, 9, 72)\n',
         '| config | point | T* default / refined (C) | r* default / refined (K) | largest pair bound default / refined (K) | '
         'max relative change of pair bounds |', '|---|---|---|---|---|---|']
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        for lab, I, m, c, fe in POINTS:
            setgrid(36, 5, 36)
            r0, p0, T0 = point(cfg, I, m, c, fe)
            setgrid(72, 9, 72)
            r1, p1, T1 = point(cfg, I, m, c, fe)
            rel = max(abs(p1[k] - p0[k]) / max(p0[k], 1e-6) for k in p0 if p0[k] > 0.5) if any(v > 0.5 for v in p0.values()) else 0.0
            L.append(f'| {cfg} | {lab} | {T0:.2f} / {T1:.2f} | {r0:.2f} / {r1:.2f} | {max(p0.values()):.2f} / '
                     f'{max(p1.values()):.2f} | {rel:.3f} |')
            print(L[-1], flush=True)
    setgrid(36, 5, 36)
    open(os.path.join(HERE, 'p14_refine.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
