"""Review round 2: control gains and kappa-bar with the pulse-resolved ripple correction (p04_kappa scaling) for all
three policies, reference variant.  python p04_gain.py -> p04_gain.md"""
import os, numpy as np
import phantich_p0 as pp, p04_kappa as pk

HERE = os.path.dirname(os.path.abspath(__file__))
L = ['| rule | model | gain ha NPC | gain har NPC | gain ha ANPC | gain har ANPC | gain ha SiC | gain har SiC | kappa sub ANPC | both ANPC |',
     '|---|---|---|---|---|---|---|---|---|---|']
for kn in ('ton_clip', 'ton_free'):
    nf = pp.KERNELS[kn]
    for corr in (False, True):
        S = {c: (pk.scaled('fvdr', c) if corr else pp.load('fvdr', c)) for c in pp.CFGS}
        D = {(c, t): pp.worst_damage(S[c], t, nf)[0] for c in pp.CFGS for t in ('base', 'ha', 'har')}
        g = lambda c, t: D[(c, 'base')] / D[(c, t)]
        L.append(f"| {kn} | {'pulse-corrected' if corr else 'averaged'} | {g('Si-NPC','ha'):.3g} | {g('Si-NPC','har'):.3g} | "
                 f"{g('Si-ANPC','ha'):.3g} | {g('Si-ANPC','har'):.3g} | {g('SiC-ANPC','ha'):.3g} | {g('SiC-ANPC','har'):.3g} | "
                 f"{D[('SiC-ANPC','base')]/D[('Si-ANPC','har')]:.3g} | {D[('SiC-ANPC','har')]/D[('Si-ANPC','har')]:.3g} |")
        print(L[-1], flush=True)
open(os.path.join(HERE, 'p04_gain.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
