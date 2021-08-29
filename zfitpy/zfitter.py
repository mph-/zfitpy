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

    def Zerror_params(self, params):

        model = self._model(*params)
        rmse = model.Zrmse(self.f, self.Z)
        if self.verbose:        
            print(model, rmse)        
        return rmse

    def Yerror_params(self, params):

        model = self._model(*params)
        rmse = model.Yrmse(self.f, self.Y)
        if self.verbose:        
            print(model, rmse)        
        return rmse

    def _optimize_brute(self, func, ranges, Ns, finish):
                
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

        if finish:
            # This calls fmin at finish
            params, rmse, foo, bar = brute(func, oranges, Ns=Ns, args=(), full_output=1)
        else:
            params, rmse, foo, bar = brute(func, oranges, Ns=Ns, args=(), full_output=1, finish=None)

        return params, rmse

    def __call__(self, ranges=None, Ns=10, finish=True, opt='Z'):
        """Ranges is a list of tuples, of the form: (min, max) or (min, max,
        numsteps).  If `numsteps` is not specified then `Ns` is used."""

        if opt == 'Z':
            func = self.Zerror_params
        elif opt == 'Y':
            func = self.Yerror_params
        else:
            raise ValueError("Opt must be 'Z' or 'Y'")
            
        if isinstance(ranges, str):
            ranges = eval(ranges)            
        
        if isinstance(ranges, dict):
            rangesdict = ranges
            ranges = []
            for paramname in self._model.paramnames:
                ranges.append(rangesdict[paramname])

        params, error = self._optimize_brute(func, ranges, Ns, finish)

        model = self._model(*params)
        model.error = error
        return model
    
        
