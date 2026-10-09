"""Leg loss engine, redistribution polytope and ceiling LP for P4 (R5).

One leg of a three-level inverter with carrier-based PWM and zero-sequence injection.
Redundancy available to a controller ("patterns"):
  * zero-sequence offset v0 (common to the three legs, so 120-degree periodic in the leg angle),
    chosen per angular bin from NOFF values spanning the feasible band;
  * ANPC only: the zero-state path U (0U2: T2,T5), L (0L2: T3,T6) or B (both paths, current split
    equally), chosen per bin, with the commutation type that goes with it (Brueckner 2005).
Constraint: zero average neutral-point current over the fundamental period.

Topologies with 1.7 kV devices at Vdc = 1800 V: Si-NPC, Si-ANPC, SiC-ANPC (T-type would need
outer devices rated for the full DC link; SiC NPC would clamp through the SiC body diode).
"""
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
LP_METHOD = 'highs-ds'
import linhkien as lk

NTH = 360            # angle grid
NBIN = 36            # angular bins for control choices (10 degrees); 72 bins x 9 offsets gives the same T*
NOFF = 5             # offset choices across the feasible band  (to 3 decimals, checked in tran_lp.py)
TEMPS = (25.0, 125.0, 150.0)   # tabulated temperatures; losses are piecewise linear in T between them
TH = np.linspace(0, 2 * np.pi, NTH, endpoint=False)
BIN = (np.arange(NTH) * NBIN) // NTH

# Switching energies of Si below 125 C: held at the 125 C value (no data; keeps loss non-decreasing in T)
def _si_esw(i, T, V): return lk.si_eon(i, max(T, 125), V) + lk.si_eoff(i, max(T, 125), V)
def _si_err(i, T, V): return lk.si_err(i, max(T, 125), V)
def _sic_esw(i, T, V): return lk.sic_eon(i, T, V) + lk.sic_eoff(i, T, V)

TECH = {
    'Si': dict(vT=lk.si_vce, vD=lk.si_vf, eT=_si_esw, eD=_si_err),
    'SiC': dict(vT=lk.sic_vds, vD=lk.sic_vsd_sync, eT=_sic_esw, eD=lk.sic_err),
}


def topology(name):
    """Chip list, module map, conduction and commutation tables.
    Role keys: ('T', k) or ('D', k) for switch position k = 1..6. Chip index of each role is given by
    'chip'. Conduction table: cond[level][sign] = [(role, share)], level in P/O_U/O_L/O_B/N.
    Commutation table: com[(pair, otype)][sign] = (transistor role, diode role)."""
    tech, topo = name.split('-')
    P = {+1: [(('T', 1), 1), (('T', 2), 1)], -1: [(('D', 1), 1), (('D', 2), 1)]}
    N = {+1: [(('D', 3), 1), (('D', 4), 1)], -1: [(('T', 3), 1), (('T', 4), 1)]}
    if topo == 'NPC':
        O = {'U': {+1: [(('D', 5), 1), (('T', 2), 1)], -1: [(('T', 3), 1), (('D', 6), 1)]}}
        com = {('PO', 'U'): {+1: (('T', 1), ('D', 5)), -1: (('T', 3), ('D', 1))},
               ('ON', 'U'): {+1: (('T', 2), ('D', 4)), -1: (('T', 4), ('D', 6))}}
        otypes = ['U']
        roles = [('T', 1), ('T', 2), ('T', 3), ('T', 4), ('D', 1), ('D', 2), ('D', 3), ('D', 4), ('D', 5), ('D', 6)]
        modules = [[('T', 1), ('T', 2), ('D', 1), ('D', 2)], [('T', 3), ('T', 4), ('D', 3), ('D', 4)], [('D', 5), ('D', 6)]]
    else:  # ANPC
        OU = {+1: [(('D', 5), 1), (('T', 2), 1)], -1: [(('D', 2), 1), (('T', 5), 1)]}
        OL = {+1: [(('T', 6), 1), (('D', 3), 1)], -1: [(('T', 3), 1), (('D', 6), 1)]}
        OB = {s: [(r, 0.5) for r, _ in OU[s] + OL[s]] for s in (+1, -1)}
        O = {'U': OU, 'L': OL, 'B': OB}
        com = {('PO', 'U'): {+1: (('T', 1), ('D', 5)), -1: (('T', 5), ('D', 1))},
               ('PO', 'L'): {+1: (('T', 2), ('D', 3)), -1: (('T', 3), ('D', 2))},
               ('PO', 'B'): {+1: (('T', 1), ('D', 5)), -1: (('T', 5), ('D', 1))},
               ('ON', 'L'): {+1: (('T', 6), ('D', 4)), -1: (('T', 4), ('D', 6))},
               ('ON', 'U'): {+1: (('T', 2), ('D', 3)), -1: (('T', 3), ('D', 2))},
               ('ON', 'B'): {+1: (('T', 6), ('D', 4)), -1: (('T', 4), ('D', 6))}}
        otypes = ['U', 'L', 'B']
        roles = [(t, k) for t in 'TD' for k in range(1, 7)]
        modules = [[('T', 1), ('T', 2), ('D', 1), ('D', 2)], [('T', 3), ('T', 4), ('D', 3), ('D', 4)],
                   [('T', 5), ('T', 6), ('D', 5), ('D', 6)]]
    if tech == 'SiC':   # one MOSFET chip per position carries both roles (synchronous rectification)
        chips = [k for k in range(1, 7)] if topo == 'ANPC' else [k for k in range(1, 5)]
        chip = {r: chips.index(r[1]) for r in roles}
        rth = np.full(len(chips), lk.SIC_RTH_JC)
        names = [f'S{k}' for k in chips]
        rcs = lk.SIC_RTH_CS_MODULE
        foster = (lk.SIC_FOSTER_R, lk.SIC_FOSTER_TAU)
    else:
        chip = {r: i for i, r in enumerate(roles)}
        rth = np.array([lk.SI_RTH_JC_IGBT if r[0] == 'T' else lk.SI_RTH_JC_FWD for r in roles])
        names = [f'{r[0]}{r[1]}' for r in roles]
        rcs = lk.SI_RTH_CS_MODULE
        foster = (lk.SI_FOSTER_R, lk.SI_FOSTER_TAU)
    nchip = len(names)
    mod_of = np.zeros(nchip, int)
    for mi, ms in enumerate(modules):
        for r in ms:
            mod_of[chip[r]] = mi
    return dict(name=name, tech=tech, topo=topo, P=P, N=N, O=O, com=com, otypes=otypes, chip=chip,
                nchip=nchip, names=names, rth=rth, rcs=rcs, mod_of=mod_of, nmod=len(modules), foster=foster)


R_HW = 10e-3      # K/W heat sink to water per module (assumption, to be replaced by FEM)
T_WATER = 40.0    # degC coolant (assumption)


SINK = None       # dict(Rf=[3x3] K/W, t=[s], Zf=[nt,3,3]) from tannhiet.py; None -> R_HW per module, uncoupled


def use_sink(path, scale=1.0):
    """Load the folded heat-sink model of tannhiet.py (scale multiplies all sink resistances)."""
    global SINK
    d = np.load(path)
    SINK = dict(Rf=d['Rf'] * scale, t=d['t'], Zf=d['Zf'] * scale)


def zmatrix(tp, r_hw=None):
    if SINK is not None and r_hw is None:
        mo = tp['mod_of']
        same = mo[:, None] == mo[None, :]
        return np.diag(tp['rth']) + same * tp['rcs'] + SINK['Rf'][mo[:, None], mo[None, :]]
    r_hw = R_HW if r_hw is None else r_hw
    """Steady-state thermal impedance junction->water: own Rth(j-c) plus shared module path."""
    same = tp['mod_of'][:, None] == tp['mod_of'][None, :]
    return np.diag(tp['rth']) + same * (tp['rcs'] + r_hw)


def offsets(m):
    """Feasible zero-sequence band and the NOFF offset choices, per angle (normalized to Vdc/2)."""
    A = 2 * m / np.sqrt(3)
    u = np.stack([A * np.sin(TH - k * 2 * np.pi / 3) for k in range(3)])
    lo, hi = -1 - u.min(0), 1 - u.max(0)
    hi = np.maximum(hi, lo)
    d = np.linspace(-1, 1, NOFF)
    v0 = (lo + hi)[None, :] / 2 + d[:, None] * (hi - lo)[None, :] / 2
    return u[0], v0              # leg-a reference, offsets [NOFF, NTH]


CLAMP_TOL = 1e-9
LP_TIME_LIMIT = 60.0
LP_LOG = []        # (method, status, seconds) of every LP that needed the fallback


def solve_lp(c, **kw):
    """linprog with a time limit; on a non-optimal status retry once with the interior-point solver."""
    import time
    t = time.time()
    res = linprog(c, method=LP_METHOD, options={'time_limit': LP_TIME_LIMIT}, **kw)
    if res.status != 0:
        res2 = linprog(c, method='highs-ipm', options={'time_limit': 5 * LP_TIME_LIMIT}, **kw)
        LP_LOG.append((LP_METHOD, res.status, 'ipm', res2.status, round(time.time() - t, 1)))
        print('LP fallback:', LP_LOG[-1], flush=True)
        res = res2
    return res


def bin_group(fe, fsw):
    """Number of consecutive angular bins that must share one control choice so that every decision interval
    contains at least one carrier period (review P0-2): smallest divisor g of NBIN with g >= NBIN*fe/fsw."""
    if fe is None or fe <= 0:
        return 1
    need = NBIN * fe / fsw
    for g in range(1, NBIN + 1):
        if NBIN % g == 0 and g >= need - 1e-12:
            return g
    return NBIN


def tie_rows(nv, NOT, g, idx):
    """Equality rows forcing identical weights within groups of g consecutive bins."""
    rows = []
    if g <= 1:
        return rows
    for b0 in range(0, NBIN, g):
        for b in range(b0 + 1, b0 + g):
            for r in range(NOFF):
                for o in range(NOT):
                    row = np.zeros(nv)
                    row[idx(b, r, o)] = 1; row[idx(b0, r, o)] = -1
                    rows.append(row)
    return rows


def loss_table(tp, I_pk, m, cosphi, fsw, Vdc=1800.0):
    """Instantaneous (carrier-averaged) chip losses for every choice, at the tabulated temperatures.
    Returns L[NOFF, NOT, NTH, nchip, len(TEMPS)] in W and inp[NOFF, NOT, NTH] (NP current, A)."""
    tech = TECH[tp['tech']]
    phi = np.arccos(np.clip(cosphi, -1, 1))
    i = I_pk * np.sin(TH - phi)
    sgn = np.where(i >= 0, 1, -1)
    ai = np.abs(i)
    ua, v0 = offsets(m)
    Vsw = Vdc / 2
    NOT = len(tp['otypes'])
    L = np.zeros((NOFF, NOT, NTH, tp['nchip'], len(TEMPS)))
    inp = np.zeros((NOFF, NOT, NTH))
    # role-wise quantities at each temperature: conduction loss with current share and switching energies
    SHARES = sorted({sh for tab in [tp["P"], tp["N"]] + list(tp["O"].values()) for s_ in (1, -1) for _, sh in tab[s_]})
    for it, T in enumerate(TEMPS):
        vT = {s: tech['vT'](ai * s, T) for s in SHARES}
        vD = {s: tech['vD'](ai * s, T) for s in SHARES}
        eT = tech['eT'](ai, T, Vsw)
        eD = tech['eD'](ai, T, Vsw)
        for r_ in range(NOFF):
            u = np.clip(ua + v0[r_], -1, 1)
            dP, dN = np.clip(u, 0, 1), np.clip(-u, 0, 1)
            dO = 1 - dP - dN
            for o_, ot in enumerate(tp['otypes']):
                acc = np.zeros((NTH, tp['nchip']))
                for lvl, duty in (('P', dP), ('N', dN), ('O', dO)):
                    table = tp['O'][ot] if lvl == 'O' else tp[lvl]
                    for s in (1, -1):
                        msk = (sgn == s) * duty
                        for role, share in table[s]:
                            v = vT[share] if role[0] == 'T' else vD[share]
                            acc[:, tp['chip'][role]] += msk * v * ai * share
                # switching losses only where the leg actually modulates between two levels; a leg clamped to
                # P (u = 1), N (u = -1) or O (u = 0) does not switch (review P0-1)
                sw_PO = (u > CLAMP_TOL) & (u < 1 - CLAMP_TOL)
                sw_ON = (u < -CLAMP_TOL) & (u > -1 + CLAMP_TOL)
                for pair, act in (('PO', sw_PO), ('ON', sw_ON)):
                    key = (pair, ot) if (pair, ot) in tp['com'] else (pair, 'U')
                    for s in (1, -1):
                        msk = act & (sgn == s)
                        rT, rD = tp['com'][key][s]
                        acc[:, tp['chip'][rT]] += msk * fsw * eT
                        acc[:, tp['chip'][rD]] += msk * fsw * eD
                L[r_, o_, :, :, it] = acc
                if it == 0:
                    inp[r_, o_] = dO * i
    return L, inp


def at_temp(Lk, Tchip):
    """Interpolate a table [..., nchip, len(TEMPS)] at per-chip temperatures (linear, extrapolated)."""
    Ts = np.array(TEMPS)
    out = np.empty(Lk.shape[:-1])
    for k, T in enumerate(Tchip):
        j = 0 if T <= Ts[1] else 1
        w = (T - Ts[j]) / (Ts[j + 1] - Ts[j])
        out[..., k] = (1 - w) * Lk[..., k, j] + w * Lk[..., k, j + 1]
    return out


def lower_bound_losses(Lk, Tlo=None, Thi=150.0):
    Tlo = T_WATER if Tlo is None else Tlo
    """Smallest loss over [Tlo, Thi] for every entry (piecewise linear: check breakpoints)."""
    cand = [at_temp(Lk, np.full(Lk.shape[-2], T)) for T in (Tlo, 125.0, Thi)]
    return np.minimum.reduce(cand)


def bin_avg(x):
    """Average the angle axis (axis=2 for loss tables, last for inp) into NBIN bins."""
    shp = list(x.shape)
    ax = 2
    x = np.moveaxis(x, ax, -1)
    out = x.reshape(*x.shape[:-1], NBIN, NTH // NBIN).mean(-1)
    return np.moveaxis(out, -1, ax)


def baseline_weights(tp, m):
    """Center offset; ANPC: zero state U in the positive half of the reference and L in the negative."""
    NOT = len(tp['otypes'])
    w = np.zeros((NBIN, NOFF, NOT))
    ua, _ = offsets(m)
    ub = ua.reshape(NBIN, -1).mean(1)
    for b in range(NBIN):
        o = 0 if (tp['topo'] == 'NPC' or ub[b] >= 0) else tp['otypes'].index('L')
        w[b, NOFF // 2, o] = 1
    return w


C_NP = 3e-3          # F, each DC-link half capacitor (assumption); NP node sees 2*C_NP
DV_NP_SPEC = 45.0    # V peak-to-peak NP voltage ripple allowed (5 % of Vdc/2, assumption)
FE_NP_MIN = 0.5      # Hz; below this the NP constraint is not applied (quasi-DC, as for the ripple)


def np_charge_matrix(tp, inpb, fe):
    """Q[j, v]: neutral-point charge (C) at the end of bin j (j < NBIN/3) per unit weight v, summed over the
    three legs (legs b, c use the leg-a policy shifted by 120 and 240 degrees). The total NP current is
    120-degree periodic with zero mean, so the charge over one third of the period describes the ripple."""
    NOT = len(tp['otypes'])
    nv = NBIN * NOFF * NOT
    idx = lambda b, r, o: (b * NOFF + r) * NOT + o
    per = NBIN // 3
    dt_bin = 1.0 / (fe * NBIN)
    Itot = np.zeros((NBIN, nv))          # total NP current in bin beta, linear in x
    for beta in range(NBIN):
        for k in range(3):
            b = (beta - k * per) % NBIN
            for r in range(NOFF):
                for o in range(NOT):
                    Itot[beta, idx(b, r, o)] += inpb[r, o, b]
    return np.cumsum(Itot[:per], axis=0) * dt_bin


def np_ripple(Q, x):
    """Peak-to-peak NP voltage (V) for weights x (flattened)."""
    q = Q @ x
    q = np.concatenate([[0.0], q])       # charge is zero at the start of the third-period
    return float((q.max() - q.min()) / (2 * C_NP))


def np_rows(Q, dQ):
    """Pairwise rows Q_j - Q_l <= dQ (j != l), i.e. ripple of the NP charge bounded by dQ."""
    Q = np.vstack([np.zeros(Q.shape[1]), Q])      # include the zero charge at the start of the period
    per = Q.shape[0]
    rows = [Q[j] - Q[l] for j in range(per) for l in range(per) if j != l]
    return np.array(rows), np.full(len(rows), dQ)


def np_setup(tp, inpb, wb, fe):
    """NP-charge rows for a point: ripple may not exceed max(spec, baseline). Returns (npc, Q, dV_baseline)."""
    if fe is None or fe < FE_NP_MIN:
        return None, None, None
    Q = np_charge_matrix(tp, inpb, fe)
    dVb = np_ripple(Q, wb.reshape(-1))
    return np_rows(Q, 2 * C_NP * max(DV_NP_SPEC, dVb) * (1 + 1e-6)), Q, dVb


def avg_losses(w, Lb):
    """Chip average losses for weights w[NBIN,NOFF,NOT] and bin-averaged losses Lb[NOFF,NOT,NBIN,nchip]."""
    return np.einsum('bro,robk->k', w, Lb) / NBIN


def ceiling_lp(tp, Lb, inpb, Z, Tw=None, objective='peak', module=None, sense=1, g=1, npc=None):
    """LP over the redistribution polytope. objective='peak': min max_j Tw+(Z p)_j.
    objective='module': min/max (sense=+1/-1) of the total loss of one module (for S_M).
    g: bins per decision interval (realisability at the carrier frequency, see bin_group).
    npc: (A, b) rows bounding the neutral-point charge ripple (review P0-3), or None."""
    Tw = T_WATER if Tw is None else Tw
    NOT = len(tp['otypes'])
    nv = NBIN * NOFF * NOT
    idx = lambda b, r, o: (b * NOFF + r) * NOT + o
    A_eq, b_eq = [], []
    for b in range(NBIN):                       # convex weights per bin
        row = np.zeros(nv + 1); row[[idx(b, r, o) for r in range(NOFF) for o in range(NOT)]] = 1
        A_eq.append(row); b_eq.append(1)
    per = NBIN // 3                              # offset marginal is 120-degree periodic
    for b in range(per):
        for k in (1, 2):
            for r in range(NOFF):
                row = np.zeros(nv + 1)
                for o in range(NOT):
                    row[idx(b, r, o)] += 1; row[idx(b + k * per, r, o)] -= 1
                A_eq.append(row); b_eq.append(0)
    row = np.zeros(nv + 1)                       # neutral-point balance
    for b in range(NBIN):
        for r in range(NOFF):
            for o in range(NOT):
                row[idx(b, r, o)] = inpb[r, o, b] / NBIN
    A_eq.append(row); b_eq.append(0)
    for tr in tie_rows(nv, NOT, g, idx):         # realisable decision intervals
        A_eq.append(np.r_[tr, 0.0]); b_eq.append(0)
    # chip loss as linear map of weights: p = Mp @ x
    Mp = np.zeros((tp['nchip'], nv))
    for b in range(NBIN):
        for r in range(NOFF):
            for o in range(NOT):
                Mp[:, idx(b, r, o)] = Lb[r, o, b, :] / NBIN
    bounds = [(0, None)] * nv + [(None, None)]
    Aeq = sparse.csr_matrix(np.array(A_eq))
    Anp, bnp = (np.zeros((0, nv + 1)), np.zeros(0)) if npc is None else (np.hstack([npc[0], np.zeros((len(npc[1]), 1))]), npc[1])
    if objective == 'peak':
        A_ub = sparse.csr_matrix(np.vstack([np.hstack([Z @ Mp, -np.ones((tp['nchip'], 1))]), Anp]))
        b_ub = np.r_[-Tw * np.ones(tp['nchip']), bnp]
        c = np.zeros(nv + 1); c[-1] = 1
        res = solve_lp(c, A_ub=A_ub, b_ub=b_ub, A_eq=Aeq, b_eq=b_eq, bounds=bounds)
        x = res.x
        return res.fun, x[:-1].reshape(NBIN, NOFF, NOT), res.status
    sel = (tp['mod_of'] == module).astype(float)
    c = np.r_[sense * (sel @ Mp), 0]
    kw = dict(A_ub=sparse.csr_matrix(Anp), b_ub=bnp) if len(bnp) else {}
    res = solve_lp(c, A_eq=Aeq, b_eq=b_eq, bounds=bounds, **kw)
    return sense * res.fun, None, res.status


def equilibrium(w, L, Z, Tw=None, iters=200):
    Tw = T_WATER if Tw is None else Tw
    """Electro-thermal steady state for fixed weights. Returns (T, p, converged)."""
    Lb = bin_avg(L)
    T = np.full(Z.shape[0], Tw + 20.0)
    for _ in range(iters):
        p = avg_losses(w, at_temp(Lb, T))
        Tn = Tw + Z @ p
        if np.max(np.abs(Tn - T)) < 1e-4:
            return Tn, p, True
        if np.max(Tn) > 400:
            return Tn, p, False
        T = 0.5 * T + 0.5 * Tn
    return T, p, False


def analyse_point(name, I_pk, m, cosphi, fsw, Tw=None, fe=None, g=None):
    """Baseline equilibrium, ceiling (bound at lower-bound losses) and equilibrium-based optimum.
    fe: output frequency; sets the realisable decision-interval grouping g (None -> g = 1)."""
    Tw = T_WATER if Tw is None else Tw
    g = bin_group(fe, fsw) if g is None else g
    tp = topology(name)
    Z = zmatrix(tp)
    L, inp = loss_table(tp, I_pk, m, cosphi, fsw)
    inpb = inp.reshape(NOFF, len(tp['otypes']), NBIN, -1).mean(-1)
    wb = baseline_weights(tp, m)
    Tb, pb, okb = equilibrium(wb, L, Z, Tw)
    npc, Q, dVb = np_setup(tp, inpb, wb, fe)
    Lb_lo = bin_avg(lower_bound_losses(L, Tw))
    Tstar, w_star, st = ceiling_lp(tp, Lb_lo, inpb, Z, Tw, g=g, npc=npc)
    Lb_eq = bin_avg(at_temp(L, Tb))           # losses frozen at baseline equilibrium temperatures
    _, w_eq, st2 = ceiling_lp(tp, Lb_eq, inpb, Z, Tw, g=g, npc=npc)
    Teq, peq, okq = equilibrium(w_eq, L, Z, Tw)
    eta = 1 - (Tstar - Tw) / (Tb.max() - Tw)
    dVeq = None if Q is None else np_ripple(Q, w_eq.reshape(-1))
    return dict(tp=tp, Z=Z, L=L, inpb=inpb, wb=wb, Tb=Tb, pb=pb, okb=okb, Tstar=Tstar, w_star=w_star,
                w_eq=w_eq, Teq=Teq, peq=peq, eta=eta, lp_status=(st, st2), g=g, npc=npc, Q=Q, dV_base=dVb, dV_ha=dVeq)
