#!/usr/bin/env python
# encoding: utf8
###############################################################################
#
#    MIT License
#
#    Copyright (c) 2021 PinchofLogic
#    Copyright (C) 2021 NaN Projectes de Programari Lliure, S.L.
#                            http://www.NaN-tic.com
#
#    Permission is hereby granted, free of charge, to any person obtaining a
#    copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THES SOFTWARE.
###############################################################################


from setuptools import setup, find_packages
from pharma_datamatrix.version import PACKAGE, VERSION, LICENSE, WEBSITE
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name=PACKAGE,
    version=VERSION,
    description='Python module to validate Pharma QR and datamatrix',
    long_description=read('README'),
    author='PinchofLogic and NaN·tic',
    author_email='info@nan-tic.com',
    url=WEBSITE,
    download_url=('https://github.com/NaN-tic/python-pharma_datamatrix/' +
        VERSION),
    packages=find_packages(),
    scripts=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        ],
    license=LICENSE,
    install_requires=[
        'datetime',
        ],
    extras_require={},
    zip_safe=False,
    test_suite='pharma_datamatrix.tests',
    )
