"""This module is a wrapper for the SciPy optimizers

Copyright 2021--2025 Michael Hayes, UCECE"""

from .zfitterbrute import ZFitterBrute
from .zfittercurve import ZFitterCurve


class ZFitter(object):

    def __init__(self, model, f, Z):
        self._model = model
        self.f = f
        self.Z = Z

    def __call__(self, ranges=None, opt=None, method='brute',
                 fmin=None, fmax=None, **kwargs):

        parts = method.split('-')
        if len(parts) > 2:
            raise ValueError('Unknown method %s' % method)
        if len(parts) == 2:
            if parts[1] not in ('Y', 'Z'):
                raise ValueError('Unknown method objective %s' % parts[1])
            if opt is not None:
                raise ValueError('Cannot specify method objective and opt')
            opt = parts[1]
        else:
            if opt is None:
                opt = 'Z'
        method = parts[0]

        f = self.f
        Z = self.Z
        if fmin is not None:
            m = f >= fmin
            f = f[m]
            Z = Z[m]
        if fmax is not None:
            m = f <= fmax
            f = f[m]
            Z = Z[m]

        if method == 'brute':
            fitter = ZFitterBrute(self._model, f, Z)
        elif method in ('trf', 'dogbox'):
            fitter = ZFitterCurve(self._model, f, Z)
        else:
            raise ValueError(
                'Unknown method %s: needs to be brute, trf, dogbox' % method)

        model, rmse, cov = fitter.optimize(
            ranges, opt, method=method, **kwargs)
        model._rmse = rmse
        model._cov = cov
        model._method = method

        for param, r in ranges.items():
            value = getattr(model, param)
            if value <= r[0]:
                print(f'Parameter {param}={value} at or below bound {r[0]}')
            elif value >= r[1]:
                print(f'Parameter {param}={value} at or above bound {r[1]}')

        return model
