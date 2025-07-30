"""
Delimiter functions for wrapping expressions.

This module provides functions to wrap expressions in various types
of delimiters with automatic sizing.
"""

from typing import Union
from .core import LatexSymb, _to_latex_str


def pths(expr: Union[LatexSymb, str]) -> LatexSymb:
    """
    Wrap expression in auto-sizing parentheses.
    
    Args:
        expr: Expression to wrap
        
    Returns:
        LatexSymb: Expression wrapped in \\left( \\right)
        
    Examples:
        >>> pths("x + y")
        LatexSymb('\\left(x + y\\right)')
    """
    return LatexSymb(f"\\left({_to_latex_str(expr)}\\right)")


def sqbr(expr: Union[LatexSymb, str]) -> LatexSymb:
    """
    Wrap expression in auto-sizing square brackets.
    
    Args:
        expr: Expression to wrap
        
    Returns:
        LatexSymb: Expression wrapped in \\left[ \\right]
        
    Examples:
        >>> sqbr("x + y")
        LatexSymb('\\left[x + y\\right]')
    """
    return LatexSymb(f"\\left[{_to_latex_str(expr)}\\right]")


def br(expr: Union[LatexSymb, str]) -> LatexSymb:
    """
    Wrap expression in auto-sizing braces.
    
    Args:
        expr: Expression to wrap
        
    Returns:
        LatexSymb: Expression wrapped in \\left\\{ \\right\\}
        
    Examples:
        >>> br("x + y")
        LatexSymb('\\left\\{x + y\\right\\}')
    """
    return LatexSymb(f"\\left\\{{{_to_latex_str(expr)}\\right\\}}")


def ang(expr: Union[LatexSymb, str]) -> LatexSymb:
    """
    Wrap expression in auto-sizing angle brackets.
    
    Args:
        expr: Expression to wrap
        
    Returns:
        LatexSymb: Expression wrapped in \\left\\langle \\right\\rangle
        
    Examples:
        >>> ang("x, y")
        LatexSymb('\\left\\langle x, y\\right\\rangle')
    """
    return LatexSymb(f"\\left\\langle {_to_latex_str(expr)}\\right\\rangle")