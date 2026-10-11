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
    fig, ax = plt.subplots(1, 2, figsize=(190 * MM, 62 * MM), gridspec_kw=dict(width_ratios=[1, 1.25]))
    a = ax[0]
    deg = np.degrees(th)
    a.fill_between(deg, 0, p, color=OK['grey'], alpha=0.25, lw=0, label='chip loss $p/p_{\\max}$')
    for fe, c, ls in ((2.0, OK['verm'], '-'), (10.0, OK['orange'], '--'), (50.0, OK['blue'], '-.')):
        T = periodic_rise(p, fe)
        a.plot(deg, T - T.min(), color=c, ls=ls, label=f'$\\tilde T_j$, $f_e$ = {fe:g} Hz (ripple {T.max() - T.min():.2f})')
    a.set_xlim(0, 360); a.set_xticks([0, 90, 180, 270, 360]); a.set_ylim(0, 1.25)
    a.set_xlabel('angle within the output period (deg)'); a.set_ylabel('normalised to $R\\,p_{\\max}$')
    a.legend(frameon=False, loc='upper right', fontsize=7)
    a.grid(alpha=.3, lw=0.4); label(a, '(a)')

    # (b) schematic history at start-up: slow component plus ripple at a rising output frequency
    b = ax[1]
    t = np.linspace(0, 12, 12000)
    fe = 0.4 + 0.8 * t                                   # output frequency rising during acceleration
    ripple_of = {f: np.ptp(periodic_rise(p, f)) for f in np.unique(np.round(fe, 2))}
    r = 30.0 * np.array([ripple_of[f] for f in np.round(fe, 2)]) / ripple_of[0.4]
    tbar = 40 + 22 * (1 - np.exp(-t / 5.0))
    phase = 2 * np.pi * np.cumsum(fe) * (t[1] - t[0])
    Tj = tbar + r / 2 * np.sin(phase)
    b.plot(t, Tj, color=OK['blue'], lw=0.8, label='$T_j$')
    b.plot(t, tbar, color=OK['black'], ls='--', lw=1.0, label='slow component $\\bar T_j$')
    b.plot(t, tbar + r / 2, color=OK['grey'], lw=0.5, ls=':')
    b.plot(t, tbar - r / 2, color=OK['grey'], lw=0.5, ls=':', label='ripple envelope, range $r$')
    # annotate the ripple cycle that starts at the minimum near t = 0.8 s (heating half-period up to the next maximum)
    i0 = np.searchsorted(t, 0.6)
    k = i0 + np.argmin(Tj[i0:i0 + 1500]); k2 = k + np.argmax(Tj[k:k + 1200])
    b.annotate('', (t[k] - 0.25, Tj[k2]), (t[k] - 0.25, Tj[k]), arrowprops=dict(arrowstyle='<->', lw=0.7, color=OK['verm']))
    b.plot([t[k] - 0.4, t[k2]], [Tj[k2]] * 2, color=OK['verm'], lw=0.5, ls=':')
    b.text(t[k] - 0.35, (Tj[k] + Tj[k2]) / 2, '$r$', color=OK['verm'], ha='right', va='center', fontsize=8)
    b.annotate('', (t[k2], Tj[k2] + 3.0), (t[k], Tj[k2] + 3.0), arrowprops=dict(arrowstyle='<->', lw=0.7, color=OK['verm']))
    b.text((t[k] + t[k2]) / 2, Tj[k2] + 3.6, '$t_{on}=1/(2f_e)$', color=OK['verm'], ha='center', va='bottom', fontsize=7)
    b.plot([t[k] - 0.1, t[k] + 1.3], [Tj[k]] * 2, color=OK['verm'], lw=0.6)
    b.text(t[k] + 1.4, Tj[k] - 0.5, '$T_{\\min}=\\bar T_j-r/2$', color=OK['verm'], va='center', fontsize=7)
    b.set_xlim(0, 12); b.set_ylim(15, 85)
    b.set_xlabel('time after start (s); $f_e$ rises from 0.4 to 10 Hz'); b.set_ylabel('$T_j$ (°C)')
    b.legend(frameon=False, loc='upper right', fontsize=7, ncol=1)
    b.grid(alpha=.3, lw=0.4); label(b, '(b)')
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


if __name__ == '__main__':
    fig_damage()
    fig_concept()
