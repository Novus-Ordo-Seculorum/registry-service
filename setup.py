#!/usr/bin/env python3

import os
import re
import subprocess as sp
import glob
import importlib

from setuptools import setup, find_packages
from setuptools.command import install
from setuptools.command import develop
from setuptools.command import alias

from axial.setup import tasks


HERE = os.path.abspath(os.path.dirname(__file__))
PACKAGES = find_packages()
SERVICE_NAME = PACKAGES[0]


with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()

with open(os.path.join(HERE, 'requirements.txt')) as f:
    REQUIREMENTS = [s.strip().replace('-', '_') for s in f.readlines()]


class Install(install.install):
    def run(self):
        tasks.pyrobuf_install(SERVICE_NAME)
        super(Install, self).run()


class Develop(develop.develop):
    def run(self):
        tasks.pyrobuf_install(SERVICE_NAME)
        super(Develop, self).run()


class Pyrobuf(alias.alias):
    def run(self):
        tasks.pyrobuf_install(SERVICE_NAME)
        super(Pyrobuf, self).run()


if __name__ == '__main__':
    setup(name='Registry Axial Microservice',
          version='1.0',
          description='Registry Microservice',
          long_description=README,
          author='Axial',
          author_email='daniel.gabriele@axial.net',
          install_requires=REQUIREMENTS,
          url=None,
          packages=PACKAGES,
          cmdclass={
            'install': Install,
            'develop': Develop,
            'pyrobuf': Pyrobuf,
            }
          )
