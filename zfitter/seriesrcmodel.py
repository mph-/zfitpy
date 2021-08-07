from .model import Model, build
from lcapy import R, C

class SeriesRCModel(Model):

    net, Zcode = build(R('Rs') + C('Cs'))

    def __init__(self, Rs, Cs):

        self.Rs = Rs
        self.Cs = Cs
        
