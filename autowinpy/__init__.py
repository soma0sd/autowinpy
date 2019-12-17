"""
AutoWinPy
=========

"""
import sys as _sys
from . import _win32 as win32
from . import _tk as tk
from ._classes import Gui, Template

__version__ = "0.2.0"

from ._core import (_set_windows_dpi)
if _sys.getwindowsversion().major > 8:
    __dpi_scale_factor__ = _set_windows_dpi()
else:
    __dpi_scale_factor__ = 1
