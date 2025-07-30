"""
AlumathGroup26 - A simple matrix calculator library
"""

from .matrix import Matrix
from .operations import multiply_matrices, add_matrices, subtract_matrices

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "Matrix",
    "multiply_matrices", 
    "add_matrices",
    "subtract_matrices"
]