"""클래스"""
from . import _win32
from typing import List, Tuple
import numpy as np

class Gui(object):
  """윈도우와 컨트롤을 핸들링하기 위한 클래스.

  Args:
    hwnd(int): 윈도우 핸들.
    [옵션]parent(:class:`Gul` or `HWND`): 부모 Gui 혹은 핸들

  **gui클래스** 는 윈도우가 비활성 상태일 때도 캡쳐나
  클릭 등을 수행하기 위한 클래스입니다.
  :func:`win32.get_windows` 는 현재 실행중인 윈도우와
  컨트롤로부터 Gui 개체를 만드는 손쉬운 방법을 제공합니다.
  

  **parent** 매개변수는 Gui가 특정 윈도우의 컨트롤인
  경우에 사용합니다. 윈도우에서 컨트롤의 상대적인 위치
  등을 계산하기 위해 필요합니다.
  """

  def __init__(self, hwnd, parent=None):
    """Window 초기화."""
    super().__init__()
    self._hwnd = hwnd
    if parent is None:
      self._parent = None
    elif isinstance(parent, type(self)):
      self._parent = parent
    elif isinstance(parent, int):
      self._parent = Gui(parent)
    else:
      raise TypeError("parent 매개변수는 int 혹은 Gui 클래스 입니다.")
    return

  def __str__(self):
    """print."""
    return "{}".format(self.name)

  def __repr__(self):
    """."""
    return "({}){}".format(self.hwnd, self.name)
  
  @property
  def hwnd(self) -> int:
    """핸들 출력.

    :returns: (`int`) 윈도우의 고유 핸들 
    """
    return self._hwnd

  @property
  def name(self) -> str:
    """이름.

    :returns: (`str`) 현재 윈도우가 가지고 있는 문자열
    """
    return _win32.get_window_text(self.hwnd)

  @property
  def parent(self) -> 'autowinpy.Gui':
    """부모 Gui.

    Return:
      (`autowinpy.Gui`) 부모가 있는 경우 부모 Gui를 반환.

      (`None`) 부모가 없는 경우.
    """
    return self._parent

  @property
  def rect(self) -> Tuple[int, int, int, int]:
    """윈도우 영역.

    Return:
      (`left, top, right, bottom`) 윈도우 영역의 좌표.
      부모가 있는 경우에는 부모를 기준으로 하는 상대좌표.

      자세한 내용은 :func:`win32.get_window_rect` 참조.
    """
    if self.is_child:
      return _win32.get_window_rect(self.hwnd, self.parent.hwnd)
    else:
      return _win32.get_window_rect(self.hwnd)

  @property
  def size(self) -> Tuple[int, int]:
    """윈도우 크기.

    :returns: (`width, height`) 윈도우의 폭과 높이.
    """
    x0, y0, x1, y1 = self.rect
    return x1 - x0, y1 - y0

  @property
  def is_active(self) -> bool:
    """제어 가능 여부.

    :returns: (`bool`) 패키지로 제어할 수 있는 요소인지 확인합니다.
    """
    return _win32.is_active_window(self.hwnd)

  @property
  def is_child(self) -> bool:
    """부모 존재 확인.

    :returns: (`bool`) 부모가 있는 UI인지 확인합니다.
    """
    return False if self._parent is None else True

  @property
  def childs(self) -> List['Gui']:
    """자식 목록.

    :returns: ([`Gui`]) 자식 윈도우/컨트롤 목록.
    """
    handles = _win32.get_child_windows(self.hwnd)
    out: List[Gui] = [Gui(i, self) for i in handles]
    return [ui for ui in out if ui.is_active]

  @property
  def screen_array(self) -> np.ndarray:
    """스크린 캡쳐.

    Returns:
      (`opencv.mat`)윈도우 스크린샷 이미지.

    자세한 내용은 :func:`win32.get_window_view_array` 참조.
    """
    image = _win32.get_window_screen_array(self.hwnd)
    return image
