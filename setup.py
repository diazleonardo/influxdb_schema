# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '1.0.0'
with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    _license = f.read()

setup(
    name='influxdb',
    version='1.0.0',
    description='Produce an HTML listing of the influxdb schema',
    long_description=readme,
    author='Leonardo Díaz',
    author_email='ldiaz@antakori.com',
    url='https://github.com/diazleonardo/influxdb_schema',
    license=_license,
    packages=find_packages(exclude=('tests', 'docs', 'res'))
)
