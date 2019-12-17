
핸들 다루기
===========

autowinpy는 핸들(HWND)을 사용해 윈도우와 해당 윈도우에 속한 요소에
접근합니다. 아래 예제는 통해 윈도우 핸들과 그 요소를 이해하는데 도움을
줄 것입니다.

.. code-block:: python

    """핸들 이해하기

    AutoWinPy를 이용해 윈도우핸들과 자식핸들의 영역을 표시하는
    tkinter GUI 프로그램입니다.
    """
    import autowinpy as awp
    import tkinter as tk

    class app(tk.Tk):
        def __init__(self, **args):
            """GUI 초기화"""
            super().__init__(**args)
            self.minsize(600, 400)
            frame1 = tk.Frame(self)
            frame2 = tk.Frame(self)
            # autowinpy의 tk지원 사용
            self.win_combo = awp.tk.tkWindowCombo(frame1)
            self.sub_combo = awp.tk.tkChildCombo(frame1, self.win_combo)
            # 이미지를 표시할 라벨
            self.win_label = tk.Label(frame2, text="view-window", background="#FAA")
            self.sub_label = tk.Label(frame2, text="view-subwindow", background="#AAF")
            self.win_combo.pack()
            self.sub_combo.pack()
            self.win_label.pack(fill="both", expand="yes")
            self.sub_label.pack(fill="both", expand="yes")
            frame1.pack(side="left", fill="y")
            frame2.pack(side="right", fill="both", expand="yes")
            # 0.5초마다 자동으로 업데이트
            self.after(500, self.update_label)
            self.win_dsize = None
            return

        def update_label(self):
            """이미지 표시 라벨 업데이트"""
            if self.win_dsize is None:
                self.win_dsize = self.win_label.winfo_width(), self.win_label.winfo_height()
            if self.sub_combo.window:
                # 자식 윈도우를 선택하면 작동
                sub_arr = self.sub_combo.window.screen_array
                sub_img = awp.tk.tk_image(sub_arr, self.win_dsize)
                self.sub_label.configure(image=sub_img)
                self.sub_label.image = sub_img
            win_arr = self.win_combo.window.screen_array
            # autowinpy의 tk_image 사용
            win_img = awp.tk.tk_image(win_arr, self.win_dsize)
            self.win_label.configure(image=win_img)
            self.win_label.image = win_img
            # 다음 0.5초 뒤에 실행
            self.after(500, self.update_label)
            return

    if __name__ == "__main__":
        app().mainloop()
