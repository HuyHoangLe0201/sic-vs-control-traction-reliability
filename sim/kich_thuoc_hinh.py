"""Report the size of every manuscript figure (PDF page size in mm) and the PNG pixel width.
python kich_thuoc_hinh.py"""
import glob, os
from pypdf import PdfReader
from PIL import Image

FIG = os.environ.get('P4_OUT', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'))
for f in sorted(glob.glob(os.path.join(FIG, 'Figure_*.pdf')), key=lambda p: int(p.split('_')[-1].split('.')[0])):
    b = PdfReader(f).pages[0].mediabox
    png = f[:-4] + '.png'
    px = Image.open(png).size if os.path.exists(png) else None
    print(f'{os.path.basename(f):14s} {float(b.width) / 72 * 25.4:6.1f} x {float(b.height) / 72 * 25.4:6.1f} mm   png {px}')
