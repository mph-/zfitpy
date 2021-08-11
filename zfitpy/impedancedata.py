"""This module parses impedance data.

Copyright 2021 Michael Hayes, UCECE"""

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

        if lines[4].startswith('Frequency(Hz), |Z|(Ohm)-data, theta-z(deg)-data'):
            foo = np.loadtxt(filename, skiprows=5, delimiter=',', comments='END')
            self.f = foo[:, 0]
            self.Z = (np.cos(np.radians(foo[:, 2])) + 1j * np.sin(np.radians(foo[:, 2]))) * foo[:, 1]

        elif lines[4].startswith('Frequency(Hz), R(Ohm)-data, X(Ohm)-data'):
        
            foo = np.loadtxt(filename, skiprows=5, delimiter=',', comments='END')
            self.f = foo[:, 0]
            self.Z = foo[:, 1] + 1j * foo[:, 2]
        else:
            raise ValueError('Unhandled format for Keysight E4990A')

        self.filename = basename(filename)
        self.name, ext = splitext(basename(filename.lower()))


class GenericImpedanceData(ImpedanceData):

    def __init__(self, filename):

        foo = np.loadtxt(filename, skiprows=0, delimiter=',', comments='#')
        if foo.shape[1] != 3:
            raise ValueError('Expecting 3 columns (frequency, real, imag')
        
        self.f = foo[:, 0]
        self.Z = foo[:, 1] + 1j * foo[:, 2]
        self.filename = basename(filename)
        self.name, ext = splitext(basename(filename.lower()))        

        
def impedancedata(filename):

    try:
        return KeysightE4990AImpedanceData(filename)
    except:
        pass

    try:
        return GenericImpedanceData(filename)
    except:
        pass    

    # Add support for other data formats.
    
    raise ValueError('Cannot determine impedance format for %s' % filename)


