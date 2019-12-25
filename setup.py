# Setup autowinpy
from setuptools import setup, find_packages
import autowinpy

VERSION = autowinpy.__version__
## CMD: create wheel
# python setup.py bdist_wheel
## CMD: upload to pypi
# twine upload dist/{}
def file_read(path: str) -> str:
    with open(path, encoding='utf8') as f:
        description = f.read()
        return description

setup(
    name             = "autowinpy",
    # FIXME: Synchronization Package Version / Download url Version
    download_url     = 'https://github.com/soma0sd/autowinpy/archive/{}.tar.gz'.format(VERSION),
    version          = VERSION,
    packages         = find_packages(exclude=['docs', '.vscode', 'tutorial']),
    description      = 'Foreground automation support for Windows OS',
    long_description = file_read('readme.md'),
    long_description_content_type='text/markdown',
    author           = 'soma0sd',
    author_email     = 'soma0sd@gmail.com',
    url              = 'https://github.com/soma0sd/autowinpy',
    project_urls     = {
        "AutoWinPy documentation": "https://soma0sd.github.io/autowinpy/",
        "AutoWinPy source": "https://github.com/soma0sd/autowinpy",
    },
    install_requires = [
        "pywin32",
        "opencv-python",
        "numpy",
        "Pillow"
    ],
    keywords         = ['windows', 'automation', 'macro'],
    python_requires  = '>=3.4',
    package_data     =  {},
    license          = "MIT",
    license_file     = 'LICENSE',
    classifiers      = [
        'Natural Language :: Korean',
        'Operating System :: Microsoft :: Windows',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
