#!/usr/bin/env python

from setuptools import setup
setup(name='nationstates',
      install_requires=["requests", "Beautifulsoup4", "xmltodict"],
      version='0.143',
      description='Nationstates API wrapper for python',
      author='Joshua Walters',
      author_email='therealdolphman@gmail.com',
      url='https://github.com/Dolphman/pynationstates',
      packages=['nationstates', 'nationstates.NSback'],
      download_url='https://github.com/Dolphman/pynationstates/tarball/0.14',
      keywords=['nationstates', 'api wrapper', 'api',
                "Nationstates API", "Nationstates API Wrapper", "Wrapper"],
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
