from .model import Model, build
from lcapy import R, L

class SeriesRLModel(Model):

    net, Zcode = build(R('Rs') + L('Ls'))

    def __init__(self, Rs, Ls):

        self.Rs = Rs
        self.Ls = Ls
        
