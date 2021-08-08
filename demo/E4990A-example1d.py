import numpy as np
from matplotlib.pyplot import subplots, style, savefig, show

from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata
from zfitter import ParallelRCPEModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = ((0, 10e3), (1e-3, 1e3), (-1, 1))

zfitter = ZFitter(ParallelRCPEModel, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.pgf'), bbox_inches='tight')
