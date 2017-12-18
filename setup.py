#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@academis.eu"

from distutils.core import setup
import sys
import time

packages = ['tilegamelib']

package_data ={
    #'test.test_data':['file1',..],
    }

setup(
        name = "tilegamelib",
        version = "0.8",
        description = "helper classes for building games from square tiles",
        license = 'MIT',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Games/Entertainment',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        install_requires = ['pygame'],
        python_requires='>=3.3',
        author="Kristian Rother",
        author_email="krother@academis.eu",
        extras_require={
            'tests': [
                'pytest',
                'pytest-pep8',
                'pytest-isort',
                'pytest-flakes',
                'pytest-cov'
            ]
        },
        #py_modules=['tilegamelib'],
        packages=packages, 
        package_data=package_data, 
        #data_files=[]#'RELEASE_NOTES.TXT', 'README.TXT', 'LICENSE_GPL.TXT']
        )
