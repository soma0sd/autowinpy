"""

"""
from ctypes import windll
from typing import List, Tuple

import numpy
from PIL import Image as pil_Image
from pythonwin import win32ui
from win32 import win32gui

import cv2

from ..type import Rect, Image


def handle_list() -> List[int]:
    """핸들 리스트 출력

    Returns:
        핸들ID 리스트
    """
    enum = lambda x, arr: arr.append(x)
    out: List[int] = []
    win32gui.EnumWindows(enum, out)
    return out

def child_handle_list(hwnd: int) -> List[int]:
    """부모 핸들로부터 자식핸들 리스트를 가져옴

    Args:
        hwnd: 부모 윈도우 핸들

    Returns:
        자식핸들 ID 리스트
    """
    enum = lambda x, arr: arr.append(x)
    out: List[HWND] = []
    win32gui.EnumChildWindows(hwnd, enum, out)
    return out

def is_active_gui(hwnd: int) -> bool:
    """핸들이 감지할 수 있는 GUI를 가지고 있는지\
    확인합니다."""
    WindowEnabled = win32gui.IsWindowEnabled(hwnd)
    WindowVisible = win32gui.IsWindowVisible(hwnd)
    return bool(WindowEnabled and WindowVisible)

def window_text(hwnd: int) -> str:
    """핸들로부터 윈도우 이름을 가져옴

    Args:
        hwnd: 윈도우 핸들

    Returns:
        윈도우 이름
    """
    txt: str = win32gui.GetWindowText(hwnd).strip()
    if txt:
        return win32gui.GetWindowText(hwnd)
    else:
        return "({})".format(hwnd)

def window_rect(hwnd: int) -> 'autowinpy.type.Rect':
    """핸들로부터 윈도우 사각영역 좌표를 가져옴

    Args:
        hwnd: 윈도우 핸들

    Returns:
        :class:`Rect <autowinpy.type.Rect>` 사각영역 객체
    """
    return Rect(*win32gui.GetWindowRect(hwnd))

def window_array(hwnd: int) -> Image:
    """윈도우 이미지를 배열 형태로 가져옴

    Args:
        hwnd: 윈도우 핸들
    
    Return:
        윈도우 이미지 배열
    """
    rect: Rect = window_rect(hwnd)
    window_dc = win32gui.GetWindowDC(hwnd)
    dc_hwnd = win32ui.CreateDCFromHandle(window_dc)
    new_dc = dc_hwnd.CreateCompatibleDC()
    # bitmap object create & select
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(dc_hwnd, rect.width, rect.height)
    new_dc.SelectObject(bitmap)
    # capturing window
    windll.user32.PrintWindow(hwnd, new_dc.GetSafeHdc(), 0x2)
    # formating image
    bitmap_array = numpy.asarray(bitmap.GetBitmapBits(), dtype='uint8')

    bmp_pil = pil_Image.frombuffer(
        'RGB', (rect.width, rect.height), bitmap_array, 'raw', 'BGRX', 0, 1)
    img = numpy.array(bmp_pil)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # close DC
    win32gui.DeleteObject(bitmap.GetHandle())
    dc_hwnd.DeleteDC()
    new_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_dc)
    return Image(img)
