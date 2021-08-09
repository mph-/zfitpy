from matplotlib.pyplot import style, savefig

from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata
from zfitter import SeriesRParallelRLModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

rangesRL2 = ((0, 0.4), (1e3, 5e3), (8e-3, 12e-3))

zfitter = ZFitter(SeriesRParallelRLModel, data.f, data.Z)

fitmodel = zfitter(ranges=rangesRL2)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
