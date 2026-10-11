"""Figure 1 of the manuscript: drive system and the two three-level leg topologies, drawn with schemdraw.
(a) split DC link with neutral point O, three-level inverter and PMSM; (b) NPC leg; (c) ANPC leg with the three dual modules.
Device positions 1-6 as in Appendix B: 1-4 form the main chain from P to N, 5 and 6 clamp the inner nodes to O.
python hinh_mach.py  -> Figure_1.pdf / .png in the output folder (190 mm wide)"""
import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import schemdraw
import schemdraw.elements as elm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('P4_OUT', os.path.join(HERE, 'out'))
MM = 1 / 25.4
FS = 7
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': FS, 'pdf.fonttype': 42, 'ps.fonttype': 42,
                     'savefig.bbox': 'standard'})
GREY, BLUE = '#7F7F7F', '#0072B2'
DY = 1.4           # height of one switch cell


def cell(d, x, ytop, k, active=True, label_left=False):
    """Switch position k between (x, ytop) and (x, ytop - DY): transistor T_k with antiparallel diode D_k
    (or diode only if active is False). Returns nothing; labels placed beside the cell."""
    xd = x + 0.85
    ym = ytop - DY / 2
    if active:
        d.add(elm.IgbtN().theta(0).anchor('collector').at((x, ytop)))
        d.add(elm.Line().at((x, ytop)).to((xd, ytop)))
        d.add(elm.Line().at((x, ytop - DY)).to((xd, ytop - DY)))
        d.add(elm.Diode().at((xd, ytop - DY)).to((xd, ytop)))
        txt = f'T{k}\nD{k}'
    else:
        d.add(elm.Diode().at((x, ytop - DY)).to((x, ytop)))
        txt = f'D{k}'
    if label_left:
        d.add(elm.Label().at((x - 0.95, ym)).label(txt, fontsize=FS, halign='right'))
    else:
        d.add(elm.Label().at(((xd if active else x) + 0.45, ym)).label(txt, fontsize=FS, halign='left'))


def leg(ax, anpc, modules=True):
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(unit=1.0, fontsize=FS, lw=0.8)
    x0, xc = 0.0, -2.6
    # main chain P - T1 - A - T2 - X - T3 - B - T4 - N
    y = {'P': 0.0, 'T1': -0.3, 'A': -2.0, 'T2': -2.3, 'X': -4.0, 'T3': -4.3, 'B': -6.0, 'T4': -6.3, 'N': -8.0}
    d.add(elm.Line().at((x0, y['P'])).to((x0, y['T1'])))
    for k, name in enumerate(('T1', 'T2', 'T3', 'T4'), 1):
        cell(d, x0, y[name], k)
    d.add(elm.Line().at((x0, y['T1'] - DY)).to((x0, y['T2'])))
    d.add(elm.Line().at((x0, y['T2'] - DY)).to((x0, y['T3'])))
    d.add(elm.Line().at((x0, y['T3'] - DY)).to((x0, y['T4'])))
    d.add(elm.Line().at((x0, y['T4'] - DY)).to((x0, y['N'])))
    for n in ('A', 'X', 'B'):
        d.add(elm.Dot().at((x0, y[n])))
    d.add(elm.Dot(open=True).at((x0, y['P'])).label('P', loc='right', fontsize=FS))
    d.add(elm.Dot(open=True).at((x0, y['N'])).label('N', loc='right', fontsize=FS))
    d.add(elm.Line().at((x0, y['X'])).to((x0 + 2.0, y['X'])))
    d.add(elm.Dot(open=True).at((x0 + 2.0, y['X'])).label('output', loc='right', fontsize=FS))
    # clamping branch: positions 5 (A - O) and 6 (O - B)
    yo = y['X']
    d.add(elm.Line().at((x0, y['A'])).to((xc, y['A'])))
    d.add(elm.Line().at((x0, y['B'])).to((xc, y['B'])))
    if anpc:
        d.add(elm.Line().at((xc, y['A'])).to((xc, y['T2'])))
        cell(d, xc, y['T2'], 5, label_left=True)
        d.add(elm.Line().at((xc, y['T2'] - DY)).to((xc, y['T3'])))
        cell(d, xc, y['T3'], 6, label_left=True)
        d.add(elm.Line().at((xc, y['T3'] - DY)).to((xc, y['B'])))
    else:
        d.add(elm.Line().at((xc, y['A'])).to((xc, y['T2'])))
        cell(d, xc, y['T2'], 5, active=False, label_left=True)
        d.add(elm.Line().at((xc, y['T2'] - DY)).to((xc, y['T3'])))
        cell(d, xc, y['T3'], 6, active=False, label_left=True)
        d.add(elm.Line().at((xc, y['T3'] - DY)).to((xc, y['B'])))
    d.add(elm.Dot().at((xc, yo)))
    d.add(elm.Line().at((xc, yo)).to((xc - 1.6, yo)))
    d.add(elm.Dot(open=True).at((xc - 1.6, yo)).label('O', loc='left', fontsize=FS))
    for n in ('A', 'B'):
        d.add(elm.Dot().at((xc, y[n])))
    d.draw(show=False)
    if anpc and modules:   # dual modules
        for (xa, xb, ya, yb) in ((-0.95, 1.25, y['T2'] - DY - 0.15, y['T1'] + 0.15),
                                 (-0.95, 1.25, y['T4'] - DY - 0.15, y['T3'] + 0.15),
                                 (xc - 0.95, xc + 1.25, y['T3'] - DY - 0.15, y['T2'] + 0.15)):
            ax.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fill=False, ls=(0, (3, 2)), lw=0.6, ec=BLUE))
    ax.set_aspect('equal'); ax.axis('off')


def system(ax):
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(unit=1.0, fontsize=FS, lw=0.8)
    yP, yO, yN = 0.0, -4.0, -8.0
    d.add(elm.Line().at((0, yP)).to((0, -1.2)))
    d.add(elm.Capacitor().at((0, -1.2)).to((0, -2.8)).label('$C$', loc='bottom', fontsize=FS))
    d.add(elm.Line().at((0, -2.8)).to((0, yO)))
    d.add(elm.Line().at((0, yO)).to((0, -5.2)))
    d.add(elm.Capacitor().at((0, -5.2)).to((0, -6.8)).label('$C$', loc='bottom', fontsize=FS))
    d.add(elm.Line().at((0, -6.8)).to((0, yN)))
    for yy, n in ((yP, 'P'), (yO, 'O'), (yN, 'N')):
        d.add(elm.Line().at((0, yy)).to((2.4, yy)))
        d.add(elm.Dot().at((0, yy)))
        d.add(elm.Label().at((1.2, yy + 0.35)).label(n, fontsize=FS))
    d.add(elm.Line().at((-1.4, yP)).to((0, yP)))
    d.add(elm.Line().at((-1.4, yN)).to((0, yN)))
    d.add(elm.Label().at((-1.9, (yP + yN) / 2)).label('$V_{dc}$', fontsize=FS))
    for yy in (yP, yN):
        d.add(elm.Dot(open=True).at((-1.4, yy)))
    # inverter box and outputs to the motor
    xb0, xb1 = 2.4, 6.0
    ax.add_patch(Rectangle((xb0, yN - 0.4), xb1 - xb0, yP - yN + 0.8, fc='#F2F2F2', ec=GREY, lw=0.6, zorder=0))
    d.add(elm.Label().at(((xb0 + xb1) / 2, -4.0)).label('three-level\ninverter\n(legs as\nin b or c)', fontsize=FS))
    xm, ym, rm = 9.0, -4.0, 1.25
    for yy, ph in ((-3.0, 'a'), (-4.0, 'b'), (-5.0, 'c')):
        xe = xm - (rm ** 2 - (yy - ym) ** 2) ** 0.5
        d.add(elm.Line().at((xb1, yy)).to((xe, yy)))
        d.add(elm.Label().at(((xb1 + xe) / 2 - 0.3, yy + 0.3)).label(ph, fontsize=FS))
    d.draw(show=False)
    ax.add_patch(Circle((xm, ym), rm, fill=False, ec='black', lw=0.8))
    ax.text(xm, ym, 'PMSM', ha='center', va='center', fontsize=FS)
    ax.text(xm, ym - rm - 0.45, '650 kW', ha='center', va='top', fontsize=FS)
    ax.set_aspect('equal'); ax.axis('off')


def main():
    fig = plt.figure(figsize=(190 * MM, 62 * MM))
    axs = [fig.add_axes(r) for r in ([0.0, 0.0, 0.36, 0.9], [0.37, 0.0, 0.30, 0.9], [0.68, 0.0, 0.32, 0.9])]
    system(axs[0]); leg(axs[1], anpc=False); leg(axs[2], anpc=True)
    ylo, yhi = -8.6, 0.6
    for a, lab, ttl, xl in zip(axs, ('(a)', '(b)', '(c)'), ('drive', 'NPC leg', 'ANPC leg'),
                               ((-3.4, 10.6), (-5.6, 3.9), (-5.6, 3.9))):
        a.set_xlim(*xl); a.set_ylim(ylo, yhi)
    for a, lab, ttl in zip(axs, ('(a)', '(b)', '(c)'), ('Drive', 'NPC leg', 'ANPC leg')):
        x0 = a.get_position().x0
        fig.text(x0 + 0.005, 0.965, lab, fontsize=8, fontweight='bold', va='center')
        fig.text(x0 + a.get_position().width / 2, 0.965, ttl, fontsize=8, va='center', ha='center')
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, 'Figure_1.pdf'))
    fig.savefig(os.path.join(OUT, 'Figure_1.png'), dpi=1000)
    print('Figure 1 ok')


# conduction paths at the neutral level for i > 0 (current out of the leg), Table B.1:
# upper path (T2, T5 on): O -> D5 -> T2 -> output; lower path (T3, T6 on): O -> T6 -> D3 -> output
XC = -2.6
UPPER = [(XC - 1.6, -4.0), (XC, -4.0), (XC, -3.7), (XC + 0.85, -3.7), (XC + 0.85, -2.3), (XC, -2.3), (XC, -2.0),
         (0, -2.0), (0, -4.0), (2.0, -4.0)]
LOWER = [(XC - 1.6, -4.0), (XC, -4.0), (XC, -6.0), (0, -6.0), (0, -5.7), (0.85, -5.7), (0.85, -4.3), (0, -4.3),
         (0, -4.0), (2.0, -4.0)]
VERM = '#D55E00'


def paths():
    """Figure 3: conduction paths of the ANPC leg at the neutral level for a positive output current."""
    fig = plt.figure(figsize=(190 * MM, 60 * MM))
    axs = [fig.add_axes([0.005 + k / 3, 0.0, 0.325, 0.88]) for k in range(3)]
    cases = (('(a)', 'Upper path (T2, T5 on)', [UPPER], 1.0), ('(b)', 'Lower path (T3, T6 on)', [LOWER], 1.0),
             ('(c)', 'Both paths', [UPPER, LOWER], 0.5))
    for a, (lab, ttl, pl, share) in zip(axs, cases):
        leg(a, anpc=True, modules=False)
        for p in pl:
            xs, ys = zip(*p)
            a.plot(xs, ys, color=VERM, lw=4.0 if share == 1 else 2.6, alpha=0.45, solid_capstyle='round', zorder=5)
        a.annotate('', (2.0, -3.75), (1.15, -3.75), arrowprops=dict(arrowstyle='-|>', color=VERM, lw=1.0))
        a.text(1.6, -3.62, '$i>0$', ha='center', va='bottom', fontsize=FS, color=VERM)
        if share != 1:
            a.text(XC + 1.25, -1.75, '$i/2$', fontsize=FS, color=VERM, ha='center')
            a.text(XC + 1.25, -6.25, '$i/2$', fontsize=FS, color=VERM, ha='center', va='top')
        a.set_xlim(-5.6, 3.9); a.set_ylim(-8.6, 0.6)
        x0 = a.get_position().x0
        fig.text(x0 + 0.005, 0.955, lab, fontsize=8, fontweight='bold', va='center')
        fig.text(x0 + a.get_position().width / 2 + 0.02, 0.955, ttl, fontsize=8, va='center', ha='center')
    fig.savefig(os.path.join(OUT, 'Figure_3.pdf'))
    fig.savefig(os.path.join(OUT, 'Figure_3.png'), dpi=1000)
    print('Figure 3 ok')


if __name__ == '__main__':
    main()
    paths()
