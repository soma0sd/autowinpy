"""패키지 & 파이썬 & 프로세스 시스템 제어
"""
from ctypes import windll
import sys


def _set_windows_dpi() -> float:
    """windows 8.1 이상을 위한 DPI 조정.

    Return:
        DPI 배율

    프로세스가 HIDPI 모드로 변경됩니다.
    이 작업은 좌표 기반의 윈도우 핸들링을 위해
    반드시 필요합니다.
    """
    if sys.getwindowsversion().major > 8:
        user32 = windll.user32
        native = user32.GetDpiForSystem()
        user32.SetProcessDPIAware()
        scaled = user32.GetDpiForSystem()
        return scaled / native
    else:
        return 1
