"""This module is a wrapper for the SciPy optimizers

Copyright 2021 Michael Hayes, UCECE"""

import numpy as np
from scipy.signal import resample
from scipy.optimize import fminbound, brute, fmin

class ZFitter(object):

    def __init__(self, model, f, Z, verbose=False):
        self._model = model
        self.verbose = verbose
        self.f = f
        self.Z = Z

    @property
    def Y(self):
        return 1 / self.Z

    def Zerror(self, model):
        
        Z = model.Z(self.f)
        Zerr = Z - self.Z
        rmse = np.sqrt(np.mean(Zerr.real**2 + Zerr.imag**2))
        if self.verbose:        
            print(model, rmse)
        return rmse        
    
    def Zparams_error(self, params):

        model = self._model(*params)
        return self.Zerror(model)

    def Yerror(self, model):

        Y = model.Y(self.f)
        Yerr = Y - self.Y
        rmse = np.sqrt(np.mean(Yerr.real**2 + Yerr.imag**2))
        if self.verbose:        
            print(model, rmse)
        return rmse            
    
    def Yparams_error(self, params):

        model = self._model(*params)
        return self.Yerror(model)        

    def __call__(self, ranges=None, Ns=10, finish=True, opt='Z'):
        """Ranges is a list of tuples, of the form: (min, max) or (min, max,
        numsteps).  If `numsteps` is not specified then `Ns` is used."""

        if isinstance(ranges, str):
            ranges = eval(ranges)            
        
        if isinstance(ranges, dict):
            rangesdict = ranges
            ranges = []
            for paramname in self._model.paramnames:
                ranges.append(rangesdict[paramname])

        oranges = []
        for r in ranges:
            if len(r) == 2:
                # Note, a complex value specifies the number of steps
                # (see numpy.mgrid).
                oranges.append(slice(r[0], r[1], complex(Ns)))
            elif len(r) == 3:
                oranges.append(slice(r[0], r[1], complex(r[2])))
            else:
                raise ValueError('Range %s can only have 2 or 3 values' % r)

        if opt == 'Z':
            func = self.Zparams_error
        elif opt == 'Y':
            func = self.Yparams_error
        else:
            raise ValueError("Opt must be 'Z' or 'Y'")
            
        if finish:
            # This calls fmin at finish
            params, fval, foo, bar = brute(func, oranges, Ns=Ns, args=(), full_output=1)
        else:
            params, fval, foo, bar = brute(func, oranges, Ns=Ns, args=(), full_output=1, finish=None)

        model = self._model(*params)
        model.error = fval
        return model
    
        
