"""

win32 모듈이 내장하고 있는 함수는 UI 클래스의
기능을 대부분 탑재하고 있습니다.

"""
from win32 import win32gui, win32api
from win32.lib import win32con
from pythonwin import win32ui
from PIL import Image
from ctypes import windll, wintypes
from ctypes import byref
from typing import List, Tuple
import numpy as np
import cv2

HWND = int

def _set_windows_dpi() -> float:
  """[private] windows 8.1 이상을 위한 DPI 조정.

  Return:
    (float) DPI 배율

  프로세스 환경이 HIDPI 모드로 변경됩니다.
  이 작업은 좌표 기반의 윈도우 핸들링을 위해
  반드시 필요합니다.
  """
  user32 = windll.user32

  native = user32.GetDpiForSystem()
  user32.SetProcessDPIAware()
  scaled = user32.GetDpiForSystem()
  return scaled / native

def get_windows() -> List[HWND]:
  """핸들 리스트 출력.

  Return:
    [`int`] 윈도우 핸들

  Example:
    .. code-block:: python

        import autowinpy as awp
        from win32 import win32gui

        window_list = awp.win32.get_windows()
        for hwnd in window_list:
            print(win32gui.GetWindowText(hwnd))
    .. code-block
    
    현재 윈도우 핸들을 나열합니다.
  """
  enum = lambda x, arr: arr.append(x)
  out: List[HWND] = []
  win32gui.EnumWindows(enum, out)
  return out

def get_child_windows(hwnd: HWND) -> List[HWND]:
  r"""자식 핸들 리스트 출력.

  Args:
    hwnd (`HWND`): 윈도우 핸들
  Return:
    ([`HWND`]) 자식 윈도우/컨트롤의 핸들 리스트
  Examples:
    .. code-block:: python

        import autowinpy as awp
        from win32 import win32gui

        window_list = get_windows()
        for hwnd in window_list:
            print(win32gui.GetWindowText(hwnd))
            childs_list = get_child_windows(hwnd)
            for chwnd in childs_list:
                print("\t", win32gui.GetWindowText(chwnd))
    .. code-block
    
    현재 윈도우와 자식 핸들 명칭을 나열합니다.
  """
  enum = lambda x, arr: arr.append(x)
  out: List[HWND] = []
  win32gui.EnumChildWindows(hwnd, enum, out)
  return out

def get_window_rect(toHWND: HWND, fromHWND: HWND=None) -> Tuple[int, int, int, int]:
  """윈도우가 그리는 사각영역의 위치좌표를 얻습니다.

  Args:
    toHWND(`HWND`): 영역좌표를 알고 싶은 윈도우의 핸들.
    fromHWND(`HWND`): (옵션) 상대위치를 구하고자 할 때 기준점이 될 윈도우
  returns:
    (left, top, right, bottom)
  
  계산 후 출력하는 좌표는 모니터의 우측 상단이 원점이며, 오른쪽으로
  갈수록 x값이 증가하고, 아래로 내려갈수록 y값이 증가합니다.

  상대좌표는 기준점이 되는 창의 왼쪽 끝을 새로운 원점으로 하며,
  오른쪽 아래로 갈수록 값이 증가합니다.
  """
  GetWindowRect = windll.user32.GetWindowRect
  toRect = wintypes.RECT()
  fromRect = wintypes.RECT()
  GetWindowRect(wintypes.HWND(toHWND), byref(toRect))
  if fromHWND is None:
    return toRect.left, toRect.top, toRect.right, toRect.bottom
  else:
    GetWindowRect(wintypes.HWND(fromHWND), byref(fromRect))
    left = toRect.left - fromRect.left
    right = toRect.right - fromRect.left
    top = toRect.top - fromRect.top
    bottom = toRect.bottom - fromRect.top
    return left, right, top, bottom

def get_window_view_array(hwnd:HWND) -> np.ndarray:
  """윈도우 화면을 가져옵니다.

  Args:
    hwnd(`HWND`): 윈도우 핸들

  Return:
    (`opencv.mat`) 선택한 창의 내용을 OpenCV나 Numpy에서 사용할
    수 있는 BGR이미지를 출력합니다.
  """
  # window rect and size
  x0, y0, x1, y1 = get_window_rect(hwnd)
  w, h = x1 - x0, y1 - y0
  ## create DC
  wDC = win32gui.GetWindowDC(hwnd)
  dcObj = win32ui.CreateDCFromHandle(wDC)
  cDC = dcObj.CreateCompatibleDC()
  ## bitmap object make & select
  dataBitMap = win32ui.CreateBitmap()
  dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
  cDC.SelectObject(dataBitMap)
  ## capturing window
  windll.user32.PrintWindow(hwnd, cDC.GetSafeHdc(), 0x2)
  ## formating image
  bmparray = np.asarray(dataBitMap.GetBitmapBits(), dtype='uint8')
  bmp_pil = Image.frombuffer('RGB', (w, h), bmparray, 'raw', 'BGRX', 0, 1)
  img = np.array(bmp_pil)
  img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
  # close DC
  win32gui.DeleteObject(dataBitMap.GetHandle())
  dcObj.DeleteDC()
  cDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, wDC)
  return img
