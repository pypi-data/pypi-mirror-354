# latexsymb

A Python package for composable LaTeX mathematical expressions.

## Overview

`latexsymb` transforms the way mathematical LaTeX expressions are written in Python by providing a programmatic, composable approach. Instead of writing error-prone LaTeX syntax with backslashes and braces, you can build complex mathematical expressions using intuitive Python functions and operators.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from latexsymb import lsymb, pths, Sum, sin, cos, alpha, beta

# Create basic symbols
x = lsymb("x")
y = lsymb("y")

# Use operators to build expressions
fraction = x / y  # → \frac{x}{y}
power = x ** "2"  # → x^{2}

# Use mathematical functions
sine_expr = sin(x)  # → \sin\left(x\right)

# Build complex expressions
summation = Sum(sin(alpha * x), "i=1", "n")
# → \sum_{i=1}^{n} \sin\left(\alpha x\right)

print(summation)
```

## Key Features

### 1. Operator Overloading

Mathematical operators work intuitively:

```python
from latexsymb import lsymb

x = lsymb("x")
y = lsymb("y")

# Basic operations
x + y     # → x+y
x - y     # → x-y  
x * y     # → x y (space-separated)
x / y     # → \frac{x}{y}
x ** "2"  # → x^{2}
```

### 2. Delimiter Functions

Auto-sizing delimiters for clean expressions:

```python
from latexsymb import pths, sqbr, br, ang

pths("x + y")     # → \left(x + y\right)
sqbr("x + y")     # → \left[x + y\right]
br("x + y")       # → \left\{x + y\right\}
ang("x, y")       # → \left\langle x, y\right\rangle
```

### 3. Mathematical Functions

Standard mathematical notation:

```python
from latexsymb import Sum, Prod, Int, lim, dd, pp

Sum("x_i", "i=1", "n")      # → \sum_{i=1}^{n} x_i
Prod("a_i", "i=1", "n")     # → \prod_{i=1}^{n} a_i
Int("x^2", "dx", "0", "1")  # → \int_{0}^{1} x^2 \, dx
lim("f(x)", "x", "0")       # → \lim_{x\rightarrow0} f(x)
dd("f(x)", "x")             # → \frac{d}{dx} f(x)
pp("f(x,y)", "x")           # → \frac{\partial}{\partial x} f(x,y)
```

### 4. Common Mathematical Functions

Callable functions that produce proper LaTeX:

```python
from latexsymb import sin, cos, log, ln, exp, sqrt

sin("x")         # → \sin\left(x\right)
cos("\\theta")   # → \cos\left(\theta\right)
log("x", "2")    # → \log_{2}\left(x\right)
ln("x")          # → \ln\left(x\right)
exp("x")         # → \exp\left(x\right)
sqrt("x")        # → \sqrt{x}
```

### 5. Pre-defined Symbols

Common symbols and Greek letters:

```python
from latexsymb import alpha, beta, gamma, pi, infty, R, C

# Greek letters
alpha   # → \alpha
beta    # → \beta
pi      # → \pi

# Mathematical constants
infty   # → \infty

# Number sets  
R       # → \mathbb{R}
C       # → \mathbb{C}
```

### 6. LaTeX Environments

Create multi-line equations and inline math:

```python
from latexsymb import lenv, il

# Inline math
il("x + y")  # → $x + y$

# Multi-line environments
equations = ["x &= y", "y &= z"]
lenv("align*", equations)
# → \begin{align*}x &= yy &= z\end{align*}
```

## Complex Examples

### Quadratic Formula

```python
from latexsymb import lsymb, sqrt

a, b, c = lsymb("a"), lsymb("b"), lsymb("c")

# x = (-b ± √(b² - 4ac)) / (2a)
discriminant = sqrt(b**"2" - lsymb("4")*a*c)
formula = (-b + lsymb("\\pm") + discriminant) / (lsymb("2")*a)

print(formula)
# → \frac{-b+\pm+\sqrt{b^{2}-4 a c}}{2 a}
```

### Taylor Series

```python
from latexsymb import Sum, under, lsymb, dd

x, a, n = lsymb("x"), lsymb("a"), lsymb("n")
f = lsymb("f")

# f(x) = Σ(n=0 to ∞) [f⁽ⁿ⁾(a)/n!] (x-a)ⁿ
term = (dd(f, under(x, n)) / lsymb("n!")) * (x - a)**n
taylor = Sum(term, "n=0", "\\infty")

print(taylor)
```

## Running Tests

```bash
pytest tests/
```

## License

MIT License