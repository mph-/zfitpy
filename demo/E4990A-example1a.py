import numpy as np
from matplotlib.pyplot import subplots, style, savefig, show

from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata
from zfitter.parallel2seriesrlmodel import Parallel2SeriesRLModel

style.use('z.mplstyle')

data = impedancedata('E4990A-example1.csv')

rangesRL2 = ((60e-3, 90e-3), (8e-3, 12e-3),
             (15, 80), (10e-3, 30e-3))

zfitter = ZFitter(Parallel2SeriesRLModel, data.f, data.Z)

fitmodel = zfitter(ranges=rangesRL2)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.pgf'), bbox_inches='tight')
