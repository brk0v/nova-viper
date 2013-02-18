#!/usr/bin/env python

from setuptools import setup, find_packages
from nova_viper import __version__


setup(name='nova-viper',
      version=__version__,
      license='GNU GPL v2.1',
      description='cloud computing vip',
      author='Viacheslav Biriukov',
      author_email='v.v.biriukov@gmail.com',
      url='http://biriukov.me',
      packages=find_packages(exclude=['bin', 'redhat', 'smoketests', 'tests', 'pacemaker', 'debian']),
      scripts=['bin/nova-viper'],
      py_modules=[],
      test_suite='tests'
)

