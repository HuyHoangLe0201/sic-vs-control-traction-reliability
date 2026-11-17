"""Tightened floor (p_bound_fine.py) for every mission variant, NPAR processes at a time (CAEE editor point c).
Copies as in chay_bound.py: Si of the SiC-frequency variants and SiC of the switching-energy variant equal fvdr.
python chay_bound_fine.py  -> p_bound_fine_<variant>_<cfg>.json, logs pbf_<variant>_<cfg>.log, chay_bound_fine.log"""
import os, sys, json, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
NPAR = 7
VARIANTS = ['fvdr', 'fvdr75', 'fvdr_h2500', 'fvdr_h10000', 'fvdr_t10', 'fvdr_t30', 'fvdr_tw50', 'fvdr_tw60', 'fvdr_tw65',
            'fvdr_sic3k', 'fvdr_sic5k', 'fvdr_esw', 'fv', 'fvdr_par'] + [f'fvdr_u{u}' for u in ('0.3', '0.4', '0.5', '0.6', '0.7')]
CFGS = ['Si-ANPC', 'SiC-ANPC', 'Si-NPC']        # longest first
COPY = {('fvdr_sic3k', 'Si-NPC'), ('fvdr_sic3k', 'Si-ANPC'), ('fvdr_sic5k', 'Si-NPC'), ('fvdr_sic5k', 'Si-ANPC'),
        ('fvdr_esw', 'SiC-ANPC')}
out = lambda v, c: os.path.join(HERE, f'p_bound_fine_{v}_{c}.json')
jobs = [(v, c) for c in CFGS for v in VARIANTS if (v, c) not in COPY and not os.path.exists(out(v, c))]
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
log = open(os.path.join(HERE, 'chay_bound_fine.log'), 'a', buffering=1)
running, n_done, t0 = [], 0, time.time()
log.write(f'{len(jobs)} jobs\n')
while jobs or running:
    while jobs and len(running) < NPAR:
        v, c = jobs.pop(0)
        f = open(os.path.join(HERE, f'pbf_{v}_{c}.log'), 'w')
        p = subprocess.Popen([sys.executable, '-u', 'p_bound_fine.py', c, v], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, env=ENV)
        running.append((p, v, c, f, time.time()))
    time.sleep(10)
    for item in list(running):
        p, v, c, f, ts = item
        if p.poll() is not None:
            f.close(); running.remove(item); n_done += 1
            log.write(f'{time.time() - t0:7.0f}s done {v} {c} rc={p.returncode} ({time.time() - ts:.0f}s) [{n_done}]\n')
for v, c in COPY:
    j = json.load(open(out('fvdr', c))); j['variant'] = v; j['copied_from'] = 'fvdr'
    pub = json.load(open(os.path.join(HERE, f'daodong_{v}_{c}.json')))['bounds_tw']
    for st in j['bounds']:
        j['bounds'][st]['D_floor_published'] = pub[st]['D_bound_rip']
    json.dump(j, open(out(v, c), 'w'), indent=1, default=float)
log.write(f'ALL DONE {time.time() - t0:.0f}s\n')
