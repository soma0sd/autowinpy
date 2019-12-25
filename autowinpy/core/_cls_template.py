"""템플릿 클래스
"""
from ..type import Image, Rect
from typing import List, Tuple
import cv2
import numpy

class TemplateError(Exception):
    """템플릿 오류 처리"""

    def __init__(self, message: str):
        """초기화"""
        self.message: str = message

    def __str__(self) -> str:
        """메시지 전달"""
        return self.message


class Template:
    """이미지 서칭을 위한 탬플릿 클래스

    Keyword Args:
        path (str): 파일 경로
        matched_width (int): 이미지 서칭에 사용할 너비, 기본값 ``None``
        matched_height (int): 이미지 서칭에 사용할 높이, 기본값 ``None``
        threshold (float): 이미지 서치 성공을 판단할 문턱값, 기본값 ``0.8``
        screen_area ([int, int, int, int]):
            스크린 매칭 영역, 기본값 ``[0, 0, 100, 100]``

    Todo:
        [새로운 키워드] ``mask_color``: 특정 색상을 마스크 키로 사용
    """
    
    __module__ = 'autowinpy'

    def __init__(self, **args):
        """탬플릿 초기화"""
        self._path:str = args.get("path", None)
        self._matched_width:int = args.get("matched_width", None)
        self._matched_height:int = args.get("matched_height", None)
        self._threshold:float = args.get("threshold", 0.8)
        self._screen_area:List[int, int, int, int] = args.get("screen_area", [0,0,100,100])
        self._image: Image = Image(cv2.imread(self._path, cv2.IMREAD_UNCHANGED))
        # variables validation
        _w, _h = self._image.size()
        if self._path is None:
            raise TemplateError("필수 인수가 없습니다. path")
        if _h < 20 or _w < 20:
            raise TemplateError("템플릿 이미지의 크기가 너무 작습니다")
        if self._threshold > 1 or self._threshold < 0:
            raise TemplateError("문턱값은 0에서 1사이입니다.")
        if min(self._screen_area) < 0 or max(self._screen_area) > 100:
            raise TemplateError("스크린 영역은 0(%)에서 100(%)사이 값을 가집니다.")
        # variables override
        if self._matched_width and self._matched_height is None:
            self._matched_height = int(self._matched_width * _w / _h)
        if self._matched_height and self._matched_width is None:
            self._matched_width = int(self._matched_height * _h / _w)

    @property
    def origin_image(self) -> Image:
        """원본 이미지 출력"""
        return self._image
    
    @property
    def match_size(self) -> Tuple[int, int]:
        """매칭 사이즈 출력"""
        return self._matched_width, self._matched_height

    def configure(self, **args) -> dict:
        """현재 설정을 변경하거나 출력합니다.

        Keyword Args:
            matched_width (int): 이미지 서칭에 사용할 너비
            matched_height (int): 이미지 서칭에 사용할 높이
            threshold (float): 이미지 서치 성공을 판단할 문턱값
            screen_area ([int, int, int, int]): 스크린 매칭 영역

        Returns:
            (dict) 현재 설정
        """
        _matched_width:int = args.get("matched_width", self._matched_width)
        _matched_height:int = args.get("matched_height", self._matched_height)
        _threshold:float = args.get("threshold", self._threshold)
        _screen_area:List[int, int, int, int] = args.get("screen_area", self._screen_area)
        if _threshold > 1 or _threshold < 0:
            raise TemplateError("문턱값은 0에서 1사이입니다.")
        if min(_screen_area) < 0 or max(_screen_area) > 100:
            raise TemplateError("스크린 영역은 0(%)에서 100(%)사이 값을 가집니다.")
        self._matched_width = _matched_width
        self._matched_height = _matched_height
        self._threshold = _threshold
        self._screen_area = _screen_area
        return {
            "path": self._path,
            "matched_width": self._matched_width,
            "matched_height": self._matched_height,
            "threshold": self._threshold,
            "screen_area": self._screen_area
        }

    def mask(self, dsize: Tuple[int, int]=None) -> Image:
        """마스크 이미지 출력

        Args:
            dsize (width, height): [선택] 출력할 마스크의 너비와 높이

        Returns:
            마스크 이미지, 이미지에 투명 채널이 없는 경우 ``None``
        """
        if self._image.len_channels < 3:
            return None  # is grayscale
        mask_function = numpy.vectorize(
            lambda x: 0 if x < 255 else 255, otypes=[numpy.uint8])
        transparent_channel = self._image.channel(3)
        mask = mask_function(transparent_channel)
        if dsize is None:
            return mask
        dw, iw = dsize[0], self._image.width
        method = cv2.INTER_AREA if dw < iw else cv2.INTER_LINEAR
        mask = cv2.resize(mask, dsize, interpolation=method)
        return mask

    def screen_search(self, screen: Image) -> Tuple[bool, Rect]:
        """스크린에서 탬플릿을 찾습니다

        Args:
            screen: 탬플릿을 탐색할 이미지
        
        Returns:
            (``bool``) 탐색 성공 여부,
            (:class:`type.Rect`) 탐색 결과 영역
        """
        screen_gray: Image = screen.grayscale
        template_gray: Image = self._image.grayscale
        use_mask: bool = False
        mask: Image = self.mask(self.match_size)
        if not self._matched_width is None:
            template_gray.size()
        if None and not mask is None:
            use_mask = True
        if not self._matched_width is None and not mask is None:
            mask.size(self._matched_width, self._matched_height)
        method = cv2.TM_CCORR_NORMED if use_mask else cv2.TM_CCOEFF_NORMED
        match_data = cv2.matchTemplate(screen_gray, template_gray, method, mask=mask)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(match_data)
        loc = Rect().xywh(*maxLoc, *self.match_size)
        if maxVal > self._threshold:
            return True, loc
        else:
            return False, loc
