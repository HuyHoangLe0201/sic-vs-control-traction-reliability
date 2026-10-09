"""Review item P1-1: rainflow counting of the superposed junction-temperature history versus the separate counting of
mean-temperature cycles and output-frequency ripple cycles used in the paper.

The superposed history T(t) = Tmean(t) + T~(theta(t)) is represented by its extrema: within every simulation step, the
ripple contributes 2 f_e dt half-cycles with turning points Tmean +- r/2 at the phase instants theta = k pi (the mean
temperature is interpolated linearly between steps). Steps without ripple contribute their mean temperature. The
sequence is counted with the same ASTM rainflow, and every cycle is evaluated with its own heating time (half-cycle
duration), as in the separate counting.

python p11_rainflow.py  -> p11_rainflow.md
"""
import os, numpy as np
import tonthuong as tt, donhay

HERE = os.path.dirname(os.path.abspath(__file__))
CFGS = ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')


def superposed(Tm, rip, fe, t):
    dt = t[1] - t[0]
    phase = np.r_[0.0, np.cumsum(fe * dt)] * 2.0          # half-cycles elapsed at the step boundaries
    T_out, t_out = [], []
    for i in range(len(t)):
        if fe[i] < 0.5 or rip[i] < tt.DT_MIN:
            T_out.append(np.array([Tm[i]])); t_out.append(np.array([t[i]]))
            continue
        k0, k1 = int(np.ceil(phase[i])), int(np.floor(phase[i + 1] - 1e-12))
        if k1 < k0:
            T_out.append(np.array([Tm[i]])); t_out.append(np.array([t[i]]))
            continue
        k = np.arange(k0, k1 + 1)
        tk = t[i] + (k - phase[i]) / (2 * fe[i])
        Tn = Tm[min(i + 1, len(t) - 1)]
        mean = Tm[i] + (Tn - Tm[i]) * (tk - t[i]) / dt
        T_out.append(mean + np.where(k % 2 == 0, 0.5, -0.5) * rip[i])
        t_out.append(tk)
    return np.concatenate(T_out), np.concatenate(t_out)


def chip_damages(d, tag, k, nf):
    t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    Tm, rip = d[f'{tag}_Tj'][:, k], d[f'{tag}_rip'][:, k]
    sep = tt.damage_lowfreq(Tm, t, nf)[0] + tt.damage_ripple(Tm, rip, fe, dt, nf)
    Ts, ts = superposed(Tm, rip, fe, t)
    sup = tt.damage_lowfreq(Ts, ts, nf)[0]
    return sep, sup


def main():
    L = ['# P1-1: separate vs superposed rainflow counting (fvdr, most damaged chip under separate counting)\n',
         '| config | policy | rule | chip | D separate | D superposed | ratio |', '|---|---|---|---|---|---|---|']
    D = {}
    for c in CFGS:
        d = np.load(os.path.join(HERE, f'mophong_fvdr_{c}.npz'))
        names = list(d['names'])
        for tag in ('base', 'har'):
            for st in ('ton_clip', 'ton_free'):
                nf = donhay.nf_setting(st)
                # worst chip under separate counting; superposed evaluated for the three most damaged chips
                seps = []
                for k in range(len(names)):
                    seps.append(chip_damages(d, tag, k, nf) if True else None)
                ksep = int(np.argmax([s[0] for s in seps])); ksup = int(np.argmax([s[1] for s in seps]))
                D[(c, tag, st)] = (seps[ksep][0], seps[ksup][1])
                L.append(f'| {c} | {tag} | {st} | {names[ksep]} / {names[ksup]} | {seps[ksep][0]:.3g} | {seps[ksup][1]:.3g} | '
                         f'{seps[ksup][1] / seps[ksep][0]:.3f} |')
                print(L[-1], flush=True)
    L.append('\n| rule | counting | kappa sub vs Si-NPC+har | kappa sub vs Si-ANPC+har | both vs Si-ANPC |')
    L.append('|---|---|---|---|---|')
    for st in ('ton_clip', 'ton_free'):
        for j, lab in ((0, 'separate'), (1, 'superposed')):
            g = lambda c, tag: D[(c, tag, st)][j]
            L.append(f"| {st} | {lab} | {g('SiC-ANPC', 'base') / g('Si-NPC', 'har'):.3g} | "
                     f"{g('SiC-ANPC', 'base') / g('Si-ANPC', 'har'):.3g} | {g('SiC-ANPC', 'har') / g('Si-ANPC', 'har'):.3g} |")
    open(os.path.join(HERE, 'p11_rainflow.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[-6:]))


if __name__ == '__main__':
    main()
