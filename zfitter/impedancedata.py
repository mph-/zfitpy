import numpy as np
from os.path import basename, splitext


class ImpedanceData(object):

    @property
    def Y(self):
        return 1 / self.Z
    

class KeysightE4990AImpedanceData(ImpedanceData):

    def __init__(self, filename):

        lines = open(filename).readlines()
        if not lines[0].startswith('!Agilent Technologies,E4990A'):
            raise ValueError('Not Keysight E4990A')
        
        foo = np.loadtxt(filename, skiprows=5, delimiter=',', comments='END')
        self.f = foo[:, 0]
        self.Z = foo[:, 1] + 1j * foo[:, 2]
        self.filename = basename(filename)
        self.name, ext = splitext(basename(filename.lower()))

        
def impedancedata(filename):

    try:
        return KeysightE4990AImpedanceData(filename)
    except:
        pass

    # Add support for other data formats.
    
    raise ValueError('Cannot determine impedance format for %s' % filename)


