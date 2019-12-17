# AutoWinPy
[![PyPI](https://img.shields.io/pypi/v/autowinpy)](#)
[![license](https://img.shields.io/github/license/soma0sd/autowinpy)](#)
[![Pre-Release Date](https://img.shields.io/github/release-date-pre/soma0sd/autowinpy)](#)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/autowinpy)](#)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/autowinpy)](#)


[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/autowinpy)](#)
[![platform: windows](https://img.shields.io/badge/windows-10%20%7C%208.1%20%7C%207-3399ee)](#)

* 사용자매뉴얼: https://soma0sd.github.io/autowinpy/
* PyPI: https://pypi.org/project/autowinpy/

윈도우 앱의 자동화를 편리하게 만들어주는 패키지입니다.

다음 환경에서 제작되었습니다.

> Windows 10 (1909) 64비트
>
> Python 3.8 64비트 - Anaconda 배포판

아마도 이런 환경까지는 제대로 작동할 듯 합니다.

> Windows 7, 8.1, 10
>
> Python 3.4 이상

패키지는 현재 개발중이며, 네이밍 규칙을 언제든 변경할 수 있으므로
현재는 패키지를 사용하기보단 필요한 함수만 골라 임시로 활용하시는
것을 추천합니다.

## 0.3 업데이트

* (`0.3.1`) tk 지원함수 수정, 코어함수 추가 
* Template 클래스 추가: 이미지 서칭 지원

## 0.2 업데이트

* Tkinter GUI 지원기능 추가
* 클래스 이름 변경: `autowinpy.UI` -> `autowinpy.Gui`
* Gui 클래스의 parent는 윈도우 핸들도 매개변수로 받습니다.
* (:hammer:Fix) 윈도우 네이티브 앱 캡쳐시 검은 화면만 나오는 문제
