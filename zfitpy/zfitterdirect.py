"""This module is a wrapper for the SciPy optimizers

Copyright 2025 Michael Hayes, UCECE"""

from scipy.optimize import direct
from .zfitterbase import ZFitterBase


class ZFitterDirect(ZFitterBase):
    """Class for non-linear least-squares using the DIRECT algorithm."""

    def Zerror_params(self, params):

        model = self._model(*params)
        rmse = model.Zrmse(self.f, self.Z)
        if self.verbose > 1:
            print(model, rmse)
        return rmse

    def Yerror_params(self, params):

        model = self._model(*params)
        rmse = model.Yrmse(self.f, self.Y)
        if self.verbose > 1:
            print(model, rmse)
        return rmse

    def optimize(self, ranges=None, opt='Z', maxiter=10000,
                 maxfun=1000000, **kwargs):
        """Ranges is a list of tuples, of the form: (min, max) or (min, max,
        numsteps)."""

        kwargs.pop('Ns', None)
        kwargs.pop('finish', None)
        kwargs.pop('method', None)
        self.verbose = kwargs.pop('verbose', 0)

        if opt == 'Z':
            func = self.Zerror_params
        elif opt == 'Y':
            func = self.Yerror_params
        else:
            raise ValueError("Opt must be 'Y' or 'Z'")

        ranges = self._make_ranges(ranges)

        bounds = []

        for m, r in enumerate(ranges):
            if len(r) in (2, 3):
                bounds.append((r[0], r[1]))
            else:
                raise ValueError('Range %s can only have 2 or 3 values' % r)

        res = direct(func, bounds, args=(), maxiter=maxiter, maxfun=maxfun,
                     **kwargs)
        params = res.x

        print(res.message)

        model = self._model(*params)
        if opt == 'Z':
            rmse = model.Zrmse(self.f, self.Z)
        else:
            rmse = model.Yrmse(self.f, self.Z)

        return model, rmse, None
