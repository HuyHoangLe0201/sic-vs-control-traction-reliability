"""External comment MC3: mission damage with the true minimum of the ripple waveform instead of T_mean - r/2.
For every operating point and policy, the periodic component is reconstructed from the same 12 loss harmonics used in the
mission simulation; its minimum relative to the range, a_k = -min/r, replaces 1/2 in T_min = T_mean - a_k r.

python p_tmin_mission.py <cfg> [variant]  -> ptmin_<variant>_<cfg>.json
"""
import os, sys, json, numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h, donhay
import tran_daodong as td

HERE = os.path.dirname(os.path.abspath(__file__))


def asym(H, rth, foster, fe):
    R, tau = foster
    hh = np.arange(1, H.shape[0] + 1)
    Zh = (R[None, :] / (1 + 1j * 2 * np.pi * fe * hh[:, None] * tau[None, :])).sum(1)
    q = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    T = np.real(np.einsum('hk,h,hq->qk', H, Zh, np.exp(1j * np.outer(hh, q)))) * rth[None, :]
    r = T.max(0) - T.min(0)
    return np.where(r > 1e-6, -T.min(0) / np.maximum(r, 1e-9), 0.5)


def damage(Tj, rip, a, t, fe, nf):
    dt = t[1] - t[0]
    out = []
    for k in range(Tj.shape[1]):
        Dl = tt.damage_lowfreq(Tj[:, k], t, nf)[0]
        m = rip[:, k] >= tt.DT_MIN
        ton = 1.0 / (2.0 * np.maximum(fe[m], 1e-3))
        Dr = float(np.sum(fe[m] * dt / nf(rip[m, k], Tj[m, k] - a[m, k] * rip[m, k], ton)))
        out.append(Dl + Dr)
    return max(out)


def main(cfg, variant='fvdr'):
    pf = 'hoso_50km_dr.csv'
    prof = td.apply_variant(variant, h.load_profile(os.path.join(HERE, pf)), cfg)
    base = h.OpCache(cfg); rc = td.RippleCache(cfg, base); tp = base.tp
    d = np.load(os.path.join(HERE, f'mophong_{variant}_{cfg}.npz'))
    t, fe = d['t'], d['fe']
    A = {tag: np.full(d['base_rip'].shape, 0.5) for tag in ('base', 'ha', 'har')}
    memo = {}
    for i in range(len(t)):
        I, m, c, f = prof['I'][i], prof['m'][i], prof['c'][i], prof['fe'][i]
        if I <= 0 or f < 0.5:
            continue
        k = base.key(I, m, c, f)
        if k not in memo:
            d0 = base.get(I, m, c, f); dh = rc.get(I, m, c, f)
            memo[k] = {'base': d0['base_H'], 'ha': d0['ha_H'], 'har': dh['har_H']}
        for tag in A:
            A[tag][i] = asym(memo[k][tag], tp['rth'], tp['foster'], f)
    out = {}
    for tag in A:
        out[tag] = {}
        for st in ('ton_clip', 'ton_free'):
            nf = donhay.nf_setting(st)
            out[tag][st] = dict(sym=damage(d[f'{tag}_Tj'], d[f'{tag}_rip'], np.full_like(A[tag], 0.5), t, fe, nf),
                                true=damage(d[f'{tag}_Tj'], d[f'{tag}_rip'], A[tag], t, fe, nf))
    json.dump(out, open(os.path.join(HERE, f'ptmin_{variant}_{cfg}.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1), flush=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'fvdr')
