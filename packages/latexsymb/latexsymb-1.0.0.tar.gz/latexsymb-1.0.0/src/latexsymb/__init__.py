"""
latexsymb: A Python package for composable LaTeX mathematical expressions.

This package provides a programmatic way to build LaTeX mathematical expressions
using Python operators and functions, making mathematical typesetting more 
readable and maintainable.
"""

from .core import LatexSymb, lsymb
from .operators import under, at
from .delimiters import pths, sqbr, br, ang
from .mathematical import Sum, Prod, Int, lim, dd, pp
from .environments import lenv, il
from .common import *

__version__ = "1.0.0"
__author__ = "Nicolas Escobar"

__all__ = [
    "LatexSymb",
    "lsymb", 
    "under",
    "at",
    "pths",
    "sqbr", 
    "br",
    "ang",
    "Sum",
    "Prod",
    "Int", 
    "lim",
    "dd",
    "pp",
    "lenv",
    "il",
]