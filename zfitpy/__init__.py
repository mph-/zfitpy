"""Zfitter is a Python library for impedance data fitting to
electrical one-ports.  The electrical network is specified using Lcapy
notation, such as R('R1') + L('L1').

Copyright 2021 Michael Hayes, UCECE

"""

from .zfitter import *
from .model import *
from .plotter import *
from .impedancedata import *
from .models import *
from .zfit import *

import pkg_resources

__version__ = pkg_resources.require('zfitter')[0].version
