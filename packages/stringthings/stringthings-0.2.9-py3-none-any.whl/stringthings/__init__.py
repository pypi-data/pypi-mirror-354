# -*-coding: utf-8 -*-
"""
Created on Mon Jan 01 13:53:33 2024

@author: Martín Araya
"""

__version__ = "0.2.9"
__release__ = 20250609

from .dates import format_date, is_date, format_date as date
from .numbers import is_numeric, get_number
from .splits import multisplit, split_dmmmy
from .compression import expand, compress
from .filenames import extension, Filepath, get_folder, get_file, get_name, get_extension

__all__ = ['multisplit',
           'split_dmmmy', 'format_date', 'is_date',
           'is_numeric', 'get_number',
           'expand', 'compress',
           'extension', 'get_folder', 'get_file', 'get_name', 'get_extension']
