#!/usr/bin/env python
"""
Copyright 2010 Kristian Rother. All rights reserved.

Please see the LICENSE file that should have been included
as part of this package.
"""

__author__="Kristian Rother"
__email__ ="krother@academis.eu"

from setuptools import setup, find_packages
import os

def open_file(fname):
   return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = ['arcade']

package_data ={
    'tilegamelib': ['data/*.ttf', 'data/*.png', 'data/*.conf', 'data/*.xpm', 'data/*.txt']
    #'test.test_data':['file1',..],
    }

setup(
    name = "tilegamelib",
    version = "0.9.1",
    description = "helper classes for building games from square tiles",
    long_description=open_file('README.md'),
    keywords='game programming',

    license = 'MIT',
    url='https://github.com/krother/tilegamelib',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'sliding_puzzle=tilegamelib.games.sliding_puzzle:main',
            'collect_fruit=tilegamelib.games.collect_fruit:main',
            'boxes=tilegamelib.games.boxes:main',
            'snake=tilegamelib.games.snake:main',
            'pac=tilegamelib.games.pac:main',
        ],
    },
    python_requires='>=3.8',
    author="Kristian Rother",
    author_email="krother@academis.eu",

    packages=find_packages(include=['tilegamelib', 'tilegamelib.*']),
    package_data=package_data,
    include_package_data=True,
    #data_files=[]#'RELEASE_NOTES.TXT', 'README.TXT', 'LICENSE_GPL.TXT']
    zip_safe=False,
)
