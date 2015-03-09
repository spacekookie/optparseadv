#!/usr/bin/env python
# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : GPL 2.0 (See LICENSE)
# Comment  : Setup script for the library.
#
# =========================================================

from setuptools import setup, find_packages
import os

execfile('src/version.py')

# vf = open(os.path.join('src', 'VERSION'))
# __version__ = vf.read().strip()

setup(
    name='advoptparse',
    version=__version__,
    url='http://github.com/SpaceKookie/OptionsPie/',
    license='GNU Public Liense 2.0',
    author='Katharina Sabel',
    author_email='katharina.sabel@2rsoftworks.de',
    description='Advanced python commandline argument parser',
    packages=['src'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
)
