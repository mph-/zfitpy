"""This module provides the impedance Model class.

Models can be dynamically created given a network described using
Lcapy network syntax, e.g., "R('R1') + L('L1') | R('R2')".

Impedances are calculated using Lcapy.  To speed up evaluations, the
impedance calculating code is lazily compiled and cached.

Copyright 2021 Michael Hayes, UCECE

"""

from lcapy import f, t, G, R, C, L, CPE, Par, Ser
import numpy as np

models = {}

def modelmake(name, net, paramnames=None):

    if isinstance(net, str):
        net = eval(net)
    
    if paramnames is None:
        Z = eval('(%s).Z(f)' % net)
        paramnames = Z.symbols
        paramnames.pop('t', None)
        paramnames.pop('f', None)
    
    params = ', '.join(paramnames)
    
    docstring = name + '(' + params + '): ' + str(net)
    newclass = type(name, (Model, ), {'__doc__': docstring})
    newclass.net = net
    newclass.paramnames = paramnames
    models[name] = newclass
    return newclass


class Model(object):

    _Zcode = None
    error = 0

    def __init__(self, *args):
        """Create model instance."""

        if len(args) == 0:
            return
        
        for m, p in enumerate(self.paramnames):
            setattr(self, p, args[m])
    
    def __repr__(self):
        return self.__str__()

    def __call__(self, i, t):

        return self.v(i, t)

    def v(self, i, t):
        """Calculate voltage drop across the network given a current signal."""

        return self.net.subs(vars(self)).Z.response(i, t)
    
    def i(self, v, t):
        """Calculate current through the network given an applied voltage
        signal."""        

        return self.net.subs(vars(self)).Y.response(v, t)        

    def draw(self, filename=None):
        """Draw the network."""

        self.net.draw(filename)

    def _build(self, foo, name):
    
        paramnames = foo.symbols
        paramnames.pop('t', None)
        paramnames.pop('f', None)        
        
        codestr = str(foo)
        for p in paramnames:
            codestr = codestr.replace(p, 'self.' + p)
        code = compile(codestr, name, 'eval')

        return code

    def _Zbuild(self):    

        return self._build(self.net.Z(f), 'Z')

    def Z(self, f):
        """Return impedance at frequency `f`; `f` can be an ndarray."""

        if self._Zcode is None:
            # Cache result for class
            self.__class__._Zcode = self._Zbuild()
        
        j = 1j
        pi = np.pi
        
        return eval(self._Zcode)
    
    def Y(self, f):
        """Return admittance at frequency `f`; `f` can be an ndarray."""        

        return 1 / self.Z(f)

    def __str__(self):

        parts = []
        for var, val in vars(self).items():
            if var == 'error':
                continue
            
            units = {'R': ' ohms', 'C': ' F', 'L': ' H', 'K':'', 'a':''}[var[0]]

            # Could convert units to have SI prefixes
            parts.append('%s=%.2e%s' % (var, val, units))

        return ', '.join(parts)
