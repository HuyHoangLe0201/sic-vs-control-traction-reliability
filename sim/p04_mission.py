"""Review round 2 (P0-4): policy-aware pulse-resolved correction of the mission ripple.

For every distinct operating point of a run with f_e >= 4 Hz, the ratio pulsed/averaged of the peak-to-peak ripple of
each chip is computed with xung_policy for the baseline policy, the mean-temperature law and the ripple-aware law, with
two Foster networks: nominal (with the microsecond term, an extrapolation below the datasheet range) and without the
microsecond term (time range of the virtual junction temperature). The stored mission ripple is scaled step by step
and the damage of the most damaged chip is recomputed for both heating-time rules.

python p04_mission.py <cfg> <variant>  -> p04m_<variant>_<cfg>.json
"""
import os, sys, json, time, numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h, donhay
import tran_daodong as td, xung_policy as xp

HERE = os.path.dirname(os.path.abspath(__file__))
FE_MIN = 4.0


def worst(Tj, rip, t, fe, nf):
    dt = t[1] - t[0]
    D = [tt.damage_lowfreq(Tj[:, k], t, nf)[0] + tt.damage_ripple(Tj[:, k], rip[:, k], fe, dt, nf) for k in range(Tj.shape[1])]
    return float(max(D))


def main(cfg, variant):
    pf = 'hoso_50km_dr75.csv' if 'dr75' in variant else ('hoso_50km_dr.csv' if 'dr' in variant else 'hoso_50km.csv')
    prof = td.apply_variant(variant, h.load_profile(os.path.join(HERE, pf)), cfg)
    I, M, C, FE = prof['I'], prof['m'], prof['c'], prof['fe']
    base = h.OpCache(cfg)
    rc = td.RippleCache(cfg, base)
    tp = base.tp
    fos = xp.fosters_of(tp)
    xp.FSW = h.FSW
    Q = {}                                    # key -> {tag: [ratio per foster]}
    t0 = time.time()
    for i in range(len(I)):
        if I[i] <= 0 or FE[i] < FE_MIN:
            continue
        k = base.key(I[i], M[i], C[i], FE[i])
        if k in Q:
            continue
        d0 = base.get(I[i], M[i], C[i], FE[i]); r = d0['r']
        dh = rc.get(I[i], M[i], C[i], FE[i])
        Ik, mk, sk = k[0], max(k[1], 0.01), 0.95 * k[2]
        Q[k] = {}
        for tag, w in (('base', r['wb']), ('ha', r['w_eq']), ('har', dh['w'])):
            q, _, _ = xp.ratio(tp, Ik, mk, sk, FE[i], r['Tb'], w, fosters=fos)
            Q[k][tag] = q
        if len(Q) % 10 == 0:
            print(f'  {len(Q)} points {time.time() - t0:.0f}s', flush=True)
    d = np.load(os.path.join(HERE, f'mophong_{variant}_{cfg}.npz'))
    t, fe = d['t'], d['fe']
    keys = [base.key(I[i], M[i], C[i], FE[i]) if (I[i] > 0 and FE[i] >= FE_MIN) else None for i in range(len(I))]
    out = {}
    for tag in ('base', 'ha', 'har'):
        Tj, rip = d[f'{tag}_Tj'], d[f'{tag}_rip']
        out[tag] = {}
        for fi, fname in enumerate(('nominal', 'no_us_term')):
            fac = np.ones_like(rip)
            for i, k in enumerate(keys):
                if k is not None:
                    fac[i] = Q[k][tag][fi]
            out[tag][fname] = {st: worst(Tj, rip * fac, t, fe, donhay.nf_setting(st)) for st in ('ton_clip', 'ton_free')}
        out[tag]['averaged'] = {st: worst(Tj, rip, t, fe, donhay.nf_setting(st)) for st in ('ton_clip', 'ton_free')}
    json.dump(dict(cfg=cfg, variant=variant, n_points=len(Q), D=out), open(os.path.join(HERE, f'p04m_{variant}_{cfg}.json'), 'w'),
              indent=1)
    print(json.dumps(out, indent=1), flush=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
