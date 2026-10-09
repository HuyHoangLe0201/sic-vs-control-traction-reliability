"""Review item P1-9: sensitivity to the current division in the ANPC 'both paths' zero state.
The bound T*, the mean-temperature law and the single-point min-max ripple r* are recomputed with a 60/40 and a 40/60
division between the upper (D5/T2, D2/T5) and the lower path (T6/D3, T3/D6) instead of 50/50.

python p19_share.py  -> p19_share.md
"""
import os, numpy as np
import tonhao as th, dao_dong as dd

HERE = os.path.dirname(os.path.abspath(__file__))
_topology = th.topology
POINTS = [('start-up', 462.0, 0.10, 0.95, 5.0), ('acceleration', 462.0, 0.30, 0.95, 30.0),
          ('braking', 383.0, 0.17, -0.95, 20.0), ('high speed', 462.0, 0.95, 0.95, 150.0)]


def topo_share(a):
    def f(name):
        tp = _topology(name)
        if tp['topo'] == 'ANPC':
            OU, OL = tp['O']['U'], tp['O']['L']
            tp['O']['B'] = {s: [(r, a) for r, _ in OU[s]] + [(r, 1 - a) for r, _ in OL[s]] for s in (1, -1)}
        return tp
    return f


def point(cfg, I, m, c, fe):
    r = th.analyse_point(cfg, I, m, c, 1500.0, fe=fe)
    tp = r['tp']
    G = dd.ripple_map(tp, th.at_temp(r['L'], r['Tb']), fe)
    Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], r['g'])
    rs = dd.ripple_lp(tp, G, Aeq, beq, npc=r['npc'])[0]
    return r['Tstar'], r['Teq'].max(), rs


def main():
    th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
    L = ['# P1-9: current division in the ANPC both-paths state (upper share 0.5 / 0.6 / 0.4)\n',
         '| config | point | T* (C) | T_eq of mean-temperature law (C) | r* (K) |', '|---|---|---|---|---|']
    for cfg in ('Si-ANPC', 'SiC-ANPC'):
        for lab, I, m, c, fe in POINTS:
            vals = []
            for a in (0.5, 0.6, 0.4):
                th.topology = topo_share(a)
                vals.append(point(cfg, I, m, c, fe))
            th.topology = _topology
            L.append(f'| {cfg} | {lab} | ' + ' / '.join(f'{v[0]:.1f}' for v in vals) + ' | ' +
                     ' / '.join(f'{v[1]:.1f}' for v in vals) + ' | ' + ' / '.join(f'{v[2]:.2f}' for v in vals) + ' |')
            print(L[-1], flush=True)
    open(os.path.join(HERE, 'p19_share.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
