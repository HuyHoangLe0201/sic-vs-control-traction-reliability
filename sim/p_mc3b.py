"""Review round 5: error of the amplitude correction of the pulse-resolved model over a wider set of mission operating
points and all three policies (baseline, mean-temperature law, ripple-aware law), extending p_mc3.py.

For operating points taken from the mission (base case, f_e >= 20 Hz, spread over the output-frequency range, motoring
and braking), the damage per output period of the single corrected cycle (range r_p, T_min = Tbar - r_p/2,
t_on = 1/(2 f_e)) is compared with rainflow counting of the resolved waveform, for the most loaded chip, both thermal
networks and both heating-time rules.

python p_mc3b.py <cfg>  -> p_mc3b_<cfg>.json ;  python p_mc3b.py summary -> p_mc3b.md
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NETS = ('nominal', 'no us term')
FE_SET = (20.0, 50.0, 100.0, 147.0, 200.0, 250.0)


def run(cfg):
    import tonhao as th, tonthuong as tt, hanhtrinh as h, donhay
    import tran_daodong as td, xung_policy as xp
    prof = td.apply_variant('fvdr', h.load_profile(os.path.join(HERE, 'hoso_50km_dr.csv')), cfg)
    I, M, C, FE = prof['I'], prof['m'], prof['c'], prof['fe']
    base = h.OpCache(cfg)
    rc = td.RippleCache(cfg, base)
    tp = base.tp
    fos = xp.fosters_of(tp)
    xp.FSW = h.FSW
    # one motoring and one braking point near each target output frequency, at the largest current there
    pts = []
    for sgn in (1, -1):
        for fe0 in FE_SET:
            idx = [i for i in range(len(I)) if I[i] > 0 and np.sign(C[i]) == sgn and abs(FE[i] - fe0) <= 0.08 * fe0]
            if idx:
                i = max(idx, key=lambda j: I[j])
                pts.append(i)
    rows = []
    for i in pts:
        k = base.key(I[i], M[i], C[i], FE[i])
        d0 = base.get(I[i], M[i], C[i], FE[i]); r = d0['r']
        dh = rc.get(I[i], M[i], C[i], FE[i])
        Ik, mk, sk, fe = k[0], max(k[1], 0.01), 0.95 * k[2], float(FE[i])
        for pname, w in (('baseline', r['wb']), ('mean-temperature law', r['w_eq']), ('ripple-aware law', dh['w'])):
            rp, _, t, wp = xp.policy_ripple(tp, Ik, mk, sk, fe, r['Tb'], w, pulsed=True, fosters=fos, wave=True)
            ra, _, _, wa = xp.policy_ripple(tp, Ik, mk, sk, fe, r['Tb'], w, pulsed=False, fosters=fos, wave=True)
            nper = int(round((t[-1] + (t[1] - t[0])) * fe))
            per = int(round(1 / fe / (t[1] - t[0])))
            sl = slice((2 if nper > 4 else 1) * per, nper * per)
            for inet, nt in enumerate(NETS):
                kk = int(np.argmax(ra[inet]))
                Tm = r['Tb'][kk]
                for st in ('ton_clip', 'ton_free'):
                    nf = donhay.nf_setting(st)
                    d_corr = 0.0 if rp[inet][kk] < tt.DT_MIN else 1.0 / nf(rp[inet][kk], Tm - rp[inet][kk] / 2, 1 / (2 * fe))
                    y = wp[inet][sl, kk]
                    D, _ = tt.damage_lowfreq(Tm + y - y.mean(), t[sl], nf=nf, closed=True)
                    d_rf = D / (t[sl][-1] - t[sl][0] + (t[1] - t[0])) / fe
                    rows.append(dict(cfg=cfg, I=float(Ik), m=float(mk), cos=float(sk), fe=fe, policy=pname, chip=tp['names'][kk],
                                     net=nt, rule=st, r_a=float(ra[inet][kk]), r_p=float(rp[inet][kk]),
                                     ratio=(d_rf / d_corr) if d_corr > 0 else None))
            print(cfg, Ik, round(fe), pname, 'done', flush=True)
    json.dump(rows, open(os.path.join(HERE, f'p_mc3b_{cfg}.json'), 'w'), indent=1)


def summary():
    rows = []
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        rows += json.load(open(os.path.join(HERE, f'p_mc3b_{cfg}.json')))
    out = ['# Amplitude correction versus rainflow counting, extended set of points (review round 5)', '',
           'ratio = rainflow damage of the pulse-resolved waveform / damage of the single corrected cycle',
           '(below 1: the mission correction overstates the damage).', '',
           '| network | rule | policy | n | min | median | max |', '|---|---|---|---|---|---|---|']
    for nt in NETS:
        for st in ('ton_clip', 'ton_free'):
            for pol in ('baseline', 'mean-temperature law', 'ripple-aware law'):
                v = np.array([x['ratio'] for x in rows if x['net'] == nt and x['rule'] == st and x['policy'] == pol
                              and x['ratio'] is not None and x['r_p'] >= 1.0])
                if len(v):
                    out.append(f'| {nt} | {st} | {pol} | {len(v)} | {v.min():.2f} | {np.median(v):.2f} | {v.max():.2f} |')
    out += ['', 'Points with r_p >= 1 K only (smaller cycles contribute negligibly).', '',
            '| config | I | fe | cos | policy | chip | network | rule | r_a | r_p | ratio |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for x in rows:
        q = '' if x['ratio'] is None else f"{x['ratio']:.2f}"
        out.append(f"| {x['cfg']} | {x['I']:.0f} | {x['fe']:.0f} | {x['cos']:+.2f} | {x['policy']} | {x['chip']} | {x['net']} | "
                   f"{x['rule']} | {x['r_a']:.2f} | {x['r_p']:.2f} | {q} |")
    open(os.path.join(HERE, 'p_mc3b.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('\n'.join(out[:20]))


if __name__ == '__main__':
    summary() if sys.argv[1] == 'summary' else run(sys.argv[1])
