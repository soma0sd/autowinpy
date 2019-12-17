# Setup autowinpy
from setuptools import setup, find_packages
import autowinpy


## CMD: create wheel
# python setup.py bdist_wheel
## CMD: upload to pypi
# twine upload dist/{}
with open('readme.md', encoding='utf8') as f:
    description = f.read()

setup(
    name             = "autowinpy",
    # FIXME: Synchronization Package Version / Download url Version
    download_url     = 'https://github.com/soma0sd/autowinpy/archive/0.3.1.tar.gz',
    version          = '0.3.1',
    packages         = find_packages(exclude = ['docs', '.vscode']),
    description      = 'Foreground automation support for Windows OS',
    long_description = description,
    long_description_content_type='text/markdown',
    author           = 'soma0sd',
    author_email     = 'soma0sd@gmail.com',
    url              = 'https://github.com/soma0sd/autowinpy',
    install_requires = [
        "pywin32",
        "opencv-python",
        "numpy",
        "Pillow"
    ],
    keywords         = ['windows', 'automation', 'macro'],
    python_requires  = '>=3',
    package_data     =  {},
    zip_safe         = False,
    license          = 'MIT',
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
