"""
alumath_peergroup_6: A Python library for matrix multiplication with support for different dimensions.

This library provides efficient matrix multiplication operations including:
- Standard matrix multiplication
- Element-wise multiplication (Hadamard product)
- Broadcasting for compatible dimensions
- Comprehensive error handling
"""

from .matrix import Matrix
from .operations import MatrixOperations
from .exceptions import DimensionError, InvalidMatrixError

__version__ = "1.0.0"
__author__ = "Peergroup 6"
__email__ = "peergroup6@example.com"

__all__ = [
    "Matrix",
    "MatrixOperations", 
    "DimensionError",
    "InvalidMatrixError",
    "multiply",
    "hadamard_product",
    "broadcast_multiply"
]

# Convenience functions
def multiply(matrix_a, matrix_b, method="standard"):
    """
    Multiply two matrices using the specified method.
    
    Args:
        matrix_a: First matrix (list of lists or Matrix object)
        matrix_b: Second matrix (list of lists or Matrix object)
        method: Multiplication method ("standard", "hadamard", "broadcast")
    
    Returns:
        Matrix: Result of multiplication
    """
    ops = MatrixOperations()
    
    if not isinstance(matrix_a, Matrix):
        matrix_a = Matrix(matrix_a)
    if not isinstance(matrix_b, Matrix):
        matrix_b = Matrix(matrix_b)
    
    if method == "standard":
        return ops.standard_multiply(matrix_a, matrix_b)
    elif method == "hadamard":
        return ops.hadamard_product(matrix_a, matrix_b)
    elif method == "broadcast":
        return ops.broadcast_multiply(matrix_a, matrix_b)
    else:
        raise ValueError(f"Unknown method: {method}")

def hadamard_product(matrix_a, matrix_b):
    """Element-wise multiplication of two matrices."""
    return multiply(matrix_a, matrix_b, method="hadamard")

def broadcast_multiply(matrix_a, matrix_b):
    """Multiply matrices with broadcasting support."""
    return multiply(matrix_a, matrix_b, method="broadcast")
