"""Device models for P4 (MR version), digitized 2026-10-06 from the Mitsubishi datasheets in
TaiLieu_P4/datasheet/:
  Si : CM600DX-34T   (1700 V / 600 A IGBT + FWD, publication Jan 2025)
  SiC: FMF600DXE-34BN (1700 V / 600 A full SiC MOSFET, publication Oct 2023)

Values marked "table" are printed typical values; all others are read by eye from the
"typical" performance curves (chip level), estimated reading error about +-2 % of full scale.
Anchor points (table values) are checked in self_check().
"""
import numpy as np

# ----------------------------------------------------------------------------------- Si IGBT
# Collector-emitter saturation voltage, chip, VGE = 15 V (p. 9, top right; table p. 4)
SI_I = np.array([0, 100, 200, 300, 400, 600, 800, 1000, 1200.0])
SI_VCE = {   # T [degC] -> V
    25:  np.array([0, 1.10, 1.32, 1.50, 1.65, 1.95, 2.22, 2.48, 2.75]),
    125: np.array([0, 1.10, 1.45, 1.72, 1.93, 2.35, 2.75, 3.13, 3.53]),
    150: np.array([0, 1.10, 1.48, 1.77, 2.00, 2.45, 2.88, 3.28, 3.73]),
}
# FWD forward voltage, chip (p. 9, bottom right; table p. 4)
SI_IF = np.array([0, 100, 200, 400, 600, 800, 1000, 1200.0])
SI_VF = {
    25:  np.array([0, 1.45, 1.70, 2.22, 2.62, 3.00, 3.35, 3.68]),
    125: np.array([0, 1.27, 1.62, 2.22, 2.73, 3.12, 3.50, 3.85]),
    150: np.array([0, 1.25, 1.60, 2.22, 2.75, 3.15, 3.53, 3.90]),
}
# Switching energies per pulse [mJ], VCC = 1000 V, RG = 0 ohm (p. 10, bottom left; table p. 4 at 150 C)
SI_IE = np.array([0, 60, 200, 400, 600, 800, 1000, 1200.0])
SI_EON = {125: np.array([0, 14, 30, 62, 103, 158, 218, 292]),
          150: np.array([0, 17, 35, 70, 117.4, 180, 258, 355])}
SI_EOFF = {125: np.array([0, 27, 53, 90, 132, 180, 240, 305]),
           150: np.array([0, 30, 60, 100, 143.7, 195, 255, 327])}
SI_ERR = {125: np.array([0, 27, 44, 58, 65, 69, 72, 74]),
          150: np.array([0, 36, 54, 69, 78, 83, 86, 88])}
SI_VREF = 1000.0
# Thermal (table p. 5; Foster table p. 11, normalized to Rth(j-c))
SI_RTH_JC_IGBT = 53e-3      # K/W
SI_RTH_JC_FWD = 81e-3       # K/W
SI_RTH_CS_MODULE = 11.5e-3  # K/W, case to heat sink per module, grease
SI_FOSTER_R = np.array([0.0124, 0.0739, 0.3505, 0.5632])   # normalized, sum ~ 1
SI_FOSTER_TAU = np.array([1.961e-5, 1.4e-3, 1.79e-2, 9.44e-2])  # s

# ----------------------------------------------------------------------------------- SiC MOSFET
# Drain-source on-state voltage, chip, VGS = 15 V, forward (p. 6, top right; table p. 2)
SIC_I = np.array([0, 100, 200, 300, 400, 600, 800, 1000, 1200.0])
SIC_VDS = {
    25:  np.array([0, 0.20, 0.42, 0.63, 0.86, 1.35, 1.92, 2.50, 3.18]),
    125: np.array([0, 0.32, 0.65, 1.00, 1.35, 2.09, 2.90, 3.85, 4.93]),
    150: np.array([0, 0.37, 0.75, 1.13, 1.52, 2.38, 3.40, 4.42, 5.68]),
}
# Reverse conduction with channel on (synchronous rectification), VGS = 15 V (p. 7, top right)
SIC_IR = np.array([0, 200, 400, 600, 800, 1000, 1200.0])
SIC_VSD_SYNC = {
    25:  np.array([0, 0.36, 0.73, 1.08, 1.45, 1.80, 2.20]),
    125: np.array([0, 0.63, 1.28, 1.93, 2.60, 3.30, 4.08]),
    150: np.array([0, 0.72, 1.47, 2.23, 3.00, 3.75, 4.70]),
}
# Body diode (VGS = -7 V), only during dead time: table p. 2, chip, at 600 A
SIC_VSD_BODY_600 = {25: 4.20, 125: 3.84, 150: 3.77}
# Switching energies per pulse [mJ], VDD = 900 V, RG = 1.2/0.75 ohm, Tvj = 150 C only (p. 8; table p. 2)
SIC_IE = np.array([0, 60, 200, 400, 600, 800, 1000, 1200.0])
SIC_EON_150 = np.array([0, 6.0, 14.0, 24.5, 36.0, 48.5, 62.5, 78.0])
SIC_EOFF_150 = np.array([0, 1.0, 1.8, 5.5, 11.0, 17.5, 26.5, 37.5])
SIC_ERR_150 = np.array([0, 1.5, 5.5, 12.0, 18.0, 23.5, 28.0, 32.0])
SIC_VREF = 900.0
SIC_RTH_JC = 60e-3          # K/W per switch
SIC_RTH_CS_MODULE = 15e-3   # K/W per module
SIC_FOSTER_R = np.array([2.13e-2, 7.32e-2, 2.33e-1, 6.65e-1])
SIC_FOSTER_TAU = np.array([1.51e-5, 4.57e-4, 6.19e-3, 3.45e-2])

# Voltage scaling exponent of switching energy, E ~ (V/Vref)^KV. Assumption (no curve in the
# datasheets); varied in Monte Carlo.
KV_SI, KV_SIC = 1.0, 1.0


def _interp_T(table, T):
    """Linear interpolation (and extrapolation) in temperature between tabulated curves."""
    Ts = sorted(table)
    T = float(T)
    if T <= Ts[0]:
        a, b = Ts[0], Ts[1]
    elif T >= Ts[-1]:
        a, b = Ts[-2], Ts[-1]
    else:
        a = max(t for t in Ts if t <= T); b = min(t for t in Ts if t > T)
    w = (T - a) / (b - a)
    return (1 - w) * np.asarray(table[a]) + w * np.asarray(table[b])


def _lookup(x, table, T, i):
    return np.interp(np.abs(i), x, _interp_T(table, T))


# --- Si
def si_vce(i, T): return _lookup(SI_I, SI_VCE, T, i)
def si_vf(i, T): return _lookup(SI_IF, SI_VF, T, i)
def si_eon(i, T, V): return 1e-3 * _lookup(SI_IE, SI_EON, max(T, 25), i) * (V / SI_VREF) ** KV_SI
def si_eoff(i, T, V): return 1e-3 * _lookup(SI_IE, SI_EOFF, max(T, 25), i) * (V / SI_VREF) ** KV_SI
def si_err(i, T, V): return 1e-3 * _lookup(SI_IE, SI_ERR, max(T, 25), i) * (V / SI_VREF) ** KV_SI


# --- SiC (switching energies given only at 150 C: taken temperature-independent, an assumption
#     that is conservative below 150 C only if E rises with T; varied +-15 % in Monte Carlo)
def sic_vds(i, T): return _lookup(SIC_I, SIC_VDS, T, i)
def sic_vsd_sync(i, T): return _lookup(SIC_IR, SIC_VSD_SYNC, T, i)
def sic_eon(i, T, V): return 1e-3 * np.interp(np.abs(i), SIC_IE, SIC_EON_150) * (V / SIC_VREF) ** KV_SIC
def sic_eoff(i, T, V): return 1e-3 * np.interp(np.abs(i), SIC_IE, SIC_EOFF_150) * (V / SIC_VREF) ** KV_SIC
def sic_err(i, T, V): return 1e-3 * np.interp(np.abs(i), SIC_IE, SIC_ERR_150) * (V / SIC_VREF) ** KV_SIC


def fit_v0_r(vtable, x, T, imin=150, imax=800):
    """Least-squares v0 + r*i fit over the operating current range."""
    m = (x >= imin) & (x <= imax)
    A = np.c_[np.ones(m.sum()), x[m]]
    v0, r = np.linalg.lstsq(A, _interp_T(vtable, T)[m], rcond=None)[0]
    return v0, r


def rel_tempco(f, i, T1=25, T2=150):
    """Relative temperature coefficient c = d ln p / dT, averaged between T1 and T2."""
    return np.log(f(i, T2) / f(i, T1)) / (T2 - T1)


def self_check():
    """Compare digitized curves with the printed table values (anchors)."""
    rows = [
        ('Si VCEsat 600A 25C', si_vce(600, 25), 1.95), ('Si VCEsat 600A 125C', si_vce(600, 125), 2.35),
        ('Si VCEsat 600A 150C', si_vce(600, 150), 2.45), ('Si VEC 600A 25C', si_vf(600, 25), 2.65),
        ('Si VEC 600A 150C', si_vf(600, 150), 2.75),
        ('Si Eon 600A 150C [mJ]', 1e3 * si_eon(600, 150, 1000), 117.4),
        ('Si Eoff 600A 150C [mJ]', 1e3 * si_eoff(600, 150, 1000), 143.7),
        ('Si Err 600A 150C [mJ]', 1e3 * si_err(600, 150, 1000), 78.0),
        ('SiC VDS 600A 25C', sic_vds(600, 25), 1.35), ('SiC VDS 600A 125C', sic_vds(600, 125), 2.09),
        ('SiC VDS 600A 150C', sic_vds(600, 150), 2.38),
        ('SiC Eon 600A [mJ]', 1e3 * sic_eon(600, 150, 900), 36.0),
        ('SiC Eoff 600A [mJ]', 1e3 * sic_eoff(600, 150, 900), 11.0),
        ('SiC Err 600A [mJ]', 1e3 * sic_err(600, 150, 900), 18.0),
        ('Si Foster sum', SI_FOSTER_R.sum(), 1.0), ('SiC Foster sum', SIC_FOSTER_R.sum(), 1.0),
    ]
    return [(n, float(v), ref, 100 * (float(v) - ref) / ref) for n, v, ref in rows]


if __name__ == '__main__':
    print(f"{'anchor':28s} {'model':>8s} {'table':>8s} {'err %':>7s}")
    for n, v, ref, e in self_check():
        print(f'{n:28s} {v:8.3f} {ref:8.3f} {e:7.2f}')
    print()
    for T in (25, 125, 150):
        v0, r = fit_v0_r(SI_VCE, SI_I, T)
        v0d, rd = fit_v0_r(SI_VF, SI_IF, T)
        v0s, rs = fit_v0_r(SIC_VDS, SIC_I, T)
        print(f'T={T:3d} C  Si IGBT v0={v0:.3f} V r={1e3*r:.3f} mOhm | FWD v0={v0d:.3f} V r={1e3*rd:.3f} mOhm | '
              f'SiC v0={v0s:.3f} V r={1e3*rs:.3f} mOhm')
    print()
    for i in (300, 462, 600):
        print(f'I={i:4d} A  c(Si VCE)={rel_tempco(si_vce, i):.5f}/K  c(Si VF)={rel_tempco(si_vf, i):.5f}/K  '
              f'c(SiC VDS)={rel_tempco(sic_vds, i):.5f}/K  c(Si Eon,125-150)='
              f'{np.log(si_eon(i,150,900)/si_eon(i,125,900))/25:.5f}/K')
