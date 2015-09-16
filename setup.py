#!/usr/bin/env python

from setuptools import setup
setup(name='nationstates',
      install_requires=["requests", "Beautifulsoup4"],
      version='Pre-Release',
      description='Nationstates API wrapper',
      author='Joshua Walters',
      author_email='',
      url='https://github.com/Dolphman/pynationstates',
      packages=['nationstates', 'nationstates.NSback']
     )
