#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='playpen-plus',
    version='0.1',
    packages=find_packages(),
    description='Google+ APIs messing about',
    author='Matt Sullivan',
    author_email='matt.j.sullivan@gmail.com',
    install_requires = ['flask>=0.10', 'Flask-KVSession>=0.4', 'google-api-python-client>=1.1']
)