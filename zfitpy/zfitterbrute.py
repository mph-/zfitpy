"""This module is a wrapper for the SciPy optimizers

Copyright 2021 Michael Hayes, UCECE"""

from scipy.optimize import brute, fmin
from .zfitterbase import ZFitterBase


class ZFitterBrute(ZFitterBase):
    """Class for non-linear least-squares using the brute force
    SciPy algorithm."""

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

    def optimize(self, ranges=None, opt='Z', Ns=10, finish='fmin', **kwargs):
        """Ranges is a list of tuples, of the form: (min, max) or (min, max,
        numsteps).  If `numsteps` is not specified then `Ns` is used."""

        kwargs.pop('method', None)
        self.verbose = kwargs.pop('verbose', 0)

        if finish in ('none', 'None', ''):
            finish = None
        elif finish == 'fmin':
            finish = fmin

        if opt == 'Z':
            func = self.Zerror_params
        elif opt == 'Y':
            func = self.Yerror_params
        else:
            raise ValueError("Opt must be 'Y' or 'Z'")

        ranges = self._make_ranges(ranges)

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

        params, rmse, foo, bar = brute(func, oranges, Ns=Ns, args=(),
                                       finish=finish, full_output=1)

        model = self._model(*params)
        return model, rmse, None
