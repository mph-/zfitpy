"""This module is a wrapper for the SciPy optimizers

Copyright 2021--2025 Michael Habyes, UCECE"""

from numpy import zeros, hstack
from scipy.optimize import curve_fit
from .zfitterbase import ZFitterBase


class ZFitterCurve(ZFitterBase):
    """Class for non-linear least-squares using the trf and dogbox
    SciPy algorithms."""

    def Z_params(self, f, *params):
        Z = self._model(*params).Z(f)
        return hstack((Z.real, Z.imag))

    def Y_params(self, f, *params):
        Y = self._model(*params).Y(f)
        return hstack((Y.real, Y.imag))

    def optimize(self, ranges=None, opt='Z', ftol=1e-14, xtol=1e-14,
                 maxfev=1e5, **kwargs):
        """Ranges is a list of tuples, of the form: (min, max)."""

        kwargs.pop('Ns', None)
        kwargs.pop('finish', None)

        if opt == 'Z':
            func = self.Z_params
            ydata = self.Z
        elif opt == 'Y':
            func = self.Y_params
            ydata = self.Y
        else:
            raise ValueError("Opt must be 'Z' or 'Y'")

        ranges = self._make_ranges(ranges)

        bounds_min = zeros(len(ranges))
        bounds_max = zeros(len(ranges))

        for m, r in enumerate(ranges):
            if len(r) in (2, 3):
                bounds_min[m] = r[0]
                bounds_max[m] = r[1]
            else:
                raise ValueError('Range %s can only have 2 or 3 values' % r)

        bounds = (bounds_min, bounds_max)

        # Initial guess.
        p0 = 0.5 * (bounds_min + bounds_max)

        ydata = hstack((ydata.real, ydata.imag))
        params, cov = curve_fit(func, self.f, ydata, p0=p0,
                                bounds=bounds, ftol=ftol, xtol=xtol,
                                maxfev=maxfev, **kwargs)
        #err = sqrt(diag(cov))

        model = self._model(*params)

        if opt == 'Z':
            rmse = model.Zrmse(self.f, self.Z)
        else:
            rmse = model.Yrmse(self.f, self.Y)

        return model, rmse, cov
