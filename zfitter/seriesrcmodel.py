from .model import Model
from lcapy import R, C

class SeriesRCModel(Model):

    net = R('Rs') + C('Cs')

    def __init__(self, Rs, Cs):

        self.Rs = Rs
        self.Cs = Cs
        
