"""Break-even capability of SiC-ANPC against Si-ANPC (substitution and both controlled) for the design variants with
the carrier-averaged and the pulse-resolved model (review round 4, item 7). Reads p04m_<variant>_<cfg>.json; where only
one technology changes in a variant (sic3k, sic5k: SiC; esw: Si) the base-case file of the other is used.
python p04_var_summary.py -> p04_var_summary.md"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
V = [('fvdr', 'Base case'), ('fvdr75', 'Derating to 75%'), ('fvdr_h2500', 'h_eff = 2500'), ('fvdr_h10000', 'h_eff = 10000'),
     ('fvdr_t10', 'Plate 10 mm'), ('fvdr_t30', 'Plate 30 mm'), ('fvdr_tw50', 'Coolant 50 C'), ('fvdr_tw60', 'Coolant 60 C'),
     ('fvdr_tw65', 'Coolant 65 C'), ('fvdr_sic3k', 'SiC at 3 kHz'), ('fvdr_sic5k', 'SiC at 5 kHz'),
     ('fvdr_esw', 'Si E_sw extrapolated'), ('fv', 'No derating'), ('fvdr_par', 'Two modules')]
SIC_ONLY, SI_ONLY = ('fvdr_sic3k', 'fvdr_sic5k'), ('fvdr_esw',)


def load(v, c):
    if (v in SIC_ONLY and c == 'Si-ANPC') or (v in SI_ONLY and c == 'SiC-ANPC'):
        v = 'fvdr'
    fn = os.path.join(HERE, f'p04m_{v}_{c}.json')
    return json.load(open(fn))['D'] if os.path.exists(fn) else None


rows, out = [], {}
hdr = ('| Variant | rule | model | kb subst. | kb both | gain har Si-ANPC | gain har SiC |', '|---|---|---|---|---|---|---|')
for v, lab in V:
    s, si = load(v, 'SiC-ANPC'), load(v, 'Si-ANPC')
    if s is None or si is None:
        rows.append(f'| {lab} | - | missing | | | | |')
        continue
    out[v] = {}
    for st in ('ton_clip', 'ton_free'):
        for m in ('averaged', 'no_us_term', 'nominal'):
            ks = s['base'][m][st] / si['har'][m][st]
            kb = s['har'][m][st] / si['har'][m][st]
            gsi = si['base'][m][st] / si['har'][m][st]
            gsc = s['base'][m][st] / s['har'][m][st]
            out[v][f'{st}/{m}'] = dict(kb_sub=ks, kb_both=kb, gain_si=gsi, gain_sic=gsc)
            rows.append(f'| {lab} | {st} | {m} | {ks:.2f} | {kb:.2f} | {gsi:.1f} | {gsc:.1f} |')
txt = '\n'.join(hdr + tuple(rows)) + '\n'
for st in ('ton_clip', 'ton_free'):
    for m in ('averaged', 'no_us_term', 'nominal'):
        vals = [(out[v][f'{st}/{m}']['kb_both'], v) for v in out]
        subs = [(out[v][f'{st}/{m}']['kb_sub'], v) for v in out]
        if vals:
            txt += (f'\n{st} {m}: kb both max {max(vals)[0]:.2f} ({max(vals)[1]}), min {min(vals)[0]:.2f}; '
                    f'kb subst range {min(subs)[0]:.2f}-{max(subs)[0]:.2f} over {len(vals)} variants')
open(os.path.join(HERE, 'p04_var_summary.md'), 'w', encoding='utf-8').write(txt + '\n')
json.dump(out, open(os.path.join(HERE, 'p04_var_summary.json'), 'w'), indent=1)
print(txt)
