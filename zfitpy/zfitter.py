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

    def zmodel_error(self, params):

        model = self._model(*params)
        Z = model.Z(self.f)
        Zerr = Z - self.Z
        rmse = np.sqrt(np.mean(Zerr.real**2 + Zerr.imag**2))
        if self.verbose:        
            print(model, rmse)
        return rmse

    def __call__(self, ranges=None, Ns=10, finish=True):

        if isinstance(ranges, str):
            ranges = eval(ranges)            
        
        if isinstance(ranges, dict):
            rangesdict = ranges
            ranges = []
            for paramname in self._model.paramnames:
                ranges.append(rangesdict[paramname])
        
        if finish:
            # This calls fmin at finish
            params, fval, foo, bar = brute(self.zmodel_error, ranges, Ns=Ns, args=(), full_output=1)
        else:
            params, fval, foo, bar = brute(self.zmodel_error, ranges, Ns=Ns, args=(), full_output=1, finish=None)

        model = self._model(*params)
        model.error = fval
        return model
    
        
