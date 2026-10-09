"""3D finite-volume model of the water-cooled heat sink (replaces the assumed R_hw, tau_hw).

Geometry (ASSUMPTIONS, varied in the sensitivity study): nine 152 x 62 mm modules (three legs of three modules)
on one aluminium cold plate, 10 mm gaps, plate 20 mm thick, k = 200 W/mK, rho*c = 2.42e6 J/m3K; the water
channels are lumped into an equivalent heat-transfer coefficient h_eff on the bottom face; other faces adiabatic.
Heat from a module enters uniformly over its footprint on the top face (the case-to-sink grease is part of the
module model). Output: steady module-to-module resistances and step responses, folded onto one leg (the three
legs carry the same mean loss pattern), and a 3-term Foster fit of every folded response.

python tannhiet.py  -> tannhiet.json, tannhiet.png
"""
import json, os, numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
G = dict(mod_x=0.062, mod_y=0.152, gap=0.010, t=0.020, k=200.0, rc=2.42e6, h=5000.0, dx=0.004, dz=0.004)


def build(g=G):
    npos = g.get('npos', 3)
    nx = int(round((npos * g['mod_x'] + (npos + 1) * g['gap']) / g['dx']))
    ny = int(round((3 * g['mod_y'] + 4 * g['gap']) / g['dx']))
    nz = int(round(g['t'] / g['dz']))
    N = nx * ny * nz
    idx = lambda i, j, k: (k * ny + j) * nx + i
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    gx = g['k'] * g['dx'] * g['dz'] / g['dx']       # conductance between x-neighbours (dy = dx)
    gz = g['k'] * g['dx'] * g['dx'] / g['dz']
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                p = idx(i, j, k)
                for (ii, jj, kk, gg) in ((i + 1, j, k, gx), (i, j + 1, k, gx), (i, j, k + 1, gz)):
                    if ii < nx and jj < ny and kk < nz:
                        q = idx(ii, jj, kk)
                        rows += [p, q]; cols += [q, p]; vals += [-gg, -gg]
                        diag[p] += gg; diag[q] += gg
    hconv = g['h'] * g['dx'] * g['dx'] / (0.5 * g['dz'] / g['k'] * g['h'] * g['dx'] * g['dx'] + 1)  # cell centre -> water
    bottom = [idx(i, j, 0) for j in range(ny) for i in range(nx)]
    diag[bottom] += hconv
    K = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N)) + sparse.diags(diag)
    C = np.full(N, g['rc'] * g['dx'] * g['dx'] * g['dz'])
    # module footprints on the top layer: leg l (row along y), position p (along x)
    foot = []
    for leg in range(3):
        for pos in range(npos):
            x0 = g['gap'] + pos * (g['mod_x'] + g['gap']); y0 = g['gap'] + leg * (g['mod_y'] + g['gap'])
            cells = [idx(i, j, nz - 1) for j in range(ny) for i in range(nx)
                     if x0 <= (i + 0.5) * g['dx'] <= x0 + g['mod_x'] and y0 <= (j + 0.5) * g['dx'] <= y0 + g['mod_y']]
            foot.append(np.array(cells))
    return K, C, foot, (nx, ny, nz)


def responses(g=G, t_end=300.0, dt=0.5):
    K, C, foot, shape = build(g)
    N = K.shape[0]
    nm = len(foot)
    B = np.zeros((N, nm))
    for m, cells in enumerate(foot):
        B[cells, m] = 1.0 / len(cells)                     # 1 W spread over the footprint
    Mavg = np.zeros((nm, N))
    for m, cells in enumerate(foot):
        Mavg[m, cells] = 1.0 / len(cells)                  # mean top temperature under each module
    Rss = Mavg @ splu(K.tocsc()).solve(B)                  # steady [nm x nm], K/W
    A = (sparse.diags(C / dt) + K).tocsc()
    lu = splu(A)
    nt = int(t_end / dt)
    X = np.zeros((N, nm)); Z = np.zeros((nt, nm, nm))
    for n in range(nt):
        X = lu.solve(C[:, None] / dt * X + B)
        Z[n] = Mavg @ X
    t = dt * np.arange(1, nt + 1)
    return Rss, t, Z


def fold(Rss, Z):
    """Leg-level response: source module of position j in every leg, observed at position i of the middle leg."""
    leg = 1
    Rf = np.zeros((3, 3)); Zf = np.zeros((Z.shape[0], 3, 3))
    for i in range(3):
        for j in range(3):
            src = [3 * l + j for l in range(3)]
            Rf[i, j] = Rss[3 * leg + i, src].sum()
            Zf[:, i, j] = Z[:, 3 * leg + i, src].sum(1)
    return Rf, Zf


def foster_fit(t, z, n=3):
    R0 = z[-1]
    def res(p):
        r, tau = np.exp(p[:n]), np.exp(p[n:])
        return (r[None, :] * (1 - np.exp(-t[:, None] / tau[None, :]))).sum(1) - z
    p0 = np.r_[np.log(np.full(n, max(R0, 1e-6) / n)), np.log([2.0, 15.0, 60.0])]
    sol = least_squares(res, p0)
    return np.exp(sol.x[:n]), np.exp(sol.x[n:]), float(np.max(np.abs(sol.fun)) / max(abs(R0), 1e-9))


def main():
    Rss, t, Z = responses()
    Rf, Zf = fold(Rss, Z)
    fits = {}
    for i in range(3):
        for j in range(3):
            r, tau, err = foster_fit(t, Zf[:, i, j])
            fits[f'{i}{j}'] = dict(R=r.tolist(), tau=tau.tolist(), rel_err=err)
    out = dict(geometry=G, R_single_module_self=float(Rss[4, 4]), R_folded=Rf.tolist(), foster=fits,
               note='folded: sum over the three legs of the source at the same position; middle leg observed')
    json.dump(out, open(os.path.join(HERE, 'tannhiet.json'), 'w'), indent=1)
    print('self resistance of the centre module alone (K/kW):', round(1e3 * Rss[4, 4], 2))
    print('folded leg matrix (K/kW):\n', np.round(1e3 * Rf, 2))
    for k, v in fits.items():
        print(k, 'R(K/kW)=', np.round(1e3 * np.array(v['R']), 2), 'tau(s)=', np.round(v['tau'], 1), 'fit err', round(v['rel_err'], 3))
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4))
    for i in range(3):
        for j in range(3):
            ax.plot(t, 1e3 * Zf[:, i, j], label=f'M{i+1} <- M{j+1}', lw=1.2 if i == j else 0.8, ls='-' if i == j else '--')
    ax.set_xlabel('t (s)'); ax.set_ylabel('Z sink (K/kW), three legs folded'); ax.grid(alpha=.3); ax.legend(fontsize=7, ncol=3)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, 'tannhiet.png'), dpi=110)


def fold_par(Rss, Z):
    """Two modules in parallel per position (6 per leg): observe the first module of type i in the middle leg,
    sum the sources of type j over both twins and all three legs."""
    leg, npos = 1, 6
    Rf = np.zeros((3, 3)); Zf = np.zeros((Z.shape[0], 3, 3))
    for i in range(3):
        for j in range(3):
            obs = npos * leg + 2 * i
            src = [npos * l + 2 * j + tw for l in range(3) for tw in (0, 1)]
            Rf[i, j] = Rss[obs, src].sum()
            Zf[:, i, j] = Z[:, obs, src].sum(1)
    return Rf, Zf


def variant_npz(tag, **over):
    """Write tannhiet_step_<tag>.npz for a geometry/convection variant (used by tran_daodong variant fv_<tag>)."""
    g = dict(G, **over)
    Rss, t, Z = responses(g)
    Rf, Zf = (fold_par if g.get('npos', 3) == 6 else fold)(Rss, Z)
    np.savez(os.path.join(HERE, f'tannhiet_step_{tag}.npz'), t=t, Zf=Zf, Rf=Rf)
    print(tag, 'folded diag (K/kW):', np.round(1e3 * np.diag(Rf), 2), 'coupling:', round(1e3 * Rf[0, 1], 2))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'par':
        variant_npz('par', npos=6)
    elif len(sys.argv) > 1 and sys.argv[1] == 'variants':
        variant_npz('h2500', h=2500.0); variant_npz('h10000', h=10000.0)
        variant_npz('t10', t=0.010); variant_npz('t30', t=0.030)
    else:
        main()
