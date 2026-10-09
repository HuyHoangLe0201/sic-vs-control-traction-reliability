"""Rerun all mission variants (review P0-3/P0-12) with at most NPAR concurrent processes.
python chay_tatca.py   -> logs dd3_<variant>_<cfg>.log, summary chay_tatca.log"""
import os, sys, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
NPAR = 7
VARIANTS = sys.argv[1].split(',') if len(sys.argv) > 1 else ['fvdr', 'fvdr75', 'fvdr_h2500', 'fvdr_h10000', 'fvdr_t10', 'fvdr_t30', 'fv', 'fvdr_par'] + \
           [f'fvdr_u{u}' for u in ('0.3', '0.4', '0.5', '0.6', '0.7')]
CFGS = ['SiC-ANPC', 'Si-ANPC', 'Si-NPC']   # slowest first
# SiC switching-frequency variants change only the SiC run (Si results are those of fvdr)
jobs = [(v, c) for v in VARIANTS for c in CFGS if not ('_sic' in v and not c.startswith('SiC')) and not ('_esw' in v and c.startswith('SiC'))]
NJOB = len(jobs)
running, done = [], []
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')   # avoid oversubscription
log = open(os.path.join(HERE, 'chay_tatca.log'), 'a', buffering=1)
t0 = time.time()
while jobs or running:
    while jobs and len(running) < NPAR:
        v, c = jobs.pop(0)
        f = open(os.path.join(HERE, f'dd3_{v}_{c}.log'), 'w')
        p = subprocess.Popen([sys.executable, '-u', 'tran_daodong.py', c, v], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, env=ENV)
        running.append((p, v, c, f, time.time()))
        log.write(f'{time.time()-t0:7.0f}s start {v} {c}\n')
    time.sleep(5)
    for item in list(running):
        p, v, c, f, ts = item
        if p.poll() is not None:
            f.close(); running.remove(item); done.append((v, c, p.returncode))
            log.write(f'{time.time()-t0:7.0f}s done  {v} {c} rc={p.returncode} ({time.time()-ts:.0f}s) [{len(done)}/{NJOB}]\n')
log.write(f'ALL DONE {time.time()-t0:.0f}s, failures: {[d for d in done if d[2] != 0]}\n')
