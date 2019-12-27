"""Gui 클래스
"""
from .. import win32
from typing import List
from ..type import Image
import numpy
import re

class Gui:
    """윈도우 앱 제어 클래스

    Args:
        hwnd: 핸들 ID
    """

    __module__ = 'autowinpy'

    def __init__(self, hwnd: int):
        """초기화"""
        self._hwnd = hwnd

    def __str__(self):
        """출력"""
        return self.name

    def __repr__(self):
        """터미널 출력"""
        return "({}) {}".format(self.hwnd, self.name)

    @property
    def _is_active(self) -> bool:
        return win32.is_active_gui(self.hwnd)

    @property
    def name(self) -> str:
        """(str) 윈도우 이름"""
        return win32.window_text(self.hwnd)

    @property
    def hwnd(self) -> int:
        """(int) 윈도우 핸들 ID"""
        return self._hwnd
    
    @property
    def rect(self) -> 'autowinpy.type.Rect':
        """윈도우 :class:`Rect <autowinpy.type.Rect>`
        사각영역 객체
        """
        return win32.window_rect(self.hwnd)

    def childs(self) -> List['autowinpy.Gui']:
        """자식 :class:`Gui` 목록 출력"""
        child_list =  [Gui(h) for h in win32.child_handle_list(self.hwnd)]
        return [g for g in child_list if g._is_active]

    def image_array(self) -> Image:
        """이미지 출력"""
        return Image(win32.window_array(self.hwnd))

def window_list() -> List[Gui]:
    """활성 윈도우를 Gui 목록으로 출력

    Return:
        :class:`Gui` 리스트
    """
    win_list: List[Gui] = [Gui(h) for h in win32.handle_list()]
    return [g for g in win_list if g._is_active]

def find_window(name_re:str) -> List[Gui]:
    """정규표현식으로 윈도우를 찾습니다.

    Returns:
        정규식 규칙을 포함하는 :class:`Gui` 리스트

    Note:
        ``re.search()`` 를 만족하는 윈도우를 출력하기 때문에,
        문자열을 포함하거나 일치하는 윈도우를 찾을 때도 활용할
        수 있습니다.
    """
    _rex = re.compile(name_re)
    wins = [win for win in window_list() if _rex.search(win.name)]
    return wins
