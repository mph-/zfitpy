from matplotlib.pyplot import style, savefig

from zfitpy import ZFitter
from zfitpy import Plotter
from zfitpy import impedancedata
from zfitpy import Parallel2SeriesRLModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

ranges = {'R1': (60e-3, 90e-3), 'L1': (8e-3, 12e-3),
          'R2': (15, 80), 'L2': (10e-3, 30e-3)}

zfitter = ZFitter(Parallel2SeriesRLModel, data.f, data.Z)

fitmodel = zfitter(ranges=ranges)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
