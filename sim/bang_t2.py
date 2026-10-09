"""Table T2: electro-thermal runaway margin at the actual operating losses (Proposition runaway margin,
Lemma stability). For each configuration and operating point, baseline policy:
  - per chip: L_c = Z_jj * p_j(T_w) * c_j, c_j = (dp_j/dT)/p_j at T_w; bracket 1/(e L_c) <= mu <= 1/L_c
  - coupled: spectral radius rho(Z(0) K) at the electro-thermal equilibrium (stable iff < 1); 1/rho is the linear-law
    load margin of the coupled leg.
"""
import os, numpy as np
import tonhao as th

HERE = os.path.dirname(os.path.abspath(__file__))
th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
POINTS = [('motor, start', 462, 0.10, 0.95), ('motor, mid', 462, 0.50, 0.95), ('motor, top speed', 462, 0.95, 0.95),
          ('brake, top speed', 405, 0.95, -0.95), ('overload 1.5x', 693, 0.50, 0.95)]


def slope_at(tab, T):
    """d tab / dT for piecewise-linear [..., 3] tables at temperature T."""
    Ts = np.array(th.TEMPS)
    j = 0 if T <= Ts[1] else 1
    return (tab[..., j + 1] - tab[..., j]) / (Ts[j + 1] - Ts[j])


def main():
    rows = []
    for cfg in ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'):
        for lab, I, m, c in POINTS:
            r = th.analyse_point(cfg, I, m, c, 1500)
            tp, Z = r['tp'], r['Z']
            Lb = th.bin_avg(r['L'])
            tab = np.einsum('bro,robkt->kt', r['wb'], Lb) / th.NBIN            # [nchip, 3]
            Tw = th.T_WATER
            pw = th.at_temp(tab[None], np.full(tp['nchip'], Tw))[0] if False else np.array(
                [np.interp(Tw, th.TEMPS, tab[k]) for k in range(tp['nchip'])])
            dp = np.array([slope_at(tab[k], Tw) for k in range(tp['nchip'])])
            cj = dp / np.maximum(pw, 1e-9)
            Lc = np.diag(Z) * pw * cj
            k = int(np.argmax(Lc))
            dpe = np.array([slope_at(tab[q], r['Tb'][q]) for q in range(tp['nchip'])])
            rho = float(np.max(np.abs(np.linalg.eigvals(Z @ np.diag(np.maximum(dpe, 0))))))
            rows.append((cfg, lab, tp['names'][k], pw[k], cj[k], np.diag(Z)[k], Lc[k], 1 / (np.e * Lc[k]),
                         1 / Lc[k], rho, 1 / rho, r['Tb'].max(), r['okb']))
    hdr = ('| config | point | chip | p_c (W) | c (1/K) | R_jj (K/W) | L_c | 1/(e L_c) | 1/L_c | rho(ZK) | 1/rho | '
           'T_peak (C) | converged |\n|' + '---|' * 13 + '\n')
    with open(os.path.join(HERE, 'bang_t2.md'), 'w', encoding='utf-8') as f:
        f.write(hdr)
        for r in rows:
            f.write('| ' + ' | '.join([r[0], r[1], r[2], f'{r[3]:.0f}', f'{r[4]:.4f}', f'{r[5]:.4f}', f'{r[6]:.4f}',
                                        f'{r[7]:.1f}', f'{r[8]:.1f}', f'{r[9]:.4f}', f'{r[10]:.1f}', f'{r[11]:.1f}',
                                        str(r[12])]) + ' |\n')
    print(open(os.path.join(HERE, 'bang_t2.md'), encoding='utf-8').read())


if __name__ == '__main__':
    main()
