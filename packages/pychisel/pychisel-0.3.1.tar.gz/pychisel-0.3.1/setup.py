# -*- coding: utf-8 -*-
"""
File: setup.py
Location: pychisel
Created at: 09/06/2025
Author: Anderson Alves Monteiro <https://www.github.com/tekoryu>

Setup file for PyChisel - Automated tools for quick preparation of Pandas DataFrames.
"""
from setuptools import setup, find_packages

setup(
    name='pychisel',
    version='0.3.1',
    description='Automated tools for quick preparation of Pandas DataFrames.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Anderson Monteiro',
    author_email='alvesmonteiroanderson@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.0',
    ],
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
