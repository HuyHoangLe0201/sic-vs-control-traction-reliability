"""Supplementary tables: all mission variants, one table per heating-time rule.
python bang_allvar.py -> appC_allvar.tex (Tables C.4 and C.5) in the output folder"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
V = [('fvdr', 'Base case'), ('fvdr75', 'Derating to 75\\%'), ('fvdr_h2500', '$h_{\\mathrm{eff}}=2500$'),
     ('fvdr_h10000', '$h_{\\mathrm{eff}}=10000$'), ('fvdr_t10', 'Plate \\SI{10}{mm}'), ('fvdr_t30', 'Plate \\SI{30}{mm}'),
     ('fvdr_tw50', 'Coolant \\SI{50}{\\celsius}'), ('fvdr_tw60', 'Coolant \\SI{60}{\\celsius}'),
     ('fvdr_tw65', 'Coolant \\SI{65}{\\celsius}'), ('fvdr_sic3k', 'SiC \\SI{3}{kHz}'), ('fvdr_sic5k', 'SiC \\SI{5}{kHz}'),
     ('fvdr_esw', 'Si $E_{sw}$ extrapolated'), ('fv', 'No derating'), ('fvdr_par', 'Two modules'),
     ('fvdr_u0.3', '$u=0.3$'), ('fvdr_u0.4', '$u=0.4$'), ('fvdr_u0.5', '$u=0.5$'), ('fvdr_u0.6', '$u=0.6$'), ('fvdr_u0.7', '$u=0.7$')]
C = ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')
J = {v: {c: json.load(open(os.path.join(HERE, f'daodong_{v}_{c}.json'))) for c in C} for v, _ in V}


def table(st, rule, label, extra=''):
    rows = []
    for v, lab in V:
        D = lambda c, t: J[v][c]['sim'][f'{t}|{st}']['D']
        sh = [f"{100 * J[v][c]['sim'][f'base|{st}']['D_rip'] / D(c, 'base'):.0f}" for c in C]
        ce = [f"{D(c, 'base') / J[v][c]['bounds_tw'][st]['D_bound_rip']:.0f}" for c in C]
        ga = [f"{D(c, 'base') / D(c, 'har'):.1f}" for c in C]
        rows.append(lab + ' & ' + ' & '.join(sh + ce + ga) + r' \\')
    return r'''\begin{table}[p]
\centering
\caption{All variants, ''' + rule + r''' rule: ripple share, ceiling and reduction by the ripple-aware law.}
\label{''' + label + r'''}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}lccccccccc@{}}
\toprule
 & \multicolumn{3}{c}{Ripple share (\%)} & \multicolumn{3}{c}{Ceiling} & \multicolumn{3}{c}{Ripple-aware law} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(l){8-10}
Variant & NPC & ANPC & SiC & NPC & ANPC & SiC & NPC & ANPC & SiC \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular*}
''' + extra + r'''\end{table}
'''


note = r'''
\smallskip
\begin{minipage}{\linewidth}\footnotesize
NPC, ANPC, SiC: Si-NPC, Si-ANPC and SiC-ANPC inverters; $h_{\mathrm{eff}}$ in \si{W/(m^2\cdot K)}.
\end{minipage}
'''
tex = table('ton_clip', 'clipped', 'tab:allvar', note) + '\n' + table('ton_free', 'unclipped', 'tab:allvar2', note)
OUT = os.environ.get('P4_OUT', os.path.join(HERE, 'out')); os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'appC_allvar.tex'), 'w', encoding='utf-8').write(tex)
print(tex[:900])
