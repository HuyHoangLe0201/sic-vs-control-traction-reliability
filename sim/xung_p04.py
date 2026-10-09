"""Review item P0-4: pulse-resolved check of the carrier-averaged loss model at low pulse ratio.

For a few high-f_e operating points of the mission, the leg is simulated with naturally sampled phase-disposition
PWM (asynchronous carrier at f_sw), conduction losses per switching state and switching energies deposited as
impulses at the actual commutation instants. The chip Foster networks are integrated exactly at a step of
1/(400 f_sw). The peak-to-peak junction ripple per fundamental period is compared with the same model driven by
the carrier-averaged losses (as used in the mission simulations), for the baseline policy.

python xung_p04.py  -> xung_p04.md, xung_p04.json
"""
import os, json, numpy as np
import tonhao as th

HERE = os.path.dirname(os.path.abspath(__file__))
FSW = 1500.0
NPER = 12          # fundamental periods simulated (the first two are discarded); 4 below 40 Hz
POINTS = [  # (label, I_pk, m, cos phi, f_e) taken from the derated mission profile
    ('motor 4.8 Hz', 340.8, 0.040, 0.95, 4.75),
    ('motor 9.7 Hz', 455.2, 0.082, 0.95, 9.70),
    ('motor 20 Hz', 462.0, 0.167, 0.95, 19.71),
    ('motor 30 Hz', 462.0, 0.253, 0.95, 29.83),
    ('brake 10 Hz', 383.9, 0.087, -0.95, 10.29),
    ('brake 20 Hz', 382.8, 0.171, -0.95, 20.19),
    ('motor 57 Hz', 462.0, 0.485, 0.95, 57.1),
    ('motor 97 Hz', 462.0, 0.824, 0.95, 97.1),
    ('motor 147 Hz', 462.0, 0.95, 0.95, 147.1),
    ('motor 197 Hz', 462.0, 0.95, 0.95, 197.0),
    ('motor 247 Hz', 462.0, 0.95, 0.95, 247.0),
    ('brake 153 Hz', 404.8, 0.95, -0.95, 153.0),
    ('brake 250 Hz', 404.8, 0.95, -0.95, 249.8),
]


def chip_temps(cfg, I, m, c):
    """Baseline equilibrium chip temperatures (used to evaluate the device characteristics)."""
    r = th.analyse_point(cfg, I, m, c, FSW)
    return r['Tb']


def simulate(cfg, I, m, c, fe, Tchip, pulsed=True):
    tp = th.topology(cfg)
    tech = th.TECH[tp['tech']]
    nc = tp['nchip']
    dt = 1.0 / (FSW * 400)
    nper = NPER if fe >= 40 else 4
    n = int(round(nper / fe / dt))
    t = np.arange(n) * dt
    th_ = (2 * np.pi * fe * t) % (2 * np.pi)
    ua, v0 = th.offsets(m)
    u = np.interp(th_, th.TH, ua + v0[th.NOFF // 2], period=2 * np.pi)
    ua_t = np.interp(th_, th.TH, ua, period=2 * np.pi)
    phi = np.arccos(np.clip(c, -1, 1))
    i = I * np.sin(th_ - phi)
    sgn = np.where(i >= 0, 1, -1); ai = np.abs(i)
    ot = np.where(ua_t >= 0, 'U', 'L') if tp['topo'] == 'ANPC' else np.full(n, 'U')
    Vsw = 900.0
    P = np.zeros((n, nc))
    Tc = Tchip                                             # per-chip evaluation temperature
    # conduction: state sequence (pulsed) or duty weights (averaged)
    car = np.abs(((t * FSW) % 1.0) * 2 - 1)                # triangular carrier in [0, 1]
    if pulsed:
        sP = (u > 0) & (u > car); sN = (u < 0) & (-u > car)
        wP, wN = sP.astype(float), sN.astype(float)
    else:
        wP, wN = np.clip(u, 0, 1), np.clip(-u, 0, 1)
    wO = 1 - wP - wN

    def add_cond(table, w, mask_ot=None):
        for s in (1, -1):
            msk = (sgn == s) * w
            if mask_ot is not None:
                msk = msk * mask_ot
            for role, share in table[s]:
                k = tp['chip'][role]
                v = (tech['vT'] if role[0] == 'T' else tech['vD'])(ai * share, Tc[k])
                P[:, k] += msk * v * ai * share
    add_cond(tp['P'], wP); add_cond(tp['N'], wN)
    for o in tp['otypes']:
        if o in ('U', 'L'):
            add_cond(tp['O'][o], wO, (ot == o).astype(float))
    # switching
    if pulsed:
        lev = np.where(wP > 0, 1, np.where(wN > 0, -1, 0))
        ev = np.nonzero(np.diff(lev))[0] + 1
        for e in ev:
            pair = 'PO' if max(lev[e], lev[e - 1]) == 1 else 'ON'
            key = (pair, ot[e]) if (pair, ot[e]) in tp['com'] else (pair, 'U')
            rT, rD = tp['com'][key][sgn[e]]
            kT, kD = tp['chip'][rT], tp['chip'][rD]
            # turn-on and turn-off energies are both charged per carrier period in the averaged model;
            # here each transition carries half of (Eon + Eoff) and half of Err
            P[e, kT] += 0.5 * tech['eT'](ai[e], Tc[kT], Vsw) / dt
            P[e, kD] += 0.5 * tech['eD'](ai[e], Tc[kD], Vsw) / dt
    else:
        act_PO = (u > th.CLAMP_TOL) & (u < 1 - th.CLAMP_TOL)
        act_ON = (u < -th.CLAMP_TOL) & (u > -1 + th.CLAMP_TOL)
        for pair, act in (('PO', act_PO), ('ON', act_ON)):
            for o in np.unique(ot):
                key = (pair, o) if (pair, o) in tp['com'] else (pair, 'U')
                for s in (1, -1):
                    msk = act & (sgn == s) & (ot == o)
                    rT, rD = tp['com'][key][s]
                    kT, kD = tp['chip'][rT], tp['chip'][rD]
                    if msk.any():
                        P[msk, kT] += FSW * tech['eT'](ai[msk], Tc[kT], Vsw)
                        P[msk, kD] += FSW * tech['eD'](ai[msk], Tc[kD], Vsw)
    # Foster networks (exact discretisation), started at the mean-loss steady state
    R, tau = tp['foster']
    a = np.exp(-dt / tau)
    Rk = tp['rth'][:, None] * R[None, :]
    from scipy.signal import lfilter
    Tj = np.zeros((n, nc))
    for j in range(nc):
        for q in range(len(tau)):
            x0 = Rk[j, q] * P[:, j].mean()
            y, _ = lfilter([Rk[j, q] * (1 - a[q])], [1, -a[q]], P[:, j], zi=[a[q] * x0])
            Tj[:, j] += y
    per = int(round(1 / fe / dt))
    rip = [Tj[j * per:(j + 1) * per].max(0) - Tj[j * per:(j + 1) * per].min(0) for j in range(2 if nper > 4 else 1, nper)]
    rip = np.array(rip)
    return dict(rip_max=rip.max(0), rip_mean=rip.mean(0), Pmean=P.mean(0), names=tp['names'])


def main():
    out, L = {}, ['# P0-4: pulse-resolved vs carrier-averaged losses (baseline policy, f_sw = 1.5 kHz)\n',
                  '| config | point | pulse ratio | worst chip | ripple avg model (K) | ripple pulsed, mean / max over periods (K) | '
                  'ratio max/avg | mean loss pulsed/avg |', '|---|---|---|---|---|---|---|---|']
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        for lab, I, m, c, fe in POINTS:
            Tb = chip_temps(cfg, I, m, c)
            ra = simulate(cfg, I, m, c, fe, Tb, pulsed=False)
            rp = simulate(cfg, I, m, c, fe, Tb, pulsed=True)
            k = int(np.argmax(ra['rip_max']))
            kp = int(np.argmax(rp['rip_max']))
            rec = dict(rip_avg=ra['rip_max'].tolist(), rip_pulse_max=rp['rip_max'].tolist(),
                       rip_pulse_mean=rp['rip_mean'].tolist(), P_avg=ra['Pmean'].tolist(), P_pulse=rp['Pmean'].tolist(),
                       names=ra['names'])
            out[f'{cfg}|{lab}'] = rec
            L.append(f"| {cfg} | {lab} | {FSW / fe:.1f} | {ra['names'][k]} / {rp['names'][kp]} | {ra['rip_max'][k]:.2f} | "
                     f"{rp['rip_mean'][kp]:.2f} / {rp['rip_max'][kp]:.2f} | {rp['rip_max'][kp] / ra['rip_max'][k]:.2f} | "
                     f"{rp['Pmean'].sum() / ra['Pmean'].sum():.3f} |")
            print(L[-1], flush=True)
    open(os.path.join(HERE, 'xung_p04.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    json.dump(out, open(os.path.join(HERE, 'xung_p04.json'), 'w'), indent=1)


if __name__ == '__main__':
    th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
    main()
