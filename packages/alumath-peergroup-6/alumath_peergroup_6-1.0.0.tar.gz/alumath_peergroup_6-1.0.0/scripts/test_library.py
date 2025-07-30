"""
Test script to demonstrate the alumath_peergroup_6 library functionality.
"""

import sys
import os

# Add the library to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from alumath_peergroup_6 import Matrix, multiply, hadamard_product, broadcast_multiply
from alumath_peergroup_6 import DimensionError, InvalidMatrixError

def test_basic_functionality():
    """Test basic matrix operations."""
    print("=== Testing Basic Functionality ===")
    
    # Create test matrices
    matrix_a = Matrix([[1, 2], [3, 4]])
    matrix_b = Matrix([[5, 6], [7, 8]])
    
    print(f"Matrix A:\n{matrix_a}")
    print(f"Matrix B:\n{matrix_b}")
    
    # Test standard multiplication
    result_standard = multiply(matrix_a, matrix_b, method="standard")
    print(f"Standard multiplication (A × B):\n{result_standard}")
    
    # Test Hadamard product
    result_hadamard = hadamard_product(matrix_a, matrix_b)
    print(f"Hadamard product (A ⊙ B):\n{result_hadamard}")
    
    print()

def test_different_dimensions():
    """Test multiplication with different dimensions."""
    print("=== Testing Different Dimensions ===")
    
    # Test rectangular matrices
    matrix_a = Matrix([[1, 2, 3], [4, 5, 6]])  # 2×3
    matrix_b = Matrix([[7, 8], [9, 10], [11, 12]])  # 3×2
    
    print(f"Matrix A (2×3):\n{matrix_a}")
    print(f"Matrix B (3×2):\n{matrix_b}")
    
    result = multiply(matrix_a, matrix_b, method="standard")
    print(f"A × B (2×2):\n{result}")
    
    # Test with column vector
    column_vector = Matrix([[1], [2], [3]])  # 3×1
    print(f"Column vector (3×1):\n{column_vector}")
    
    result_vector = multiply(matrix_a, column_vector, method="standard")
    print(f"A × column_vector (2×1):\n{result_vector}")
    
    print()

def test_broadcasting():
    """Test broadcasting functionality."""
    print("=== Testing Broadcasting ===")
    
    # Test scalar multiplication
    matrix = Matrix([[1, 2], [3, 4]])
    scalar = Matrix([[3]])
    
    print(f"Matrix:\n{matrix}")
    print(f"Scalar:\n{scalar}")
    
    result_broadcast = broadcast_multiply(matrix, scalar)
    print(f"Matrix × Scalar (broadcasting):\n{result_broadcast}")
    
    # Test row vector broadcasting
    row_vector = Matrix([[2, 3]])  # 1×2
    matrix_2x2 = Matrix([[1, 1], [1, 1]])  # 2×2
    
    print(f"Row vector (1×2):\n{row_vector}")
    print(f"Matrix (2×2):\n{matrix_2x2}")
    
    # This will work with broadcasting
    try:
        result_row = broadcast_multiply(row_vector, matrix_2x2)
        print(f"Row vector × Matrix (broadcasting):\n{result_row}")
    except DimensionError as e:
        print(f"Broadcasting not supported for these dimensions: {e}")
    
    print()

def test_error_handling():
    """Test error handling."""
    print("=== Testing Error Handling ===")
    
    # Test invalid matrix creation
    try:
        invalid_matrix = Matrix([[1, 2], [3]])  # Inconsistent row lengths
    except InvalidMatrixError as e:
        print(f"✓ Caught InvalidMatrixError: {e}")
    
    # Test incompatible dimensions
    try:
        matrix_a = Matrix([[1, 2]])  # 1×2
        matrix_b = Matrix([[3], [4], [5]])  # 3×1
        result = multiply(matrix_a, matrix_b, method="standard")
    except DimensionError as e:
        print(f"✓ Caught DimensionError: {e}")
    
    # Test Hadamard product with different dimensions
    try:
        matrix_a = Matrix([[1, 2]])  # 1×2
        matrix_b = Matrix([[3, 4], [5, 6]])  # 2×2
        result = hadamard_product(matrix_a, matrix_b)
    except DimensionError as e:
        print(f"✓ Caught DimensionError for Hadamard product: {e}")
    
    print()

def test_matrix_properties():
    """Test matrix properties and methods."""
    print("=== Testing Matrix Properties ===")
    
    matrix = Matrix([[1, 2, 3], [4, 5, 6]])
    
    print(f"Matrix:\n{matrix}")
    print(f"Shape: {matrix.shape}")
    print(f"Rows: {matrix.rows}, Columns: {matrix.cols}")
    print(f"Element at (0,1): {matrix.get_element(0, 1)}")
    print(f"Row 0: {matrix.get_row(0)}")
    print(f"Column 1: {matrix.get_column(1)}")
    
    # Test transpose
    transposed = matrix.transpose()
    print(f"Transposed:\n{transposed}")
    
    # Test copy
    matrix_copy = matrix.copy()
    print(f"Copy equals original: {matrix == matrix_copy}")
    
    print()

def run_all_tests():
    """Run all test functions."""
    print("Running alumath_peergroup_6 Library Tests")
    print("=" * 50)
    
    test_basic_functionality()
    test_different_dimensions()
    test_broadcasting()
    test_error_handling()
    test_matrix_properties()
    
    print("All tests completed successfully! 🎉")

if __name__ == "__main__":
    run_all_tests()
