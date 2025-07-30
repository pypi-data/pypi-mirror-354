"""
Tests for mathematical functions and operators.
"""

import pytest
from latexsymb import (
    lsymb, under, at, pths, sqbr, br, ang, 
    Sum, Prod, Int, lim, dd, pp, lenv, il,
    sin, cos, tan, log, ln, exp, sqrt
)


class TestOperators:
    """Test additional operators."""
    
    def test_under_subscript(self):
        """Test subscript creation."""
        x = lsymb("x")
        result = under(x, "i")
        assert str(result) == "x_{i}"
    
    def test_at_function_call(self):
        """Test function call notation."""
        f = lsymb("f")
        result = at(f, "x")
        assert str(result) == "f\\left(x\\right)"


class TestDelimiters:
    """Test delimiter functions."""
    
    def test_pths_parentheses(self):
        """Test parentheses wrapping."""
        expr = "x + y"
        result = pths(expr)
        assert str(result) == "\\left(x + y\\right)"
    
    def test_sqbr_square_brackets(self):
        """Test square brackets wrapping."""
        expr = "x + y"
        result = sqbr(expr)
        assert str(result) == "\\left[x + y\\right]"
    
    def test_br_braces(self):
        """Test braces wrapping."""
        expr = "x + y"
        result = br(expr)
        assert str(result) == "\\left\\{x + y\\right\\}"
    
    def test_ang_angle_brackets(self):
        """Test angle brackets wrapping."""
        expr = "x, y"
        result = ang(expr)
        assert str(result) == "\\left\\langle x, y\\right\\rangle"


class TestMathematicalFunctions:
    """Test mathematical function notation."""
    
    def test_sum_basic(self):
        """Test basic summation."""
        result = Sum("x_i")
        assert str(result) == "\\sum x_i"
    
    def test_sum_with_limits(self):
        """Test summation with limits."""
        result = Sum("x_i", "i=1", "n")
        assert str(result) == "\\sum_{i=1}^{n} x_i"
    
    def test_prod_basic(self):
        """Test basic product."""
        result = Prod("x_i")
        assert str(result) == "\\prod x_i"
    
    def test_prod_with_limits(self):
        """Test product with limits."""
        result = Prod("x_i", "i=1", "n")
        assert str(result) == "\\prod_{i=1}^{n} x_i"
    
    def test_int_basic(self):
        """Test basic integral."""
        result = Int("x^2")
        assert str(result) == "\\int x^2 \\, dx"
    
    def test_int_custom_measure(self):
        """Test integral with custom measure."""
        result = Int("f(x)", "dt")
        assert str(result) == "\\int f(x) \\, dt"
    
    def test_int_with_limits(self):
        """Test integral with limits."""
        result = Int("x^2", "dx", "0", "1")
        assert str(result) == "\\int_{0}^{1} x^2 \\, dx"
    
    def test_lim_basic(self):
        """Test basic limit."""
        result = lim("f(x)", "x")
        assert str(result) == "\\lim_{x\\rightarrow\\infty} f(x)"
    
    def test_lim_custom_target(self):
        """Test limit with custom target."""
        result = lim("f(x)", "x", "0")
        assert str(result) == "\\lim_{x\\rightarrow0} f(x)"
    
    def test_dd_derivative(self):
        """Test derivative notation."""
        result = dd("f(x)", "x")
        assert str(result) == "\\frac{d}{d x} f(x)"
    
    def test_pp_partial_derivative(self):
        """Test partial derivative notation."""
        result = pp("f(x,y)", "x")
        assert str(result) == "\\frac{\\partial}{\\partial x} f(x,y)"


class TestEnvironments:
    """Test LaTeX environment functions."""
    
    def test_il_inline_math(self):
        """Test inline math wrapper."""
        result = il("x + y")
        assert result == "$x + y$"
    
    def test_lenv_basic(self):
        """Test basic environment creation."""
        rows = ["x &= y", "y &= z"]
        result = lenv("align*", rows)
        assert result == "\\begin{align*}x &= yy &= z\\end{align*}"


class TestCommonFunctions:
    """Test common mathematical functions."""
    
    def test_sin_function(self):
        """Test sine function."""
        result = sin("x")
        assert str(result) == "\\sin\\left(x\\right)"
    
    def test_cos_function(self):
        """Test cosine function."""
        result = cos("\\theta")
        assert str(result) == "\\cos\\left(\\theta\\right)"
    
    def test_tan_function(self):
        """Test tangent function.""" 
        result = tan("x")
        assert str(result) == "\\tan\\left(x\\right)"
    
    def test_log_function_basic(self):
        """Test logarithm function without base."""
        result = log("x")
        assert str(result) == "\\log\\left(x\\right)"
    
    def test_log_function_with_base(self):
        """Test logarithm function with base."""
        result = log("x", "2")
        assert str(result) == "\\log_{2}\\left(x\\right)"
    
    def test_ln_function(self):
        """Test natural logarithm function."""
        result = ln("x")
        assert str(result) == "\\ln\\left(x\\right)"
    
    def test_exp_function(self):
        """Test exponential function."""
        result = exp("x")
        assert str(result) == "\\exp\\left(x\\right)"
    
    def test_sqrt_function(self):
        """Test square root function."""
        result = sqrt("x")
        assert str(result) == "\\sqrt{x}"


class TestComplexUsage:
    """Test complex real-world usage patterns."""
    
    def test_quadratic_formula(self):
        """Test building the quadratic formula."""
        a = lsymb("a")
        b = lsymb("b") 
        c = lsymb("c")
        
        # x = (-b ± √(b² - 4ac)) / (2a)
        discriminant = sqrt(b**"2" - lsymb("4") * a * c)
        numerator = -b + lsymb("\\pm") + discriminant
        result = numerator / (lsymb("2") * a)
        
        expected = "\\frac{-b+\\pm+\\sqrt{b^{2}-4 a c}}{2 a}"
        assert str(result) == expected
    
    def test_derivative_of_composite(self):
        """Test derivative of composite function."""
        # d/dx[sin(x²)]
        inner = lsymb("x") ** "2"
        func = sin(inner)
        result = dd(func, "x")
        
        expected = "\\frac{d}{d x} \\sin\\left(x^{2}\\right)"
        assert str(result) == expected