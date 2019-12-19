"""클래스"""
from . import _win32
from typing import List, Tuple
import os
import numpy as np
import cv2

class Gui(object):
    """윈도우와 컨트롤을 핸들링하기 위한 클래스.

    Args:
        hwnd(int): 윈도우 핸들.
        [옵션]parent(:class:`Gul` or `HWND`): 부모 Gui 혹은 핸들

    **gui클래스** 는 윈도우가 비활성 상태일 때도 캡쳐나
    클릭 등을 수행하기 위한 클래스입니다.
    :func:`win32.get_windows` 는 현재 실행중인 윈도우와
    컨트롤로부터 Gui 개체를 만드는 손쉬운 방법을 제공합니다.


    **parent** 매개변수는 Gui가 특정 윈도우의 컨트롤인
    경우에 사용합니다. 윈도우에서 컨트롤의 상대적인 위치
    등을 계산하기 위해 필요합니다.
    """

    def __init__(self, hwnd, parent=None):
        """Window 초기화."""
        super().__init__()
        self._hwnd = hwnd
        if parent is None:
            self._parent = None
        elif isinstance(parent, type(self)):
            self._parent = parent
        elif isinstance(parent, int):
            self._parent = Gui(parent)
        else:
            raise TypeError("parent 매개변수는 int 혹은 Gui 클래스 입니다.")
        return

    def __str__(self):
        """print."""
        return "{}".format(self.name)

    def __repr__(self):
        """."""
        return "({}){}".format(self.hwnd, self.name)

    @property
    def hwnd(self) -> int:
        """핸들 출력.

        :returns: (`int`) 윈도우의 고유 핸들 
        """
        return self._hwnd

    @property
    def name(self) -> str:
        """이름.

        :returns: (`str`) 현재 윈도우가 가지고 있는 문자열
        """
        return _win32.get_window_text(self.hwnd)

    @property
    def parent(self) -> 'autowinpy.Gui':
        """부모 Gui.

        Return:
        (:class:`autowinpy.Gui`) 부모가 있는 경우 부모 Gui를 반환.

        (`None`) 부모가 없는 경우.
        """
        return self._parent

    @property
    def rect(self) -> Tuple[int, int, int, int]:
        """윈도우 영역.

        Return:
        (`left, top, right, bottom`) 윈도우 영역의 좌표.
        부모가 있는 경우에는 부모를 기준으로 하는 상대좌표.

        자세한 내용은 :func:`win32.get_window_rect` 참조.
        """
        if self.is_child:
            return _win32.get_window_rect(self.hwnd, self.parent.hwnd)
        else:
            return _win32.get_window_rect(self.hwnd)

    @property
    def size(self) -> Tuple[int, int]:
        """윈도우 크기.

        :returns: (`width, height`) 윈도우의 폭과 높이.
        """
        x0, y0, x1, y1 = self.rect
        return x1 - x0, y1 - y0

    @property
    def is_active(self) -> bool:
        """제어 가능 여부.

        :returns: (`bool`) 패키지로 제어할 수 있는 요소인지 확인합니다.
        """
        return _win32.is_active_window(self.hwnd)

    @property
    def is_child(self) -> bool:
        """부모 존재 확인.

        :returns: (`bool`) 부모가 있는 UI인지 확인합니다.
        """
        return False if self._parent is None else True

    @property
    def childs(self) -> List['Gui']:
        """자식 목록.

        :returns: ([:class:`autowinpy.Gui`]) 자식 윈도우/컨트롤 목록.
        """
        handles = _win32.get_child_windows(self.hwnd)
        out: List[Gui] = [Gui(i, self) for i in handles]
        return [ui for ui in out]

    @property
    def screen_array(self) -> np.ndarray:
        """스크린 캡쳐.

        Returns:
        (`opencv.mat`)윈도우 스크린샷 이미지.

        자세한 내용은 :func:`win32.get_window_view_array` 참조.
        """
        image = _win32.get_window_screen_array(self.hwnd)
        return image

class Template(object):
    """템플릿 클래스.

    Args:
        path(`str`): 템플릿 파일의 경로
        args(`key=value`): 템플릿 속성
    
    탬플릿(Template)은 조각그림을 담고 있는 클래스입니다.

    **args**
    
    * "use_mask" (`Bool`: `True`): 해당 탬플릿에 마스크를 사용할지\
        결정합니다.
    * "matched_width", "matched_height" (`int`: `None`): 탬플릿의\
        매칭 너비나 높이를 지정하면 원본 크기가 아닌 지정한 크기로\
        이미지 서칭을 수행합니다. 둘 중 하나만 지정해도 자동으로 비율에\
        맞게 확대/축소됩니다.
    * "threshold" (`float`: `0.8`): 템플릿 유무를 판단할 문턱값입니다.\
        낮을수록 정확도가 떨어집니다.
    * "screen_area" (`[int, int, int, int]`: `[0, 0, 100, 100]`):\
        스크린에서 매칭할 영역을 %값으로 지정합니다. 
    
    """

    def __init__(self, path: str=None, **args):
        """autowinpy.Template"""
        super().__init__()
        ## init variables
        self._path = path
        self._name = os.path.basename(path)
        self._image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self._use_mask = args.get("use_mask", True)
        self._matched_width = args.get("matched_width", None)
        self._matched_height = args.get("matched_height", None)
        self._threshold = args.get("threshold", 0.8)
        self._screen_area = args.get("screen_area", [0,0,100,100])
        ## variables configure
        # mask
        def mask_function(value):
            return 0 if value < 2 else 255
        gen_mask = np.vectorize(mask_function, otypes=[np.uint8])
        self.mask = gen_mask(self._image)

        
    def __str__(self): return self._name

    @property
    def configure(self) -> dict:
        """(`Dict`)현재 설정을 반환합니다."""
        return {
            "path": self._path,
            "matched_width": self._matched_width,
            "matched_height": self._matched_height,
            "threshold": self._threshold,
            "screen_area": self._screen_area
        }

    def image_search(self, screen: np.ndarray, mode="pos", **options):
        """스크린에 템플릿이 있는지 확인합니다.

        Args:
            screen(`opencv.mat`): 이미지를 찾을 이미지 행렬입니다.
            mode(기본값: "pos"): 출력 정보를 결정합니다.
                여러 속성을 함꺼번에 줄 수 있습니다.
            options(`key=value`): 이번 매칭 한정으로 탬플릿 속성을 변경하고자\
                할 때 사용합니다. 가능한 옵션: use_mask, matched_width, matched_height,\
                threshold, screen_area
        
        Returns:
            다중출력시 아래의 순서대로 출력합니다.

            * [mode: "exist"]: 이미지가 존재하는지 확인합니다.\
                매칭값이 문턱값(threshold)을 넘는 경우 True를 반환합니다.
            * [mode: "pos"]: 찾아낸 이미지의 상대적인 위치를 출력합니다.\
                `(x0, y0), (x1, y1)` 형태로 출력하며 각각 왼쪽 상단 모서리와 \
                오른쪽 하단 모서리의 좌표입니다.
            * [mode: "rect"]: 찾아낸 영역을 표시한 새로운 screen 요소를\
                반환합니다.
            
        ``mode="pos"+"exist"`` 나 ``mode="rect"+"exist"`` 와 같은 혼합속성도
        가능합니다. 단, 출력하는 순서는 입력한 모드의 순서가 아닌 위의 목록 순서를
        따릅니다. 가령 ``mode="pos"+"exist"`` 을 매개변수로 하더라도 출력 결과는
        ``True, (x0, y0), (x1, y1)`` 과 같은 형태가 됩니다.

        """
        if len(screen.shape) > 2:
            screen_mat = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        ## init parameters
        area: Tuple = options.get("screen_area", self._screen_area)
        tpl_w: int = options.get("matched_width", self._matched_width)
        tpl_h: int = options.get("matched_height", self._matched_height)
        threshold: float = options.get("threshold", self._threshold)
        use_mask: bool = options.get("use_mask", self._use_mask)
        # matched size configure
        _im_h, _im_w = self.image.shape[:2]
        if tpl_w and tpl_h is None:
            tpl_h = int(tpl_w * _im_h / _im_w)
        elif tpl_h and tpl_w is None:
            tpl_w = int(tpl_h * _im_w / _im_h)
        elif tpl_h is None and tpl_w is None:
            tpl_w, tpl_w = _im_w, _im_h
        _method = cv2.INTER_AREA if _im_w < tpl_w else cv2.INTER_LINEAR
        tpl_img = cv2.resize(self._image, (tpl_w, tpl_h), interpolation=_method)
        tpl_mask = cv2.resize(self.mask, (tpl_w, tpl_h), interpolation=_method)
        tpl_mask = tpl_mask if use_mask else None
        del _im_h, _im_w, _method
        # match area
        scr_h, scr_w = screen_mat.shape[:2]
        area = (
            int(area[0] * scr_w / 100),
            int(area[1] * scr_w / 100),
            int(area[2] * scr_h / 100),
            int(area[3] * scr_h / 100)
        )
        scr_mat = screen_mat[area[2]:area[3], area[0]:area[1]]
        _method = cv2.TM_CCORR_NORMED if use_mask else cv2.TM_CCOEFF_NORMED
        match_data = cv2.matchTemplate(scr_mat, tpl_img, _method, mask=tpl_mask)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(match_data)
        output = []
        if "exist" in mode:
            output.append(False if maxVal < threshold else True)
        if "pos" in mode:
            maxLocF = maxLoc[0]+tpl_w, maxLoc[1]+tpl_h
            output.append((maxLoc, maxLocF))
        if "rect" in mode:
            image = cv2.rectangle(screen, maxLoc, maxLocF, (0, 0, 255), 2)
            image = cv2.putText(image, self._name, maxLoc, cv2.CV_FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            output.append(image)
        return tuple(output)
