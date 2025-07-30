# alumath_peergroup_6

A comprehensive Python library for matrix multiplication with support for different dimensions and broadcasting.

## Features

- **Standard Matrix Multiplication**: Classic A × B multiplication
- **Element-wise Multiplication**: Hadamard product for same-dimension matrices
- **Broadcasting Support**: Intelligent dimension handling for compatible matrices
- **Comprehensive Error Handling**: Clear error messages for invalid operations
- **Pure Python**: No external dependencies required
- **Type Hints**: Full type annotation support
- **Extensive Documentation**: Complete API documentation and examples

## Installation

\`\`\`bash
pip install alumath_peergroup_6
\`\`\`

## Quick Start

```python
from alumath_peergroup_6 import Matrix, multiply

# Create matrices
matrix_a = Matrix([[1, 2], [3, 4]])
matrix_b = Matrix([[5, 6], [7, 8]])

# Standard matrix multiplication
result = multiply(matrix_a, matrix_b, method="standard")
print(result)

# Element-wise multiplication
result = multiply(matrix_a, matrix_b, method="hadamard")
print(result)

# Broadcasting multiplication
scalar = Matrix([[2]])
result = multiply(matrix_a, scalar, method="broadcast")
print(result)
