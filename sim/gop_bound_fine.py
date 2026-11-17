"""Merge the tightened floor (p_bound_fine_<variant>_<cfg>.json) into daodong_<variant>_<cfg>.json as 'bounds_fine'
(same layout as 'bounds_tw': D_bound_rip per rule), and check that no simulated policy falls below it.
python gop_bound_fine.py"""
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
worst = (1e9, None)
worst_rip = (1e9, None)
ncase = 0
n = 0
for fn in sorted(glob.glob(os.path.join(HERE, 'p_bound_fine_*.json'))):
    f = json.load(open(fn))
    v, c = f.get('variant', 'fvdr'), f['cfg']
    dn = os.path.join(HERE, f'daodong_{v}_{c}.json')
    j = json.load(open(dn))
    if any(b.get('D_floor_published') is None for b in f['bounds'].values()):   # Kaggle runs: fill in locally
        for st, b in f['bounds'].items():
            b['D_floor_published'] = j['bounds_tw'][st]['D_bound_rip']
        json.dump(f, open(fn, 'w'), indent=1, default=float)
    j['bounds_fine'] = {st: dict(D_bound_rip=b['D_floor'], candidates=b['candidates'], D_floor_pairs=b['D_floor_pairs'], argmax=b['argmax'],
                                 ratio=f['ratio'], n_points=f['n_points'])
                        for st, b in f['bounds'].items()}
    json.dump(j, open(dn, 'w'), indent=1, default=float)
    n += 1
    for st, b in f['bounds'].items():
        for k, s in j['sim'].items():
            tag, rule = k.split('|')
            if rule == st:
                if tag not in ('base', 'ha', 'har'):
                    continue
                ncase += 1
                r = s['D'] / b['D_floor']
                if r < worst[0]:
                    worst = (r, f'{v} {c} {k}')
                r = s['D_rip'] / b['D_floor']
                if r < worst_rip[0]:
                    worst_rip = (r, f'{v} {c} {k}')
        print(f'{v:12s} {c:9s} {st}: ceiling {j["sim"][f"base|{st}"]["D"] / b["D_floor"]:7.1f} '
              f'(published {j["sim"][f"base|{st}"]["D"] / b["D_floor_published"]:7.1f})')
print(n, 'files merged;', ncase, 'cases; smallest D / floor:', worst, '; smallest D_rip / floor:', worst_rip)
