"""
AluMathPeerGroup10 - A Python package for matrix operations.

This package provides a Matrix class and common matrix operations
including addition, subtraction, multiplication, and transposition.
"""

__version__ = "0.1.0"
__author__ = "AluMath Peer Group 10"
__email__ = "alumath.peergroup10@example.com"

from .matrix import Matrix
from .operations import multiply, add, subtract, transpose

__all__ = [
    'Matrix',
    'multiply',
    'add',
    'subtract',
    'transpose',
]
