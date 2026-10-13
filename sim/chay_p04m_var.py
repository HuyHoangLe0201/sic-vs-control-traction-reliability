"""Run p04_mission.py (pulse-resolved correction) for the design variants of Table 3, so that the robustness of the
break-even capability with both inverters controlled is checked with the pulse-resolved model in every variant
(review round 4, item 7). Si-ANPC is not re-run where only SiC changes (sic3k, sic5k), SiC-ANPC not where only Si
changes (esw). The variants that decide the conclusion (coolant 65/60 C, SiC at 5 kHz) are run first."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
NPAR = int(sys.argv[1]) if len(sys.argv) > 1 else 10
FIRST = [('fvdr_tw65', 'SiC-ANPC'), ('fvdr_tw65', 'Si-ANPC'), ('fvdr_tw60', 'SiC-ANPC'), ('fvdr_tw60', 'Si-ANPC'),
         ('fvdr_sic5k', 'SiC-ANPC'), ('fvdr_tw50', 'SiC-ANPC'), ('fvdr_tw50', 'Si-ANPC'), ('fvdr_sic3k', 'SiC-ANPC')]
REST = []
for v in ('fvdr75', 'fvdr_h2500', 'fvdr_h10000', 'fvdr_t10', 'fvdr_t30', 'fv', 'fvdr_par'):
    REST += [(v, 'SiC-ANPC'), (v, 'Si-ANPC')]
REST.append(('fvdr_esw', 'Si-ANPC'))
jobs = [j for j in FIRST + REST if not os.path.exists(os.path.join(HERE, f'p04m_{j[0]}_{j[1]}.json'))]
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
log = open(os.path.join(HERE, 'chay_p04m_var.log'), 'a', buffering=1)
log.write(f'{len(jobs)} jobs, NPAR={NPAR}\n')
run, n, t0 = [], 0, time.time()
while jobs or run:
    while jobs and len(run) < NPAR:
        v, c = jobs.pop(0)
        f = open(os.path.join(HERE, f'p04m_{v}_{c}.log'), 'w')
        run.append((subprocess.Popen([sys.executable, '-u', 'p04_mission.py', c, v], cwd=HERE, stdout=f,
                                     stderr=subprocess.STDOUT, env=ENV), v, c, f, time.time()))
    time.sleep(10)
    for it in list(run):
        p, v, c, f, ts = it
        if p.poll() is not None:
            f.close(); run.remove(it); n += 1
            log.write(f'{time.time() - t0:7.0f}s done {v} {c} rc={p.returncode} ({time.time() - ts:.0f}s) [{n}]\n')
log.write(f'ALL DONE {time.time() - t0:.0f}s\n')
