from matplotlib.pyplot import style, savefig
from lcapy import CPE, R

from zfitpy import ZFitter
from zfitpy import Plotter
from zfitpy import impedancedata
from zfitpy import modelmake

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = {'R1': (1e-3, 1e3), 'K': (1e-3, 1e3), 'alpha': (-1, 1), 'R2': (100, 1e4)}

# Create model
Model = modelmake('Model', (CPE('K', 'alpha') | R('R2')) + R('R1'), ('K', 'alpha', 'R1', 'R2'))

zfitter = ZFitter(Model, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
