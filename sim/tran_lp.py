"""R5: redistribution polytope and ceiling over an operating-point grid.
Outputs tran_lp.csv, tran_lp_hoitu.csv (grid convergence) and tran_lp.png."""
import os, time, numpy as np
import tonhao as th

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIGS = ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')
I_GRID = (200, 300, 462, 600)
M_GRID = (0.1, 0.3, 0.5, 0.7, 0.95)
MODES = (('motor', 0.95), ('brake', -0.95))
FSW = 1500.0


def module_spread(r):
    """S_M of Proposition (mechanism selectivity): max - min module loss over the polytope (at T_water)."""
    tp = r['tp']
    Lb = th.bin_avg(th.at_temp(r['L'], np.full(tp['nchip'], th.T_WATER)))
    out = []
    for mi in range(tp['nmod']):
        hi, _, _ = th.ceiling_lp(tp, Lb, r['inpb'], r['Z'], objective='module', module=mi, sense=-1)
        lo, _, _ = th.ceiling_lp(tp, Lb, r['inpb'], r['Z'], objective='module', module=mi, sense=1)
        out.append((lo, hi))
    return out


def main():
    rows = []
    t0 = time.time()
    for cfg in CONFIGS:
        for mode, cphi in MODES:
            for I in I_GRID:
                for m in M_GRID:
                    r = th.analyse_point(cfg, I, m, cphi, FSW)
                    tp = r['tp']
                    k = int(np.argmax(r['Tb']))
                    sp = module_spread(r) if I == 462 else [(np.nan, np.nan)] * tp['nmod']
                    pmod_b = [r['pb'][tp['mod_of'] == mi].sum() for mi in range(tp['nmod'])]
                    rows.append(dict(cfg=cfg, mode=mode, I=I, m=m, P_leg=r['pb'].sum(), hottest=tp['names'][k],
                                     Tb=r['Tb'].max(), Tstar=r['Tstar'], Teq=r['Teq'].max(), eta=r['eta'],
                                     ok=int(r['okb']), lp=str(r['lp_status']),
                                     S_rel=max((hi - lo) / max(pb, 1e-9) for (lo, hi), pb in zip(sp, pmod_b))))
                    print(f"{cfg:9s} {mode:5s} I={I:3d} m={m:.2f} Tb={rows[-1]['Tb']:6.1f} T*={r['Tstar']:6.1f} "
                          f"Teq={rows[-1]['Teq']:6.1f} eta={r['eta']:.3f} hot={tp['names'][k]} "
                          f"S_rel={rows[-1]['S_rel']:.3f}  [{time.time()-t0:.0f}s]", flush=True)
    keys = list(rows[0])
    with open(os.path.join(HERE, 'tran_lp.csv'), 'w') as f:
        f.write(','.join(keys) + '\n')
        for r in rows:
            f.write(','.join(f'{r[k]:.4f}' if isinstance(r[k], float) else str(r[k]) for k in keys) + '\n')

    # grid convergence of the bound at three points
    conv = []
    for cfg, I, m in (('Si-NPC', 462, 0.3), ('Si-ANPC', 462, 0.5), ('SiC-ANPC', 462, 0.5)):
        vals = []
        for nbin, noff in ((36, 5), (72, 9)):
            th.NBIN, th.NOFF = nbin, noff
            vals.append(th.analyse_point(cfg, I, m, 0.95, FSW)['Tstar'])
        th.NBIN, th.NOFF = 36, 5
        conv.append((cfg, I, m, *vals))
        print('convergence', conv[-1], flush=True)
    with open(os.path.join(HERE, 'tran_lp_hoitu.csv'), 'w') as f:
        f.write('cfg,I,m,Tstar_36x5,Tstar_72x9\n')
        for c in conv:
            f.write(','.join(map(str, c)) + '\n')

    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(12, 6.5), sharey=True)
    for j, cfg in enumerate(CONFIGS):
        for i, (mode, _) in enumerate(MODES):
            for I in I_GRID:
                sel = [r for r in rows if r['cfg'] == cfg and r['mode'] == mode and r['I'] == I]
                ax[i, j].plot([r['m'] for r in sel], [r['eta'] for r in sel], 'o-', label=f'{I} A')
            ax[i, j].set_title(f'{cfg}, {mode}'); ax[i, j].grid(alpha=.3)
            ax[i, j].set_xlabel('m'); ax[0, 0].legend()
        ax[0, 0].set_ylabel('eta (redistributable imbalance)'); ax[1, 0].set_ylabel('eta')
    fig.tight_layout(); fig.savefig(os.path.join(HERE, 'tran_lp.png'), dpi=110)


if __name__ == '__main__':
    main()
