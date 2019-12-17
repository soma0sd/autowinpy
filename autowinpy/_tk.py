"""

내장 GUI 패키지인 Tkinter와 AutoWinPy를 사용하는 경우
**autowinpy.tk** 모듈의 함수와 클래스를 사용할 수 있습니다.

Example:
    윈도우를 선택하면 윈도우의 스크린샷을 라벨에 표시하는
    스크립트.

.. code-block:: python

    import autowinpy as awp
    import tkinter as tk

    def select_gui():
        # 윈도우 선택시 실행할 함수
        global combo, label
        window: awp.Gui = combo.window
        im_ar = window.screen_array
        dsize = int(im_ar.shape[1] * 0.5), int(im_ar.shape[0] * 0.5)
        im_tk = awp.tk.tk_image(im_ar, dsize)
        label.configure(image=im_tk)
        label.image = im_tk
        print("윈도우 선택: {}".format(window))
        return

    app = tk.Tk()
    combo = awp.tk.tkWindowCombo(app)
    combo.bind_select(select_gui)
    label = tk.Label(app, text="screen")
    label.pack()
    combo.pack()
    app.mainloop()
.. code-block


Example:
    윈도우 선택 후, 컨트롤을 선택하면 컨트롤의 스크린샷을 라벨에 전달.

.. code-block:: python

    import autowinpy as awp
    import tkinter as tk

    def select_gui():
        # 윈도우 선택시 실행할 함수
        global combo_sub, label
        window: awp.Gui = combo_sub.window
        im_ar = window.screen_array
        dsize = int(im_ar.shape[1] * 0.5), int(im_ar.shape[0] * 0.5)
        im_tk = awp.tk.tk_image(im_ar, dsize)
        label.configure(image=im_tk)
        label.image = im_tk
        print("윈도우 선택: {}".format(window))
        return

    app = tk.Tk()
    combo_win = awp.tk.tkWindowCombo(app)
    combo_sub = awp.tk.tkChildCombo(app, combo_win)
    combo_sub.bind_select(select_gui)
    label = tk.Label(app, text="screen")
    label.pack()
    combo_win.pack()
    combo_sub.pack()
    app.mainloop()
.. code-block

"""
from . import _win32

from typing import Tuple, Callable, List
from PIL import Image, ImageTk
from tkinter import ttk
import numpy
import cv2

try:
    from autowinpy import Gui
except ImportError:
    from .__init__ import Gui



def tk_image(image: numpy.ndarray, dsize: Tuple[int, int]=None, mode="fit") -> 'PIL.ImageTk':
    """OpenCV 이미지를 Tk 이미지로 변환.

    Args:
        image (`opencv.mat`): OpenCV용 이미지요소.
        dsize (`(width, height)`): [옵션] 변환할 사이즈.
        mode: [옵션] dsize를 지정한 경우, 채우기 모드를 선택합니다.\
            `"fill"` 은 dsize를 가득 채웁니다.\
            `"fit"` 은 원본의 가로세로 비율을 유지한 상태로 dsize를 채웁니다.

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
        if mode == "fit":
            # width / height
            img_r = cv_img.shape[1] / cv_img.shape[0]
            dsi_r = dsize[0] / dsize[1]
            if img_r < dsi_r:
                dsize = int(dsize[1]*img_r), dsize[1]
            else:
                dsize = dsize[0], int(dsize[0]/img_r)
        elif mode == "fill":
            pass
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
        **kw: 속성 (TK레퍼런스_ 참조)

    tkinter GUI에서 사용할 수 있는 윈도우선택 콤보박스
    입니다. tkinter.ttk.Combobox_ 를 상속합니다.

    .. _tkinter.ttk.Combobox: https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_combobox.htm

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
        """윈도우 선택 콤보박스

        Args:
            master: 상위 위젯
            **kw: 속성 (TK레퍼런스_ 참조)

        tkinter GUI에서 사용할 수 있는 윈도우선택 콤보박스
        입니다. tkinter.ttk.Combobox_ 를 상속합니다.

        .. _tkinter.ttk.Combobox: https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_combobox.htm
        """
        super().__init__(master=master, **kw)
        self._windows: List[Gui] = []
        self._update_list()
        self.current(0)
        self.bind_select(self._update_list)

    def _update_list(self, e=None):
        """윈도우 목록 업데이트"""
        windows = [Gui(hwnd) for hwnd in _win32.get_windows()]
        self._windows = [ui for ui in windows if ui.is_active]
        self['values'] = self._windows
        return

    @property
    def window_list(self) -> List[Gui]:
        """윈도우 리스트를 출력합니다.

        Returns:
            ([:class:`autowinpy.Gui`]) Gui 리스트
        """
        return self._windows

    @property
    def window(self) -> Gui:
        """현재 선택한 윈도우를 출력합니다.

        Return:
            (:class:`autowinpy.Gui`) 선택중인 Gui
        """
        index = self.current()
        return self.window_list[index]

    @property
    def screen(self) -> numpy.ndarray:
        """현재 선택한 윈도우의 스크린을 반환.

        Return:
            (`numpy.ndarray`) 선택한 윈도우의 이미지
        """
        return self.window.screen_array

    def bind_select(self, func: Callable=None):
        """함수 바인딩

        Args:
            func: 선택시 콜백

        콜백함수 **func** 는 콤보 목록에서 하나를 선택하는 경우 작동합니다.
        """
        self.bind("<<ComboboxSelected>>", lambda x: func(), "+")
        return


class tkChildCombo(ttk.Combobox):
    """ttk 자식 선택 콤보박스.

    Args:
        master: 상위 위젯
        win_combo: 윈도우 선택 콤보박스
        **kw: 속성 (TK레퍼런스_ 참조)

    tkinter GUI에서 :class:`autowinpy.tk.tkWindowCombo` 와 함께 사용할 수
    있는 자식선택 콤보박스 입니다.
    """

    def __init__(self, master=None, win_combo=None, **kw):
        """ttk 자식 선택 콤보박스.

        Args:
            master: 상위 위젯
            win_combo: 윈도우 선택 콤보박스
            **kw: 속성 (TK레퍼런스_ 참조)

        tkinter GUI에서 :class:`autowinpy.tk.tkWindowCombo`와 함께 사용할 수
        있는 자식선택 콤보박스 입니다.
        """
        super().__init__(master=master, **kw)
        if win_combo is None:
            raise TypeError("[win_combo] 윈도우 선택 콤보박스를 등록해야 합니다.")
        self._windows: List[Gui] = []
        self._win_combo: tkWindowCombo = win_combo
        self._win_combo.bind_select(self._window_combo_select)
    
    def _window_combo_select(self):
        self._windows = self._win_combo.window.childs
        self['values'] = self._windows
        self.set('')
        return

    @property
    def window(self) -> Gui:
        """현재 선택한 윈도우를 출력합니다.
        윈도우를 선택하지 않은 경우, None을 반환합니다.

        Return:
            (:class:`autowinpy.Gui`) 선택중인 Gui
        """
        if self.current() < 0:
            return None
        else:
            index = self.current()
            return self.window_list[index]
    
    @property
    def window_list(self) -> List[Gui]:
        """윈도우 리스트를 출력합니다.

        Returns:
            ([:class:`autowinpy.Gui`]) Gui 리스트
        """
        return self._windows
    
    def bind_select(self, func=None):
        """함수 바인딩

        Args:
            func: 선택시 콜백

        콜백함수 **func** 는 콤보 목록에서 하나를 선택하는 경우 작동합니다.
        """
        self.bind("<<ComboboxSelected>>", lambda x: func(), "+")
        return
