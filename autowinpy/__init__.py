"""
autowinpy
=========


"""
import sys as _sys
from . import _win32 as win32
from . import tk
from ._types import UI

__version__ = "0.1.0"

if _sys.getwindowsversion().major > 8:
    __dpi_scale_factor__ = win32._set_windows_dpi()
else:
    __dpi_scale_factor__ = 1
