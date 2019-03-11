"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

setup(
    name='paragrammer',
    version='0.1dev',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'matplotlib~=3.0.2',
        'scipy~=1.2.1',
        'scikit-learn~=0.20.3'
    ]
)