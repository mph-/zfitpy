import numpy as np
from matplotlib.pyplot import subplots, style, savefig, show, plot
from model import Model
import numpy as np

class SeriesRCModel(Model):

    def __init__(self, Rs, Cs):

        self.Rs = Rs
        self.Cs = Cs
        self.params = (Rs, Cs)

    def __str__(self):
        return 'Rs=%.2e ohms, Cs=%.2e F' % self.params
        
    def Z(self, f):

        s = 2j * np.pi * f
        Z1 = self.Rs + self.Cs / s
        return Z1

    def Y(self, f):
        return 1 / self.Z(f)

    def zimpulse(self, t):

        Rs, Cs = self.params

        h = np.exp(-t / (Cs * Rs)) / Cs * (t >= 0)

        return h, 0, 0
              
