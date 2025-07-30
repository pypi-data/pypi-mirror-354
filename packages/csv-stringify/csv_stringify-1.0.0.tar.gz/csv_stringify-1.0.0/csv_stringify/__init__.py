"""
csv-stringify: A Python package for converting data to CSV format.
"""

__version__ = "1.0.0"
__author__ = "Abderrahim GHAZALI"
__email__ = "ghazali.abderrahim1@gmail.com"
__description__ = "Convert Python data structures to CSV format"

from .core import (
    CSVStringifier,
    stringify,
    stringify_sync,
    stringify_records,
    stringify_rows
)

__all__ = [
    'CSVStringifier',
    'stringify',
    'stringify_sync',
    'stringify_records',
    'stringify_rows'
]