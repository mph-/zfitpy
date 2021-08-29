from matplotlib.pyplot import style, savefig

from zfitpy import ZFitter
from zfitpy import Plotter
from zfitpy import impedancedata
from zfitpy import SeriesRCPEModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = {'R1': (60e-3, 90e-3), 'K': (1e-3, 1e3),
          'alpha': (-1, 1)}

zfitter = ZFitter(SeriesRCPEModel, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
