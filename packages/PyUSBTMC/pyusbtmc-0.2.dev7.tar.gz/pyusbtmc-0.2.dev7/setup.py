#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
"""
import os,platform,re,sys

extra=dict()
if sys.version_info >= (3,):
    PY3=True
    extra['use_2to3'] = True

#from distutils.core import setup
#from distutils.extension import Extension
from setuptools import setup, Extension

try:
   from setuptools.command.build_py import build_py_2to3 as build_py #for Python3
except ImportError:
   from setuptools.command.build_py import build_py     # for Python2

#from Cython.Distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import Cython.Compiler.Options

# python2/python3
extra=dict()

# try:
#     from distutils.command.build_py import build_py_2to3 as build_py #for Python3
# except ImportError:
#     from distutils.command.build_py import build_py     # for Python2

rev="$Revision: 0.2.dev2$" #[N!]N(.N)*[{a|b|rc}N][.postN][.devN] PEP 440
sysname=platform.system()
HGTag = "$HGTag: $"
HGTagShort="$HGTagShort: 0.2.dev.7 $"
HGdate="$HGdate"
HGLastLog="$lastlog: correct typo in PyUSBTMC.py $"
HGcheckedIn="$checked in by: Noboru Yamamoto <noboru.yamamoto@kek.jp> $"


setup(
    name="PyUSBTMC",
    version=HGTagShort[1:-1].split(":")[1].strip(),
    #version="0.2.dev3",
    author="Noboru Yamamoto, KEK, JAPAN",
    author_email = "Noboru.YAMAMOTO@kek.jp",
    description = "Python module to control USBTMC/USB488 from python",
    long_description="""
    Python module to control USBTMC/USB488 from python.
    It requires pyusb module and libusb (or openusb) library to run. 
    Although it is still in the development stage, it can read/write data from/to the devices.
    """,
    #platforms="tested on MacOSX10.7",
    url="http://www-acc.kek.jp/EPICS_Gr/products/",
    py_modules=["PyUSBTMC", "lsusb", "usbids",
                #"samples.test_DPO", "samples.test_dso_anim",
                #"samples.python_usbtmc_sample",
                #"samples.PyUSBTMC_sample"
                ],
    packages=["samples"],
    package_dir={"samples":"./samples", "":"./"},
    data_files=[("share/misc",['usb.ids'])],
    ext_modules=cythonize(
        [
            Extension("cPyUSBTMC", ["cPyUSBTMC.pyx"]),
        ],
        compiler_directives={"language_level":"3"}, # "2","3","3str"
        annotate=True,
    ),
)
