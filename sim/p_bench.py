"""Benchmark against published thermal-control principles (CAEE rejection, 2026-11-16), base case (variant fvdr).

Two published laws are re-implemented inside the same policy class, loss tables, neutral-point and decision-interval
constraints, thermal model and mission as the paper's own laws:

  'liu'  -- Liu et al., Energies 18 (2025) 2241, ANPC traction inverter: junction-temperature equalisation by mixing
            the commutation paths of the zero level at a ratio set by the temperature difference of the devices,
            centred offset (synchronous SVPWM, no zero-sequence freedom used for thermal purposes). Steady-state
            equivalent here: centred offset, zero-level path shares constant over each half period (one mixing ratio
            per sign of the reference), chosen to minimise the peak mean junction temperature (equalised devices).
            Not applicable to the NPC leg, which has no zero-level path choice.
  'bal'  -- thermal-stress balancing in the sense of FS-MPC balancing of junction temperatures (Novak et al., OJPEL 2
            (2021) 124): the full redundant-state class (offset and path), objective = spread of the mean junction
            temperatures max_k T_k - min_k T_k (+ 1 % of the peak as tie-break).

Both are evaluated with losses frozen at the baseline equilibrium (as the mean-temperature law of the paper) and
simulated over the mission with the carrier-averaged model; damage of the most damaged chip for both heating-time
rules. The paper's own laws (base, mean-temperature 'ha', ripple-aware 'har') and the floor are read from
daodong_fvdr_<cfg>.json / the bound files for the comparison.
python p_bench.py <cfg>  -> p_bench_<cfg>.json ;  python p_bench.py summary -> p_bench.md
"""
import os, sys, json, time
import numpy as np
from scipy import sparse

HERE = os.path.dirname(os.path.abspath(__file__))


def build_rows(th, tp, Lb, inpb, g, npc):
    """Equality rows (convexity per bin, 120-degree offset marginal, NP balance, decision intervals), loss map Mp
    and NP inequality rows, exactly as tonhao.ceiling_lp."""
    NOT = len(tp['otypes'])
    nv = th.NBIN * th.NOFF * NOT
    idx = lambda b, r, o: (b * th.NOFF + r) * NOT + o
    A, bq = [], []
    for b in range(th.NBIN):
        row = np.zeros(nv); row[[idx(b, r, o) for r in range(th.NOFF) for o in range(NOT)]] = 1
        A.append(row); bq.append(1)
    per = th.NBIN // 3
    for b in range(per):
        for k in (1, 2):
            for r in range(th.NOFF):
                row = np.zeros(nv)
                for o in range(NOT):
                    row[idx(b, r, o)] += 1; row[idx(b + k * per, r, o)] -= 1
                A.append(row); bq.append(0)
    row = np.zeros(nv)
    for b in range(th.NBIN):
        for r in range(th.NOFF):
            for o in range(NOT):
                row[idx(b, r, o)] = inpb[r, o, b] / th.NBIN
    A.append(row); bq.append(0)
    for tr in th.tie_rows(nv, NOT, g, idx):
        A.append(np.asarray(tr)[:nv]); bq.append(0)
    Mp = np.zeros((tp['nchip'], nv))
    for b in range(th.NBIN):
        for r in range(th.NOFF):
            for o in range(NOT):
                Mp[:, idx(b, r, o)] = Lb[r, o, b, :] / th.NBIN
    Anp, bnp = (np.zeros((0, nv)), np.zeros(0)) if npc is None else (np.asarray(npc[0]), np.asarray(npc[1]))
    return np.array(A), np.array(bq), Mp, Anp, bnp, nv, idx


def liu_rows(th, tp, m, nv, idx):
    """Centred offset and one zero-level path mix per sign of the reference."""
    NOT = len(tp['otypes'])
    ua, _ = th.offsets(m)
    ub = ua.reshape(th.NBIN, -1).mean(1)
    A = []
    for b in range(th.NBIN):
        for r in range(th.NOFF):
            if r != th.NOFF // 2:
                for o in range(NOT):
                    row = np.zeros(nv); row[idx(b, r, o)] = 1; A.append(row)
    rc = th.NOFF // 2
    for sgn in (1, -1):
        bins = [b for b in range(th.NBIN) if (ub[b] >= 0) == (sgn > 0)]
        for b in bins[1:]:
            for o in range(NOT):
                row = np.zeros(nv); row[idx(b, rc, o)] = 1; row[idx(bins[0], rc, o)] = -1; A.append(row)
    return np.array(A)


def solve_policy(th, tp, r, m, kind, Tw):
    Lb = th.bin_avg(th.at_temp(r['L'], r['Tb']))
    A, bq, Mp, Anp, bnp, nv, idx = build_rows(th, tp, Lb, r['inpb'], r['g'], r['npc'])
    if kind == 'liu':
        Al = liu_rows(th, tp, m, nv, idx)
        A, bq = np.vstack([A, Al]), np.r_[bq, np.zeros(len(Al))]
    ZM = r['Z'] @ Mp
    nc = tp['nchip']
    if kind == 'liu':                       # min peak T: variables x, t
        c = np.r_[np.zeros(nv), 1.0]
        Aub = np.vstack([np.hstack([ZM, -np.ones((nc, 1))]), np.hstack([Anp, np.zeros((len(bnp), 1))])])
        bub = np.r_[-Tw * np.ones(nc), bnp]
        Aeq = np.hstack([A, np.zeros((len(A), 1))])
        bounds = [(0, None)] * nv + [(None, None)]
    else:                                   # 'bal': min (tmax - tmin) + 0.01 tmax: variables x, tmax, tmin
        c = np.r_[np.zeros(nv), 1.01, -1.0]
        Aub = np.vstack([np.hstack([ZM, -np.ones((nc, 1)), np.zeros((nc, 1))]),
                         np.hstack([-ZM, np.zeros((nc, 1)), np.ones((nc, 1))]),
                         np.hstack([Anp, np.zeros((len(bnp), 2))])])
        bub = np.r_[-Tw * np.ones(nc), Tw * np.ones(nc), bnp]
        Aeq = np.hstack([A, np.zeros((len(A), 2))])
        bounds = [(0, None)] * nv + [(None, None)] * 2
    res = th.solve_lp(c, A_ub=sparse.csr_matrix(Aub), b_ub=bub, A_eq=sparse.csr_matrix(Aeq), b_eq=bq, bounds=bounds)
    if res.x is None:
        return None, res.status
    return res.x[:nv].reshape(th.NBIN, th.NOFF, len(tp['otypes'])), res.status


def run(cfg):
    import tonhao as th, hanhtrinh as h, tran_daodong as td, donhay
    prof = td.apply_variant('fvdr', h.load_profile(os.path.join(HERE, 'hoso_50km_dr.csv')), cfg)
    base = h.OpCache(cfg)
    tp = base.tp
    kinds = ['bal'] + (['liu'] if tp['topo'] == 'ANPC' else [])
    status = {k: [] for k in kinds}
    orig_get = base.get

    def get(I, m, c, fe=None):
        d = orig_get(I, m, c, fe)
        if d is None or kinds[0] in d:
            return d
        r = d['r']
        k = base.key(I, m, c, fe)
        for kind in kinds:
            w, st = solve_policy(th, tp, r, max(k[1], 0.01), kind, th.T_WATER)
            status[kind].append(int(st))
            if w is None:                   # infeasible restriction: fall back to the baseline policy
                w = r['wb']
            Teq, _, _ = th.equilibrium(w, r['L'], r['Z'])
            d[kind], d[kind + '_H'] = h.policy_tables(r['L'], w, Teq)
            d['dV_' + kind] = None if r['Q'] is None else th.np_ripple(r['Q'], w.reshape(-1))
        return d
    base.get = get
    t0 = time.time()
    out = dict(cfg=cfg, sim={})
    for kind in ['base'] + kinds:
        sim = h.simulate(cfg, prof, base, kind)
        for st in ('ton_clip', 'ton_free'):
            dj, _ = h.damages(sim, prof, nf=donhay.nf_setting(st))
            j = int(np.argmax([x['D'] for x in dj]))
            out['sim'][f'{kind}|{st}'] = dict(chip=tp['names'][j], D=dj[j]['D'], D_rip=dj[j]['D_rip'],
                                              rip_max=max(x['rip_max'] for x in dj),
                                              Tpeak=max(x['Tpeak'] for x in dj))
        out['sim'][f'{kind}|E_loss_MJ'] = float(3 * sim['P'].sum() * (prof['t'][1] - prof['t'][0]) / 1e6)
        out['sim'][f'{kind}|dV_max'] = float(sim['dV'].max())
        print(cfg, kind, f'{time.time() - t0:.0f}s', flush=True)
    out['lp_status'] = {k: {str(s): status[k].count(s) for s in set(status[k])} for k in kinds}
    json.dump(out, open(os.path.join(HERE, f'p_bench_{cfg}.json'), 'w'), indent=1, default=float)


def summary():
    L = ['| config | rule | law | D (rel. to baseline) | reduction | share of ceiling | E_loss (MJ) | NP ripple (V) |',
         '|---|---|---|---|---|---|---|---|']
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        b = json.load(open(os.path.join(HERE, f'p_bench_{cfg}.json')))['sim']
        dd_ = json.load(open(os.path.join(HERE, f'daodong_fvdr_{cfg}.json')))
        for st in ('ton_clip', 'ton_free'):
            Db = b[f'base|{st}']['D']
            rows = [('baseline', Db, b['base|E_loss_MJ'], b['base|dV_max'])]
            for kind, lab in (('bal', 'temperature balancing (Novak-type)'), ('liu', 'path-mix equalisation (Liu-type)')):
                if f'{kind}|{st}' in b:
                    rows.append((lab, b[f'{kind}|{st}']['D'], b[f'{kind}|E_loss_MJ'], b[f'{kind}|dV_max']))
            for tag, lab in (('ha', 'mean-temperature law (paper)'), ('har', 'ripple-aware law (paper)')):
                rows.append((lab, dd_['sim'][f'{tag}|{st}']['D'], dd_['np'][tag]['E_loss_MJ'], dd_['np'][tag]['dV_max']))
            ceil = Db / dd_['bounds_tw'][st]['D_bound_rip']
            for lab, D, E, dv in rows:
                g = Db / D
                share = f'{100 * g / ceil:.0f}%'
                L.append(f'| {cfg} | {st} | {lab} | {D / Db:.3f} | {g:.1f} | {share} | {E:.2f} | {dv:.0f} |')
    open(os.path.join(HERE, 'p_bench.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    summary() if sys.argv[1] == 'summary' else run(sys.argv[1])
