"""This module provides a simple function for fitting an electric model to measured impedance data.

Copyright 2021 Michael Hayes, UCECE"""

from .impedancedata import ImpedanceData, impedancedata
from .model import modelmake, Model
from .zfitter import ZFitter

def zfit(data, model, ranges, Ns=10):
    """Fit impedance data to a model.

    `data` can be a filename string or and `ImpedanceData` object
    `model` can be a string describing the network model or a `Model` class
    `ranges` is a dictionary of the search ranges for each component
    `Ns` is the number of search steps in each dimension.

    Returns: `ImpedanceData` object and a best-fit `Model` object.
    """

    if not isinstance(data, ImpedanceData):
        data = impedancedata(data)

    if not isinstance(model, Model):
        model = modelmake('Model', model)

    zfitter = ZFitter(model, data.f, data.Z)
        
    fitmodel = zfitter(ranges=ranges, Ns=Ns)

    return data, fitmodel
