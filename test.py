"""

"""
from ctypes import windll
import autowinpy as awp
import tkinter as tk
import cv2

def view_update():
  global com1, lab1
  window = com1.window
  im_cv = window.screen_array
  im_cv = cv2.resize(im_cv, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
  im_tk = awp.tk.tk_image(im_cv)
  lab1.configure(image=im_tk)
  lab1.image = im_tk
  return

app = tk.Tk()
com1 = awp.tk.tkWindowCombo(app)
com1.bind_select(view_update)
com1.pack()
lab1 = tk.Label(app, text="viewer")
lab1.pack()
app.mainloop()
