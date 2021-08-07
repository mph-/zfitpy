from .model import Model
from lcapy import R, L

class Parallel3SeriesRLModel(Model):

    net = (R('R1') + L('L1')) | (R('R2') + L('L2')) | (R('R3') + L('L3'))
    
    def __init__(self, R1, L1, R2, L2, R3, L3):

        self.R1 = R1
        self.L1 = L1
        self.R2 = R2
        self.L2 = L2
        self.R3 = R3
        self.L3 = L3        
