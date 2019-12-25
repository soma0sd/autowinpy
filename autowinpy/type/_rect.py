"""
"""
from typing import Tuple

class Rect:
    """사각영역"""

    __module__ = 'autowinpy.type'

    def __init__(self, left=0, top=0, right=0, bottom=0):
        """초기화"""
        self.xyxy(left, top, right, bottom)

    @property
    def left(self) -> int:
        """왼쪽 좌표"""
        return self._left

    @property
    def right(self) -> int:
        """오른쪽 좌표"""
        return self._right

    @property
    def top(self) -> int:
        """상단 좌표"""
        return self._top

    @property
    def bottom(self) -> int:
        """하단 좌표"""
        return self._bottom

    @property
    def width(self) -> int:
        """너비"""
        return self._right - self._left
    
    @property
    def height(self) -> int:
        """높이"""
        return self._bottom - self._top
    
    @property
    def size(self) -> Tuple[int, int]:
        """너비와 높이 출력"""
        return self.width, self.height

    @property
    def start(self) -> Tuple[int, int]:
        """시작 좌표"""
        return self._left, self._top

    @property
    def end(self) -> Tuple[int, int]:
        """끝 좌표"""
        return self._right, self._bottom

    def xyxy(self, left:int, top:int, right:int, bottom:int):
        """좌, 상, 우, 하 수치를 기준으로 재정의합니다."""
        self._left: int = left
        self._right: int = right
        self._top: int = top
        self._bottom: int = bottom
        return self

    def xywh(self, left:int, top:int, width:int, height:int):
        """시작 좌표와 너비, 높이로 재정의합니다."""
        self._left: int = left
        self._top: int = top
        self._right: int = left + width
        self._bottom: int = top + height
        return self
