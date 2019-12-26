"""tkinter를 위한 변환, 생성 함수"""
from ..type import Image
from PIL import Image as pil_Image
from PIL import ImageTk as pil_ImageTk
from typing import Tuple
import cv2

def image_tk(image: Image, dsize:Tuple[int, int]=None, fill:bool=False) -> 'ImageTk':
    """autowinpy의 이미지를 tkinter 이미지로 변환

    Args:
        image: 변환할 이미지
        dsize: [옵션] 기본값 ``None``
        fill: [옵션] 기본값 ``False``

    Returns:
        tkinter 이미지
    """
    image = image.convert(cv2.COLOR_BGR2RGB)
    if fill is True and not dsize is None:
        # fill image
        image = image.size(*dsize)
    elif fill is False and not dsize is None:
        # fit image
        img_w, img_h = image.size()
        lab_w, lab_h = dsize
        aspect_ratio_image = img_w / img_h
        aspect_ratio_label = lab_w / lab_h
        if aspect_ratio_image >= aspect_ratio_label:
            # image more flat than label
            image = image.size(width=lab_w)
        else:
            # image more elongate than label
            image = image.size(height=lab_h)
    pil_image = pil_Image.fromarray(image)
    return pil_ImageTk.PhotoImage(pil_image)
