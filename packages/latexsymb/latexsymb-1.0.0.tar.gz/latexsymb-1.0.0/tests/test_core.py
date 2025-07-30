"""
Tests for the core LatexSymb functionality.
"""

import pytest
from latexsymb import LatexSymb, lsymb


class TestLatexSymb:
    """Test the LatexSymb class."""
    
    def test_init_single_string(self):
        """Test creating LatexSymb with single string."""
        x = LatexSymb("x")
        assert str(x) == "x"
    
    def test_init_multiple_strings(self):
        """Test creating LatexSymb with multiple strings."""
        expr = LatexSymb("x", "=", "y")
        assert str(expr) == "x=y"
    
    def test_init_mixed_types(self):
        """Test creating LatexSymb with mixed string and LatexSymb objects."""
        x = LatexSymb("x")
        y = LatexSymb("y")
        expr = LatexSymb(x, "=", y)
        assert str(expr) == "x=y"
    
    def test_repr(self):
        """Test string representation."""
        x = LatexSymb("x")
        assert repr(x) == "LatexSymb('x')"
    
    def test_addition(self):
        """Test addition operator."""
        x = LatexSymb("x")
        y = LatexSymb("y")
        result = x + y
        assert str(result) == "x+y"
    
    def test_addition_with_string(self):
        """Test addition with string."""
        x = LatexSymb("x")
        result = x + "y"
        assert str(result) == "x+y"
        
        result = "x" + x
        assert str(result) == "x+x"
    
    def test_subtraction(self):
        """Test subtraction operator."""
        x = LatexSymb("x")
        y = LatexSymb("y")
        result = x - y
        assert str(result) == "x-y"
    
    def test_multiplication(self):
        """Test multiplication operator (space-separated)."""
        x = LatexSymb("x")
        y = LatexSymb("y")
        result = x * y
        assert str(result) == "x y"
    
    def test_division(self):
        """Test division operator (fraction)."""
        x = LatexSymb("x")
        y = LatexSymb("y")
        result = x / y
        assert str(result) == "\\frac{x}{y}"
    
    def test_power(self):
        """Test power operator (superscript)."""
        x = LatexSymb("x")
        result = x ** "2"
        assert str(result) == "x^{2}"
    
    def test_equality(self):
        """Test equality comparison."""
        x1 = LatexSymb("x")
        x2 = LatexSymb("x")
        y = LatexSymb("y")
        
        assert x1 == x2
        assert x1 != y
        assert x1 != "x"  # Different types
    
    def test_hash(self):
        """Test that LatexSymb objects are hashable."""
        x = LatexSymb("x")
        y = LatexSymb("y")
        
        # Should be able to put in set
        s = {x, y}
        assert len(s) == 2
        
        # Same content should have same hash
        x2 = LatexSymb("x")
        assert hash(x) == hash(x2)


class TestLsymbFunction:
    """Test the lsymb convenience function."""
    
    def test_lsymb_single_arg(self):
        """Test lsymb with single argument."""
        x = lsymb("x")
        assert isinstance(x, LatexSymb)
        assert str(x) == "x"
    
    def test_lsymb_multiple_args(self):
        """Test lsymb with multiple arguments."""
        expr = lsymb("x", "=", "y")
        assert str(expr) == "x=y"
    
    def test_lsymb_mixed_types(self):
        """Test lsymb with mixed types."""
        x = lsymb("x")
        expr = lsymb(x, "+", "1")
        assert str(expr) == "x+1"


class TestComplexExpressions:
    """Test building complex mathematical expressions."""
    
    def test_nested_fractions(self):
        """Test nested fraction expressions."""
        x = lsymb("x")
        y = lsymb("y")
        z = lsymb("z")
        
        # (x/y)/z = \frac{\frac{x}{y}}{z}
        result = (x / y) / z
        assert str(result) == "\\frac{\\frac{x}{y}}{z}"
    
    def test_mixed_operations(self):
        """Test expressions with mixed operations."""
        x = lsymb("x")
        y = lsymb("y")
        
        # x^2 + y^2
        result = x**"2" + y**"2"
        assert str(result) == "x^{2}+y^{2}"
    
    def test_complex_expression(self):
        """Test a complex mathematical expression."""
        a = lsymb("a")
        b = lsymb("b")
        c = lsymb("c")
        
        # (a + b) / c^2
        result = (a + b) / (c ** "2")
        assert str(result) == "\\frac{a+b}{c^{2}}"