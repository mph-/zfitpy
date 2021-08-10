from matplotlib.pyplot import style, savefig
from zfitter import zfit
from zfitter import Plotter

style.use('z.mplstyle')

net = "(CPE('K', 'alpha') | R('R2')) + R('R1')"
ranges = {'R1': (1e-3, 1e3), 'K': (1e-3, 1e3), 'alpha': (-1, 1), 'R2': (100, 1e4)}

data, fitmodel = zfit('E4990A-example1.csv', net, ranges, Ns=10)

plotter = Plotter()
plotter.Z_error(data, fitmodel)

savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
