"""드래그

그림판을 연 상태에서 실행하면 대각선을 그리는 프로그램
"""
import autowinpy as awp
import tkinter as tk

# 그림판이라는 이름을 가진 첫 번째 창의 7번째 요소
window = awp.find_window("그림판")[0].childs()[6]

def image_update():
    """화면 표시 라벨 업데이트"""
    global label, app, window
    im_tk = awp.atk.image_tk(window.image_array(), (400, 300))
    label.configure(image=im_tk)
    label.image = im_tk
    app.after(300, image_update)

def draw_line():
    """대각선을 그리는 명령"""
    global window
    width, height = window.rect.size
    awp.win32.post_drag(window.hwnd, 30, 30, width-40, height-40)

app = tk.Tk()
app.minsize(400, 300)
# 화면 표시 라벨
label = tk.Label(app, text="view", bg="#FAA")
label.pack(side="bottom", fill="both", expand="yes")
# 대각선을 그리는 버튼
button = tk.Button(app, text="선 그리기", command=lambda: app.after(0, draw_line))
button.pack(side="top", fill="x")
# 화면 갱신 루프 시작
app.after(10, image_update)
app.mainloop()
