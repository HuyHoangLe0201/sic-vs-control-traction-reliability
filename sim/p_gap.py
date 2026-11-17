"""Gap between the ripple-aware law and the tightened floor (CAEE editor point c), base case.
The ratio D_har / D_floor is split exactly into three factors for the chip with the largest ripple damage under the law:
  F1 = R_w / D_floor   ripple damage of the law with the cycle minimum at the coolant temperature, over the floor
                       (freedom of the floor to choose a different policy at every step and for a fixed chip weighting,
                        losses at the coolant temperature, remaining frequency slack)
  F2 = R / R_w         actual cycle minimum instead of the coolant temperature
  F3 = D / R           slow (mission-level) cycles, which the floor omits
python p_gap.py -> p_gap.json and LaTeX rows p_gap_rows.tex"""
import os, json, numpy as np
import tonhao as th, tonthuong as tt, donhay
HERE = os.path.dirname(os.path.abspath(__file__))
out, rows = {}, []
for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
    z = np.load(os.path.join(HERE, f'mophong_fvdr_{cfg}.npz'))
    dj = json.load(open(os.path.join(HERE, f'daodong_fvdr_{cfg}.json')))
    fb = json.load(open(os.path.join(HERE, f'p_bound_fine_fvdr_{cfg}.json')))['bounds']
    t, fe = z['t'], z['fe']; dt = t[1] - t[0]
    Tj, rip = z['har_Tj'], z['har_rip']
    for st in ('ton_clip', 'ton_free'):
        nf = donhay.nf_setting(st)
        def Drip(k, Tmin):
            m = (rip[:, k] >= tt.DT_MIN) & (fe >= 0.5)
            ton = 1 / (2 * np.maximum(fe[m], 1e-3))
            return float(np.sum(fe[m] * dt / nf(rip[m, k], Tmin[m], ton)))
        Rk = [Drip(k, Tj[:, k] - rip[:, k] / 2) for k in range(Tj.shape[1])]
        k = int(np.argmax(Rk))
        R, Rw = Rk[k], Drip(k, np.full(len(t), th.T_WATER))
        D = dj['sim'][f'har|{st}']['D']; Db = dj['sim'][f'base|{st}']['D']; F = fb[st]['D_floor']
        o = dict(chip=str(z['names'][k]), ceil_pub=Db / fb[st]['D_floor_published'], ceil=Db / F, red=Db / D,
                 F1=Rw / F, F2=R / Rw, F3=D / R)
        out[f'{cfg}|{st}'] = o
        rule = 'clipped' if st == 'ton_clip' else 'unclipped'
        rows.append(f"{cfg} & {rule} & {o['ceil_pub']:.0f} & {o['ceil']:.0f} & {o['red']:.1f} & {o['F1']:.2f} & "
                    f"{o['F2']:.2f} & {o['F3']:.2f} \\\\")
        print(cfg, st, {a: (round(b, 2) if isinstance(b, float) else b) for a, b in o.items()})
json.dump(out, open(os.path.join(HERE, 'p_gap.json'), 'w'), indent=1)
open(os.path.join(HERE, 'p_gap_rows.tex'), 'w', newline='\n').write('\n'.join(rows) + '\n')
