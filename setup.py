#!/usr/bin/env python
"""

The MIT License (MIT)

Copyright (c) 2015-2018 Dolphman

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


version = '2.0.0.0'

from setuptools import setup
setup(name='nationstates',
      install_requires=["nsapiwrapper"],
      version=version,
      description='Nationstates API wrapper for python',
      author='Joshua Walters',
      author_email='dolphdevgithub@gmail.com',
      url='https://github.com/Dolphman/pynationstates',
      packages=['nationstates'],
      package_data={'': ['LICENSE.txt', "readme.md"]},
      download_url='https://github.com/DolphDev/pynationstates/releases/tag/'+version,
      keywords=['nationstates', 'api wrapper', 'api',
                "Nationstates API", "Nationstates API Wrapper", "Wrapper",
                "nationstates python bindings", "web api", "web wrapper"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6"],
      license="MIT"
      )
