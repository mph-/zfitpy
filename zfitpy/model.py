"""This module provides the impedance Model class.

Models can be dynamically created given a network described using
Lcapy network syntax, e.g., "R('R1') + L('L1') | R('R2')".

Impedances are calculated using Lcapy.  To speed up evaluations, the
impedance calculating code is lazily compiled and cached.

Copyright 2021 Michael Hayes, UCECE

"""

from lcapy import f, t, G, R, C, L, CPE, Par, Ser, jf
from math import floor, log10
from numpy import mean, sqrt, pi as npi
from .engformatter import EngFormatter

models = {}


def round_to_n(x, n):
    """Round to n significant figures."""

    if x == 0:
        return x

    return round(x, -int(floor(log10(abs(x)))) + (n - 1))


def modelmake(name, net, paramnames=None):

    if isinstance(net, str):
        net = eval(net)

    if paramnames is None:
        try:
            # For Lcapy 0.99
            paramnames = net.params
        except:
            Z = eval('(%s).Z(jf)' % net)
            paramnames = Z.symbols
            paramnames.pop('t', None)
            paramnames.pop('f', None)

    params = ', '.join(paramnames)

    docstring = name + '(' + params + '): ' + str(net)
    newclass = type(name, (Model, ), {'__doc__': docstring})
    newclass._net = net
    newclass.paramnames = paramnames
    models[name] = newclass
    return newclass


class Model(object):

    _Ycode = None
    _Zcode = None
    _rmse = 0
    _cov = None
    _method = ''

    def __init__(self, *args):
        """Create model instance."""

        if len(args) == 0:
            return

        # Add parameter attributes
        for m, p in enumerate(self.paramnames):
            setattr(self, p, args[m])

    def __repr__(self):
        return self.__str__()

    def __call__(self, i, t):

        return self.v(i, t)

    def v(self, i, t):
        """Calculate voltage drop across the network given a current signal."""

        return self._net.subs(vars(self)).Z.response(i, t)

    def i(self, v, t):
        """Calculate current through the network given an applied voltage
        signal."""

        return self._net.subs(vars(self)).Y.response(v, t)

    def draw(self, filename=None, layout='horizontal'):
        """Draw the network."""

        if filename is not None and filename.endswith('.sch'):
            outfile = open(filename, 'w')
            sch = self._net.sch(layout=layout)
            outfile.write(str(sch))
            outfile.close()
        else:
            self._net.draw(filename, layout=layout)

    def _build(self, foo, name):
        paramnames = foo.symbols
        paramnames.pop('t', None)
        paramnames.pop('f', None)

        # FIXME if have R1 and R since the replacement will fail.
        codestr = str(foo)
        for p in paramnames:
            codestr = codestr.replace(p, 'self.' + p)
        code = compile(codestr, name, 'eval')

        return code

    def _Ybuild(self):

        return self._build(self._net.Y(jf), 'Y')

    def _Zbuild(self):

        return self._build(self._net.Z(jf), 'Z')

    def Z(self, f):
        """Return impedance at frequency `f`; `f` can be an ndarray."""

        if self._Zcode is None:
            # Cache result for class
            self.__class__._Zcode = self._Zbuild()

        j = 1j
        pi = npi

        return eval(self._Zcode)

    def Y(self, f):
        """Return admittance at frequency `f`; `f` can be an ndarray."""

        if self._Ycode is None:
            # Cache result for class
            self.__class__._Ycode = self._Ybuild()

        j = 1j
        pi = npi

        return eval(self._Ycode)

    def __str__(self):

        return self.title(sfmax=3)

    def title(self, sfmax=3):

        parts = []
        for var, val in vars(self).items():
            if var[0] == '_':
                continue

            try:
                units = {'R': 'ohm', 'C': 'F',
                         'L': 'H', 'K': '', 'a': ''}[var[0]]
            except KeyError:
                units = ''

            parts.append('%s=%s' %
                         (var, EngFormatter(hundreds=True, sfmax=sfmax).str(val, units)))

        return ', '.join(parts)

    def defs(self, dp=10):

        defs = {}
        for var, val in vars(self).items():
            if var[0] == '_':
                continue
            defs[var] = round_to_n(val, dp)

        return defs

    @property
    def net(self):
        return self._net.subs(vars(self))

    def Yrmse(self, f, Y):

        Yerr = Y - self.Y(f)
        rmse = sqrt(mean(Yerr.real**2 + Yerr.imag**2))
        return rmse

    def Zrmse(self, f, Z):

        Zerr = Z - self.Z(f)
        rmse = sqrt(mean(Zerr.real**2 + Zerr.imag**2))
        return rmse

    @property
    def error(self):
        return self._rmse
