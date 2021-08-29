from matplotlib.pyplot import style, savefig
from zfitpy import zfit
from zfitpy import Plotter

style.use('z.mplstyle')

net = "R('R1') + L('L1') + ((L('L2') + R('R2')) | L('Lm'))"
ranges = {'L1': (0, 10e-3), 'L2': (-200e-6, -50e-6), 'Lm': (20e-6, 5e-3),
          'R1': (1e-3, 200e-3), 'R2': (0, 500e-3)}

data, fitmodel = zfit('E4990A-example1.csv', net, ranges, Ns=20)

print(fitmodel)
print(fitmodel.error)

plotter = Plotter()
plotter.Z_error(data, fitmodel)


savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
