"""Policy-aware pulse-resolved ripple (review round 2, item P0-4).

For an operating point and a policy w[NBIN, NOFF, NOT] (time shares per angular bin), the leg is simulated with
naturally sampled phase-disposition PWM. Within every angular bin, consecutive carrier periods are allocated to the
(offset, zero-level path) choices in proportion to their time shares (contiguous blocks), so that the carrier-period
realisation of the policy is reproduced. Conduction losses per switching state and switching energies at the
commutation instants feed the chip Foster networks (exact discretisation via lfilter). The same routine with duty-cycle
averaging gives the carrier-averaged reference; the ratio pulsed/averaged of the peak-to-peak ripple per fundamental
period is the correction applied to the mission ripple.
Changes of the zero-level path between carrier periods are not charged with commutation energy (as in the averaged
model).
"""
import numpy as np
from scipy.signal import lfilter
import tonhao as th

FSW = 1500.0


ALLOC = 'interleaved'   # 'interleaved': choices spread evenly over the carrier periods; 'blocks': contiguous


def policy_ripple(tp, I, m, c, fe, Tchip, w, pulsed=True, nper=None, spp=400, fosters=None):
    tech = th.TECH[tp['tech']]
    nc = tp['nchip']
    dt = 1.0 / (FSW * spp)
    nper = nper or (12 if fe >= 40 else 4)
    n = int(round(nper / fe / dt))
    t = np.arange(n) * dt
    th_ = (2 * np.pi * fe * t) % (2 * np.pi)
    ua, v0 = th.offsets(m)
    ua_t = np.interp(th_, th.TH, ua, period=2 * np.pi)
    v0_t = np.stack([np.interp(th_, th.TH, v0[r], period=2 * np.pi) for r in range(th.NOFF)])   # [NOFF, n]
    NOT = len(tp['otypes'])
    # --- allocation of choices: per carrier period (pulsed) or time-share weights (averaged)
    b = np.minimum((th_ / (2 * np.pi) * th.NBIN).astype(int), th.NBIN - 1)
    wf = w.reshape(th.NBIN, -1)                                   # [NBIN, NOFF*NOT]
    if pulsed:
        kc = np.floor(t * FSW)                                    # carrier-period index
        tc = (kc + 0.5) / FSW                                     # midpoint of the carrier period
        thc = (2 * np.pi * fe * tc) % (2 * np.pi)
        bc = np.minimum((thc / (2 * np.pi) * th.NBIN).astype(int), th.NBIN - 1)
        if ALLOC == 'blocks':
            pos = (thc / (2 * np.pi) * th.NBIN) - bc              # position of the period within its bin, [0, 1)
        else:
            pos = (kc * 0.6180339887498949) % 1.0                 # low-discrepancy sequence over carrier periods
        cum = np.cumsum(wf, axis=1)
        cum = cum / cum[:, -1:]
        choice = np.array([np.searchsorted(cum[bb], p, side='right') for bb, p in zip(bc, pos)])
        choice = np.minimum(choice, wf.shape[1] - 1)
        W = np.zeros((n, wf.shape[1])); W[np.arange(n), choice] = 1.0
    else:
        W = wf[b]                                                 # [n, NOFF*NOT]
    W = W.reshape(n, th.NOFF, NOT)
    phi = np.arccos(np.clip(c, -1, 1))
    i = I * np.sin(th_ - phi)
    sgn = np.where(i >= 0, 1, -1); ai = np.abs(i)
    P = np.zeros((n, nc))
    Vsw = 900.0
    car = np.abs(((t * FSW) % 1.0) * 2 - 1)
    shares = sorted({sh for tab in [tp['P'], tp['N']] + list(tp['O'].values()) for s_ in (1, -1) for _, sh in tab[s_]})
    vT = {(s, k): tech['vT'](ai * s, Tchip[k]) for s in shares for k in range(nc)}
    vD = {(s, k): tech['vD'](ai * s, Tchip[k]) for s in shares for k in range(nc)}
    eT = {k: tech['eT'](ai, Tchip[k], Vsw) for k in range(nc)}
    eD = {k: tech['eD'](ai, Tchip[k], Vsw) for k in range(nc)}
    for r in range(th.NOFF):
        u = np.clip(ua_t + v0_t[r], -1, 1)
        for o, ot in enumerate(tp['otypes']):
            wr = W[:, r, o]
            if not wr.any():
                continue
            if pulsed:
                sP = ((u > 0) & (u > car)).astype(float); sN = ((u < 0) & (-u > car)).astype(float)
            else:
                sP, sN = np.clip(u, 0, 1), np.clip(-u, 0, 1)
            sO = 1 - sP - sN
            for lvl, duty in (('P', sP), ('N', sN), ('O', sO)):
                table = tp['O'][ot] if lvl == 'O' else tp[lvl]
                for s in (1, -1):
                    msk = (sgn == s) * duty * wr
                    for role, share in table[s]:
                        k = tp['chip'][role]
                        v = vT[(share, k)] if role[0] == 'T' else vD[(share, k)]
                        P[:, k] += msk * v * ai * share
            if pulsed:
                lev = np.where(sP > 0, 1, np.where(sN > 0, -1, 0))
                ev = np.nonzero(np.diff(lev))[0] + 1
                ev = ev[wr[ev] > 0]
                for e in ev:
                    pair = 'PO' if max(lev[e], lev[e - 1]) == 1 else 'ON'
                    key = (pair, ot) if (pair, ot) in tp['com'] else (pair, 'U')
                    rT, rD = tp['com'][key][sgn[e]]
                    kT, kD = tp['chip'][rT], tp['chip'][rD]
                    P[e, kT] += 0.5 * eT[kT][e] / dt
                    P[e, kD] += 0.5 * eD[kD][e] / dt
            else:
                for pair, act in (('PO', (u > th.CLAMP_TOL) & (u < 1 - th.CLAMP_TOL)),
                                  ('ON', (u < -th.CLAMP_TOL) & (u > -1 + th.CLAMP_TOL))):
                    key = (pair, ot) if (pair, ot) in tp['com'] else (pair, 'U')
                    for s in (1, -1):
                        msk = act & (sgn == s)
                        rT, rD = tp['com'][key][s]
                        kT, kD = tp['chip'][rT], tp['chip'][rD]
                        P[:, kT] += msk * wr * FSW * eT[kT]
                        P[:, kD] += msk * wr * FSW * eD[kD]
    per = int(round(1 / fe / dt))
    j0 = 2 if nper > 4 else 1
    out = []
    for R, tau in (fosters or [tp['foster']]):
        a = np.exp(-dt / tau)
        Rk = tp['rth'][:, None] * R[None, :]
        Tj = np.zeros((n, nc))
        for j in range(nc):
            pm = P[:, j].mean()
            for q in range(len(tau)):
                if R[q] == 0:
                    continue
                y, _ = lfilter([Rk[j, q] * (1 - a[q])], [1, -a[q]], P[:, j], zi=[a[q] * Rk[j, q] * pm])
                Tj[:, j] += y
        rip = np.array([Tj[j * per:(j + 1) * per].max(0) - Tj[j * per:(j + 1) * per].min(0) for j in range(j0, nper)])
        out.append(rip.max(0))
    return out, P.mean(0)


def fosters_of(tp):
    """Nominal Foster network, and the network without the microsecond term (merged into the next term), i.e. the
    thermal impedance restricted to the time range of the virtual junction temperature."""
    R, tau = tp['foster']
    return [(R, tau), (np.r_[0.0, R[0] + R[1], R[2:]], tau)]


def ratio(tp, I, m, c, fe, Tchip, w, fosters=None):
    """Per-chip ratio pulsed/averaged of the peak-to-peak ripple for each Foster network (1 where the averaged ripple
    is below 0.2 K). Returns lists over the networks."""
    fs = fosters or [tp['foster']]
    rp, _ = policy_ripple(tp, I, m, c, fe, Tchip, w, pulsed=True, fosters=fs)
    ra, _ = policy_ripple(tp, I, m, c, fe, Tchip, w, pulsed=False, fosters=fs)
    q = [np.where(a_ > 0.2, p_ / np.maximum(a_, 1e-9), 1.0) for p_, a_ in zip(rp, ra)]
    return q, rp, ra
