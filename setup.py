#!/usr/bin/env python
# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : GPL 2.0 (See LICENSE)
# Comment  : Setup script for the library.
#
# =========================================================

from setuptools import setup, find_packages

execfile('advoptparse/version.py')

setup(name='advoptparse',
      license='GNU General Public Liense 2.0',
      version=__version__,
      description='Advanced python commandline argument parser',
      long_description='A more advanced commandline argument parser that can handle top and bottom level commands as well as command-chaining as well as field handling.',
      author='Katharina Sabel',
      author_email='katharina.sabel@2rsoftworks.de',
      url='http://github.com/SpaceKookie/AdvOptParse/',
      packages=['advoptparse'],
     )
