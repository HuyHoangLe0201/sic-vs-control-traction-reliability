"""Mechanism figures of the manuscript.
Figure 5: why the output-frequency ripple is large at low output frequency (Foster low-pass, Si IGBT network of
Table C.1) and how a temperature history is split into slow and ripple cycles (schematic).
Figure 6: idea of the ceiling (every law is a point of the policy polytope; the linear program finds the best one,
schematic) and the break-even capability with the base-case damages of Section 4.3.
python hinh_coche.py -> Figure_5 and Figure_6 (.pdf, .png) in the output folder"""
import os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('P4_OUT', os.path.join(HERE, 'out'))
MM = 1 / 25.4
OK = dict(black='#000000', orange='#E69F00', sky='#56B4E9', green='#009E73', blue='#0072B2', verm='#D55E00',
          grey='#8C8C8C')
plt.rcParams.update({'font.size': 8, 'axes.labelsize': 8, 'legend.fontsize': 7, 'xtick.labelsize': 7,
                     'ytick.labelsize': 7, 'axes.linewidth': 0.6, 'lines.linewidth': 1.0, 'pdf.fonttype': 42,
                     'ps.fonttype': 42, 'savefig.bbox': 'standard', 'figure.constrained_layout.use': True})
# normalised Foster network of the Si IGBT (Table C.1)
A_SI = np.array([0.0124, 0.0739, 0.3505, 0.5632])
TAU_SI = np.array([0.0196, 1.40, 17.9, 94.4]) * 1e-3
# normalised Foster network of the SiC MOSFET (Table C.1)
A_SIC = np.array([0.0213, 0.0732, 0.233, 0.665])
TAU_SIC = np.array([0.0151, 0.457, 6.19, 34.5]) * 1e-3


def label(ax, s):
    ax.text(-0.13, 1.02, s, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom')


def save(fig, k):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, f'Figure_{k}.pdf'))
    fig.savefig(os.path.join(OUT, f'Figure_{k}.png'), dpi=1000)
    plt.close(fig)
    print('Figure', k, 'ok')


def periodic_rise(p, fe, a=A_SI, tau=TAU_SI):
    """Periodic part of the junction temperature (in units of R * p_max) for a loss waveform p(theta) over one
    output period at output frequency fe, from all harmonics of p filtered by the Foster network."""
    P = np.fft.rfft(p) / len(p)
    h = np.arange(len(P))
    z = (a[None, :] / (1 + 1j * 2 * np.pi * h[:, None] * fe * tau[None, :])).sum(axis=1)
    Tk = P * z
    Tk[0] = 0
    return np.fft.irfft(Tk * len(p), n=len(p))


def fig_damage():
    th = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    p = np.clip(np.sin(th), 0, None) ** 2          # conduction-dominated loss of one chip: one half-period per cycle
    fig, ax = plt.subplots(1, 3, figsize=(190 * MM, 62 * MM), gridspec_kw=dict(width_ratios=[1, 1, 1.15]))
    # (a) thermal impedance seen by a loss harmonic of frequency f (Table 1 resistances, Table C.1 Foster networks)
    a = ax[0]
    f = np.logspace(-1, 3, 400)
    for R, aa, tt, lab, c, ls in ((53, A_SI, TAU_SI, 'Si IGBT', OK['blue'], '-'), (81, A_SI, TAU_SI, 'Si FWD', OK['sky'], '--'),
                                 (60, A_SIC, TAU_SIC, 'SiC MOSFET', OK['verm'], '-.')):
        z = np.abs((aa[None, :] / (1 + 1j * 2 * np.pi * f[:, None] * tt[None, :])).sum(axis=1))
        a.loglog(f, R * z, color=c, ls=ls, label=lab)
    a.axvspan(0.5, 250, color=OK['grey'], alpha=0.15, lw=0)
    a.text(11, 105, 'output frequencies\nof the mission', ha='center', va='center', fontsize=7, color=OK['grey'])
    a.set_xlim(0.1, 1000); a.set_ylim(1, 150)
    a.set_xlabel('frequency (Hz)'); a.set_ylabel('$|Z_{th(j-c)}|$ (K/kW)')
    a.legend(frameon=False, loc='lower left', fontsize=7)
    a.grid(alpha=.3, lw=0.4, which='both'); label(a, '(a)')
    # (b) periodic junction temperature for one loss waveform at three output frequencies (Si IGBT network)
    b = ax[1]
    deg = np.degrees(th)
    b.fill_between(deg, 0, p, color=OK['grey'], alpha=0.25, lw=0, label='loss $p/p_{\\max}$')
    for fe, c, ls in ((2.0, OK['verm'], '-'), (10.0, OK['orange'], '--'), (50.0, OK['blue'], '-.')):
        T = periodic_rise(p, fe)
        b.plot(deg, T - T.min(), color=c, ls=ls, label=f'{fe:g} Hz: ripple {T.max() - T.min():.2f}')
    b.set_xlim(0, 360); b.set_xticks([0, 90, 180, 270, 360]); b.set_ylim(0, 1.3)
    b.set_xlabel('angle in the output period (deg)'); b.set_ylabel('$\\tilde T_j/(R\\,p_{\\max})$')
    b.legend(frameon=False, loc='upper right', fontsize=7)
    b.grid(alpha=.3, lw=0.4); label(b, '(b)')
    # (c) schematic history at start-up: slow component plus ripple at a rising output frequency
    c_ = ax[2]
    t = np.linspace(0, 12, 12000)
    fe = 0.4 + 0.8 * t                                   # output frequency rising during acceleration
    ripple_of = {fq: np.ptp(periodic_rise(p, fq)) for fq in np.unique(np.round(fe, 2))}
    r = 30.0 * np.array([ripple_of[fq] for fq in np.round(fe, 2)]) / ripple_of[0.4]
    tbar = 40 + 22 * (1 - np.exp(-t / 5.0))
    phase = 2 * np.pi * np.cumsum(fe) * (t[1] - t[0])
    Tj = tbar + r / 2 * np.sin(phase)
    c_.plot(t, Tj, color=OK['blue'], lw=0.7, label='$T_j$')
    c_.plot(t, tbar, color=OK['black'], ls='--', lw=1.0, label='slow part $\\bar T_j$')
    c_.plot(t, tbar - r / 2, color=OK['grey'], lw=0.5, ls=':', label='ripple envelope')
    c_.plot(t, tbar + r / 2, color=OK['grey'], lw=0.5, ls=':')
    i0 = np.searchsorted(t, 0.6)
    k = i0 + np.argmin(Tj[i0:i0 + 1500]); k2 = k + np.argmax(Tj[k:k + 1200])
    c_.annotate('', (t[k] - 0.25, Tj[k2]), (t[k] - 0.25, Tj[k]), arrowprops=dict(arrowstyle='<->', lw=0.7, color=OK['verm']))
    c_.plot([t[k] - 0.4, t[k2]], [Tj[k2]] * 2, color=OK['verm'], lw=0.5, ls=':')
    c_.text(t[k] - 0.35, (Tj[k] + Tj[k2]) / 2, '$r$', color=OK['verm'], ha='right', va='center', fontsize=8)
    c_.annotate('', (t[k2], Tj[k2] + 3.0), (t[k], Tj[k2] + 3.0), arrowprops=dict(arrowstyle='<->', lw=0.7, color=OK['verm']))
    c_.text((t[k] + t[k2]) / 2, Tj[k2] + 3.6, '$t_{on}=1/(2f_e)$', color=OK['verm'], ha='center', va='bottom', fontsize=7)
    c_.plot([t[k] - 0.1, t[k] + 1.3], [Tj[k]] * 2, color=OK['verm'], lw=0.6)
    c_.text(t[k] + 1.4, Tj[k] - 0.5, '$T_{\\min}=\\bar T_j-r/2$', color=OK['verm'], va='center', fontsize=7)
    c_.set_xlim(0, 12); c_.set_ylim(15, 85)
    c_.set_xlabel('time after start (s)'); c_.set_ylabel('$T_j$ (°C)')
    c_.legend(frameon=False, loc='upper right', fontsize=7)
    c_.grid(alpha=.3, lw=0.4); label(c_, '(c)')
    save(fig, 5)


def fig_concept():
    fig, ax = plt.subplots(1, 2, figsize=(190 * MM, 65 * MM), gridspec_kw=dict(width_ratios=[1, 1.25]))
    # (a) schematic policy polytope with level sets of a linear objective
    a = ax[0]
    V = np.array([[0.08, 0.15], [0.62, 0.05], [0.92, 0.38], [0.80, 0.86], [0.30, 0.92], [0.05, 0.55]])
    a.add_patch(Polygon(V, closed=True, fc=OK['sky'], alpha=0.25, ec=OK['blue'], lw=0.8))
    g = np.array([0.55, 0.85])                            # objective direction (to be minimised)
    xx, yy = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
    cs = a.contour(xx, yy, g[0] * xx + g[1] * yy, levels=np.linspace(0.15, 1.3, 8), colors=OK['grey'],
                   linewidths=0.5, linestyles='--')
    vbest = V[np.argmin(V @ g)]
    a.plot(*vbest, marker='*', ms=11, color=OK['verm'], zorder=5)
    a.annotate('linear-program optimum:\nbest admissible policy', vbest, (0.36, 0.08), fontsize=7, color=OK['verm'],
               arrowprops=dict(arrowstyle='->', lw=0.6, color=OK['verm']), va='bottom')
    pb, pl = np.array([0.55, 0.62]), np.array([0.40, 0.40])
    a.plot(*pb, 'o', color=OK['black'], ms=5); a.text(pb[0] + 0.03, pb[1] + 0.02, 'baseline policy', fontsize=7)
    a.plot(*pl, 's', color=OK['blue'], ms=5); a.text(pl[0] + 0.03, pl[1] - 0.06, 'a control law', fontsize=7,
                                                    color=OK['blue'])
    a.text(0.62, 0.80, '$\\mathcal{X}(o)$: admissible\npolicies', fontsize=7, color=OK['blue'], ha='center')
    a.annotate('', (0.88, 0.12), (0.98, 0.30), arrowprops=dict(arrowstyle='->', lw=0.7, color=OK['grey']))
    a.text(0.985, 0.31, 'lower\nobjective', fontsize=7, color=OK['grey'], ha='right', va='bottom')
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.set_xticks([]); a.set_yticks([])
    a.set_xlabel('time share of one redundant choice'); a.set_ylabel('time share of another choice')
    label(a, '(a)')

    # (b) break-even capability, base case (carrier-averaged model, clipped rule), damages relative to Si-ANPC baseline
    b = ax[1]
    k = np.logspace(-1, 1.2, 200)
    d_base, d_law, d_floor = 1.0, 1 / 12.8, 1 / 74
    s_base, s_law = 0.090, 0.023
    b.axvspan(0.25, 0.6, color=OK['grey'], alpha=0.2, lw=0)
    b.text(0.387, 2.3, 'soldered\nSiC', ha='center', va='top', fontsize=7, color=OK['grey'])
    b.axhline(d_base, color=OK['grey'], lw=0.8, ls=':')
    b.axhline(d_law, color=OK['blue'], lw=1.0)
    b.axhline(d_floor, color=OK['blue'], lw=1.0, ls='--')
    b.text(11, d_base * 1.12, 'Si-ANPC, baseline', ha='right', fontsize=7, color=OK['grey'])
    b.text(11, d_law * 1.12, 'Si-ANPC, ripple-aware law', ha='right', fontsize=7, color=OK['blue'])
    b.text(0.105, d_floor * 0.8, 'Si-ANPC, damage floor (any law)', ha='left', va='top', fontsize=7, color=OK['blue'])
    b.plot(k, s_base / k, color=OK['verm'], lw=1.2, label='SiC, baseline policy: $D^{\\mathrm{SiC}}(1)/\\kappa$')
    b.plot(k, s_law / k, color=OK['verm'], lw=1.2, ls='-.', label='SiC, ripple-aware law')
    for x, y, txt, va in ((s_base / d_law, d_law, '$\\bar\\kappa=1.15$\n(substitution)', 'bottom'),
                          (s_law / d_law, d_law, '$\\bar\\kappa=0.29$\n(both controlled)', 'bottom'),
                          (s_base / d_floor, d_floor, '$\\bar\\kappa_{\\mathrm{bound}}=6.6$', 'bottom')):
        b.plot(x, y, 'o', ms=4, color=OK['black'], zorder=5)
        b.text(x, y * 1.35, txt, ha='center', va=va, fontsize=7)
    b.set_xscale('log'); b.set_yscale('log'); b.set_xlim(0.1, 11.5); b.set_ylim(5e-3, 2.5)
    b.set_xlabel('power-cycling capability of SiC relative to Si, $\\kappa$')
    b.set_ylabel('relative damage per run')
    b.legend(frameon=False, loc='upper right', bbox_to_anchor=(1.0, 0.86), fontsize=7)
    b.grid(alpha=.3, lw=0.4, which='both'); label(b, '(b)')
    save(fig, 6)


def fig_pulse():
    """Figure 11: junction temperature of the outer transistor T1 of Si-ANPC over one output period at a high output
    frequency (baseline policy), carrier-averaged versus pulse-resolved model, with and without the microsecond term."""
    import sys
    sys.path.insert(0, HERE)
    import tonhao as th, xung_policy as xp
    th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
    cfg, I, m, c, fe = 'Si-ANPC', 462.0, 0.95, 0.95, 147.0
    r = th.analyse_point(cfg, I, m, c, 1500, fe=fe); tp = r['tp']
    fos = xp.fosters_of(tp)
    rp, _, t, wp = xp.policy_ripple(tp, I, m, c, fe, r['Tb'], r['wb'], pulsed=True, fosters=fos, wave=True)
    ra, _, _, wa = xp.policy_ripple(tp, I, m, c, fe, r['Tb'], r['wb'], pulsed=False, fosters=fos, wave=True)
    k = list(tp['names']).index('T1')
    per = int(round(1 / fe / (t[1] - t[0]))); j = 2
    sl = slice(j * per, (j + 1) * per)
    tt = (t[sl] - t[sl][0]) * 1e3
    curves = ((wa[0][sl, k], OK['black'], '--', 1.2, f'carrier-averaged ({ra[0][k]:.1f} K)'),
              (wp[1][sl, k], OK['blue'], '-', 1.0, f'pulse-resolved, no µs term ({rp[1][k]:.1f} K)'),
              (wp[0][sl, k], OK['verm'], '-', 0.6, f'pulse-resolved, nominal ({rp[0][k]:.1f} K)'))
    ref = wa[0][sl, k].mean()
    fig, ax = plt.subplots(1, 2, figsize=(190 * MM, 60 * MM), gridspec_kw=dict(width_ratios=[1.6, 1]))
    for y, col, ls, lw, lab in curves:
        ax[0].plot(tt, y - ref, color=col, ls=ls, lw=lw, label=lab)
    ax[0].set_xlim(0, tt[-1]); ax[0].set_xlabel('time in the output period (ms)')
    ax[0].set_ylabel('junction temperature rise (K)')
    ax[0].legend(frameon=False, loc='upper right', fontsize=7)
    ax[0].grid(alpha=.3, lw=0.4); label(ax[0], '(a)')
    # (b) zoom on two switching periods around the current maximum
    y0 = wa[0][sl, k]; i_mx = int(np.argmax(y0)); half = int(round(1.0 / 1500 / (t[1] - t[0])))
    zs = slice(max(i_mx - half, 0), min(i_mx + half, len(tt)))
    for y, col, ls, lw, lab in curves:
        ax[1].plot(tt[zs], (y - ref)[zs], color=col, ls=ls, lw=lw)
    ax[1].set_xlim(tt[zs][0], tt[zs][-1]); ax[1].set_xlabel('time (ms), two switching periods')
    ax[1].grid(alpha=.3, lw=0.4); label(ax[1], '(b)')
    save(fig, 11)


def fig_runaway():
    """Figure 12: graphical construction of the runaway margin (Proposition 3) in normalised variables u = c (T - T_w)
    and y = R c p, for the SiC chip at maximum speed (L_c = 0.062, Table C.3). The heat removal is y = u; the loss is
    y = mu L_c f(u) with f = exp(u) (a) or f = 1 + u (b). Filled markers: stable equilibria; open: unstable."""
    from scipy.optimize import brentq
    Lc = 0.062
    u = np.linspace(0, 2.6, 400)
    mu_e, mu_l, mu_i = 1 / (np.e * Lc), 1 / Lc, 4.0
    fig, ax = plt.subplots(1, 2, figsize=(190 * MM, 62 * MM))
    # (a) exponential temperature dependence
    a = ax[0]
    a.plot(u, u, color=OK['black'], lw=1.3, label='heat removal')
    a.plot(u, Lc * np.exp(u), color=OK['blue'], lw=1.1, label='loss, rated load')
    a.plot(u, mu_i * Lc * np.exp(u), color=OK['grey'], lw=0.9, ls=':', label=f'loss, load ×{mu_i:g}')
    a.plot(u, mu_e * Lc * np.exp(u), color=OK['verm'], lw=1.1, ls='--',
           label=f'loss, load ×{mu_e:.1f} $=1/(e\\mathcal{{L}}_c)$')
    g = lambda x, mu: mu * Lc * np.exp(x) - x
    xs0 = brentq(g, 0, 1, args=(1.0,)); x1, x2 = brentq(g, 0, 1, args=(mu_i,)), brentq(g, 1, 2.6, args=(mu_i,))
    a.plot(xs0, xs0, 'o', color=OK['blue'], ms=4)
    a.plot(x1, x1, 'o', color=OK['grey'], ms=4); a.plot(x2, x2, 'o', mfc='white', mec=OK['grey'], ms=4)
    a.plot(1, 1, 'o', color=OK['verm'], ms=4)
    a.annotate('runaway\nthreshold', (1, 1), (1.75, 0.45), fontsize=7, color=OK['verm'], ha='center',
               arrowprops=dict(arrowstyle='->', lw=0.6, color=OK['verm']))
    a.legend(frameon=False, loc='upper left', fontsize=7)
    a.set_title('Exponential loss growth', fontsize=8)
    # (b) linear temperature dependence
    b = ax[1]
    b.plot(u, u, color=OK['black'], lw=1.3, label='heat removal')
    b.plot(u, Lc * (1 + u), color=OK['blue'], lw=1.1, label='loss, rated load')
    b.plot(u, 8 * Lc * (1 + u), color=OK['grey'], lw=0.9, ls=':', label='loss, load ×8')
    b.plot(u, mu_l * Lc * (1 + u), color=OK['verm'], lw=1.1, ls='--',
           label=f'loss, load ×{mu_l:.0f} $=1/\\mathcal{{L}}_c$')
    xe, xe8 = Lc / (1 - Lc), 8 * Lc / (1 - 8 * Lc)
    b.plot(xe, xe, 'o', color=OK['blue'], ms=4); b.plot(xe8, xe8, 'o', color=OK['grey'], ms=4)
    b.text(0.35, 2.25, 'parallel to the heat removal:\nno equilibrium', color=OK['verm'], fontsize=7, ha='left',
           va='center', rotation=0)
    b.legend(frameon=False, loc='lower right', bbox_to_anchor=(1.0, 0.1), fontsize=7)
    b.set_title('Linear loss growth', fontsize=8)
    for k, ax_ in enumerate(ax):
        ax_.set_xlim(0, 2.6); ax_.set_ylim(0, 2.6)
        ax_.set_xlabel('normalised junction rise $c\\,(T-T_w)$'); ax_.set_ylabel('normalised power $R\\,c\\,p$')
        ax_.grid(alpha=.3, lw=0.4); label(ax_, '(a)' if k == 0 else '(b)')
    save(fig, 12)


if __name__ == '__main__':
    import sys
    todo = sys.argv[1:] or ['5', '6', '11', '12']
    for n, f_ in (('5', fig_damage), ('6', fig_concept), ('11', fig_pulse), ('12', fig_runaway)):
        if n in todo:
            f_()
