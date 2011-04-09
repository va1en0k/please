#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='please',
      version='0.0.1',

      description="A simple interactive command line configurator",
      author="Valya Golev",
      author_email="me@valyagolev.net",
      
      packages=find_packages(),
      zip_safe=False,

      scripts=['pyplease/bin/please'],

#      install_requires=[
#        'django>=1.3'
#        ],
      include_package_data=True,

      classifiers=[
      ])
