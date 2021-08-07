from .model import Model, build
from lcapy import R, L

class Parallel2SeriesRLModel(Model):

    net, Zcode = build((R('R1') + L('L1')) | (R('R2') + L('L2')))
    
    def __init__(self, R1, L1, R2, L2):

        self.R1 = R1
        self.L1 = L1
        self.R2 = R2
        self.L2 = L2
