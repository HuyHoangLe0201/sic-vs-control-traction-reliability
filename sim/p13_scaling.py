"""Review item P1-3: validation of the first-order scaling used in the Monte Carlo and Sobol analyses,
T' = T_w + s_R s_P (T - T_w), against complete electro-thermal re-simulations with scaled thermal resistances (chip,
case-sink and heat sink) and scaled losses (baseline policy, reference variant).

python p13_scaling.py  -> p13_scaling.md
"""
import os, numpy as np
import tonhao as th, hanhtrinh as h, donhay
import tran_daodong as td
from mc_b10 import chip_damage_samples

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = [(1.1, 1.1), (0.9, 0.9), (1.1, 0.9), (1.0, 1.1)]


def worst(sim, prof, st):
    dj, _ = h.damages(sim, prof, nf=donhay.nf_setting(st))
    k = int(np.argmax([x['D'] for x in dj]))
    return dj[k]['D'], k


def main():
    L = ['# P1-3: first-order scaling vs complete re-simulation (fvdr, baseline policy)\n',
         '| config | s_R | s_P | rule | D re-simulated | D scaled | ratio scaled/re-simulated |', '|---|---|---|---|---|---|---|']
    for cfg in ('Si-NPC', 'SiC-ANPC'):
        prof = td.apply_variant('fvdr', h.load_profile(os.path.join(HERE, 'hoso_50km_dr.csv')), cfg)
        cache = h.OpCache(cfg)
        sim0 = h.simulate(cfg, prof, cache, 'base')
        tp = cache.tp
        rth0, rcs0 = tp['rth'].copy(), tp['rcs']
        Zf0, Rf0 = th.SINK['Zf'].copy(), th.SINK['Rf'].copy()
        store = {k: (d['base'].copy(), d['base_H'].copy()) for k, d in cache.data.items() if d}
        for sR, sP in CASES:
            tp['rth'] = rth0 * sR; tp['rcs'] = rcs0 * sR
            th.SINK['Zf'] = Zf0 * sR; th.SINK['Rf'] = Rf0 * sR
            for k, d in cache.data.items():
                if d:
                    d['base'] = store[k][0] * sP; d['base_H'] = store[k][1] * sP
            sim = h.simulate(cfg, prof, cache, 'base')
            for st in ('ton_clip', 'ton_free'):
                if st == 'ton_free':
                    import tonthuong as tt; old = tt.TON_RANGE; tt.TON_RANGE = (1e-4, 15.0)
                Dfull, kf = worst(sim, prof, 'ton_clip')
                # scaled nominal history, worst chip over all chips
                s = np.array([sR * sP])
                import tonthuong as tt
                Dsc = max(chip_damage_samples(sim0['Tj'][:, k], sim0['rip'][:, k], prof['fe'], prof['t'], s,
                                              np.array([tt.CIPS['b1']]), np.array([tt.CIPS['b2']]), th.T_WATER)[0]
                          for k in range(tp['nchip']))
                if st == 'ton_free':
                    tt.TON_RANGE = old
                L.append(f'| {cfg} | {sR} | {sP} | {st} | {Dfull:.3g} | {Dsc:.3g} | {Dsc / Dfull:.3f} |')
                print(L[-1], flush=True)
        tp['rth'] = rth0; tp['rcs'] = rcs0; th.SINK['Zf'] = Zf0; th.SINK['Rf'] = Rf0
    open(os.path.join(HERE, 'p13_scaling.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
