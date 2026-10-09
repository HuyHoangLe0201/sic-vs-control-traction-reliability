"""R3b: ceiling for the fundamental-frequency junction ripple, and a ripple-aware control law.

At an operating point o and output frequency f_e, the periodic part of the junction temperature of
chip k is linear in the policy weights x:  T~_k(theta; x) = sum_v G[k, theta, v] x_v.  The ripple range
r_k(x) = max_theta T~_k - min_theta T~_k is convex in x, so
    r*_S = min_x  mean_{k in S} r_k(x)        (S: one chip or a symmetric pair)
is a linear program (epigraph form).  For any law acting through redundant states, the worst-chip
per-trip ripple damage is at least  sum_o n_o d(r*_S(o), T_w)  for every S (Jensen + monotonicity of d),
with n_o = f_e * dt fixed by the mission.  Losses are frozen at the baseline quasi-static temperatures
(electro-thermal correction of second order; checked against simulation).
"""
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
import tonhao as th

NQ = 36   # angle samples for the epigraph constraints


def eq_constraints(tp, inpb, g=1):
    """Convex weights per bin, 120-degree periodic offset marginal, neutral-point balance, and identical
    weights within decision intervals of g bins (realisability at the carrier frequency)."""
    NOT = len(tp['otypes']); NB, NO = th.NBIN, th.NOFF
    nv = NB * NO * NOT
    idx = lambda b, r, o: (b * NO + r) * NOT + o
    rows, rhs = [], []
    for b in range(NB):
        row = np.zeros(nv); row[[idx(b, r, o) for r in range(NO) for o in range(NOT)]] = 1
        rows.append(row); rhs.append(1)
    per = NB // 3
    for b in range(per):
        for k in (1, 2):
            for r in range(NO):
                row = np.zeros(nv)
                for o in range(NOT):
                    row[idx(b, r, o)] += 1; row[idx(b + k * per, r, o)] -= 1
                rows.append(row); rhs.append(0)
    row = np.zeros(nv)
    for b in range(NB):
        for r in range(NO):
            for o in range(NOT):
                row[idx(b, r, o)] = inpb[r, o, b] / NB
    rows.append(row); rhs.append(0)
    for tr in th.tie_rows(nv, NOT, g, idx):
        rows.append(tr); rhs.append(0)
    return np.array(rows), np.array(rhs), nv


def ripple_map(tp, LT, fe):
    """G[k, q, v]: ripple temperature of chip k at angle q per unit weight v. LT = L at fixed temps
    [NOFF, NOT, NTH, nchip]."""
    NOT = len(tp['otypes']); NB, NO, N = th.NBIN, th.NOFF, th.NTH
    mask = (th.BIN[None, :] == np.arange(NB)[:, None]).astype(float)          # [NB, N]
    R, tau = tp['foster']
    h = np.arange(1, N // 2)
    Zn = (R[None, :] / (1 + 1j * 2 * np.pi * fe * h[:, None] * tau[None, :])).sum(1)   # [H]
    thq = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
    E = np.exp(1j * np.outer(h, thq))                                         # [H, NQ]
    G = np.zeros((tp['nchip'], NQ, NB, NO, NOT))
    for r in range(NO):
        for o in range(NOT):
            wav = LT[r, o][None, :, :] * mask[:, :, None]                     # [NB, N, nchip]
            X = np.fft.rfft(wav, axis=1)[:, 1:N // 2, :]                      # [NB, H, nchip]
            T = 2.0 / N * np.real(np.einsum('bhk,h,hq->kqb', X, Zn, E))       # [nchip, NQ, NB]
            G[:, :, :, r, o] = T * tp['rth'][:, None, None]
    return G.reshape(tp['nchip'], NQ, -1)


def ripple_lp(tp, G, Aeq0, beq0, weights=None, npc=None, tie=None):
    """weights=None: min max_k r_k (control law). weights=w: min sum_k w_k r_k (bound).
    npc: (A, b) neutral-point charge rows on x (review P0-3).
    tie: (ZM, Tw, eps) two-stage tie-break for the control law (review P0-12): after s* = min max_k r_k,
    minimise the peak mean junction temperature max_j Tw + (ZM x)_j subject to max_k r_k <= (1 + eps) s*."""
    nc, nq, nv = G.shape
    # variables: x (nv), u (nc), l (nc), s (1)
    nvar = nv + 2 * nc + 1
    Ub, bub = [], []
    Gf = G.reshape(nc * nq, nv)
    Iu = sparse.kron(sparse.eye(nc), np.ones((nq, 1)))
    Ub.append(sparse.hstack([sparse.csr_matrix(Gf), -Iu, sparse.csr_matrix((nc * nq, nc)), sparse.csr_matrix((nc * nq, 1))]))
    Ub.append(sparse.hstack([sparse.csr_matrix(-Gf), sparse.csr_matrix((nc * nq, nc)), Iu, sparse.csr_matrix((nc * nq, 1))]))
    bub += [np.zeros(nc * nq), np.zeros(nc * nq)]
    c = np.zeros(nvar)
    if npc is not None:
        Ub.append(sparse.hstack([sparse.csr_matrix(npc[0]), sparse.csr_matrix((len(npc[1]), 2 * nc + 1))]))
        bub.append(npc[1])
    if weights is None:   # epigraph rows last, so that their duals are the last nc marginals
        Ub.append(sparse.hstack([sparse.csr_matrix((nc, nv)), sparse.eye(nc), -sparse.eye(nc), -np.ones((nc, 1))]))
        bub.append(np.zeros(nc))
        c[-1] = 1
    else:
        c[nv:nv + nc] = weights; c[nv + nc:nv + 2 * nc] = -weights
    A_ub = sparse.vstack(Ub).tocsr()
    A_eq = sparse.hstack([sparse.csr_matrix(Aeq0), sparse.csr_matrix((Aeq0.shape[0], 2 * nc + 1))]).tocsr()
    bounds = [(0, None)] * nv + [(None, None)] * (2 * nc + 1)
    b_ub = np.concatenate(bub)
    res = th.solve_lp(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=beq0, bounds=bounds)
    x = res.x[:nv]
    if weights is None:   # dual weights of the epigraph rows u_k - l_k <= s: the worst-chip mixture
        mu = -np.asarray(res.ineqlin.marginals)[-nc:]
        mu = np.clip(mu, 0, None)
        dual = mu / mu.sum() if mu.sum() > 0 else np.full(nc, 1.0 / nc)
        fun, st = res.fun, res.status
        if tie is not None and st == 0:
            ZM, Tw, eps = tie
            nj = ZM.shape[0]
            # variables: x, u, l, s (fixed by bound), t
            A2 = sparse.vstack([sparse.hstack([A_ub, sparse.csr_matrix((A_ub.shape[0], 1))]),
                                sparse.hstack([sparse.csr_matrix(ZM), sparse.csr_matrix((nj, 2 * nc + 1)), -np.ones((nj, 1))])]).tocsr()
            b2 = np.r_[b_ub, -Tw * np.ones(nj)]
            A_eq2 = sparse.hstack([A_eq, sparse.csr_matrix((A_eq.shape[0], 1))]).tocsr()
            c2 = np.zeros(nvar + 1); c2[-1] = 1
            bnd2 = bounds[:-1] + [(None, (1 + eps) * fun + 1e-9), (None, None)]
            res2 = th.solve_lp(c2, A_ub=A2, b_ub=b2, A_eq=A_eq2, b_eq=beq0, bounds=bnd2)
            if res2.status == 0:
                x = res2.x[:nv]
        r = (G @ x).max(1) - (G @ x).min(1)
        return fun, x, r, st, dual
    r = (G @ x).max(1) - (G @ x).min(1)
    return res.fun, x, r, res.status


def orbits(tp):
    """Symmetric chip groups (upper/lower half-bridge symmetry)."""
    names = tp['names']
    if tp['tech'] == 'SiC':
        pairs = [('S1', 'S4'), ('S2', 'S3'), ('S5', 'S6')]
    elif tp['topo'] == 'NPC':
        pairs = [('T1', 'T4'), ('T2', 'T3'), ('D1', 'D4'), ('D2', 'D3'), ('D5', 'D6')]
    else:
        pairs = [('T1', 'T4'), ('T2', 'T3'), ('T5', 'T6'), ('D1', 'D4'), ('D2', 'D3'), ('D5', 'D6')]
    out = []
    for a, b in pairs:
        w = np.zeros(len(names)); w[names.index(a)] = 0.5; w[names.index(b)] = 0.5
        out.append((f'{a}{b}', w))
    return out
