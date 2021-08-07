from .model import Model
from lcapy import R, L

class SeriesRLModel(Model):

    net = R('Rs') + L('Ls')

    def __init__(self, Rs, Ls):

        self.Rs = Rs
        self.Ls = Ls
        
