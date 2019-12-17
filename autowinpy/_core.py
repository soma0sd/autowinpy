"""
AutoWinPy::CORE
===============

* 패키지 초기화
* 기본 함수
"""
from . import _win32
from ._classes import Gui
from ctypes import windll
from typing import List
import re


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

def window_list() -> List["autowinpy.Gui"]:
  """윈도우 목록 출력

  Returns:
    ([:class:`autowinpy.Gui`]) 현재 제어가능한 창 목록
  """
  guis: List[Gui] = [Gui(h) for h in _win32.get_windows()]
  return [gui for gui in guis if gui.is_active]

def find_window(name_re:str) -> List["autowinpy.Gui"]:
  """정규표현식으로 윈도우를 찾습니다.

  Returns:
    ([:class:`autowinpy.Gui`]) 일치하는 이름을 가진
    윈도우 목록
  """
  _rex = re.compile(name_re)
  return [win for win in window_list() if _rex.match(win.name)]
