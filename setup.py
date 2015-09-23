#!/usr/bin/env python

from setuptools import setup
setup(name='nationstates',
      install_requires=["requests", "Beautifulsoup4", "xmltodict"],
      version='0.1',
      description='Nationstates API wrapper for python',
      author='Joshua Walters',
      author_email='therealdolphman@gmail.com',
      url='https://github.com/Dolphman/pynationstates',
      packages=['nationstates', 'nationstates.NSback'],
      download_url='https://github.com/Dolphman/pynationstates/tarball/0.1',
      keywords=['nationstates', 'api wrapper', 'api', "Nationstates API", "Nationstates API Wrapper", "Wrapper"]
      )
