#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@academis.eu"

from setuptools import setup, find_packages
import sys
import time

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['arcade']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

package_data ={
    'tilegamelib': ['data/*.ttf', 'data/*.png', 'data/*.conf', 'data/*.xpm', 'data/*.txt']
    #'test.test_data':['file1',..],
    }

setup(
        name = "tilegamelib",
        version = "0.8.2",
        description = "helper classes for building games from square tiles",
        keywords='game programming',
        long_description=readme,
        license = 'MIT',
        url='https://github.com/krother/kristians_hello_world',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Games/Entertainment',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
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
        install_requires=requirements,
        #setup_requires=setup_requirements,
        test_suite='tests',
        tests_require=test_requirements,
        python_requires='>=3.6',
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
        packages=find_packages(include=['tilegamelib', 'tilegamelib.*']),
        package_data=package_data,
        include_package_data=True,
        #data_files=[]#'RELEASE_NOTES.TXT', 'README.TXT', 'LICENSE_GPL.TXT']
        zip_safe=False,

)
