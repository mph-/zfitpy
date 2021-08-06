from .model import Model
import numpy as np

class Parallel4SeriesRLModel(Model):
    
    def __init__(self, R1, L1, R2, L2, R3, L3, R4, L4):

        self.R1 = R1
        self.L1 = L1
        self.R2 = R2
        self.L2 = L2
        self.R3 = R3
        self.L3 = L3
        self.R4 = R4
        self.L4 = L4
        self.params = (R1, L1, R2, L2, R3, L3, R4, L4)

    def __str__(self):
        return 'R1=%.2e ohms, L1=%.2e H, R2=%.2e ohms, L2=%.2e H, R3=%.2e ohms, L3=%.2e H, R4=%.2e ohms, L4=%.2e H' % self.params
        
    def Z(self, f):

        s = 2j * np.pi * f
        Z1 = self.R1 + s * self.L1
        Z2 = self.R2 + s * self.L2
        Z3 = self.R3 + s * self.L3
        Z4 = self.R4 + s * self.L4        
        return 1 / (1 / Z1 + 1 / Z2 + 1 / Z3 + 1 / Z4)

    def Y(self, f):
        return 1 / self.Z(f)
    
    def zimpulse(self, i, t):

        # Can of worms.  TODO
        raise ValueError('TODO')

    def yimpulse(self, t):

        R1, L1, R2, L2, R3, L3, R4, L4 = self.params

        h1 = np.exp(-t * R1 / L1) * (t >= 0) / L1
        h2 = np.exp(-t * R2 / L2) * (t >= 0) / L2
        h3 = np.exp(-t * R3 / L3) * (t >= 0) / L3
        h4 = np.exp(-t * R4 / L4) * (t >= 0) / L4                
        h = h1 + h2 + h3 + h4
        
        return h, 0, 0    
    
