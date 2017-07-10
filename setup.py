#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

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
        author="Kristian Rother",
        author_email="krother@rubor.de",
        packages=packages, 
        package_data=package_data, 
        #data_files=[]#'RELEASE_NOTES.TXT', 'README.TXT', 'LICENSE_GPL.TXT']
        )
