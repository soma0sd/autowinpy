"""

"""
from ctypes import windll
from time import sleep
from typing import List, Tuple

import numpy
from PIL import Image as pil_Image
from pythonwin import win32ui
from win32 import win32api, win32gui

import cv2

from ..type import Image, Rect


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

def post_cilck(hwnd: int, x: int, y: int):
    """핸들로 클릭 메시지 전송

    Args:
        hwnd: GUI 핸들
        x: 클릭할 x 좌표
        y: 클릭할 y 좌표
    """
    lParam: int = x | y << 16
    win32api.PostMessage(hwnd, 0x0201, 0x0001, lParam)
    sleep(0.01)
    win32api.PostMessage(hwnd, 0x0202, 0x0000, lParam)
    sleep(0.01)

def post_drag(hwnd: int, x0: int, y0: int, x1: int, y1: int, dtime: float=0.01):
    """핸들로 드래그 메시지 전송
    
    Args:
        hwnd: GUI 핸들
        x0: 드래그를 시작할 x 좌표
        y0: 드래그를 시작할 y 좌표
        x1: 드래그를 끝낼 x 좌표
        y1: 드래그를 끝낼 y 좌표
        dtime: 이동 스탭별 시간 간격. 기본값 ``0.01`` (초)
    """
    lParam = lambda x, y: x | y << 16
    distance = int(numpy.sqrt(pow(abs(x1-x0), 2) + pow(abs(y1-y0), 2)) / 3)
    position = numpy.linspace(x0, x1, distance), numpy.linspace(y0, y1, distance)
    win32api.PostMessage(hwnd, 0x0201, 0x0001, lParam(x0, y0))
    sleep(dtime)
    for x, y in zip(*position):
        x, y = int(x), int(y)
        win32api.PostMessage(hwnd, 0x0200, 0x0001, lParam(x, y))
        sleep(dtime)
    win32api.PostMessage(hwnd, 0x0202, 0x0000, lParam(x1, y1))
    sleep(dtime)
