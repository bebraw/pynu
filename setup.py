#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pynu - Python Node Utilities
Copyright (C) 2010 Juho Vepsäläinen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/
"""
from distutils.core import setup
import pynu

setup(name='Pynu',
    version=pynu.__version__,
    description='Pynu provides utility classes that offer basic graph tree \
    traversal and manipulation functionality.',
    #long_description=pynu.__doc__,
    author=pynu.__author__,
    author_email='bebraw@gmail.com',
    url='http://github.com/bebraw/pynu',
    license='GPLv3',
    packages=['pynu', ],
    package_dir={'pynu': 'pynu', },
    data_files=[('readme', ['README', ]), ('todo', ['TODO', ]), ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development',
          ],
    )
