from matplotlib.pyplot import style, savefig

from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata
from zfitter import ParallelRCPEModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = {'R1': (0, 10e3), 'K': (1e-3, 1e3), 'alpha': (-1, 1)}

zfitter = ZFitter(ParallelRCPEModel, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_fit(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
