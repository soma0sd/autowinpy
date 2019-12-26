"""윈도우와 자식

AutoWinPy를 이용해 윈도우핸들과
자식핸들의 영역을 표시하는
tkinter GUI 프로그램
"""
import autowinpy as awp
import tkinter as tk

class app(tk.Tk):
    """Tkinter GUI 어플리케이션"""

    def __init__(self, **args):
        """GUI 초기화"""
        super().__init__(**args)
        self.minsize(600, 400)
        frame1 = tk.Frame(self)
        frame2 = tk.Frame(self)
        # autowinpy의 tk지원 사용
        self.win_combo = awp.atk.GuiSelectCombo(frame1)
        self.sub_combo = awp.atk.GuiSelectCombo(frame1, self.win_combo)
        # 이미지를 표시할 라벨
        self.win_label = tk.Label(frame2, text="view-window", background="#FAA")
        self.sub_label = tk.Label(frame2, text="view-subwindow", background="#AAF")
        self.win_combo.pack()
        self.sub_combo.pack()
        self.win_label.pack(fill="both", expand="yes")
        self.sub_label.pack(fill="both", expand="yes")
        frame1.pack(side="left", fill="y")
        frame2.pack(side="right", fill="both", expand="yes")
        # 초기화 직후 실행
        self.after(100, self.update_label)
        self.win_dsize = None
        return

    def update_label(self):
        """이미지 표시 라벨 업데이트"""
        if self.win_dsize is None:
            self.win_dsize = self.win_label.winfo_width(), self.win_label.winfo_height()
        if self.sub_combo.selected:
            # 자식 윈도우를 선택하면 작동
            try:
                sub_arr = self.sub_combo.selected.image_array()
                sub_img = awp.atk.image_tk(sub_arr, self.win_dsize)
                self.sub_label.configure(image=sub_img)
                self.sub_label.image = sub_img
            except:
                self.after(500, self.update_label)
                return
        if self.win_combo.selected is None:
            self.after(500, self.update_label)
            return
        # autowinpy의 image_tk 사용
        try:
            win_arr = self.win_combo.selected.image_array()
            win_img = awp.atk.image_tk(win_arr, self.win_dsize)
            self.win_label.configure(image=win_img)
            self.win_label.image = win_img
        finally:
            self.after(500, self.update_label)
            return

if __name__ == "__main__":
    app().mainloop()
