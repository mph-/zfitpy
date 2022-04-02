"""This module is a wrapper for the SciPy optimizers

Copyright 2021 Michael Hayes, UCECE"""


class ZFitterBase(object):

    def __init__(self, model, f, Z):
        self._model = model
        self.verbose = 0
        self.f = f
        self.Z = Z

    @property
    def Y(self):
        return 1 / self.Z

    def _make_ranges(self, ranges):

        if isinstance(ranges, str):
            ranges = eval(ranges)

        if isinstance(ranges, dict):
            rangesdict = ranges
            ranges = []
            for paramname in self._model.paramnames:
                ranges.append(rangesdict[paramname])

        return ranges
