"""
AutoWinPy::CORE
===============

* 패키지 초기화
"""
from ctypes import windll

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
