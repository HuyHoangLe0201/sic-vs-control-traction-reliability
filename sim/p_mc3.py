"""Review comment MC3: is the amplitude correction of the pulse-resolved model equivalent to rainflow counting of the
pulse-resolved temperature history?

The mission correction replaces the ripple r of every chip by r_p = r * (pulsed / averaged peak-to-peak ratio) and
keeps one cycle per output period with T_min = Tbar - r_p/2 and t_on = 1/(2 f_e). Here, at representative high-f_e
operating points, the damage per output period of that representation is compared with rainflow counting of the
resolved waveform itself (every cycle with its own range, minimum and half-cycle duration), for both thermal networks
(nominal, without the microsecond term), two policies and both heating-time rules.

python p_mc3.py -> p_mc3.md
"""
import os
import numpy as np
import tonhao as th, tonthuong as tt, xung_policy as xp, donhay

HERE = os.path.dirname(os.path.abspath(__file__))
th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
POINTS = [('Si-ANPC', 462.0, 0.95, 0.95, 147.0), ('Si-ANPC', 273.0, 0.95, 0.95, 250.0),
          ('SiC-ANPC', 462.0, 0.95, 0.95, 147.0), ('SiC-ANPC', 273.0, 0.95, 0.95, 250.0)]
NETS = ('nominal', 'no us term')


def per_period_rainflow(T, t, fe, nf):
    D, _ = tt.damage_lowfreq(T, t, nf=nf, closed=True)
    return D / (t[-1] - t[0] + (t[1] - t[0])) / fe       # damage per output period


rows = []
summary = {st: {nt: [] for nt in NETS} for st in ('ton_clip', 'ton_free')}
for cfg, I, m, c, fe in POINTS:
    r = th.analyse_point(cfg, I, m, c, 1500, fe=fe)
    tp = r['tp']; fos = xp.fosters_of(tp)
    pols = [('baseline', r['wb'])] + ([('mean-temperature law', r['w_eq'])] if 'w_eq' in r else [])
    for pname, w in pols:
        rp, _, t, wp = xp.policy_ripple(tp, I, m, c, fe, r['Tb'], w, pulsed=True, fosters=fos, wave=True)
        ra, _, _, wa = xp.policy_ripple(tp, I, m, c, fe, r['Tb'], w, pulsed=False, fosters=fos, wave=True)
        nper = int(round((t[-1] + (t[1] - t[0])) * fe))
        per = int(round(1 / fe / (t[1] - t[0])))
        j0 = 2 if nper > 4 else 1
        sl = slice(j0 * per, nper * per)
        for inet, nt in enumerate(NETS):
            k = int(np.argmax(ra[inet]))                      # most loaded chip in the averaged model
            for st in ('ton_clip', 'ton_free'):
                nf = donhay.nf_setting(st)
                Tm = r['Tb'][k]
                d_corr = 0.0 if rp[inet][k] < tt.DT_MIN else 1.0 / nf(rp[inet][k], Tm - rp[inet][k] / 2, 1 / (2 * fe))
                y = wp[inet][sl, k]
                d_rf = per_period_rainflow(Tm + y - y.mean(), t[sl], fe, nf)
                ya = wa[inet][sl, k]
                d_ra = per_period_rainflow(Tm + ya - ya.mean(), t[sl], fe, nf)
                d_ca = 0.0 if ra[inet][k] < tt.DT_MIN else 1.0 / nf(ra[inet][k], Tm - ra[inet][k] / 2, 1 / (2 * fe))
                q = d_rf / d_corr if d_corr > 0 else float('nan')
                qa = d_ra / d_ca if d_ca > 0 else float('nan')
                summary[st][nt].append(q)
                rows.append(f'| {cfg} | {I:.0f} A, {fe:.0f} Hz | {pname} | {tp["names"][k]} | {nt} | {st} | '
                            f'{ra[inet][k]:.2f} | {rp[inet][k]:.2f} | {qa:.2f} | {q:.2f} |')
        print(cfg, I, fe, pname, 'done', flush=True)
out = ['# MC3: amplitude correction versus rainflow counting of the pulse-resolved history', '',
       'Most loaded chip of each point (averaged model). r_a, r_p: averaged and pulse-resolved peak-to-peak ripple (K).',
       'Ratio averaged: rainflow damage of the averaged waveform / single cycle of range r_a (check of the reference).',
       'Ratio pulsed: rainflow damage of the pulse-resolved waveform / single cycle of range r_p (the mission correction).', '',
       '| config | point | policy | chip | network | rule | r_a | r_p | ratio averaged | ratio pulsed |',
       '|---|---|---|---|---|---|---|---|---|---|'] + rows + ['']
for st in summary:
    for nt in NETS:
        v = np.array(summary[st][nt])
        out.append(f'- {st}, {nt}: ratio pulsed {np.nanmin(v):.2f}--{np.nanmax(v):.2f}')
open(os.path.join(HERE, 'p_mc3.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out[-4:]))
