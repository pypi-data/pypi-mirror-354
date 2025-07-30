# -*- coding: utf-8 -*-
"""
File: __init__.py
Location: pychisel
Created at: 09/06/2025
Author: Anderson Alves Monteiro <https://www.github.com/tekoryu>

PyChisel - Automated tools for quick preparation of Pandas DataFrames.
"""
from pychisel.core import Splitter, split
from pychisel.exceptions import SplittingError

__all__ = ['Splitter', 'split', 'SplittingError']
