"""Appendix E table: break-even capability of SiC-ANPC against Si-ANPC with ripple-aware control, carrier-averaged model
and pulse-resolved best estimate (without the microsecond term), for every design variant of Table 3.
python bang_pulsevar.py -> appE_pulsevar.tex (reads p04_var_summary.json written by p04_var_summary.py)"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('P4_OUT', os.path.join(HERE, 'out')); os.makedirs(OUT, exist_ok=True)
S = json.load(open(os.path.join(HERE, 'p04_var_summary.json')))
V = [('fvdr', 'Base case'), ('fvdr75', r'Derating to 75\%'), ('fvdr_h2500', r'$h_{\mathrm{eff}}=2500$'),
     ('fvdr_h10000', r'$h_{\mathrm{eff}}=10000$'), ('fvdr_t10', r'Plate \SI{10}{mm}'), ('fvdr_t30', r'Plate \SI{30}{mm}'),
     ('fvdr_tw50', r'Coolant \SI{50}{\celsius}'), ('fvdr_tw60', r'Coolant \SI{60}{\celsius}'),
     ('fvdr_tw65', r'Coolant \SI{65}{\celsius}'), ('fvdr_sic3k', r'SiC at \SI{3}{kHz}'), ('fvdr_sic5k', r'SiC at \SI{5}{kHz}'),
     ('fvdr_esw', r'Si $E_{sw}$ extrapolated'), ('fv', 'No derating'), ('fvdr_par', 'Two modules')]
L = [r'\begin{table}[pos=!htbp]', r'\centering',
     r'\caption{Break-even capability $\kb$ of SiC-ANPC against Si-ANPC with the ripple-aware law for every design variant: carrier-averaged model and pulse-resolved best estimate (without the microsecond term).}',
     r'\label{tab:pulsevar}', r'\small', r'\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}lcccccccc@{}}', r'\toprule',
     r' & \multicolumn{4}{c}{Clipped rule} & \multicolumn{4}{c}{Unclipped rule} \\',
     r'\cmidrule(lr){2-5}\cmidrule(l){6-9}',
     r' & \multicolumn{2}{c}{Substitution} & \multicolumn{2}{c}{Both} & \multicolumn{2}{c}{Substitution} & \multicolumn{2}{c}{Both} \\',
     r'\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(l){8-9}',
     r'Variant & Avg. & Pulse & Avg. & Pulse & Avg. & Pulse & Avg. & Pulse \\', r'\midrule']
for v, lab in V:
    if v not in S:
        continue
    c = []
    for st in ('ton_clip', 'ton_free'):
        for q in ('kb_sub', 'kb_both'):
            c += [S[v][f'{st}/averaged'][q], S[v][f'{st}/no_us_term'][q]]
    order = [c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]]
    L.append(lab + ' & ' + ' & '.join(f'{x:.2f}' for x in order) + r' \\')
L += [r'\bottomrule', r'\end{tabular*}', '', r'\smallskip', r'\begin{minipage}{\linewidth}\footnotesize',
      r'Avg.: carrier-averaged model; Pulse: pulse-resolved model without the microsecond term. Substitution: SiC with the baseline policy; Both: both inverters with the ripple-aware law.',
      r'\end{minipage}', r'\end{table}']
open(os.path.join(OUT, 'appE_pulsevar.tex'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
