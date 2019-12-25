"""
AutoWinPy
==========

"""
from . import win32
from . import type
from . import core
from .core import *
from .win32 import *
from .type import *


__version__ = "0.4.0"
"""패키지 버전"""

__dpi_scale_factor__ = core._set_windows_dpi()
"""HIDPI 배율"""
