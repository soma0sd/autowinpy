"""

tkinter는 쉽게 사용할 수 있는 GUI 패키지입니다.
"""
from . import _win32
from . import _types

from PIL import Image, ImageTk
from typing import Tuple, Callable, List
from tkinter import ttk
import numpy
import cv2


def tk_image(image: numpy.ndarray, dsize: Tuple[int, int]=None) -> 'PIL.ImageTk':
    """OpenCV 이미지를 Tk 이미지로 변환.

    Args:
        image (`opencv.mat`): OpenCV용 이미지요소.
        dsize (`(width, height)`): [옵션] 변환할 사이즈.

    Return:
        (`ImageTK`) tkinter 위젯에 사용할 수 있는 이미지 요소.

    Example:
        .. code-block:: python

            import autowinpy as awp
            import tkinter as tk

        .. code-block
    """
    cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if not dsize is None:
        if dsize[0] * dsize[1] < cv_img.shape[0] * cv_img.shape[1]:
            method = cv2.INTER_AREA
        else:
            method = cv2.INTER_LINEAR
        cv_img = cv2.resize(cv_img, dsize, method)
    pil_img = Image.fromarray(cv_img)
    tk_img = ImageTk.PhotoImage(pil_img)
    return tk_img

class tkWindowCombo(ttk.Combobox):
    """ttk 윈도우 선택 콤보박스.

    Args:
        master: 상위 위젯
        kw: 속성 (TK레퍼런스_ 참조)

    tkinter GUI에서 사용할 수 있는 윈도우선택 콤보박스
    입니다.

    Example:
        .. code-block:: python

            import autowinpy as awp
            import tkinter as tk
            app = tk.Tk()
            com1 = awp.tk.tkWindowCombo(app)
            log = lambda: print("({}) {}".format(com1.window.hwnd, com1.window))
            com1.bind_select(log)
            com1.pack()
            app.mainloop()
        .. code-block

    .. _TK레퍼런스: https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_combobox.htm
    """
    def __init__(self, master=None, **kw):
        """콤보박스 초기화"""
        super().__init__(master=master, **kw)
        self._windows: List['autowinpy.UI'] = []
        self._update_list()
        self.current(0)
        self.bind_select(self._update_list)

    def _update_list(self, e=None):
        """윈도우 목록 업데이트"""
        windows = [_types.UI(hwnd) for hwnd in _win32.get_windows()]
        self._windows = [ui for ui in windows if ui.is_active]
        self['values'] = self._windows
        return

    @property
    def window_list(self) -> List['autowinpy.UI']:
        """윈도우 리스트를 출력합니다.

        Returns:
            [:class:`autowinpy.UI`] UI 리스트
        """
        return self._windows

    @property
    def window(self) -> 'autowinpy.UI':
        """현재 선택한 윈도우를 출력합니다.

        Return:
            (:class:`autowinpy.UI`) 선택중인 UI
        """
        index = self.current()
        return self.window_list[index]

    def bind_select(self, func: Callable=None):
        """함수 바인딩

        Args:
            func: 선택시 작동할 함수를 등록

        콜백함수 **func** 는 콤보 목록에서 하나를 선택하는 경우 작동합니다.
        """
        self.bind("<<ComboboxSelected>>", lambda x: func(), "+")
        return
