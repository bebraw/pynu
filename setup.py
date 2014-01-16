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
from setuptools import setup
import pynu


# XXX: breaks build!
def long_description():
    description_files = ('README', 'CHANGELOG', )

    file_contents = list()
    for file in description_files:
        file_contents.append(open(file).read())

    return '\n\n'.join(file_contents)

setup(name='Pynu',
    version=pynu.__version__,
    description='Pynu provides utility classes that offer basic graph tree \
traversal and manipulation functionality.',
    #long_description=long_description(),
    author=pynu.__author__,
    author_email='bebraw@gmail.com',
    url='http://github.com/bebraw/pynu',
    license='MIT',
    keywords=['graph', 'nodes', ],
    packages=['pynu', ],
    package_dir={'pynu': 'pynu', },
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development',
          ],
    )
