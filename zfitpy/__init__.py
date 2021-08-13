"""Zfitpy is a Python library for fitting electrical one-port models
to measured impedance data.  The electrical network is specified using
Lcapy notation, such as R('R1') + L('L1').

Copyright 2021 Michael Hayes, UCECE

"""
name = "zfitpy"

import pkg_resources

from .zfitter import *
from .model import *
from .plotter import *
from .impedancedata import *
from .models import *
from .zfit import *

__version__ = pkg_resources.require('zfitpy')[0].version
