# Reproduction code: damage ceilings of redundant-state thermal control and break-even capability of SiC

Simulation code and result files for the paper

> *Redundant-state thermal control versus SiC: damage ceilings and break-even capability in traction inverters*, submitted to Microelectronics Reliability.

The study compares, for a 650 kW three-level traction inverter on a high-speed mission, loss redistribution through
redundant switching states (Si NPC and ANPC legs) with the substitution of Si IGBTs by SiC MOSFETs (SiC ANPC leg). All
results are obtained by simulation.

## Contents

| Path | Content |
|---|---|
| `sim/*.py` | Models, simulation drivers, post-processing, figures and tables (Python, flat layout; every script reads and writes in its own folder) |
| `sim/daodong_<variant>_<cfg>.json` | Mission results per variant and configuration: damage under the three policies, both heating-time rules, damage floor and ceiling |
| `sim/p04m_*.json`, `sim/ptmin_*.json` | Pulse-resolved correction (Section 5.2) and true-minimum check (Appendix D) |
| `sim/hoso_*.csv` | Mission profiles (0.1 s step) |
| `sim/tannhiet_step*.npz`, `sim/tannhiet.json` | Step responses of the finite-volume heat-sink model |
| `sim/tran_lp*.csv` | Redistributable-imbalance index over the operating-point grid (Fig. E.2) |
| `sim/summaries/*.md` | Outputs of the post-processing scripts as used in the paper |
| Release asset `P4_code_histories.zip` | Simulated junction-temperature histories `mophong_<variant>_<cfg>.npz` (57 files, about 200 MB), needed by the post-processing scripts |

Configurations: `Si-NPC`, `Si-ANPC`, `SiC-ANPC`. Variants (19): `fvdr` (base case), `fvdr75`, `fvdr_h2500`,
`fvdr_h10000`, `fvdr_t10`, `fvdr_t30`, `fvdr_tw50`, `fvdr_tw60`, `fvdr_tw65`, `fvdr_sic3k`, `fvdr_sic5k`, `fvdr_esw`,
`fv` (no derating), `fvdr_par` (two parallel modules) and `fvdr_u0.3` ... `fvdr_u0.7` (utilisation sweep).

The device characteristics were digitised from the manufacturer datasheets of the Mitsubishi Electric CM600DX-34T and
FMF600DXE-34BN modules (cited in the paper) and are contained in `sim/linhkien.py`; the datasheets themselves are not
redistributed. Source comments and some identifiers are partly in Vietnamese.

## Requirements

Python 3.12 with the packages in `requirements.txt` (tested with the versions listed there):

```bash
pip install -r requirements.txt
```

## Reproducing the figures and tables from the stored results (minutes)

Download `P4_code_histories.zip` from the release and extract it into `sim/`. Then, in `sim/`:

```bash
python hinh_mach.py
```

```bash
python hinh_coche.py
```

```bash
python hinh_bai.py
```

```bash
python bang_allvar.py
```

```bash
python so_lieu_bai.py
```

Figures 1–10, E.1 and E.2 (`Figure_N.pdf`, `Figure_E1.pdf`, `Figure_E2.pdf`, `.png`) and Tables E.2–E.3 (`appC_allvar.tex`) are written to `sim/out/` (or to the folder
given by the environment variable `P4_OUT`); `so_lieu_bai.md` lists the numbers quoted in the text. The other
post-processing scripts (`p04_summary.py`, `phantich_p0.py`, `p11_rainflow.py`, `p12_system.py`, `mc_b10.py`,
`sobol2.py`, `sobol3.py`, ...) regenerate the corresponding files in `sim/summaries/`.

## Re-running the simulations (hours)

The full chain, in order:

1. `python linhkien.py`: device models and check against the tabulated datasheet values.
2. `python hoso_nhiemvu.py plot` and `python hoso_nhiemvu.py derate`: mission profiles `hoso_50km.csv`,
   `hoso_25km.csv` and, with low-frequency derating, `hoso_50km_dr.csv` and `hoso_50km_dr75.csv`.
3. `python tannhiet.py`, `python tannhiet.py variants` and `python tannhiet.py par`: finite-volume heat-sink step
   responses `tannhiet_step*.npz`.
4. `python tran_lp.py`: imbalance index over the operating-point grid (Fig. E.2).
5. `python chay_tatca.py`: mission simulations (calls `tran_daodong.py <cfg> <variant>`), writing `daodong_*.json` and
   `mophong_*.npz`; several hours on 7 cores. Without an argument it runs the base case, the derating, heat-sink,
   two-module and utilisation variants; the remaining variants are passed as a comma-separated list:
   `python chay_tatca.py fvdr_tw50,fvdr_tw60,fvdr_tw65,fvdr_sic3k,fvdr_sic5k,fvdr_esw`.
6. `python chay_bound.py`: conservative ripple bound (damage floor and ceilings) for every variant (`p15_bound.py`),
   about 5 h on 7 cores.
7. `python chay_p04m.py`: pulse-resolved correction for the base case and the utilisation sweep (`p04_mission.py`),
   about 3.5 h on 7 cores.
8. Post-processing, figures and tables as above.

Set `OMP_NUM_THREADS=1` for the parallel drivers (they do so themselves) to avoid oversubscription of the linear
algebra libraries.

## Map from the paper to the code

| Paper | Script |
|---|---|
| Table 1, device models | `linhkien.py` |
| Figs. 1 and 3, drive, leg topologies and conduction paths | `hinh_mach.py` (schemdraw) |
| Fig. 2, Fig. 4, mission | `hinh_bai.py`, `hoso_nhiemvu.py` |
| Figs. 5, 6 and E.1, damage mechanism, ceiling and break-even concept, runaway margins | `hinh_coche.py` (Fig. E.1 from `bang_t2.md`) |
| Fig. 10, switching-period excursions | `hinh_coche.py` with `xung_policy.py` |
| Sec. 3.1–3.2, Theorem 1 (Appendix A), Fig. E.2 | `tonhao.py`, `tran_lp.py` |
| Sec. 3.3–3.4, Proposition 1, ripple-aware law | `dao_dong.py`, `p15_bound.py` |
| Sec. 2.4, rainflow and CIPS08 | `tonthuong.py` |
| Sec. 4, Table 2, Figs. 7–8 | `tran_daodong.py`, `hanhtrinh.py`, `so_lieu_bai.py`, `hinh_bai.py` |
| Sec. 5.2, Table 4 | `xung_policy.py`, `p04_mission.py`, `p04_summary.py`, `xung_p04.py` |
| Sec. 5.3, Table 5, superposed rainflow | `phantich_p0.py`, `p11_rainflow.py` |
| Sec. 5.1, Table 3, Fig. 9 | `tran_daodong.py`, `hinh_f8.py`, `hinh_bai.py` |
| Sec. 5.4 and Appendix E, Sobol, Monte Carlo B10, series system | `sobol2.py`, `sobol3.py`, `mc_b10.py`, `p13_scaling.py`, `p12_system.py` |
| Sec. 6.1, Table E.1 | `bang_t2.py` |
| Sec. 6.2, baseplate solder | `phantich_p0.py` |
| Appendix D, numerical checks | `p_round3.py`, `p_tmin_mission.py`, `p14_refine.py`, `p19_share.py`, `p_harm.py`, `xung_p04.py` |
| Appendix D, cut-off of the damage model in the ripple bound; amplitude correction versus rainflow of the pulse-resolved history | `p_cutoff.py`, `p_floor_check.py`, `p_mc3.py` |
| Tables E.2–E.3, all variants | `bang_allvar.py` |

## Licence

MIT, see `LICENSE`.
