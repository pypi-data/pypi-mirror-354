"""
Common mathematical symbols and constants.

This module provides pre-defined LatexSymb objects for frequently used
mathematical symbols, Greek letters, and operators, as well as callable
mathematical functions.
"""

from typing import Union
from .core import lsymb, LatexSymb
from .operators import at

# Greek letters (lowercase)
alpha = lsymb("\\alpha")
beta = lsymb("\\beta")
gamma = lsymb("\\gamma")
delta = lsymb("\\delta")
epsilon = lsymb("\\epsilon")
varepsilon = lsymb("\\varepsilon")
zeta = lsymb("\\zeta")
eta = lsymb("\\eta")
theta = lsymb("\\theta")
vartheta = lsymb("\\vartheta")
iota = lsymb("\\iota")
kappa = lsymb("\\kappa")
lambda_ = lsymb("\\lambda")  # lambda is a Python keyword
mu = lsymb("\\mu")
nu = lsymb("\\nu")
xi = lsymb("\\xi")
pi = lsymb("\\pi")
varpi = lsymb("\\varpi")
rho = lsymb("\\rho")
varrho = lsymb("\\varrho")
sigma = lsymb("\\sigma")
varsigma = lsymb("\\varsigma")
tau = lsymb("\\tau")
upsilon = lsymb("\\upsilon")
phi = lsymb("\\phi")
varphi = lsymb("\\varphi")
chi = lsymb("\\chi")
psi = lsymb("\\psi")
omega = lsymb("\\omega")

# Greek letters (uppercase)
Alpha = lsymb("\\Alpha")
Beta = lsymb("\\Beta")
Gamma = lsymb("\\Gamma")
Delta = lsymb("\\Delta")
Epsilon = lsymb("\\Epsilon")
Zeta = lsymb("\\Zeta")
Eta = lsymb("\\Eta")
Theta = lsymb("\\Theta")
Iota = lsymb("\\Iota")
Kappa = lsymb("\\Kappa")
Lambda = lsymb("\\Lambda")
Mu = lsymb("\\Mu")
Nu = lsymb("\\Nu")
Xi = lsymb("\\Xi")
Pi = lsymb("\\Pi")
Rho = lsymb("\\Rho")
Sigma = lsymb("\\Sigma")
Tau = lsymb("\\Tau")
Upsilon = lsymb("\\Upsilon")
Phi = lsymb("\\Phi")
Chi = lsymb("\\Chi")
Psi = lsymb("\\Psi")
Omega = lsymb("\\Omega")

# Mathematical operators and symbols
infty = lsymb("\\infty")
partial = lsymb("\\partial")
nabla = lsymb("\\nabla")
sum_sym = lsymb("\\sum")
prod_sym = lsymb("\\prod")
int_sym = lsymb("\\int")
oint = lsymb("\\oint")

# Relations
eq = lsymb("=")
neq = lsymb("\\neq")
leq = lsymb("\\leq")
geq = lsymb("\\geq")
lt = lsymb("<")
gt = lsymb(">")
approx = lsymb("\\approx")
equiv = lsymb("\\equiv")
sim = lsymb("\\sim")
propto = lsymb("\\propto")

# Set theory
in_ = lsymb("\\in")  # in is a Python keyword
notin = lsymb("\\notin")
subset = lsymb("\\subset")
subseteq = lsymb("\\subseteq")
supset = lsymb("\\supset")
supseteq = lsymb("\\supseteq")
cup = lsymb("\\cup")
cap = lsymb("\\cap")
emptyset = lsymb("\\emptyset")
setminus = lsymb("\\setminus")

# Logic
land = lsymb("\\land")  # and is a Python keyword
lor = lsymb("\\lor")  # or is a Python keyword
lnot = lsymb("\\lnot")  # not is a Python keyword
implies = lsymb("\\implies")
iff = lsymb("\\iff")
forall = lsymb("\\forall")
exists = lsymb("\\exists")

# Arrows
rightarrow = lsymb("\\rightarrow")
leftarrow = lsymb("\\leftarrow")
leftrightarrow = lsymb("\\leftrightarrow")
Rightarrow = lsymb("\\Rightarrow")
Leftarrow = lsymb("\\Leftarrow")
Leftrightarrow = lsymb("\\Leftrightarrow")
mapsto = lsymb("\\mapsto")

# Mathematical functions (callable)
def sin(x: Union[LatexSymb, str]) -> LatexSymb:
    """Sine function: sin(x)"""
    return at(lsymb("\\sin"), x)

def cos(x: Union[LatexSymb, str]) -> LatexSymb:
    """Cosine function: cos(x)"""
    return at(lsymb("\\cos"), x)

def tan(x: Union[LatexSymb, str]) -> LatexSymb:
    """Tangent function: tan(x)"""
    return at(lsymb("\\tan"), x)

def sec(x: Union[LatexSymb, str]) -> LatexSymb:
    """Secant function: sec(x)"""
    return at(lsymb("\\sec"), x)

def csc(x: Union[LatexSymb, str]) -> LatexSymb:
    """Cosecant function: csc(x)"""
    return at(lsymb("\\csc"), x)

def cot(x: Union[LatexSymb, str]) -> LatexSymb:
    """Cotangent function: cot(x)"""
    return at(lsymb("\\cot"), x)

def sinh(x: Union[LatexSymb, str]) -> LatexSymb:
    """Hyperbolic sine function: sinh(x)"""
    return at(lsymb("\\sinh"), x)

def cosh(x: Union[LatexSymb, str]) -> LatexSymb:
    """Hyperbolic cosine function: cosh(x)"""
    return at(lsymb("\\cosh"), x)

def tanh(x: Union[LatexSymb, str]) -> LatexSymb:
    """Hyperbolic tangent function: tanh(x)"""
    return at(lsymb("\\tanh"), x)

def log(x: Union[LatexSymb, str], base: Union[LatexSymb, str] = None) -> LatexSymb:
    """Logarithm function: log(x) or log_base(x)"""
    if base is None:
        return at(lsymb("\\log"), x)
    else:
        from .operators import under
        return at(under(lsymb("\\log"), base), x)

def ln(x: Union[LatexSymb, str]) -> LatexSymb:
    """Natural logarithm function: ln(x)"""
    return at(lsymb("\\ln"), x)

def exp(x: Union[LatexSymb, str]) -> LatexSymb:
    """Exponential function: exp(x)"""
    return at(lsymb("\\exp"), x)

def sqrt(x: Union[LatexSymb, str]) -> LatexSymb:
    """Square root function: sqrt(x)"""
    return lsymb(f"\\sqrt{{{x}}}")

# Function symbols (not callable)
lim_sym = lsymb("\\lim")
sup = lsymb("\\sup")
inf = lsymb("\\inf")
max_sym = lsymb("\\max")
min_sym = lsymb("\\min")
arg_max = lsymb("\\arg\\max")
arg_min = lsymb("\\arg\\min")

# Common number sets
R = lsymb("\\mathbb{R}")  # Real numbers
C = lsymb("\\mathbb{C}")  # Complex numbers
Z = lsymb("\\mathbb{Z}")  # Integers
N = lsymb("\\mathbb{N}")  # Natural numbers
Q = lsymb("\\mathbb{Q}")  # Rational numbers

# Miscellaneous
cdot = lsymb("\\cdot")
times = lsymb("\\times")
div = lsymb("\\div")
pm = lsymb("\\pm")
mp = lsymb("\\mp")
star = lsymb("\\star")
ast = lsymb("\\ast")
dagger = lsymb("\\dagger")
ddagger = lsymb("\\ddagger")
ell = lsymb("\\ell")
hbar = lsymb("\\hbar")
Re = lsymb("\\Re")
Im = lsymb("\\Im")

# Export all symbols and functions
__all__ = [
    # Greek lowercase
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta",
    "theta", "vartheta", "iota", "kappa", "lambda_", "mu", "nu", "xi", "pi",
    "varpi", "rho", "varrho", "sigma", "varsigma", "tau", "upsilon", "phi",
    "varphi", "chi", "psi", "omega",
    
    # Greek uppercase  
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Pi", "Rho", "Sigma",
    "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
    
    # Mathematical operators
    "infty", "partial", "nabla", "sum_sym", "prod_sym", "int_sym", "oint",
    
    # Relations
    "eq", "neq", "leq", "geq", "lt", "gt", "approx", "equiv", "sim", "propto",
    
    # Set theory
    "in_", "notin", "subset", "subseteq", "supset", "supseteq", "cup", "cap",
    "emptyset", "setminus",
    
    # Logic
    "land", "lor", "lnot", "implies", "iff", "forall", "exists",
    
    # Arrows
    "rightarrow", "leftarrow", "leftrightarrow", "Rightarrow", "Leftarrow",
    "Leftrightarrow", "mapsto",
    
    # Mathematical functions (callable)
    "sin", "cos", "tan", "sec", "csc", "cot", "sinh", "cosh", "tanh",
    "log", "ln", "exp", "sqrt",
    
    # Function symbols
    "lim_sym", "sup", "inf", "max_sym", "min_sym", "arg_max", "arg_min",
    
    # Number sets
    "R", "C", "Z", "N", "Q",
    
    # Miscellaneous
    "cdot", "times", "div", "pm", "mp", "star", "ast", "dagger", "ddagger",
    "ell", "hbar", "Re", "Im",
]