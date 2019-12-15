"""

tkinter는 쉽게 사용할 수 있는 GUI 패키지입니다.
"""
from PIL import Image, ImageTk
from typing import Tuple
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
