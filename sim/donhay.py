"""Sensitivity study for R6 (one-at-a-time around the baseline).

python donhay.py <variant>      -> runs simulations, writes donhay_<variant>.json
python donhay.py tonghop        -> aggregates all json files into donhay.md

Simulation variants: base, ilim (low-speed current limit), rhw5, rhw20, tw60, sic5k (SiC at 5 kHz).
Damage-model settings applied to every simulation: ton_clip (CIPS08, t_on clipped to [1,15] s),
ton_free (t_on not clipped below), hoff_e10 / hoff_e4 / hoff_pl (SiC: Hoffmann 2023 + Cougo 2026 with
beta' = -10, -4, or plastic term only).
"""
import os, sys, json, numpy as np
import tonhao as th, tonthuong as tt, hanhtrinh as h

HERE = os.path.dirname(os.path.abspath(__file__))
CFGS = ('Si-NPC', 'Si-ANPC', 'SiC-ANPC')


def nf_setting(name):
    if name == 'ton_clip':
        return lambda d, Tm, on: tt.cips08_nf(d, Tm, on)
    if name == 'ton_free':
        def f(d, Tm, on):
            lo = tt.TON_RANGE; tt.TON_RANGE = (1e-4, 15.0)
            try:
                return tt.cips08_nf(d, Tm, on)
            finally:
                tt.TON_RANGE = lo
        return f
    if name == 'hoff_e10':
        return lambda d, Tm, on: tt.sic_nf_hoffmann(d, Tm, beta_e=-10.0)
    if name == 'hoff_e4':
        return lambda d, Tm, on: tt.sic_nf_hoffmann(d, Tm, beta_e=-4.0)
    if name == 'hoff_pl':
        return lambda d, Tm, on: 2.33e9 * np.power(d, -3.581) * np.exp(1537.0 / (Tm + 273.15))
    raise ValueError(name)


SETTINGS_SI = ('ton_clip', 'ton_free')
SETTINGS_SIC = ('ton_clip', 'ton_free', 'hoff_e10', 'hoff_e4', 'hoff_pl')


def limit_current(prof, k0=0.6, f_lim=5.0):
    """Low-speed current limit: I scaled by k0 at f_e = 0 rising linearly to 1 at f_lim (time axis kept)."""
    p = dict(prof)
    p['I'] = prof['I'] * np.minimum(1.0, k0 + (1 - k0) * prof['fe'] / f_lim)
    return p


def worst(dlist):
    k = int(np.argmax([d['D'] for d in dlist]))
    return dict(chip=k, D=dlist[k]['D'], D_low=dlist[k]['D_low'], D_rip=dlist[k]['D_rip'],
                dT=dlist[k]['dT_max'], Tpeak=dlist[k]['Tpeak'], rip=max(d['rip_max'] for d in dlist))


def run(variant):
    prof = h.load_profile(os.path.join(HERE, 'hoso_50km.csv'))
    cfgs = CFGS
    if variant == 'ilim':
        prof = limit_current(prof)
    elif variant == 'rhw5':
        th.R_HW = 5e-3
    elif variant == 'rhw20':
        th.R_HW = 20e-3
    elif variant == 'tw60':
        th.T_WATER = 60.0
    elif variant == 'sic5k':
        h.FSW = 5000.0
        cfgs = ('SiC-ANPC',)
    out = {}
    for cfg in cfgs:
        cache = h.OpCache(cfg)
        for tag in ('base', 'ha'):
            sim = h.simulate(cfg, prof, cache, tag)
            for st in (SETTINGS_SIC if cfg.startswith('SiC') else SETTINGS_SI):
                dj, ds = h.damages(sim, prof, nf=nf_setting(st))
                w = worst(dj)
                w['solder'] = max(d['D_rel'] for d in ds)
                w['dTc'] = max(d['dTc_max'] for d in ds)
                out[f'{cfg}|{tag}|{st}'] = w
        print(variant, cfg, 'done', flush=True)
    with open(os.path.join(HERE, f'donhay_{variant}.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)


def tonghop():
    import glob
    V = {}
    for fn in sorted(glob.glob(os.path.join(HERE, 'donhay_*.json'))):
        V[os.path.basename(fn)[7:-5]] = json.load(open(fn))
    base = V['base']
    get = lambda v, key: V[v].get(key, base.get(key))
    rows = []
    order = ['base', 'ilim', 'rhw5', 'rhw20', 'tw60', 'sic5k']
    for v in [o for o in order if o in V]:
        for st_si, st_sic in (('ton_clip', 'ton_clip'), ('ton_free', 'ton_free'),
                              ('ton_clip', 'hoff_e10'), ('ton_clip', 'hoff_e4'), ('ton_clip', 'hoff_pl')):
            if v != 'base' and (st_si, st_sic) != ('ton_clip', 'ton_clip') and v not in ('ilim',):
                continue
            g = lambda cfg, tag, st: get(v, f'{cfg}|{tag}|{st}')
            npc_b, npc_h = g('Si-NPC', 'base', st_si), g('Si-NPC', 'ha', st_si)
            anp_b, anp_h = g('Si-ANPC', 'base', st_si), g('Si-ANPC', 'ha', st_si)
            sic_b, sic_h = g('SiC-ANPC', 'base', st_sic), g('SiC-ANPC', 'ha', st_sic)
            kappa_model = st_sic.startswith('hoff')
            rows.append(dict(
                variant=v, model=f'Si:{st_si} / SiC:{st_sic}',
                rip_share_npc=npc_b['D_rip'] / npc_b['D'], rip_share_sic=sic_b['D_rip'] / sic_b['D'],
                gain_npc=npc_b['D'] / npc_h['D'], gain_anpc=anp_b['D'] / anp_h['D'], gain_sic=sic_b['D'] / sic_h['D'],
                # with a SiC-specific model the ratio is a direct comparison (SiC wins if < 1);
                # with CIPS08 it is the break-even capability kappa-bar (SiC wins if kappa > value)
                vs_npc_ha=sic_b['D'] / npc_h['D'], vs_anpc_ha=sic_b['D'] / anp_h['D'], vs_npc_base=sic_b['D'] / npc_b['D'],
                kind='D_SiC/D_Si (SiC wins if <1)' if kappa_model else 'kappa_bar (SiC wins if kappa > value)',
                solder_sic_vs_npcha=sic_b['solder'] / npc_h['solder'],
                solder_gain_npc=npc_b['solder'] / npc_h['solder'],
                rip_si=npc_b['rip'], rip_sic=sic_b['rip']))
    with open(os.path.join(HERE, 'donhay.md'), 'w', encoding='utf-8') as f:
        f.write('| variant | damage model | ripple share Si-NPC / SiC | gain HA NPC / ANPC / SiC | SiC vs NPC+HA | '
                'SiC vs ANPC+HA | SiC vs NPC base | meaning | solder SiC/(NPC+HA) | solder gain HA (NPC) | '
                'max ripple Si / SiC (K) |\n|' + '---|' * 11 + '\n')
        for r in rows:
            f.write(f"| {r['variant']} | {r['model']} | {r['rip_share_npc']:.0%} / {r['rip_share_sic']:.0%} | "
                    f"{r['gain_npc']:.1f} / {r['gain_anpc']:.1f} / {r['gain_sic']:.1f} | {r['vs_npc_ha']:.3g} | "
                    f"{r['vs_anpc_ha']:.3g} | {r['vs_npc_base']:.3g} | {r['kind']} | {r['solder_sic_vs_npcha']:.2f} | "
                    f"{r['solder_gain_npc']:.2f} | {r['rip_si']:.0f} / {r['rip_sic']:.0f} |\n")
    print(open(os.path.join(HERE, 'donhay.md'), encoding='utf-8').read())


if __name__ == '__main__':
    if sys.argv[1] == 'tonghop':
        tonghop()
    else:
        run(sys.argv[1])
