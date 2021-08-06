import numpy as np
from os.path import basename, splitext


class ImpedanceData(object):

    @property
    def Y(self):
        return 1 / self.Z
    

class KeysightE4990AImpedanceData(ImpedanceData):

    def __init__(self, filename):

        foo = np.loadtxt(filename, skiprows=5, delimiter=',', comments='END')
        self.f = foo[:, 0]
        self.Z = foo[:, 1] + 1j * foo[:, 2]
        self.filename = basename(filename)
        self.name, ext = splitext(basename(filename.lower()))
        
