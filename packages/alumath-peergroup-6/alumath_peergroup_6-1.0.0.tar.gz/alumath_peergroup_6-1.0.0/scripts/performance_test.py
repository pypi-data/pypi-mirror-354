"""
Performance testing script for the alumath_peergroup_6 library.
"""

import time
import sys
import os

# Add the library to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from alumath_peergroup_6 import Matrix, multiply

def create_test_matrix(rows, cols, value=1):
    """Create a test matrix filled with a specific value."""
    return Matrix([[value for _ in range(cols)] for _ in range(rows)])

def time_operation(operation_name, operation_func):
    """Time an operation and print the result."""
    start_time = time.time()
    result = operation_func()
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"{operation_name}: {execution_time:.4f} seconds")
    return result, execution_time

def performance_test():
    """Run performance tests on different matrix sizes."""
    print("=== Performance Testing ===")
    
    sizes = [(10, 10), (50, 50), (100, 100)]
    
    for rows, cols in sizes:
        print(f"\nTesting {rows}×{cols} matrices:")
        
        # Create test matrices
        matrix_a = create_test_matrix(rows, cols, 2)
        matrix_b = create_test_matrix(cols, rows, 3)
        
        # Test standard multiplication
        result, exec_time = time_operation(
            f"Standard multiplication ({rows}×{cols} × {cols}×{rows})",
            lambda: multiply(matrix_a, matrix_b, method="standard")
        )
        
        # Test Hadamard product (same size matrices)
        matrix_c = create_test_matrix(rows, cols, 4)
        result, exec_time = time_operation(
            f"Hadamard product ({rows}×{cols} ⊙ {rows}×{cols})",
            lambda: multiply(matrix_a, matrix_c, method="hadamard")
        )
        
        # Test scalar multiplication
        scalar = Matrix([[5]])
        result, exec_time = time_operation(
            f"Scalar multiplication ({rows}×{cols} × scalar)",
            lambda: multiply(matrix_a, scalar, method="broadcast")
        )

if __name__ == "__main__":
    performance_test()
