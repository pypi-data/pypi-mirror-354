# pylint:disable=C0111
from .reader import CCtiReader, MODE_AUTO, MODE_MEMORY, MODE_MMAP

__all__ = [
    "CCtiReader",
	"MODE_AUTO",
	"MODE_MEMORY",
	"MODE_MMAP"
]

__version__ = "1.1.16"
__author__ = "AISpera CTIDB"
__license__ = "Apache License, Version 2.0"