"""
Matrix operations including various multiplication methods.
"""

from typing import List, Union
from .matrix import Matrix
from .exceptions import DimensionError

class MatrixOperations:
    """
    A class containing various matrix multiplication operations.
    """
    
    def standard_multiply(self, matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        """
        Perform standard matrix multiplication (A × B).
        
        Args:
            matrix_a: First matrix (m × n)
            matrix_b: Second matrix (n × p)
            
        Returns:
            Matrix: Result matrix (m × p)
            
        Raises:
            DimensionError: If matrices cannot be multiplied
        """
        if matrix_a.cols != matrix_b.rows:
            raise DimensionError(
                f"Cannot multiply matrices of shapes {matrix_a.shape} and {matrix_b.shape}. "
                f"Number of columns in first matrix ({matrix_a.cols}) must equal "
                f"number of rows in second matrix ({matrix_b.rows})."
            )
        
        result_data = []
        for i in range(matrix_a.rows):
            row = []
            for j in range(matrix_b.cols):
                element = sum(matrix_a.get_element(i, k) * matrix_b.get_element(k, j) 
                            for k in range(matrix_a.cols))
                row.append(element)
            result_data.append(row)
        
        return Matrix(result_data)
    
    def hadamard_product(self, matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        """
        Perform element-wise multiplication (Hadamard product).
        
        Args:
            matrix_a: First matrix
            matrix_b: Second matrix
            
        Returns:
            Matrix: Result matrix with same dimensions
            
        Raises:
            DimensionError: If matrices have different dimensions
        """
        if matrix_a.shape != matrix_b.shape:
            raise DimensionError(
                f"Matrices must have the same dimensions for Hadamard product. "
                f"Got {matrix_a.shape} and {matrix_b.shape}."
            )
        
        result_data = []
        for i in range(matrix_a.rows):
            row = []
            for j in range(matrix_a.cols):
                element = matrix_a.get_element(i, j) * matrix_b.get_element(i, j)
                row.append(element)
            result_data.append(row)
        
        return Matrix(result_data)
    
    def broadcast_multiply(self, matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        """
        Perform multiplication with broadcasting support.
        
        This method supports:
        - Matrix × Scalar (1×1 matrix)
        - Row vector × Matrix
        - Matrix × Column vector
        - Standard matrix multiplication
        
        Args:
            matrix_a: First matrix
            matrix_b: Second matrix
            
        Returns:
            Matrix: Result matrix
        """
        # Scalar multiplication (1×1 matrix)
        if matrix_a.shape == (1, 1):
            return self._scalar_multiply(matrix_a.get_element(0, 0), matrix_b)
        elif matrix_b.shape == (1, 1):
            return self._scalar_multiply(matrix_b.get_element(0, 0), matrix_a)
        
        # Row vector × Matrix
        elif matrix_a.rows == 1 and matrix_a.cols == matrix_b.rows:
            return self.standard_multiply(matrix_a, matrix_b)
        
        # Matrix × Column vector
        elif matrix_b.cols == 1 and matrix_a.cols == matrix_b.rows:
            return self.standard_multiply(matrix_a, matrix_b)
        
        # Broadcasting for compatible dimensions
        elif self._can_broadcast(matrix_a.shape, matrix_b.shape):
            return self._broadcast_elementwise(matrix_a, matrix_b)
        
        # Standard matrix multiplication
        elif matrix_a.cols == matrix_b.rows:
            return self.standard_multiply(matrix_a, matrix_b)
        
        else:
            raise DimensionError(
                f"Cannot broadcast or multiply matrices of shapes {matrix_a.shape} and {matrix_b.shape}"
            )
    
    def _scalar_multiply(self, scalar: Union[int, float], matrix: Matrix) -> Matrix:
        """Multiply matrix by scalar."""
        result_data = []
        for i in range(matrix.rows):
            row = []
            for j in range(matrix.cols):
                row.append(scalar * matrix.get_element(i, j))
            result_data.append(row)
        return Matrix(result_data)
    
    def _can_broadcast(self, shape_a: tuple, shape_b: tuple) -> bool:
        """Check if two shapes can be broadcast together."""
        # Simple broadcasting rules
        if shape_a == shape_b:
            return True
        
        # One dimension is 1
        if (shape_a[0] == 1 and shape_a[1] == shape_b[1]) or \
           (shape_a[1] == 1 and shape_a[0] == shape_b[0]) or \
           (shape_b[0] == 1 and shape_b[1] == shape_a[1]) or \
           (shape_b[1] == 1 and shape_b[0] == shape_a[0]):
            return True
        
        return False
    
    def _broadcast_elementwise(self, matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        """Perform element-wise multiplication with broadcasting."""
        max_rows = max(matrix_a.rows, matrix_b.rows)
        max_cols = max(matrix_a.cols, matrix_b.cols)
        
        result_data = []
        for i in range(max_rows):
            row = []
            for j in range(max_cols):
                # Get elements with broadcasting
                a_val = matrix_a.get_element(
                    i if matrix_a.rows > 1 else 0,
                    j if matrix_a.cols > 1 else 0
                )
                b_val = matrix_b.get_element(
                    i if matrix_b.rows > 1 else 0,
                    j if matrix_b.cols > 1 else 0
                )
                row.append(a_val * b_val)
            result_data.append(row)
        
        return Matrix(result_data)
