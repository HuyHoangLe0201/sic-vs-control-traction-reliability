"""Recompute the conservative ripple bound (p15_bound.py) for every mission variant, NPAR processes at a time.
python chay_bound.py  -> logs bd_<variant>_<cfg>.log, chay_bound.log"""
import os, sys, json, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
NPAR = 7
VARIANTS = ['fvdr', 'fvdr75', 'fvdr_h2500', 'fvdr_h10000', 'fvdr_t10', 'fvdr_t30', 'fvdr_tw50', 'fvdr_tw60', 'fvdr_tw65',
            'fvdr_sic3k', 'fvdr_sic5k', 'fvdr_esw', 'fv', 'fvdr_par'] + [f'fvdr_u{u}' for u in ('0.3', '0.4', '0.5', '0.6', '0.7')]
CFGS = ['SiC-ANPC', 'Si-ANPC', 'Si-NPC']


def done(v, c):
    j = json.load(open(os.path.join(HERE, f'daodong_{v}_{c}.json')))
    # done when the bound with the convex minorant of the cut-off damage (review MC1) is present
    return 'bounds_tw' in j and 'D_bound_rip_cut' in j['bounds_tw']['ton_clip']


jobs = []
for v in VARIANTS:
    for c in CFGS:
        if ('_sic' in v and not c.startswith('SiC')) or ('_esw' in v and c.startswith('SiC')):
            continue                                   # unchanged copies of fvdr, filled in afterwards
        if not done(v, c):
            jobs.append((v, c))
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
log = open(os.path.join(HERE, 'chay_bound.log'), 'a', buffering=1)
running, n_done, t0 = [], 0, time.time()
log.write(f'{len(jobs)} jobs\n')
while jobs or running:
    while jobs and len(running) < NPAR:
        v, c = jobs.pop(0)
        f = open(os.path.join(HERE, f'bd_{v}_{c}.log'), 'w')
        p = subprocess.Popen([sys.executable, '-u', 'p15_bound.py', c, v], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, env=ENV)
        running.append((p, v, c, f, time.time()))
    time.sleep(5)
    for item in list(running):
        p, v, c, f, ts = item
        if p.poll() is not None:
            f.close(); running.remove(item); n_done += 1
            log.write(f'{time.time() - t0:7.0f}s done {v} {c} rc={p.returncode} ({time.time() - ts:.0f}s) [{n_done}]\n')
# copies: Si of the SiC-frequency variants and SiC of the switching-energy variant equal the reference results
ref = {c: json.load(open(os.path.join(HERE, f'daodong_fvdr_{c}.json'))) for c in CFGS}
for v, cs in (('fvdr_sic3k', ('Si-NPC', 'Si-ANPC')), ('fvdr_sic5k', ('Si-NPC', 'Si-ANPC')), ('fvdr_esw', ('SiC-ANPC',))):
    for c in cs:
        fn = os.path.join(HERE, f'daodong_{v}_{c}.json')
        j = json.load(open(fn)); j['bounds_tb'] = j.get('bounds_tb', j['bounds']); j['bounds_tw'] = ref[c]['bounds_tw']
        json.dump(j, open(fn, 'w'), indent=1, default=float)
log.write(f'ALL DONE {time.time() - t0:.0f}s\n')
