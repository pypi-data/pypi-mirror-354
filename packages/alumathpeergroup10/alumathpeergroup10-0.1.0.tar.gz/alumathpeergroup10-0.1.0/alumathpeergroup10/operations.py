from typing import Union, List, Any, Tuple
from .matrix import Matrix

def _validate_input(matrix: Any, name: str = 'input') -> None:
    """Validate matrix input.
    
    Args:
        matrix: Input to validate
        name: Name of the parameter for error messages
        
    Raises:
        TypeError: If input is None or not a valid matrix type
    """
    if matrix is None:
        raise TypeError(f"Peer Group 10 says: {name} cannot be None")
    
    if not (isinstance(matrix, (Matrix, list)) and matrix):
        raise TypeError(f"Peer Group 10 says: {name} must be a non-empty Matrix or 2D list")

def _ensure_matrix(matrix: Any, name: str = 'input') -> Matrix:
    """Convert input to Matrix if it isn't already.
    
    Args:
        matrix: Either a Matrix object or a 2D list
        name: Name of the parameter for error messages
        
    Returns:
        Matrix object
        
    Raises:
        TypeError: If input cannot be converted to a Matrix
    """
    _validate_input(matrix, name)
    
    if isinstance(matrix, Matrix):
        return matrix
        
    try:
        return Matrix(matrix)
    except (TypeError, ValueError) as e:
        raise TypeError(f"Peer Group 10 says: Could not convert {name} to Matrix: {str(e)}")

def multiply(matrix_a: Union[Matrix, List[List[float]]], 
             matrix_b: Union[Matrix, List[List[float]]]) -> Matrix:
    """Multiply two matrices.
    
    Args:
        matrix_a: First matrix (Matrix or 2D list)
        matrix_b: Second matrix (Matrix or 2D list)
        
    Returns:
        New Matrix that is the product of matrix_a and matrix_b
        
    Raises:
        ValueError: If matrices cannot be multiplied (inner dimensions don't match)
        TypeError: If inputs cannot be converted to valid matrices
    """
    # First validate inputs
    if matrix_a is None or matrix_b is None:
        raise TypeError("Peer Group 10 says: Cannot multiply matrices: One or both matrices are None")
    
    # Convert to Matrix objects if they aren't already
    a = Matrix(matrix_a) if not isinstance(matrix_a, Matrix) else matrix_a
    b = Matrix(matrix_b) if not isinstance(matrix_b, Matrix) else matrix_b
    
    # Check for empty matrices
    if a.rows == 0 or a.cols == 0 or b.rows == 0 or b.cols == 0:
        raise ValueError("Peer Group 10 says: Cannot multiply matrices: One or both matrices are empty")
    
    # Validate dimensions for multiplication
    if a.cols != b.rows:
        raise ValueError(
            f"Peer Group 10 says: Cannot multiply matrices with shapes {a.shape} and {b.shape}: "
            f"columns of first matrix ({a.cols}) must equal rows of second matrix ({b.rows})"
        )
    
    # Perform the multiplication
    result = []
    for i in range(a.rows):
        row = []
        for j in range(b.cols):
            # Calculate dot product of row i of a and column j of b
            total = 0
            for k in range(a.cols):
                total += a.get(i, k) * b.get(k, j)
            row.append(total)
        result.append(row)
    
    return Matrix(result)

def add(matrix_a: Union[Matrix, List[List[float]]], 
        matrix_b: Union[Matrix, List[List[float]]]) -> Matrix:
    """Add two matrices.
    
    Args:
        matrix_a: First matrix (Matrix or 2D list)
        matrix_b: Second matrix (Matrix or 2D list)
        
    Returns:
        New Matrix that is the sum of matrix_a and matrix_b
        
    Raises:
        ValueError: If matrices have different shapes
        TypeError: If inputs cannot be converted to valid matrices
    """
    try:
        a = _ensure_matrix(matrix_a, 'first matrix')
        b = _ensure_matrix(matrix_b, 'second matrix')
        
        if a.shape != b.shape:
            raise ValueError(
                f"Peer Group 10 says: Cannot add matrices with different shapes: {a.shape} and {b.shape}"
            )
        
        result = [
            [a.get(i, j) + b.get(i, j) for j in range(a.cols)]
            for i in range(a.rows)
        ]
        
        return Matrix(result)
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            raise ValueError(f"Peer Group 10 says: Matrix addition failed: {str(e)}")
        raise

def subtract(matrix_a: Union[Matrix, List[List[float]]], 
             matrix_b: Union[Matrix, List[List[float]]]) -> Matrix:
    """Subtract one matrix from another.
    
    Args:
        matrix_a: First matrix (Matrix or 2D list)
        matrix_b: Second matrix (Matrix or 2D list)
        
    Returns:
        New Matrix that is matrix_a - matrix_b
        
    Raises:
        ValueError: If matrices have different shapes
        TypeError: If inputs cannot be converted to valid matrices
    """
    try:
        a = _ensure_matrix(matrix_a, 'first matrix')
        b = _ensure_matrix(matrix_b, 'second matrix')
        
        if a.shape != b.shape:
            raise ValueError(
                f"Peer Group 10 says: Cannot subtract matrices with different shapes: {a.shape} and {b.shape}"
            )
        
        result = [
            [a.get(i, j) - b.get(i, j) for j in range(a.cols)]
            for i in range(a.rows)
        ]
        
        return Matrix(result)
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            raise ValueError(f"Peer Group 10 says: Matrix subtraction failed: {str(e)}")
        raise

def transpose(matrix: Union[Matrix, List[List[float]]]) -> Matrix:
    """Transpose a matrix.
    
    Args:
        matrix: Input matrix (Matrix or 2D list)
        
    Returns:
        New Matrix that is the transpose of the input
        
    Raises:
        TypeError: If input cannot be converted to a valid matrix
    """
    try:
        m = _ensure_matrix(matrix, 'input matrix')
        
        # Create a new matrix with swapped rows and columns
        result = [
            [m.get(j, i) for j in range(m.rows)]
            for i in range(m.cols)
        ]
        
        return Matrix(result)
    except Exception as e:
        if not isinstance(e, TypeError):
            raise ValueError(f"Peer Group 10 says: Matrix transpose failed: {str(e)}")
        raise
