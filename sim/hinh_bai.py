"""Publication figures for the MR manuscript (baseline variant fvdr), following the Elsevier artwork rules:
vector PDF (fonts embedded), one file per figure (Figures 2, 4, 7-9 and E.2 (file Figure_E2); Figures 1 and 3 from hinh_mach.py, 5, 6, 10 and E.1 from hinh_coche.py), single column 90 mm / full width 190 mm,
text of at least 7 pt, colour-blind-safe Okabe-Ito palette with redundant line styles and markers.

python hinh_bai.py  -> Figure_N.pdf (+ .png at 1000 dpi) in the output folder
"""
import os, csv, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import tonhao as th, tonthuong as tt, dao_dong as dd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('P4_OUT', os.path.join(HERE, 'out'))
os.makedirs(OUT, exist_ok=True)
th.use_sink(os.path.join(HERE, 'tannhiet_step.npz'))
VAR = 'fvdr'
MM = 1 / 25.4
W1, W2 = 90 * MM, 190 * MM          # Elsevier: single column 90 mm, full width 190 mm
OK = dict(black='#000000', orange='#E69F00', sky='#56B4E9', green='#009E73', yellow='#F0E442', blue='#0072B2',
          verm='#D55E00', purple='#CC79A7', grey='#8C8C8C')
CFG = {'Si-NPC': (OK['blue'], 'o', '-'), 'Si-ANPC': (OK['verm'], 's', '--'), 'SiC-ANPC': (OK['green'], '^', '-.')}
LAW = {'base': (OK['grey'], 'baseline', ':'), 'ha': (OK['orange'], 'mean-temperature law', '--'),
       'har': (OK['blue'], 'ripple-aware law', '-')}
plt.rcParams.update({'font.size': 8, 'axes.labelsize': 8, 'legend.fontsize': 7, 'xtick.labelsize': 7,
                     'ytick.labelsize': 7, 'axes.linewidth': 0.6, 'lines.linewidth': 1.0, 'pdf.fonttype': 42,
                     'ps.fonttype': 42, 'savefig.bbox': 'standard',
                     'figure.constrained_layout.use': True})   # exact Elsevier widths, no cropping


FIGNO = {'M': 2, 1: 4, 2: 'E2', 4: 7, 5: 8, 8: 9}   # internal id -> figure number (1, 3: hinh_mach.py; 5, 6, 10, E1: hinh_coche.py; E2: Appendix E; code figures 3, 6, 7 unused)


def save(fig, n):
    k = FIGNO[n]
    fig.savefig(os.path.join(OUT, f'Figure_{k}.pdf'))
    fig.savefig(os.path.join(OUT, f'Figure_{k}.png'), dpi=1000)   # line art: >= 1000 dpi
    plt.close(fig)
    print('Figure', k, 'ok', flush=True)


def label(ax, s):
    ax.text(-0.13, 1.02, s, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom')


def figM():
    """Model chain (a) and redundancy of the three-level leg: feasible offset band and the five offset levels (b)."""
    from matplotlib.patches import FancyBboxPatch
    fig, ax = plt.subplots(1, 2, figsize=(W2, 62 * MM), gridspec_kw=dict(width_ratios=[1.25, 1]))
    a = ax[0]; a.set_xlim(0, 10); a.set_ylim(0, 10.4); a.axis('off')
    boxes = [(0.2, 8.1, 'Train model\n& derating', 'mission $I_{pk},m,\\cos\\varphi,f_e$'),
             (0.2, 5.6, 'Loss tables\n(modulation, offset, path)', 'chip losses vs angle'),
             (0.2, 3.1, 'Policy $\\mathbf{x}$ (linear program)\nbaseline / laws', 'time shares per bin'),
             (5.2, 8.1, 'Foster + finite-volume\nheat sink (electro-thermal)', '$\\bar T_j(t)$, ripple $r(t)$'),
             (5.2, 5.6, 'Rainflow + CIPS08\n(two $t_{on}$ rules)', 'damage per run'),
             (5.2, 3.1, 'Break-even $\\bar\\kappa$\nMonte Carlo, Sobol', 'SiC vs Si'),
             (2.7, 0.4, 'Linear-program bounds\nmean temperature $T^*$ and ripple', '')]
    for x, y, t, s in boxes:
        w = 4.4 if x < 5 or x > 5 else 4.4
        if y < 1:
            w = 6.8
        a.add_patch(FancyBboxPatch((x, y), w, 1.9, boxstyle='round,pad=0.05', fc='#F2F2F2', ec=OK['grey'], lw=0.6))
        a.text(x + w / 2, y + (1.3 if s else 0.95), t, ha='center', va='center', fontsize=7)
        if s:
            a.text(x + w / 2, y + 0.3, s, ha='center', va='center', fontsize=7, color=OK['blue'])
    arr = dict(arrowstyle='->', lw=0.7, color=OK['black'])
    for (x0, y0), (x1, y1) in [((2.4, 8.1), (2.4, 7.55)), ((2.4, 5.6), (2.4, 5.05)), ((4.65, 3.9), (5.2, 8.9)),
                               ((7.4, 8.1), (7.4, 7.55)), ((7.4, 5.6), (7.4, 5.05)), ((2.4, 3.1), (4.0, 2.35))]:
        a.annotate('', (x1, y1), (x0, y0), arrowprops=arr)
    label(a, '(a)')
    b = ax[1]
    m = 0.5
    ua, v0 = th.offsets(m)
    deg = np.degrees(th.TH)
    A = 2 * m / np.sqrt(3)
    us = np.stack([A * np.sin(th.TH - k * 2 * np.pi / 3) for k in range(3)])
    lo, hi = -1 - us.min(0), 1 - us.max(0)
    b.fill_between(deg, lo, hi, color=OK['sky'], alpha=0.25, lw=0, label='feasible offset band')
    for r in range(th.NOFF):
        b.plot(deg, v0[r], color=OK['blue'], lw=0.6, ls='-' if r == th.NOFF // 2 else ':',
               label='offset levels' if r == 0 else None)
    b.plot(deg, ua + v0[th.NOFF // 2], color=OK['verm'], lw=1.0, label='leg-a reference, centred offset')
    b.axhline(0, color=OK['grey'], lw=0.4)
    for k in range(0, 360, 10):
        b.axvline(k, color=OK['grey'], lw=0.15, alpha=0.5)
    b.set_xlim(0, 360); b.set_xticks(range(0, 361, 90)); b.set_xlabel(r'angle $\theta$ (deg), 36 bins')
    b.set_ylabel('normalised voltage'); b.set_ylim(-1.15, 1.15)
    b.legend(frameon=False, fontsize=7, loc='lower left', ncol=1)
    label(b, '(b)')
    save(fig, 'M')


def fig1():
    rows = list(csv.DictReader(open(os.path.join(HERE, 'hoso_50km_dr.csv'))))
    g = lambda k: np.array([float(r[k]) for r in rows])
    t = g('t_s')
    fig, ax = plt.subplots(4, 1, figsize=(W1, 105 * MM), sharex=True)
    for a, (k, lab) in zip(ax, (('v_kmh', 'v (km/h)'), ('I_pk_A', r'$I_{pk}$ (A)'), ('m', '$m$'), ('f_e_Hz', r'$f_e$ (Hz)'))):
        a.plot(t, g(k), color=OK['black'], lw=0.9); a.set_ylabel(lab); a.grid(alpha=.3, lw=0.4)
    ax[-1].set_xlabel('t (s)')
    fig.align_ylabels(ax)
    save(fig, 1)


def fig2():
    rows = []
    for line in open(os.path.join(HERE, 'tran_lp.csv')).read().splitlines()[1:]:
        p = line.split(',')
        rows.append(dict(cfg=p[0], mode=p[1], I=float(p[2]), m=float(p[3]), eta=float(p[9])))
    fig, ax = plt.subplots(2, 3, figsize=(W2, 72 * MM), sharex=True, sharey=True)
    styles = {200: (OK['sky'], 'o', ':'), 300: (OK['blue'], 's', '--'), 462: (OK['verm'], '^', '-'), 600: (OK['black'], 'D', '-.')}
    for j, cfg in enumerate(('Si-NPC', 'Si-ANPC', 'SiC-ANPC')):
        for i, mode in enumerate(('motor', 'brake')):
            a = ax[i, j]
            for I, (c, mk, ls) in styles.items():
                sel = [r for r in rows if r['cfg'] == cfg and r['mode'] == mode and int(r['I']) == I]
                a.plot([r['m'] for r in sel], [r['eta'] for r in sel], ls=ls, marker=mk, ms=3, color=c,
                       label=fr'$I_{{pk}}$ = {I} A')
            a.set_title(f'{cfg}, {"motoring" if mode == "motor" else "braking"}', fontsize=8)
            a.grid(alpha=.3, lw=0.4)
            if i == 1: a.set_xlabel('modulation index $m$')
            if j == 0: a.set_ylabel(r'$\eta$')
    ax[0, 0].legend(frameon=False)
    save(fig, 2)


def fig3():
    fig, axes = plt.subplots(1, 2, figsize=(W2, 55 * MM), gridspec_kw=dict(width_ratios=[10, 6]))
    for ax, cfg, lab in zip(axes, ('Si-NPC', 'SiC-ANPC'), ('(a)', '(b)')):
        r = th.analyse_point(cfg, 462, 0.1, 0.95, 1500, fe=5.0)      # with the NP constraint at 5 Hz
        tp = r['tp']
        LT = th.at_temp(r['L'], r['Tb'])
        G = dd.ripple_map(tp, LT, 5.0)
        Aeq, beq, _ = dd.eq_constraints(tp, r['inpb'], r['g'])
        rr = lambda x: (G @ x).max(1) - (G @ x).min(1)
        Mp = np.transpose(th.bin_avg(LT), (3, 2, 0, 1)).reshape(tp['nchip'], -1) / th.NBIN
        _, xh, rh, _, _ = dd.ripple_lp(tp, G, Aeq, beq, npc=r['npc'], tie=(r['Z'] @ Mp, th.T_WATER, 0.02))
        vals = [('base', rr(r['wb'].reshape(-1))), ('ha', rr(r['w_eq'].reshape(-1))), ('har', rh)]
        x = np.arange(tp['nchip']); w = 0.27
        hatches = {'base': '', 'ha': '////', 'har': ''}
        for i, (k, v) in enumerate(vals):
            ax.bar(x + (i - 1) * w, v, w, color=LAW[k][0], hatch=hatches[k], edgecolor='white', lw=0.3, label=LAW[k][1])
        ax.axhline(rh.max(), color=OK['verm'], ls='--', lw=0.9, label='single-point bound (min–max ripple)')
        ax.set_xticks(x); ax.set_xticklabels(tp['names'], fontsize=7); ax.set_ylabel('ripple, peak to peak (K)')
        ax.set_title(f'{cfg}', fontsize=8); ax.grid(axis='y', alpha=.3, lw=0.4); label(ax, lab)
    axes[0].legend(frameon=False)
    save(fig, 3)


def load(cfg):
    return np.load(os.path.join(HERE, f'mophong_{VAR}_{cfg}.npz'))


def worst(d, tag):
    t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    D = [tt.damage_lowfreq(d[f'{tag}_Tj'][:, k], t)[0] + tt.damage_ripple(d[f'{tag}_Tj'][:, k], d[f'{tag}_rip'][:, k], fe, dt)
         for k in range(d[f'{tag}_Tj'].shape[1])]
    return int(np.argmax(D)), D


def fig4():
    fig, axes = plt.subplots(3, 1, figsize=(W2, 96 * MM), sharex=True)
    for ax, cfg, lab in zip(axes, ('Si-NPC', 'Si-ANPC', 'SiC-ANPC'), ('(a)', '(b)', '(c)')):
        d = load(cfg)
        for tag in ('base', 'ha', 'har'):
            k, _ = worst(d, tag)
            T, r = d[f'{tag}_Tj'][:, k], d[f'{tag}_rip'][:, k]
            c, name, ls = LAW[tag]
            ax.plot(d['t'], T, color=c, ls=ls, lw=0.9, label=f'{name} ({d["names"][k]})')
            ax.fill_between(d['t'], T - r / 2, T + r / 2, color=c, alpha=.18, lw=0)
        ax.set_ylabel(r'$T_j$ (°C)'); ax.set_title(cfg, fontsize=8); ax.grid(alpha=.3, lw=0.4)
        lo_, hi_ = ax.get_ylim(); ax.set_ylim(lo_, hi_ + 0.35 * (hi_ - lo_))      # headroom for the legend
        ax.legend(frameon=False, loc='upper center', ncol=3); label(ax, lab)
    axes[-1].set_xlabel('t (s)')
    save(fig, 4)


def fig5():
    bands = [(0.5, 2), (2, 5), (5, 10), (10, 30), (30, 100), (100, 300)]
    cols = [OK['black'], OK['purple'], OK['sky'], OK['blue'], OK['green'], OK['orange'], OK['verm']]
    names = ['mean-temperature cycles'] + [f'ripple {a}–{b} Hz' for a, b in bands]
    fig, ax = plt.subplots(figsize=(W2, 50 * MM))
    ylabs = []
    for ci, cfg in enumerate(('Si-NPC', 'Si-ANPC', 'SiC-ANPC')):
        d = load(cfg); t, fe = d['t'], d['fe']; dt = t[1] - t[0]
        k, D = worst(d, 'base')
        Tj, rip = d['base_Tj'][:, k], d['base_rip'][:, k]
        sh = [tt.damage_lowfreq(Tj, t)[0] / D[k]]
        for lo, hi in bands:
            m = (fe >= lo) & (fe < hi)
            sh.append(tt.damage_ripple(Tj, np.where(m, rip, 0), fe, dt) / D[k])
        left = 0
        for j, s in enumerate(sh):
            ax.barh(ci, s, left=left, color=cols[j], edgecolor='white', lw=0.3, label=names[j] if ci == 0 else None)
            left += s
        ylabs.append(f'{cfg} ({d["names"][k]})')
    ax.set_yticks(range(3)); ax.set_yticklabels(ylabs); ax.set_xlim(0, 1); ax.invert_yaxis()
    ax.set_xlabel('share of per-run junction-level damage (baseline)')
    ax.legend(frameon=False, ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.32))
    save(fig, 5)


def fig6():
    fig, ax = plt.subplots(figsize=(W1, 60 * MM))
    w = 0.26
    keys = [('ha', OK['orange'], '////', 'mean-temperature law'), ('har', OK['blue'], '', 'ripple-aware law'),
            ('ceil', OK['verm'], '....', 'ceiling, any redundant-state law')]
    for ci, cfg in enumerate(('Si-NPC', 'Si-ANPC', 'SiC-ANPC')):
        j = json.load(open(os.path.join(HERE, f'daodong_{VAR}_{cfg}.json')))
        s = j['sim']; base = s['base|ton_clip']['D']
        vals = [base / s['ha|ton_clip']['D'], base / s['har|ton_clip']['D'], base / j.get('bounds_tw', j['bounds'])['ton_clip']['D_bound_rip']]
        for i, ((k, c, h, lab), v) in enumerate(zip(keys, vals)):
            ax.bar(ci + (i - 1) * w, v, w, color=c, hatch=h, edgecolor='white', lw=0.3, label=lab if ci == 0 else None)
            ax.text(ci + (i - 1) * w, v * 1.07, f'{v:.0f}' if v >= 20 else f'{v:.1f}', ha='center', fontsize=7)
    ax.set_yscale('log'); ax.set_xticks(range(3)); ax.set_xticklabels(['Si-NPC', 'Si-ANPC', 'SiC-ANPC'])
    ax.set_ylim(1, 1000)
    from matplotlib.ticker import LogLocator, ScalarFormatter
    ax.yaxis.set_major_locator(LogLocator(subs=(1, 2, 5))); ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.set_ylabel('per-run damage reduction (×)'); ax.grid(axis='y', alpha=.3, lw=0.4, which='both')
    ax.legend(frameon=False, loc='upper left', ncol=1, fontsize=7)
    save(fig, 6)


def fig7():
    V = {}
    import glob
    for fn in glob.glob(os.path.join(HERE, 'daodong_*_*-*.json')):
        d = json.load(open(fn)); V.setdefault(d['variant'], {})[d['cfg']] = d
    order = [('fvdr', 'base case'), ('fvdr75', 'derating 75%'), ('fvdr_h2500', r'$h_{eff}$ 2500'),
             ('fvdr_h10000', r'$h_{eff}$ 10000'), ('fvdr_t10', 'plate 10 mm'), ('fvdr_t30', 'plate 30 mm'),
             ('fvdr_tw50', r'$T_w$ 50 °C'), ('fvdr_tw60', r'$T_w$ 60 °C'), ('fvdr_tw65', r'$T_w$ 65 °C'),
             ('fvdr_sic3k', 'SiC 3 kHz'), ('fvdr_sic5k', 'SiC 5 kHz'), ('fvdr_esw', r'Si $E_{sw}$ extrap.'), ('fv', 'no derating'), ('fvdr_par', 'two modules')]
    order = [(v, n) for v, n in order if v in V]
    fig, ax = plt.subplots(figsize=(W2, 65 * MM))
    for vi, (v, _) in enumerate(order):
        get = lambda cfg: V[v][cfg]
        for st, mk in (('ton_clip', 'o'), ('ton_free', 's')):
            sb = get('SiC-ANPC')['sim'][f'base|{st}']['D']; sh = get('SiC-ANPC')['sim'][f'har|{st}']['D']
            for cfg, dx in (('Si-NPC', -0.12), ('Si-ANPC', 0.12)):
                c = CFG[cfg][0]; Dh = get(cfg)['sim'][f'har|{st}']['D']
                rule = 'clipped' if st == 'ton_clip' else 'unclipped'
                ax.scatter(vi + dx, sb / Dh, marker=mk, color=c, s=14, zorder=3)
                ax.scatter(vi + dx, sh / Dh, marker=mk, facecolors='none', edgecolors=c, s=14, zorder=3)
    ax.axhspan(0.25, 0.6, color=OK['grey'], alpha=.25, lw=0)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    hd = [Line2D([], [], ls='', marker='o', color=OK['black'], ms=4, label='SiC substitution (filled)'),
          Line2D([], [], ls='', marker='o', mfc='none', mec=OK['black'], ms=4, label='both with ripple-aware law (open)'),
          Line2D([], [], ls='', marker='s', color=CFG['Si-NPC'][0], ms=4, label='vs Si-NPC'),
          Line2D([], [], ls='', marker='s', color=CFG['Si-ANPC'][0], ms=4, label='vs Si-ANPC'),
          Line2D([], [], ls='', marker='o', color=OK['grey'], ms=4, label='circle: clipped rule'),
          Line2D([], [], ls='', marker='s', color=OK['grey'], ms=4, label='square: unclipped rule'),
          Patch(color=OK['grey'], alpha=.25, label=r'soldered SiC, $\kappa$ = 0.25–0.6')]
    ax.set_yscale('log'); ax.set_xticks(range(len(order))); ax.set_xticklabels([n for _, n in order], rotation=20)
    ax.set_ylabel(r'break-even capability $\bar\kappa$'); ax.grid(alpha=.3, lw=0.4, which='both')
    ax.legend(handles=hd, frameon=False, ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.3))
    save(fig, 7)


def fig8():
    import hinh_f8 as f8
    fig, ax = plt.subplots(1, 2, figsize=(W2, 65 * MM))
    for st, ls in (('ton_clip', '-'), ('ton_free', '--')):
        rows = [(u, f8.metrics(v, st)) for u, v in f8.PTS]
        rows = [(u, m) for u, m in rows if m]
        u = np.array([r[0] for r in rows])
        first = st == 'ton_clip'      # legend once; line style (solid/dashed) = heating-time rule, see caption
        for key, cfg, lab in (('k_sub_npc', 'Si-NPC', 'substitution vs Si-NPC'), ('k_sub_anpc', 'Si-ANPC', 'substitution vs Si-ANPC'),
                              ('k_both_anpc', 'SiC-ANPC', 'both controlled, vs Si-ANPC')):
            ax[0].semilogy(u, [r[1][key] for r in rows], ls=ls, marker=CFG[cfg][1], ms=3, color=CFG[cfg][0],
                           label=lab if first else None)
        for key, cfg, lab in (('g_npc', 'Si-NPC', 'Si-NPC, ripple-aware law'), ('g_anpc', 'Si-ANPC', 'Si-ANPC, ripple-aware law'),
                              ('c_npc', 'Si-NPC', 'Si-NPC, ceiling'), ('c_anpc', 'Si-ANPC', 'Si-ANPC, ceiling')):
            ax[1].semilogy(u, [r[1][key] for r in rows], ls=ls, marker=CFG[cfg][1] if key[0] == 'g' else 'x', ms=3,
                           color=CFG[cfg][0], alpha=1 if key[0] == 'g' else 0.55, label=lab if first else None)
    par = f8.metrics('fvdr_par', 'ton_clip')
    if par:
        ax[0].scatter([0.385], [par['k_sub_anpc']], marker='*', s=40, color=OK['black'], zorder=5,
                      label='two parallel modules')
    ax[0].axhspan(0.25, 0.6, color=OK['grey'], alpha=.25, lw=0, label=r'soldered SiC, $\kappa$ = 0.25–0.6')
    ax[0].set_xlabel('peak module utilisation $u$'); ax[0].set_ylabel(r'break-even capability $\bar\kappa$')
    ax[1].set_xlabel('peak module utilisation $u$'); ax[1].set_ylabel('damage reduction (×)')
    for a, lab in zip(ax, ('(a)', '(b)')):
        a.grid(alpha=.3, lw=0.4, which='both'); label(a, lab)
        a.legend(frameon=False, fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
    save(fig, 8)


def figGA():
    """Graphical abstract, 13 x 5 cm (Elsevier: >= 531 x 1328 px, readable at 5 x 13 cm)."""
    import hinh_f8 as f8
    fig, ax = plt.subplots(1, 3, figsize=(13 / 2.54, 5 / 2.54), gridspec_kw=dict(wspace=0.55))
    plt.rcParams.update({'font.size': 6})
    # 1: where the wear comes from (Si-NPC baseline)
    d = load('Si-NPC'); t, fe = d['t'], d['fe']; dt = t[1] - t[0]
    k, D = worst(d, 'base'); Tj, rip = d['base_Tj'][:, k], d['base_rip'][:, k]
    lf = tt.damage_lowfreq(Tj, t)[0] / D[k]
    low = tt.damage_ripple(Tj, np.where(fe < 30, rip, 0), fe, dt) / D[k]
    ax[0].bar([0, 1, 2], [lf, low, 1 - lf - low], color=[OK['grey'], OK['verm'], OK['sky']])
    ax[0].set_xticks([0, 1, 2]); ax[0].set_xticklabels(['mean\ncycles', 'ripple\n<30 Hz', 'ripple\n>30 Hz'], fontsize=5.5)
    ax[0].set_ylabel('share of chip wear', fontsize=6); ax[0].set_title('Si (baseline): start & stop', fontsize=6.5)
    # 2: control vs ceiling
    vals = []
    for cfg in ('Si-NPC', 'Si-ANPC'):
        j = json.load(open(os.path.join(HERE, f'daodong_{VAR}_{cfg}.json'))); s = j['sim']; b = s['base|ton_clip']['D']
        vals.append((b / s['har|ton_clip']['D'], b / j.get('bounds_tw', j['bounds'])['ton_clip']['D_bound_rip']))
    x = np.arange(2)
    ax[1].bar(x - 0.18, [v[0] for v in vals], 0.36, color=OK['blue'], label='ripple-aware law')
    ax[1].bar(x + 0.18, [v[1] for v in vals], 0.36, color=OK['verm'], hatch='....', edgecolor='white', lw=0.2, label='LP ceiling')
    ax[1].set_xticks(x); ax[1].set_xticklabels(['Si-NPC', 'Si-ANPC'], fontsize=5.5); ax[1].set_ylabel('damage reduction (×)', fontsize=6)
    ax[1].legend(frameon=False, fontsize=5, loc='upper left'); ax[1].set_title('how much control can buy', fontsize=6.5)
    # 3: design rule
    rows = [(u, f8.metrics(v, 'ton_clip')) for u, v in f8.PTS]
    u = [r[0] for r in rows]
    ax[2].semilogy(u, [r[1]['k_sub_anpc'] for r in rows], '-s', ms=2, color=OK['verm'], label='SiC vs controlled Si')
    ax[2].semilogy(u, [r[1]['k_both_anpc'] for r in rows], '-^', ms=2, color=OK['green'], label='both controlled')
    ax[2].axhspan(0.25, 0.6, color=OK['grey'], alpha=.3, lw=0)
    ax[2].text(0.31, 0.32, 'soldered SiC', fontsize=5)
    ax[2].set_xlabel('module utilisation', fontsize=6); ax[2].set_ylabel(r'break-even $\bar\kappa$', fontsize=6)
    ax[2].legend(frameon=False, fontsize=5, loc='lower right'); ax[2].set_title('SiC or control?', fontsize=6.5)
    for a in ax:
        a.tick_params(labelsize=5.5); a.grid(alpha=.3, lw=0.3)
    fig.savefig(os.path.join(OUT, 'graphical_abstract.pdf'))
    fig.savefig(os.path.join(OUT, 'graphical_abstract.png'), dpi=400)
    plt.close(fig)
    print('GA ok')


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or ['M', '1', '2', '4', '5', '8']):
        globals()[f'fig{n}']()
