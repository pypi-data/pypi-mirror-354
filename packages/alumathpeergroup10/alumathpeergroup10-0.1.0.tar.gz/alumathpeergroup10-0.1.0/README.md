# alumathpeergroup10

A Python library for performing matrix operations with comprehensive error handling and support for various matrix dimensions.

## Installation

```bash
pip install alumathpeergroup10
```

## Quick Start

### Creating and Multiplying Matrices

```python
from alumathpeergroup10 import Matrix, multiply

# Create two 2x2 matrices
matrix_a = Matrix([[1, 2], [3, 4]])
matrix_b = Matrix([[5, 6], [7, 8]])

# Multiply the matrices
result = multiply(matrix_a, matrix_b)
print(result)
# Output:
# 19 22
# 43 50
```

### Working with Different Dimensions

```python
from alumathpeergroup10 import Matrix, multiply

# 2x3 matrix
matrix_c = Matrix([
    [1, 2, 3],
    [4, 5, 6]
])

# 3x2 matrix
matrix_d = Matrix([
    [7, 8],
    [9, 10],
    [11, 12]
])

# Result will be 2x2
result = multiply(matrix_c, matrix_d)
print(result)
# Output:
# 58  64
# 139 154
```

### Error Handling

```python
from alumathpeergroup10 import Matrix, multiply

# Trying to multiply incompatible matrices
matrix_e = Matrix([[1, 2], [3, 4]])
matrix_f = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

try:
    result = multiply(matrix_e, matrix_f)
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Cannot multiply matrices with shapes (2, 2) and (3, 3): 
    # columns of first matrix (2) must equal rows of second matrix (3)
```

## Available Functions

### Matrix Class
- `Matrix(data: List[List[float]])`: Create a new matrix from a 2D list
- `get(row: int, col: int) -> float`: Get element at (row, col)
- `set(row: int, col: int, value: float) -> None`: Set element at (row, col)
- `@property rows -> int`: Number of rows
- `@property cols -> int`: Number of columns
- `@property shape -> Tuple[int, int]`: Matrix dimensions as (rows, cols)

### Matrix Operations
- `multiply(a: Matrix, b: Matrix) -> Matrix`: Matrix multiplication
- `add(a: Matrix, b: Matrix) -> Matrix`: Matrix addition
- `subtract(a: Matrix, b: Matrix) -> Matrix`: Matrix subtraction
- `transpose(matrix: Matrix) -> Matrix`: Matrix transpose

## Error Handling

The library provides detailed error messages for various error conditions:
- Invalid matrix dimensions for operations
- Non-rectangular matrices
- Invalid element types
- Out-of-bounds access
- None or invalid inputs

## License

MIT License - See LICENSE file for details.
