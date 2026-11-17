"""Push the tightened-floor jobs to Kaggle: one private dataset with the code and data, one private CPU kernel per job.
python day_len.py dataset          -> creates (or versions) hoangle0201/p4-bound-fine-src
python day_len.py kernels v1,v2 cfg -> one kernel per variant
python day_len.py fetch v1,v2 cfg  -> downloads the outputs into P4_mophong"""
import os, sys, json, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
USER = 'hoangle0201'
DS = 'p4-bound-fine-src'
FILES = ['dao_dong.py', 'donhay.py', 'hanhtrinh.py', 'linhkien.py', 'tonhao.py', 'tonthuong.py', 'tran_daodong.py',
         'p_bound_fine.py', 'hoso_50km.csv', 'hoso_50km_dr.csv', 'hoso_50km_dr75.csv', 'tannhiet_step.npz',
         'tannhiet_step_h2500.npz', 'tannhiet_step_h10000.npz', 'tannhiet_step_t10.npz', 'tannhiet_step_t30.npz', 'tannhiet_step_par.npz']
K = [sys.executable, '-m', 'kaggle']


def slug(v, cfg):
    return f'p4-pbf-{v}-{cfg}'.lower().replace('_', '-').replace('.', '')


def dataset():
    d = os.path.join(HERE, 'ds'); os.makedirs(d, exist_ok=True)
    for f in FILES:
        if os.path.exists(os.path.join(SIM, f)):
            shutil.copy(os.path.join(SIM, f), d)
    json.dump(dict(title='p4 bound fine src', id=f'{USER}/{DS}', licenses=[dict(name='CC0-1.0')]),
              open(os.path.join(d, 'dataset-metadata.json'), 'w'))
    r = subprocess.run(K + ['datasets', 'status', f'{USER}/{DS}'], capture_output=True, text=True)
    if 'ready' in r.stdout.lower():
        subprocess.run(K + ['datasets', 'version', '-p', d, '-m', 'update'], check=True)
    else:
        subprocess.run(K + ['datasets', 'create', '-p', d], check=True)


def kernels(vs, cfg):
    src = open(os.path.join(HERE, 'run_pbf.py'), encoding='utf-8').read()
    for v in vs:
        d = os.path.join(HERE, 'k', slug(v, cfg)); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'run.py'), 'w', encoding='utf-8', newline='\n').write(
            src.replace('__VARIANT__', v).replace('__CFG__', cfg))
        json.dump(dict(id=f'{USER}/{slug(v, cfg)}', title=slug(v, cfg), code_file='run.py', language='python',
                       kernel_type='script', is_private=True, enable_gpu=False, enable_tpu=False, enable_internet=False,
                       dataset_sources=[f'{USER}/{DS}'], competition_sources=[], kernel_sources=[]),
                  open(os.path.join(d, 'kernel-metadata.json'), 'w'), indent=1)
        subprocess.run(K + ['kernels', 'push', '-p', d], check=True)


def fetch(vs, cfg):
    for v in vs:
        d = os.path.join(HERE, 'out', slug(v, cfg)); os.makedirs(d, exist_ok=True)
        subprocess.run(K + ['kernels', 'output', f'{USER}/{slug(v, cfg)}', '-p', d], check=True)
        for f in (f'p_bound_fine_{v}_{cfg}.json', f'p_bound_fine_{v}_{cfg}.npz'):
            if os.path.exists(os.path.join(d, f)):
                shutil.copy(os.path.join(d, f), SIM); print('fetched', f)


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'dataset':
        dataset()
    else:
        (kernels if a == 'kernels' else fetch)(sys.argv[2].split(','), sys.argv[3])
