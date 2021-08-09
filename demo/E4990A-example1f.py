from matplotlib.pyplot import style, savefig
from lcapy import CPE, R

from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata
from zfitter import modelmake

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = {'R1': (0, 10e3), 'K': (1e-3, 1e3), 'alpha': (-1, 1), 'R2': (100, 1e4)}

# Create model
Model = modelmake('Model', (CPE('K', 'alpha') + R('R1')) | R('R2'), ('K', 'alpha', 'R1', 'R2'))

zfitter = ZFitter(Model, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
