.. autowinpy documentation master file, created by
   sphinx-quickstart on Fri Dec 13 11:22:42 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AutoWinPy 사용자매뉴얼
=======================

.. image:: https://img.shields.io/github/license/soma0sd/autowinpy
  :alt: License
.. image:: https://img.shields.io/pypi/v/autowinpy?label=Release
  :alt: Release


.. image:: https://img.shields.io/badge/Windows-10%20%7C%208.1%20%7C%207-brightgreen
  :alt: Windows Version - 10, 8.1, 7
.. image:: https://img.shields.io/pypi/pyversions/autowinpy
  :alt: Python Version


AutoWinPy는 윈도우 OS에서 작동하는 앱을 자동으로 제어할 수 있는


주요 기능
---------

* 활성/비활성 윈도우의 상태를 제어합니다.
* 활성/비활성 윈도우의 상태를 출력합니다.
* 활성/비활성 윈도우의 스크린샷을 가져옵니다.
* 활성/비활성 윈도우에 클릭이나 키 입력 등의 명령을 보냅니다.

.. toctree::
   :maxdepth: 2
   :caption: 문서 목록:

   overview
   reference

종속성
------

* `pywin32 <https://github.com/mhammond/pywin32>`_
* `OpenCV <https://opencv.org/>`_
* `NumPy <https://numpy.org/>`_
* `Pillow <https://python-pillow.org/>`_

**pywin32**
활성/비활성상태의 윈도우를 제어하거나 알고 있는 윈도우 내부
좌표를 클릭하고, 컨트롤에 키 입력을 보내는 등의 작업에 사용합니다.

**OpenCV**
템플릿의 유무를 판단하거나 위치를 파악하고자 할 때 사용합니다.

**NumPy**
탬플릿 마스크를 작성하거나 각종 연산에 활용합니다.

**Pillow**
윈도우 캡쳐나 OpenCV연산 결과를 GUI에 표시하기 위한 함수에
쓰입니다.


알려진 문제
-----------

**Windows 8.1 이상의 HIDPI 지원**

Windows 8.1이상에서 패키지를 사용하면 초기화 도중 프로세스를
HIDPI지원 상태로 바꿉니다. 이것으로 인해 자동화 프로그램을 GUI로
구현하는 경우, 결과물이 생각보다 작아질 것입니다.


아래의 스크립트를 통해 변화한 배율을 확인할 수 있습니다.

.. code-block:: python

  import autowinpy as awp
  print(awp.__dpi_scale_factor__)

.. code-block

패키지를 사용하지 않았을 때의 값은 `1` 이며, 패키지를 사용했을 때
원래 크기에서 50% 줄어들었다면 출력값은 `2` 가 될 것입니다.


이것은 윈도우와 컨트롤의 위치를 정확하게 파악하기 위한 필수
작업 중 생기는 일이므로 임의로 HIDPI지원을 끈다면 패키지가
정상적으로 동작하지 않습니다.

업데이트
---------

* **0.1.0** : 이제 PyPI를 통해 설치할 수 있습니다.


추가할 기능
------------

* **0.2.0** : Tkinter GUI 지원
* **0.2.0** : OpenCV 기반 이미지서칭 지원
