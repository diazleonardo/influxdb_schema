# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    _license = f.read()

setup(
    name='influxdb',
    version='1.0.0',
    description='Produce an HTML listing of thhe influxdb',
    long_description=readme,
    author='Leonardo Díaz',
    author_email='ldiaz@antakori.com',
    url='https://github.com/',
    license=_license,
    packages=find_packages(exclude=('tests', 'docs'))
)
