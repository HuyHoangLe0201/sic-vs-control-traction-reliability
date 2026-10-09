"""Figure F8: break-even capability and control gains versus module utilisation (peak current / 600 A rating).
Sweep: fvdr_u0.3 ... fvdr_u0.7 and fvdr (u = 0.77); cross-check point: fvdr_par (two parallel modules, u = 0.385).
python hinh_f8.py -> hinh_F8.png, f8.md
"""
import os, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PTS = [(0.3, 'fvdr_u0.3'), (0.4, 'fvdr_u0.4'), (0.5, 'fvdr_u0.5'), (0.6, 'fvdr_u0.6'), (0.7, 'fvdr_u0.7'), (0.77, 'fvdr')]
plt.rcParams.update({'font.size': 9})


def load(v, cfg):
    fn = os.path.join(HERE, f'daodong_{v}_{cfg}.json')
    return json.load(open(fn)) if os.path.exists(fn) else None


def metrics(v, st):
    npc, anpc, sic = load(v, 'Si-NPC'), load(v, 'Si-ANPC'), load(v, 'SiC-ANPC')
    if not (npc and anpc and sic):
        return None
    D = lambda d, tag: d['sim'][f'{tag}|{st}']['D']
    B = lambda d: d.get('bounds_tw', d['bounds'])[st]['D_bound_rip']
    return dict(k_sub_npc=D(sic, 'base') / D(npc, 'har'), k_sub_anpc=D(sic, 'base') / D(anpc, 'har'),
                k_both_anpc=D(sic, 'har') / D(anpc, 'har'), k_bound_anpc=D(sic, 'base') / B(anpc),
                g_npc=D(npc, 'base') / D(npc, 'har'), g_anpc=D(anpc, 'base') / D(anpc, 'har'),
                c_npc=D(npc, 'base') / B(npc), c_anpc=D(anpc, 'base') / B(anpc),
                solder=sic['sim'][f'base|{st}']['solder'] / anpc['sim'][f'har|{st}']['solder'])


def crossing(u, k, level):
    """Utilisation where log(kappa-bar) crosses `level` (linear interpolation in u), or None."""
    lk = np.log(k); ll = np.log(level)
    for i in range(len(u) - 1):
        if (lk[i] - ll) * (lk[i + 1] - ll) <= 0 and lk[i] != lk[i + 1]:
            return u[i] + (ll - lk[i]) * (u[i + 1] - u[i]) / (lk[i + 1] - lk[i])
    return None


def main():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    lines = ['| t_on rule | u | kappa_sub vs NPC+har | kappa_sub vs ANPC+har | kappa_both vs ANPC | kappa_bound vs ANPC | '
             'gain har NPC / ANPC | ceiling NPC / ANPC | solder SiC/(ANPC+har) |', '|' + '---|' * 9]
    cross = []
    for st, ls in (('ton_clip', '-'), ('ton_free', '--')):
        rows = [(u, metrics(v, st)) for u, v in PTS]
        rows = [(u, m) for u, m in rows if m]
        u = np.array([r[0] for r in rows])
        for key, col, lab in (('k_sub_npc', 'C0', 'SiC substitution vs Si-NPC + ripple law'),
                              ('k_sub_anpc', 'C1', 'SiC substitution vs Si-ANPC + ripple law'),
                              ('k_both_anpc', 'C2', 'both with ripple law (vs Si-ANPC)')):
            k = np.array([r[1][key] for r in rows])
            ax[0].semilogy(u, k, ls, color=col, marker='o', ms=3, label=f'{lab}, {st}')
        for key, col, lab in (('g_npc', 'C0', 'Si-NPC ripple law'), ('g_anpc', 'C1', 'Si-ANPC ripple law'),
                              ('c_npc', 'C0', 'Si-NPC ceiling'), ('c_anpc', 'C1', 'Si-ANPC ceiling')):
            ax[1].semilogy(u, [r[1][key] for r in rows], ls, color=col, marker='s' if key[0] == 'c' else 'o', ms=3,
                           alpha=1 if key[0] == 'g' else 0.5, label=f'{lab}, {st}')
        for uu, m in rows:
            lines.append(f"| {st} | {uu:.2f} | {m['k_sub_npc']:.3g} | {m['k_sub_anpc']:.3g} | {m['k_both_anpc']:.3g} | "
                         f"{m['k_bound_anpc']:.3g} | {m['g_npc']:.3g} / {m['g_anpc']:.3g} | {m['c_npc']:.3g} / {m['c_anpc']:.3g} | "
                         f"{m['solder']:.3g} |")
        ksa = np.array([r[1]['k_sub_anpc'] for r in rows])
        for lev in (0.25, 0.33, 0.6):
            cross.append((st, lev, crossing(u, ksa, lev)))
    par = {st: metrics('fvdr_par', st) for st in ('ton_clip', 'ton_free')}
    for st, mk in (('ton_clip', 'X'), ('ton_free', 'P')):
        if par[st]:
            ax[0].scatter([0.385], [par[st]['k_sub_anpc']], marker=mk, color='k', zorder=5,
                          label=f'two parallel modules (own heat sink), vs Si-ANPC, {st}')
    ax[0].axhspan(0.25, 0.6, color='grey', alpha=.2, label='published soldered SiC: kappa = 0.25-0.6')
    ax[0].set_xlabel('module utilisation u = peak current / rated current'); ax[0].set_ylabel('break-even capability kappa-bar')
    ax[0].grid(alpha=.3, which='both'); ax[0].legend(fontsize=6, loc='lower right')
    ax[1].set_xlabel('module utilisation u'); ax[1].set_ylabel('reduction of per-trip damage (x)')
    ax[1].grid(alpha=.3, which='both'); ax[1].legend(fontsize=6, ncol=2)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, 'hinh_F8.png'), dpi=130)
    lines.append('')
    for st, lev, uc in cross:
        lines.append(f'- {st}: SiC substitution vs Si-ANPC + ripple law reaches kappa-bar = {lev} at u = '
                     + (f'{uc:.2f}' if uc is not None else 'outside the sweep'))
    if par['ton_clip']:
        lines.append(f"- cross-check, two parallel modules (u = 0.385): kappa_sub vs ANPC = {par['ton_clip']['k_sub_anpc']:.3g} "
                     f"(ton_clip), {par['ton_free']['k_sub_anpc']:.3g} (ton_free)")
    open(os.path.join(HERE, 'f8.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
