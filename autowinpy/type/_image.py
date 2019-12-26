"""이미지 타입 클래스
"""
import numpy
import cv2

class ImageError(Exception):
    """이미지 오류 처리"""

    def __init__(self, message: str):
        """초기화"""
        self.message: str = message

    def __str__(self) -> str:
        """메시지 전달"""
        return self.message

class Image(numpy.ndarray):
    """AutoWinPy의 이미지 클래스

    NumPy의 ndarray를 상속합니다.

    Property:
        +--------------+--------------+----------------+
        | 이름         | 타입         | 내용           |
        +==============+==============+================+
        | width        | ``int``      | 이미지 너비    |
        +--------------+--------------+----------------+
        | height       | ``int``      | 이미지 높이    |
        +--------------+--------------+----------------+
        | len_channels | ``int``      | 이미지 채널 수 |
        +--------------+--------------+----------------+
        | grayscale    | `type.Image` | 회색조 이미지  |
        +--------------+--------------+----------------+
    """

    __module__ = 'autowinpy.type'

    def __new__(cls, n):
        """초기화"""
        return n.view(cls)

    @property
    def width(self) -> int:
        """너비"""
        return self.shape[1]
    
    @property
    def height(self) -> int:
        """높이"""
        return self.shape[0]

    @property
    def len_channels(self) -> int:
        """이미지 채널 수

        Returns:
            ``0`` 회색조,
            ``3`` RGB or BGR,
            ``4`` sRGB
        """
        if len(self.shape) < 3:
            return 0
        else:
            return self.shape[2]

    @property
    def grayscale(self) -> 'Image':
        """회색조 이미지를 출력합니다."""
        return Image(cv2.cvtColor(self, cv2.COLOR_RGB2GRAY))

    def size(self, width: int=None, height: int=None):
        """너비, 높이 변경 및 출력

        Args:
            width: 변경할 너비
            height: 변경할 높이
        
        Returns:
            ``Image`` 높이나 너비를 설정하면 비율은 유지한 채로 이미지의
            크기를 변경. 둘 다 설정하면 사이즈를 변경한 복제
            이미지를 출력.
            ``(int, int)`` 비어있는 경우 현재의 너비와 높이를 출력
        """
        _w, _h = self.width, self.height
        if width is None and height is None:
            return self.width, self.height
        elif height is None:
            height = int(width  * _h / _w)
        elif width is None:
            width  = int(height * _w / _h)
        method = cv2.INTER_AREA if _w > width else cv2.INTER_LINEAR
        return Image(cv2.resize(self, (width, height), interpolation=method))
    
    def channel(self, n: int) -> 'Image':
        """단일채널 이미지 출력
        
        Args:
            n: 채널은 0부터 시작합니다.
                sRGB의 경우 투명도 채널은 3
        """
        if self.len_channels < n or n < 0 :
            raise ImageError(
                "{} 채널이 존재하지 않습니다. 이미지 채널 수: {}".format(
                    n, self.len_channels))
        return Image(self[:,:,n])

    def convert(self, mode) -> 'Image':
        return Image(cv2.cvtColor(self, mode))
