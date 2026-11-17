"""Replace the ceiling columns (NPC, ANPC) of Table tab:sens in P4_CAEE/sec5_robust.tex by the tightened floor
('bounds_fine', clipped rule). python cap_nhat_bang_sens.py"""
import io, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
FN = os.path.join(HERE, '..', 'P4_CAEE', 'sec5_robust.tex')
V = {'Base case': 'fvdr', 'Derating to 75\\%': 'fvdr75', '$h_{\\mathrm{eff}}=2500$': 'fvdr_h2500',
     '$h_{\\mathrm{eff}}=10000$': 'fvdr_h10000', 'Plate \\SI{10}{mm}': 'fvdr_t10', 'Plate \\SI{30}{mm}': 'fvdr_t30',
     'Coolant \\SI{50}{\\celsius}': 'fvdr_tw50', 'Coolant \\SI{60}{\\celsius}': 'fvdr_tw60',
     'Coolant \\SI{65}{\\celsius}': 'fvdr_tw65', 'SiC at \\SI{3}{kHz}': 'fvdr_sic3k', 'SiC at \\SI{5}{kHz}': 'fvdr_sic5k',
     'Si $E_{sw}$ extrapolated$^{a}$': 'fvdr_esw', 'No derating': 'fv', 'Two modules': 'fvdr_par'}


def ceil(v, c):
    j = json.load(open(os.path.join(HERE, f'daodong_{v}_{c}.json')))
    return j['sim']['base|ton_clip']['D'] / j['bounds_fine']['ton_clip']['D_bound_rip']


s = io.open(FN, encoding='utf-8').read()
a = s.index('\\label{tab:sens}'); b = s.index('\\bottomrule', a)
lines = s[a:b].split('\n')
n = 0
for i, l in enumerate(lines):
    cells = [x.strip() for x in l.rstrip(' \\').split('&')]
    if len(cells) == 9 and cells[0] in V:
        v = V[cells[0]]
        old = cells[3:5]
        cells[3], cells[4] = f'{ceil(v, "Si-NPC"):.0f}', f'{ceil(v, "Si-ANPC"):.0f}'
        lines[i] = ' & '.join(cells) + ' \\\\'
        n += 1
        print(cells[0], old, '->', cells[3:5])
assert n == len(V), n
s = s[:a] + '\n'.join(lines) + s[b:]
io.open(FN, 'w', encoding='utf-8', newline='\n').write(s)
