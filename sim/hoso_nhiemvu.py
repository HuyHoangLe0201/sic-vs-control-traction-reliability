"""Mission profile for P4 (MR version): one station-to-station run of a high-speed EMU, translated
to the operating point (I_pk, m, cos phi, f_e) of one 650 kW inverter.

No standard drive cycle or open measured data exist for high-speed trains (Perpina 2012), so the
profile is generated from a train model. Every parameter below is an ASSUMPTION chosen to be
typical of an 8-car 300 km/h EMU with 1C1M PMSM drives; all are varied in the sensitivity study.
Electrical rated point taken from the project model (CoSoToanHoc.tex, sec. 650 kW):
650 kW, Vdc = 1800 V, I_pk = 462 A at m = 0.95 (SVPWM-normalized), cos phi = 0.95.
"""
import numpy as np

P = dict(
    n_motor=16,            # 1C1M: one 650 kW inverter per PMSM
    P_rated=650e3,         # W, electrical, per inverter
    M=480e3,               # kg, loaded train mass
    xi=1.06,               # rotating-mass factor
    a0=0.5,                # m/s^2, starting acceleration (adhesion / comfort limit)
    b_service=0.5,         # m/s^2, service deceleration
    davis=(6.4e3, 0.044e3, 0.00055e3),  # R = A + B v + C v^2, N with v in km/h
    v_max=300 / 3.6,       # m/s
    r_w=0.43,              # m, wheel radius
    G=2.7,                 # gear ratio
    pole_pairs=3,
    eta_m=0.96, eta_g=0.975,
    Vdc=1800.0, m_rated=0.95, I_rated=462.0, cosphi=0.95,
    L_station=50e3,        # m, station spacing
    t_dwell=120.0,         # s, station dwell
    v_fade=7 / 3.6,        # m/s, electric brake fades out below this speed
    derate_k0=None,        # low-output-frequency current derating: k = k0 at 0 Hz rising linearly to 1 at derate_f
    derate_f=10.0,         # Hz (Siemens SINAMICS S120 GH2, 04/2014, Fig. 6-22: 50 % at 0 Hz -> 100 % at 10 Hz)
    dt=0.1,
)


def resistance(v, p=P):
    A, B, C = p['davis']; vk = 3.6 * v
    return A + B * vk + C * vk ** 2


def derived(p=P):
    eta = p['eta_m'] * p['eta_g']
    Pw_max = p['n_motor'] * p['P_rated'] * eta          # wheel power limit, W
    F_max = p['xi'] * p['M'] * p['a0'] + resistance(0, p)
    v_base = Pw_max / F_max
    return eta, Pw_max, F_max, v_base


def run(p=P):
    eta, Pw_max, F_max, v_base = derived(p)
    dt, L = p['dt'], p['L_station']

    def k_der(v):   # current (hence torque) derating at low output frequency
        if p['derate_k0'] is None:
            return 1.0
        fe = p['pole_pairs'] * v / p['r_w'] * p['G'] / (2 * np.pi)
        return min(1.0, p['derate_k0'] + (1 - p['derate_k0']) * fe / p['derate_f'])

    def f_trac(v):  # maximum tractive force at wheels
        return min(F_max * k_der(v), Pw_max / max(v, 1e-6))

    def f_brake_e(v):  # maximum electric braking force (same power limit, regenerative),
        # faded out linearly below v_fade where friction brakes take over
        return min(F_max * k_der(v), Pw_max / max(v, 1e-6)) * min(1.0, v / p['v_fade'])

    # braking curve: distance needed to stop from v at service deceleration
    def d_stop(v):
        return v * v / (2 * p['b_service'])

    rows = []
    t, x, v = 0.0, 0.0, 0.0
    phase = 'accel'
    while True:
        R = resistance(v, p)
        if phase in ('accel', 'cruise') and L - x <= d_stop(v):
            phase = 'brake'
        if phase == 'accel':
            F = f_trac(v)
            if v >= p['v_max']:
                phase = 'cruise'
        if phase == 'cruise':
            F = R
        if phase == 'brake':
            F_need = -(p['xi'] * p['M'] * p['b_service'] - R)  # negative: braking force at wheels
            F = max(F_need, -f_brake_e(v))                      # rest is friction braking
        a = (F - R) / (p['xi'] * p['M']) if phase != 'brake' else -p['b_service']
        if phase == 'cruise':
            a = 0.0
        rows.append((t, x, v, a, F, phase))
        v_new = v + a * dt
        if phase == 'brake' and v_new <= 0:
            break
        if phase == 'accel' and v_new > p['v_max']:
            v_new = p['v_max']
        x += 0.5 * (v + v_new) * dt
        v = v_new
        t += dt
    # dwell
    t_end = t
    for k in range(1, int(p['t_dwell'] / dt) + 1):
        rows.append((t_end + k * dt, L, 0.0, 0.0, 0.0, 'dwell'))
    return rows


def electrical(rows, p=P):
    """Per-inverter operating point from the wheel force."""
    eta, Pw_max, F_max, v_base = derived(p)
    Vpk_max = p['m_rated'] * p['Vdc'] / np.sqrt(3)
    w_base = v_base / p['r_w'] * p['G']
    T_rated = Pw_max / p['n_motor'] / p['eta_g'] / w_base           # motor torque at F_max
    out = []
    for (t, x, v, a, F, ph) in rows:
        w_m = v / p['r_w'] * p['G']
        T_m = F * p['r_w'] / p['n_motor'] / p['G'] * (1 / p['eta_g'] if F >= 0 else p['eta_g'])
        P_mech = T_m * w_m
        P_e = P_mech / p['eta_m'] if F >= 0 else P_mech * p['eta_m']
        f_e = p['pole_pairs'] * w_m / (2 * np.pi)
        if ph == 'dwell' or abs(T_m) < 1e-9:
            I_pk, m, cphi = 0.0, 0.0, 0.0
        else:
            # one formula in both regions (voltage ~ speed below base speed, at its limit above), so the
            # current is continuous at the base speed in motoring and in braking
            k = min(1.0, w_m / w_base)
            m = p['m_rated'] * k
            if k > 1e-3:
                I_pk = abs(P_e) / (1.5 * Vpk_max * k * p['cosphi'])
            else:   # standstill limit: current ~ torque
                I_pk = p['I_rated'] * abs(T_m) / T_rated * (1.0 if T_m >= 0 else p['eta_m'] ** 2)
            cphi = p['cosphi'] * np.sign(T_m)
        out.append((t, x, 3.6 * v, a, F / 1e3, ph, T_m, w_m * 60 / (2 * np.pi), f_e, I_pk, m, cphi, P_e / 1e3))
    return out


HEADER = 't_s,x_m,v_kmh,a_ms2,F_kN,phase,T_Nm,n_rpm,f_e_Hz,I_pk_A,m,cosphi,P_e_kW'


def summary(el, p=P):
    import collections
    eta, Pw_max, F_max, v_base = derived(p)
    dt = p['dt']
    dur = collections.Counter(r[5] for r in el)
    lines = [f'Train: F_max = {F_max/1e3:.1f} kN, wheel power = {Pw_max/1e6:.2f} MW, base speed = {3.6*v_base:.0f} km/h',
             f'Station spacing {p["L_station"]/1e3:.0f} km, total trip time {el[-1][0]:.0f} s']
    for ph in ('accel', 'cruise', 'brake', 'dwell'):
        sel = [r for r in el if r[5] == ph]
        if not sel:
            continue
        I = np.array([r[9] for r in sel]); m = np.array([r[10] for r in sel]); fe = np.array([r[8] for r in sel])
        lines.append(f'{ph:6s}: {dur[ph]*dt:7.1f} s | I_pk {I.min():5.0f}-{I.max():5.0f} A | m {m.min():.2f}-{m.max():.2f} | '
                     f'f_e {fe.min():5.1f}-{fe.max():5.1f} Hz')
    return '\n'.join(lines)


if __name__ == '__main__':
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    cases = [(50e3, None, ''), (25e3, None, '')]
    if len(sys.argv) > 1 and sys.argv[1] == 'derate':
        cases = [(50e3, 0.5, '_dr'), (50e3, 0.75, '_dr75')]
    for L, k0, suf in cases:
        p = dict(P, L_station=L, derate_k0=k0)
        el = electrical(run(p), p)
        tag = f'{int(L/1e3)}km{suf}'
        with open(os.path.join(here, f'hoso_{tag}.csv'), 'w') as f:
            f.write(HEADER + '\n')
            for r in el:
                f.write(','.join(str(round(c, 4)) if not isinstance(c, str) else c for c in r) + '\n')
        print(f'--- {tag}'); print(summary(el, p))
        if len(sys.argv) > 1 and sys.argv[1] in ('plot', 'derate'):
            import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
            a = np.array([[r[0], r[2], r[9], r[10], r[8], r[12]] for r in el])
            fig, ax = plt.subplots(4, 1, figsize=(8, 8), sharex=True)
            for k, (j, lab) in enumerate([(1, 'v (km/h)'), (2, 'I_pk (A)'), (3, 'm'), (4, 'f_e (Hz)')]):
                ax[k].plot(a[:, 0], a[:, j], lw=1); ax[k].set_ylabel(lab); ax[k].grid(alpha=.3)
            ax[-1].set_xlabel('t (s)'); fig.suptitle(f'Mission profile, station spacing {tag}')
            fig.tight_layout(); fig.savefig(os.path.join(here, f'hoso_{tag}.png'), dpi=110)
