"""
Additional operators and helper functions for LatexSymb objects.

This module provides functions like subscripts, function evaluation,
and other mathematical notation patterns.
"""

from typing import Union
from .core import LatexSymb, _to_latex_str


def under(expr: Union[LatexSymb, str], subscript: Union[LatexSymb, str]) -> LatexSymb:
    """
    Create a subscript expression.
    
    Args:
        expr: The main expression
        subscript: The subscript content
        
    Returns:
        LatexSymb: Expression with subscript
        
    Examples:
        >>> x = lsymb("x")
        >>> under(x, "i")
        LatexSymb('x_{i}')
    """
    return LatexSymb(f"{_to_latex_str(expr)}_{{{_to_latex_str(subscript)}}}")


def at(f: Union[LatexSymb, str], var: Union[LatexSymb, str]) -> LatexSymb:
    """
    Create function evaluation notation f(x).
    
    Args:
        f: The function expression
        var: The variable or argument
        
    Returns:
        LatexSymb: Function with argument in parentheses
        
    Examples:
        >>> f = lsymb("f")
        >>> at(f, "x")
        LatexSymb('f\\left(x\\right)')
    """
    from .delimiters import pths
    return LatexSymb(_to_latex_str(f), str(pths(var)))