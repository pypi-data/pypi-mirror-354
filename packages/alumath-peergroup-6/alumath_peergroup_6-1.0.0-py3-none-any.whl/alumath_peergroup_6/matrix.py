"""
Matrix class for representing and manipulating matrices.
"""

from typing import List, Union, Tuple
from .exceptions import InvalidMatrixError

class Matrix:
    """
    A class to represent a matrix and provide basic matrix operations.
    """
    
    def __init__(self, data: List[List[Union[int, float]]]):
        """
        Initialize a matrix with the given data.
        
        Args:
            data: A list of lists representing the matrix
            
        Raises:
            InvalidMatrixError: If the input data is not a valid matrix
        """
        self._validate_matrix(data)
        self.data = [row[:] for row in data]  # Deep copy
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
        self.shape = (self.rows, self.cols)
    
    def _validate_matrix(self, data: List[List[Union[int, float]]]) -> None:
        """Validate that the input data represents a valid matrix."""
        if not isinstance(data, list):
            raise InvalidMatrixError("Matrix data must be a list")
        
        if not data:
            raise InvalidMatrixError("Matrix cannot be empty")
        
        if not all(isinstance(row, list) for row in data):
            raise InvalidMatrixError("All rows must be lists")
        
        row_length = len(data[0])
        if not all(len(row) == row_length for row in data):
            raise InvalidMatrixError("All rows must have the same length")
        
        for i, row in enumerate(data):
            for j, element in enumerate(row):
                if not isinstance(element, (int, float)):
                    raise InvalidMatrixError(f"Element at ({i}, {j}) must be a number")
    
    def get_element(self, row: int, col: int) -> Union[int, float]:
        """Get element at specified position."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        raise IndexError(f"Index ({row}, {col}) out of bounds for matrix of shape {self.shape}")
    
    def set_element(self, row: int, col: int, value: Union[int, float]) -> None:
        """Set element at specified position."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = value
        else:
            raise IndexError(f"Index ({row}, {col}) out of bounds for matrix of shape {self.shape}")
    
    def get_row(self, row: int) -> List[Union[int, float]]:
        """Get a specific row."""
        if 0 <= row < self.rows:
            return self.data[row][:]
        raise IndexError(f"Row {row} out of bounds")
    
    def get_column(self, col: int) -> List[Union[int, float]]:
        """Get a specific column."""
        if 0 <= col < self.cols:
            return [self.data[row][col] for row in range(self.rows)]
        raise IndexError(f"Column {col} out of bounds")
    
    def transpose(self) -> 'Matrix':
        """Return the transpose of the matrix."""
        transposed_data = [[self.data[row][col] for row in range(self.rows)] 
                          for col in range(self.cols)]
        return Matrix(transposed_data)
    
    def copy(self) -> 'Matrix':
        """Return a deep copy of the matrix."""
        return Matrix(self.data)
    
    def __str__(self) -> str:
        """String representation of the matrix."""
        max_width = max(len(str(element)) for row in self.data for element in row)
        rows = []
        for row in self.data:
            formatted_row = [str(element).rjust(max_width) for element in row]
            rows.append("[" + " ".join(formatted_row) + "]")
        return "[\n " + "\n ".join(rows) + "\n]"
    
    def __repr__(self) -> str:
        """Representation of the matrix."""
        return f"Matrix({self.data})"
    
    def __eq__(self, other) -> bool:
        """Check equality with another matrix."""
        if not isinstance(other, Matrix):
            return False
        return self.data == other.data
    
    def __getitem__(self, key) -> Union[List[Union[int, float]], Union[int, float]]:
        """Support indexing like matrix[i][j] or matrix[i]."""
        return self.data[key]
    
    def to_list(self) -> List[List[Union[int, float]]]:
        """Convert matrix to list of lists."""
        return [row[:] for row in self.data]
