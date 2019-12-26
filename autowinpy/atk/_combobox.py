"""tkinter 지원: 윈도우 선택기와 자식 선택기"""
from tkinter import ttk
from ..core import Gui, window_list
from typing import List, Callable


class GuiSelectCombo(ttk.Combobox):
    """tkinter를 위한 Gui 선택 콤보박스

    이 클래스는 `tkinter.ttk.Combobox`_ 를 상속합니다.

    Args:
        master: 상위 Tkinter 요소
        window_combo: 상위 ``GuiSelectCombo``를 매개변수로 입력하면,
            이 클래스는 자식 선택 콤보박스로 동작합니다.
        **kw: Tkinter 위젯 설정

    .. _tkinter.ttk.Combobox:
        https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_combobox.htm
    """

    __module__ = "autowinpy.atk"

    def __init__(self, master=None, window_combo:'GuiSelectCombo' =None, **kw):
        """초기화"""
        super().__init__(master=master, **kw)
        self._parent = window_combo
        self._gui_list: List[Gui] = []
        self._list_update()
        self.bind_selected(self._list_update)
        if not window_combo is None:
            self._parent.bind_selected(self._list_update)
    
    def _list_update(self, e=None):
        """Gui 목록 업데이트"""
        if self._parent is None:
            self._gui_list = window_list()
        elif not self._parent.selected is None:
            self._gui_list = self._parent.selected.childs()
        self['values'] = self._gui_list

    @property
    def selected(self) -> Gui:
        """선택한 Gui"""
        index = self.current()
        if index < 0:
            return None
        else:
            return self._gui_list[index]

    def bind_selected(self, func: Callable):
        """선택 이벤트에 함수 바인딩"""
        self.bind("<<ComboboxSelected>>", lambda x: func(), "+")
