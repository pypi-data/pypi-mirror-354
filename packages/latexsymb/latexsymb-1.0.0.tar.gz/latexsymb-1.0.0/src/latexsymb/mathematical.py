"""
Mathematical functions for sums, products, integrals, limits, and derivatives.

This module provides functions to create standard mathematical notation
for calculus and mathematical analysis.
"""

from typing import Union, Optional
from .core import LatexSymb, lsymb, _to_latex_str
from .operators import under


def Sum(f: Union[LatexSymb, str], 
        from_expr: Optional[Union[LatexSymb, str]] = None, 
        to: Optional[Union[LatexSymb, str]] = None) -> LatexSymb:
    """
    Create a summation expression.
    
    Args:
        f: The expression to sum
        from_expr: Lower limit (subscript)
        to: Upper limit (superscript)
        
    Returns:
        LatexSymb: Summation expression
        
    Examples:
        >>> Sum("x_i", "i=1", "n")
        LatexSymb('\\sum_{i=1}^{n} x_i')
    """
    result = lsymb("\\sum")
    
    if from_expr is not None:
        result = under(result, from_expr)
    
    if to is not None:
        result = result ** to
    
    return result * f


def Prod(f: Union[LatexSymb, str], 
         from_expr: Optional[Union[LatexSymb, str]] = None, 
         to: Optional[Union[LatexSymb, str]] = None) -> LatexSymb:
    """
    Create a product expression.
    
    Args:
        f: The expression to multiply
        from_expr: Lower limit (subscript)
        to: Upper limit (superscript)
        
    Returns:
        LatexSymb: Product expression
        
    Examples:
        >>> Prod("x_i", "i=1", "n")
        LatexSymb('\\prod_{i=1}^{n} x_i')
    """
    result = lsymb("\\prod")
    
    if from_expr is not None:
        result = under(result, from_expr)
    
    if to is not None:
        result = result ** to
    
    return result * f


def Int(f: Union[LatexSymb, str], 
        meas: Union[LatexSymb, str] = "dx",
        from_expr: Optional[Union[LatexSymb, str]] = None, 
        to: Optional[Union[LatexSymb, str]] = None) -> LatexSymb:
    """
    Create an integral expression.
    
    Args:
        f: The integrand
        meas: The measure (default "dx")
        from_expr: Lower limit (subscript)
        to: Upper limit (superscript)
        
    Returns:
        LatexSymb: Integral expression
        
    Examples:
        >>> Int("x^2", "dx", "0", "1")
        LatexSymb('\\int_{0}^{1} x^2 \\, dx')
    """
    result = lsymb("\\int")
    
    if from_expr is not None:
        result = under(result, from_expr)
    
    if to is not None:
        result = result ** to
    
    # Add integrand and measure with thin space
    return result * f * "\\," * meas


def lim(f: Union[LatexSymb, str], 
        var: Union[LatexSymb, str], 
        to: Union[LatexSymb, str] = "\\infty") -> LatexSymb:
    """
    Create a limit expression.
    
    Args:
        f: The expression to take the limit of
        var: The variable
        to: What the variable approaches (default ∞)
        
    Returns:
        LatexSymb: Limit expression
        
    Examples:
        >>> lim("f(x)", "x", "0")
        LatexSymb('\\lim_{x \\rightarrow 0} f(x)')
    """
    limit_base = lsymb("\\lim")
    approach = lsymb(_to_latex_str(var), "\\rightarrow", _to_latex_str(to))
    return under(limit_base, approach) * f


def dd(f: Union[LatexSymb, str], var: Union[LatexSymb, str]) -> LatexSymb:
    """
    Create a derivative expression (d/dx).
    
    Args:
        f: The function to differentiate
        var: The variable to differentiate with respect to
        
    Returns:
        LatexSymb: Derivative expression
        
    Examples:
        >>> dd("f(x)", "x")
        LatexSymb('\\frac{d}{dx} f(x)')
    """
    derivative_part = lsymb("d") / lsymb("d", " ", _to_latex_str(var))
    return LatexSymb(str(derivative_part), " ", _to_latex_str(f))


def pp(f: Union[LatexSymb, str], var: Union[LatexSymb, str]) -> LatexSymb:
    """
    Create a partial derivative expression (∂/∂x).
    
    Args:
        f: The function to differentiate
        var: The variable to differentiate with respect to
        
    Returns:
        LatexSymb: Partial derivative expression
        
    Examples:
        >>> pp("f(x,y)", "x")
        LatexSymb('\\frac{\\partial}{\\partial x} f(x,y)')
    """
    derivative_part = lsymb("\\partial") / lsymb("\\partial", " ", _to_latex_str(var))
    return LatexSymb(str(derivative_part), " ", _to_latex_str(f))