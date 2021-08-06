import numpy as np
from numpy import exp
from matplotlib.pyplot import subplots, style, savefig, show, plot
from .model import Model
import numpy as np

class Parallel2SeriesRLModel(Model):

    def __init__(self, R1, L1, R2, L2):

        self.R1 = R1
        self.L1 = L1
        self.R2 = R2
        self.L2 = L2
        self.params = (R1, L1, R2, L2)

    def __str__(self):
        return 'R1=%.2e ohms, L1=%.2e H, R2=%.2e ohms, L2=%.2e H' % self.params
        
    def Z(self, f):

        s = 2j * np.pi * f
        Z1 = self.R1 + s * self.L1
        Z2 = self.R2 + s * self.L2
        return Z1 * Z2 / (Z1 + Z2)

    def Y(self, f):
        return 1 / self.Z(f)
    
    def zimpulse(self, t):

        R1, L1, R2, L2 = self.params

        Ht = (t >= 0)
        h = (L1**2 * R2**2 - 2 * L1 * L2 * R1 * R2 + L2**2 * R1**2) * exp(-t * (R1 + R2)/(L1 + L2)) * Ht / (L1**3 + 3 * L1**2 * L2 + 3 * L1 * L2**2 + L2**3)

        d = (L1**2 * R2 + L2**2 * R1) / (L1 + L2)**2

        dd = L1 * L2 / (L1 + L2)

        return h, d, dd

    def yimpulse(self, t):

        R1, L1, R2, L2 = self.params

        h1 = np.exp(-t * R1 / L1) * (t >= 0) / L1
        h2 = np.exp(-t * R2 / L2) * (t >= 0) / L2
        h = h1 + h2
        
        return h, 0, 0
