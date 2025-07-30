"""
Core LatexSymb class and main functionality.

This module implements the core LatexSymb class that represents LaTeX 
expressions as Python objects with operator overloading.
"""

from typing import Union, Any


class LatexSymb:
    """
    A class representing LaTeX mathematical expressions.
    
    This class stores LaTeX code as strings and provides operator overloading
    to build complex expressions programmatically.
    """
    
    def __init__(self, *args: Union[str, 'LatexSymb']) -> None:
        """
        Initialize a LatexSymb object.
        
        Args:
            *args: String components or other LatexSymb objects to concatenate
        """
        parts = []
        for arg in args:
            if isinstance(arg, LatexSymb):
                parts.append(str(arg))
            else:
                parts.append(str(arg))
        self._latex = "".join(parts)
    
    def __str__(self) -> str:
        """Return the LaTeX string representation."""
        return self._latex
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"LatexSymb('{self._latex}')"
    
    def __add__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Concatenate with + operator."""
        return LatexSymb(self._latex, "+", _to_latex_str(other))
    
    def __radd__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Right-side concatenation with + operator."""
        return LatexSymb(_to_latex_str(other), "+", self._latex)
    
    def __sub__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Concatenate with - operator."""
        return LatexSymb(self._latex, "-", _to_latex_str(other))
    
    def __rsub__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Right-side concatenation with - operator."""
        return LatexSymb(_to_latex_str(other), "-", self._latex)
    
    def __mul__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Concatenate with * operator (space-separated)."""
        return LatexSymb(self._latex, " ", _to_latex_str(other))
    
    def __rmul__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Right-side concatenation with * operator."""
        return LatexSymb(_to_latex_str(other), " ", self._latex)
    
    def __truediv__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Create fraction with / operator."""
        return LatexSymb(f"\\frac{{{self._latex}}}{{{_to_latex_str(other)}}}")
    
    def __rtruediv__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Right-side fraction with / operator."""
        return LatexSymb(f"\\frac{{{_to_latex_str(other)}}}{{{self._latex}}}")
    
    def __pow__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Create superscript with ** operator."""
        return LatexSymb(f"{self._latex}^{{{_to_latex_str(other)}}}")
    
    def __rpow__(self, other: Union['LatexSymb', str]) -> 'LatexSymb':
        """Right-side superscript with ** operator."""
        return LatexSymb(f"{_to_latex_str(other)}^{{{self._latex}}}")
    
    def __eq__(self, other: Any) -> bool:
        """Check equality based on LaTeX string."""
        if isinstance(other, LatexSymb):
            return self._latex == other._latex
        return False
    
    def __hash__(self) -> int:
        """Make LatexSymb hashable."""
        return hash(self._latex)
    
    def __neg__(self) -> 'LatexSymb':
        """Unary minus operator."""
        return LatexSymb(f"-{self._latex}")


def _to_latex_str(obj: Union[LatexSymb, str]) -> str:
    """Convert object to LaTeX string."""
    if isinstance(obj, LatexSymb):
        return str(obj)
    return str(obj)


def lsymb(*args: Union[str, LatexSymb]) -> LatexSymb:
    """
    Create a LatexSymb object by concatenating arguments.
    
    Args:
        *args: String components or LatexSymb objects to concatenate
        
    Returns:
        LatexSymb: A new LatexSymb object
        
    Examples:
        >>> x = lsymb("x")
        >>> y = lsymb("y") 
        >>> expr = lsymb(x, "=", y)
        >>> str(expr)
        'x=y'
    """
    return LatexSymb(*args)