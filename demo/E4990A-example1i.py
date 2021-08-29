from matplotlib.pyplot import style, savefig

from zfitpy import ZFitter
from zfitpy import Plotter
from zfitpy import impedancedata
from zfitpy import Parallel3SeriesRLModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

rangesRL3 = ((60e-3, 90e-3), (8e-3, 12e-3),
             (15, 80), (10e-3, 30e-3),
             (15, 80), (10e-3, 30e-3))             

zfitter = ZFitter(Parallel3SeriesRLModel, data.f, data.Z)

fitmodel = zfitter(ranges=rangesRL3)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
