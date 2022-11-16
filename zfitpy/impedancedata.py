"""This module parses impedance data.

Copyright 2021--2022 Michael Hayes, UCECE"""

from numpy import loadtxt, pi, sin, cos, radians
from os.path import basename, splitext


class ImpedanceData(object):

    def __init__(self, filename, f, Z, fmin=None, fmax=None, conjugate=False):

        if fmin is not None:
            m = f >= fmin
            f = f[m]
            Z = Z[m]
        if fmax is not None:
            m = f <= fmax
            f = f[m]
            Z = Z[m]

        if conjugate:
            Z = Z.conjugate()

        self.f = f
        self.Z = Z
        self.filename = basename(filename)
        self.name, ext = splitext(self.filename)

    @property
    def Y(self):
        return 1 / self.Z


class KeysightE4990AImpedanceData(ImpedanceData):

    def __init__(self, filename, fmin, fmax, conjugate):

        lines = open(filename).readlines()
        if not lines[0].startswith('!Agilent Technologies,E4990A'):
            raise ValueError('Not Keysight E4990A')

        if lines[4].startswith('Frequency(Hz), |Z|(Ohm)-data, theta-z(deg)-data'):
            foo = loadtxt(filename, skiprows=5,
                          delimiter=',', comments='END')
            f = foo[:, 0]
            A = foo[:, 1]
            theta = radians(foo[:, 2])
            Z = (cos(theta) + 1j * sin(theta)) * A

        elif lines[4].startswith('Frequency(Hz), R(Ohm)-data, X(Ohm)-data'):

            foo = loadtxt(filename, skiprows=5,
                          delimiter=',', comments='END')
            f = foo[:, 0]
            Z = foo[:, 1] + 1j * foo[:, 2]

        elif lines[4].startswith('Frequency(Hz), Ls(H)-data, Rs(Ohm)-data'):

            foo = loadtxt(filename, skiprows=5,
                          delimiter=',', comments='END')
            f = foo[:, 0]
            Ls = foo[:, 1]
            Rs = foo[:, 2]
            Z = Rs + 1j * 2 * pi * f * Ls
        else:
            raise ValueError('Unhandled format for Keysight E4990A')

        super(KeysightE4990AImpedanceData, self).__init__(filename, f,
                                                          Z, fmin, fmax,
                                                          conjugate)


class GenericImpedanceData(ImpedanceData):

    def __init__(self, filename, fmin, fmax, conjugate):

        foo = loadtxt(filename, skiprows=0, delimiter=',', comments='#')
        if foo.shape[1] != 3:
            raise ValueError('Expecting 3 columns (frequency, real, imag')

        f = foo[:, 0]
        Z = foo[:, 1] + 1j * foo[:, 2]

        super(GenericImpedanceData, self).__init__(filename, f, Z,
                                                   fmin, fmax, conjugate)


def impedancedata(filename, fmin=None, fmax=None, conjugate=False):

    try:
        open(filename)
    except:
        raise ValueError('Cannot read file %s' % filename)

    try:
        return KeysightE4990AImpedanceData(filename, fmin, fmax, conjugate)
    except:
        pass

    try:
        return GenericImpedanceData(filename, fmin, fmax, conjugate)
    except:
        pass

    # Add support for other data formats.

    raise ValueError('Cannot determine impedance format for %s' % filename)
