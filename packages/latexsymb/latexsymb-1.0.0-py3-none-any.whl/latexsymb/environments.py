"""
LaTeX environment functions for creating multi-line equations and inline math.

This module provides functions to create LaTeX environments and 
inline mathematical expressions.
"""

from typing import Union, List
from .core import LatexSymb, _to_latex_str


def il(expr: Union[LatexSymb, str]) -> str:
    """
    Wrap expression in inline math delimiters.
    
    Args:
        expr: Expression to wrap in dollar signs
        
    Returns:
        str: Expression wrapped in $ ... $
        
    Examples:
        >>> il("x + y")
        '$x + y$'
    """
    return f"${_to_latex_str(expr)}$"


def lenv(name: str, rows: List[Union[LatexSymb, str]]) -> str:
    """
    Create a LaTeX environment with the given content.
    
    Args:
        name: Name of the LaTeX environment
        rows: List of expressions to include in the environment
        
    Returns:
        str: Complete LaTeX environment
        
    Examples:
        >>> lenv("align*", ["x &= y", "y &= z"])
        '\\begin{align*}x &= yy &= z\\end{align*}'
    """
    content = "".join(_to_latex_str(row) for row in rows)
    return f"\\begin{{{name}}}{content}\\end{{{name}}}"