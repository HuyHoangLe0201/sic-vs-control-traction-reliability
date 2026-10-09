"""Rainflow counting and damage models for P4 (R6)."""
import numpy as np

# CIPS08 (Bayerer 2008, coefficient set with T_min); K from Lutz (2018) as used by Hoffmann (2020).
CIPS = dict(K=9.30e14, b1=-4.416, b2=1285.0, b3=-0.463, b4=-0.716, b5=-0.761, b6=-0.5,
            I_wire=10.0, V100=17.0, D_um=400.0)   # I, V, D terms are constants: they cancel in every ratio
TON_RANGE = (1.0, 15.0)   # s, CIPS08 data range; t_on is clipped to it (documented extrapolation guard)
DT_MIN = 0.5              # K, cycles below are ignored


def cips08_nf(dT, Tmin, ton, p=CIPS):
    ton = np.clip(ton, *TON_RANGE)
    return (p['K'] * np.power(dT, p['b1']) * np.exp(p['b2'] / (Tmin + 273.15)) * np.power(ton, p['b3'])
            * p['I_wire'] ** p['b4'] * p['V100'] ** p['b5'] * p['D_um'] ** p['b6'])


def sic_nf_hoffmann(dT, Tmin, beta_e=-10.0, T_knee=60.0):
    """SiC model of Hoffmann (2023) with the elastic low-dT term of Cougo (2026), eqs. (3)-(4)."""
    Kp, b1, b2 = 2.33e9, -3.581, 1537.0
    Ke = Kp * (-beta_e / 50.0) * (T_knee ** b1 / T_knee ** beta_e)
    return (Kp * np.power(dT, b1) + Ke * np.power(dT, beta_e)) * np.exp(b2 / (Tmin + 273.15))


def solder_nf_rel(dT, c=-0.442):
    """Engelmaier form N ~ dT^(1/c) (strain proportional to dT); geometry cancels in ratios."""
    return np.power(dT, 1.0 / c)


def reversals(x):
    """Indices of turning points (keeps first and last sample)."""
    dx = np.diff(x)
    keep = [0]
    s_prev = 0
    for i, d in enumerate(dx):
        s = np.sign(d)
        if s == 0:
            continue
        if s_prev != 0 and s != s_prev:
            keep.append(i)
        s_prev = s
    keep.append(len(x) - 1)
    return np.array(sorted(set(keep)))


def rainflow(x, t):
    """ASTM E1049 three-point rainflow. Returns list of (range, mean, count, duration_s)."""
    idx = reversals(x)
    pts = [(x[i], t[i]) for i in idx]
    stack, out = [], []
    for p in pts:
        stack.append(p)
        while len(stack) >= 3:
            X = abs(stack[-1][0] - stack[-2][0])
            Y = abs(stack[-2][0] - stack[-3][0])
            if X < Y:
                break
            if len(stack) == 3:
                out.append((Y, 0.5 * (stack[-2][0] + stack[-3][0]), 0.5, abs(stack[-2][1] - stack[-3][1])))
                stack.pop(0)
            else:
                out.append((Y, 0.5 * (stack[-2][0] + stack[-3][0]), 1.0, abs(stack[-2][1] - stack[-3][1])))
                last = stack.pop(); stack.pop(); stack.pop(); stack.append(last)
    for a, b in zip(stack[:-1], stack[1:]):
        out.append((abs(b[0] - a[0]), 0.5 * (a[0] + b[0]), 0.5, abs(b[1] - a[1])))
    return out


def damage_lowfreq(T, t, nf=cips08_nf, closed=True):
    """Miner damage of the slow (mean) temperature history. closed=True repeats the trip so the
    largest cycle (dwell -> peak) is counted as a full cycle."""
    if closed:
        k = int(np.argmin(T))
        T = np.r_[T[k:], T[:k + 1]]; t = np.r_[t[k:], t[:k + 1] + t[-1] + (t[1] - t[0])]
    D, cyc = 0.0, []
    for rng, mean, cnt, dur in rainflow(T, t):
        if rng < DT_MIN:
            continue
        Tmin = mean - rng / 2
        d = cnt / nf(rng, Tmin, dur)
        D += d
        cyc.append((rng, Tmin, cnt, dur, d))
    return D, cyc


def damage_ripple(Tmean, ripple, f_e, dt, nf=cips08_nf):
    """Cycles at the output frequency: f_e*dt cycles per step of range `ripple`."""
    n = f_e * dt
    m = ripple >= DT_MIN
    if not np.any(m):
        return 0.0
    ton = 1.0 / (2.0 * np.maximum(f_e[m], 1e-3))
    return float(np.sum(n[m] / nf(ripple[m], Tmean[m] - ripple[m] / 2, ton)))
