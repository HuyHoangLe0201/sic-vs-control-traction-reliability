"""Run p04_mission.py for the reference variant and the utilisation sweep (NPAR parallel)."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
NPAR = 7
V = ['fvdr'] + [f'fvdr_u{u}' for u in ('0.3', '0.4', '0.5', '0.6', '0.7')]
jobs = [(v, c) for v in V for c in ('SiC-ANPC', 'Si-ANPC', 'Si-NPC')]
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
log = open(os.path.join(HERE, 'chay_p04m.log'), 'a', buffering=1); log.write(f'{len(jobs)} jobs\n')
run, n, t0 = [], 0, time.time()
while jobs or run:
    while jobs and len(run) < NPAR:
        v, c = jobs.pop(0); f = open(os.path.join(HERE, f'p04m_{v}_{c}.log'), 'w')
        run.append((subprocess.Popen([sys.executable, '-u', 'p04_mission.py', c, v], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, env=ENV), v, c, f, time.time()))
    time.sleep(5)
    for it in list(run):
        p, v, c, f, ts = it
        if p.poll() is not None:
            f.close(); run.remove(it); n += 1
            log.write(f'{time.time()-t0:7.0f}s done {v} {c} rc={p.returncode} ({time.time()-ts:.0f}s) [{n}]\n')
log.write(f'ALL DONE {time.time()-t0:.0f}s\n')
