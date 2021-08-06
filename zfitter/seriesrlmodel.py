from .model import Model
import numpy as np

class SeriesRLModel(Model):

    def __init__(self, Rs, Ls):

        self.Rs = Rs
        self.Ls = Ls
        self.params = (Rs, Ls)                

    def __str__(self):
        return 'Rs=%.2e ohms, Ls=%.2e H' % self.params
        
    def Z(self, f):

        s = 2j * np.pi * f
        Z1 = self.Rs + s * self.Ls
        return Z1

    def Y(self, f):
        return 1 / self.Z(f)

    def zimpulse(self, t):

        Rs, Ls = self.params
        
        dt = t[1] - t[0]
        n = np.arange(len(t))
        h = 4 * (-1) ** n * Ls / dt

        d = Rs - 2 * Ls / dt

        return h, d, 0

    def yimpulse(self, t):

        Rs, Ls = self.params

        h = np.exp(-t * Rs / Ls) * (t >= 0) / Ls
        
        return h, 0, 0
    
