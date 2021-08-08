from matplotlib.pyplot import style, savefig

from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata
from zfitter import SeriesRCPEModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = ((60e-3, 90e-3), (1e-3, 1e3), (-1, 1))

zfitter = ZFitter(SeriesRCPEModel, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
