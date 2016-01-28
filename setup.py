#!/usr/bin/env python
"""

   ___       __     __                 
  / _ \___  / /__  / /  __ _  ___ ____ 
 / // / _ \/ / _ \/ _ \/  ' \/ _ `/ _ \
/____/\___/_/ .__/_//_/_/_/_/\_,_/_//_/
           /_/                         


The MIT License (MIT)

Copyright (c) 2015 Dolphman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


version = '1.1.30.59'

from setuptools import setup
setup(name='nationstates',
      install_requires=["requests>=2.9.1", "Beautifulsoup4>=4.4.1", "xmltodict==0.9.2", "ezurl>=0.1.2.19"],
      version=version,
      description='Nationstates API wrapper for python',
      author='Joshua Walters',
      author_email='therealdolphman@gmail.com',
      url='https://github.com/Dolphman/pynationstates',
      packages=['nationstates', 'nationstates.NScore'],
      package_data={'': ['LICENSE.txt', "readme.md"]},
      download_url='https://github.com/Dolphman/pynationstates/releases/tag/'+version,
      keywords=['nationstates', 'api wrapper', 'api',
                "Nationstates API", "Nationstates API Wrapper", "Wrapper",
                "nationstates python bindings", "web api", "web wrapper"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.0",
                   "Programming Language :: Python :: 3.1",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5"],
      license="MIT"
      )
