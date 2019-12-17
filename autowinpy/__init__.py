"""
AutoWinPy
=========

"""
import sys as _sys
from . import _win32 as win32
from . import _tk as tk
from ._classes import Gui, Template
from ._core import (
    _set_windows_dpi,
    window_list,
    find_window
)

__version__ = "0.3.0"

if _sys.getwindowsversion().major > 8:
    __dpi_scale_factor__ = _set_windows_dpi()
else:
    __dpi_scale_factor__ = 1
