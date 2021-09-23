
#!/usr/bin/env python
"""

The MIT License (MIT)

Copyright (c) 2015-2021 DolphDev

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


version = '3.1.4'

from setuptools import setup
setup(name='nationstates',
      install_requires=["beautifulsoup4==4.9.3", "ezurl==0.1.3.25",
                        "requests==2.25.*", "xmltodict==0.12.0" ],
      version=version,
      description='Nationstates API wrapper for python',
      author='Joshua W',
      author_email='dolphdevgithub@gmail.com',
      url='https://github.com/DolphDev/pynationstates',
      packages=['nationstates', 'nationstates.nsapiwrapper'],
      package_data={'': ['LICENSE.txt', "readme.md"]},
      download_url='https://github.com/DolphDev/pynationstates/releases/tag/'+version,
      keywords=['nationstates', 'api wrapper', 'api',
                "Nationstates API", "Nationstates API Wrapper", "Wrapper",
                "nationstates python bindings", "web api", "web wrapper"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8"],
      license="MIT"
      )
