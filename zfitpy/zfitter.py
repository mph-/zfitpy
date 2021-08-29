"""This module is a wrapper for the SciPy optimizers

Copyright 2021 Michael Hayes, UCECE"""

from .zfitterbrute import ZFitterBrute
from .zfittercurve import ZFitterCurve

class ZFitter(object):

    def __init__(self, model, f, Z, verbose=False):
        self._model = model
        self.verbose = verbose
        self.f = f
        self.Z = Z

    def __call__(self, ranges=None, opt='Z', method='brute', **kwargs):

        if method == 'brute':
            fitter = ZFitterBrute(self._model, self.f, self.Z, self.verbose)
            return fitter.optimize(ranges, opt, **kwargs)
        elif method in ('trg', 'dogbox'):
            fitter = ZFitterCurve(self._model, self.f, self.Z, self.verbose)
            return fitter.optimize(ranges, opt, **kwargs)
        else:
            raise ValueError('Unknown method %s: needs to be brute, trg, dogbox' % method)
        
    
