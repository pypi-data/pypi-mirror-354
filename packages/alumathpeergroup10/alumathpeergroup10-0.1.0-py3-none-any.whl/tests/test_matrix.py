import pytest
from alumathpeergroup10.matrix import Matrix

def test_matrix_creation():
    """Test creating Matrix objects with valid inputs."""
    # Test with 2x2 matrix
    m1 = Matrix([[1, 2], [3, 4]])
    assert m1.get(0, 0) == 1
    assert m1.get(0, 1) == 2
    assert m1.get(1, 0) == 3
    assert m1.get(1, 1) == 4
    
    # Test with 1x1 matrix
    m2 = Matrix([[5]])
    assert m2.get(0, 0) == 5
    
    # Test with floating point numbers
    m3 = Matrix([[1.5, 2.5], [3.5, 4.5]])
    assert m3.get(0, 0) == 1.5
    assert m3.get(1, 1) == 4.5

def test_matrix_errors():
    """Test error handling for invalid inputs."""
    # Test empty matrix
    with pytest.raises(ValueError, match="Matrix cannot be empty"):
        Matrix([])
    
    # Test non-rectangular matrix
    with pytest.raises(ValueError, match="All rows must have the same length"):
        Matrix([[1, 2], [3]])
    
    # Test non-list input
    with pytest.raises(TypeError, match="must be a 2D list"):
        Matrix("not a matrix")
    
    # Test invalid element type
    with pytest.raises(ValueError, match="Matrix elements must be numbers"):
        Matrix([[1, 2], [3, "four"]])
    
    # Test None input
    with pytest.raises(TypeError, match="cannot be None"):
        Matrix(None)

def test_matrix_properties():
    """Test rows, cols, and shape properties."""
    # Test 2x3 matrix
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.rows == 2
    assert m.cols == 3
    assert m.shape == (2, 3)
    
    # Test 3x1 matrix
    m = Matrix([[1], [2], [3]])
    assert m.rows == 3
    assert m.cols == 1
    assert m.shape == (3, 1)
    
    # Test 1x4 matrix
    m = Matrix([[1, 2, 3, 4]])
    assert m.rows == 1
    assert m.cols == 4
    assert m.shape == (1, 4)

def test_get_set_methods():
    """Test get() and set() methods with valid and invalid indices."""
    m = Matrix([[1, 2], [3, 4]])
    
    # Test valid gets
    assert m.get(0, 0) == 1
    assert m.get(0, 1) == 2
    assert m.get(1, 0) == 3
    assert m.get(1, 1) == 4
    
    # Test valid sets
    m.set(0, 0, 10)
    m.set(0, 1, 20)
    m.set(1, 0, 30)
    m.set(1, 1, 40)
    
    assert m.get(0, 0) == 10
    assert m.get(0, 1) == 20
    assert m.get(1, 0) == 30
    assert m.get(1, 1) == 40
    
    # Test invalid indices for get
    with pytest.raises(IndexError, match="out of bounds"):
        m.get(2, 0)  # row out of bounds
    with pytest.raises(IndexError, match="out of bounds"):
        m.get(0, 2)  # column out of bounds
    with pytest.raises(IndexError, match="out of bounds"):
        m.get(-1, 0)  # negative row
    
    # Test invalid indices for set
    with pytest.raises(IndexError, match="out of bounds"):
        m.set(2, 0, 50)  # row out of bounds
    with pytest.raises(IndexError, match="out of bounds"):
        m.set(0, 2, 50)  # column out of bounds
    
    # Test invalid value type for set
    with pytest.raises(TypeError, match="must be numbers"):
        m.set(0, 0, "not a number")

    # Test negative indices (should be invalid)
    with pytest.raises(IndexError, match="out of bounds"):
        m.get(-1, -1)
    with pytest.raises(IndexError, match="out of bounds"):
        m.set(-1, -1, 100)

def test_string_representations():
    """Test string representations (__str__ and __repr__)."""
    m = Matrix([[1, 2], [3, 4]])
    
    # Test __str__
    assert str(m) == "1 2\n3 4"
    
    # Test __repr__
    assert repr(m) == "Matrix([[1, 2], [3, 4]])"
    
    # Test with floating point numbers
    m = Matrix([[1.5, 2.5], [3.5, 4.5]])
    assert str(m) == "1.5 2.5\n3.5 4.5"
    assert repr(m) == "Matrix([[1.5, 2.5], [3.5, 4.5]])"

def test_equality():
    """Test matrix equality comparison."""
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2], [3, 4]])
    m3 = Matrix([[5, 6], [7, 8]])
    m4 = Matrix([[1, 2, 3], [4, 5, 6]])
    
    # Test equality with same values
    assert m1 == m2
    
    # Test inequality with different values
    assert m1 != m3
    
    # Test with different shapes
    assert m1 != m4
    
    # Test with non-Matrix object
    assert m1 != [[1, 2], [3, 4]]
    
    # Test with None
    assert (m1 == None) is False


def test_matrix_multiplication_basic():
    """Test basic 2x2 matrix multiplication."""
    from alumathpeergroup10.operations import multiply
    
    # Test identity matrix multiplication
    a = Matrix([[1, 0], [0, 1]])
    b = Matrix([[4, 1], [2, 2]])
    result = multiply(a, b)
    assert result.get(0, 0) == 4
    assert result.get(0, 1) == 1
    assert result.get(1, 0) == 2
    assert result.get(1, 1) == 2
    
    # Test non-identity multiplication
    c = Matrix([[1, 2], [3, 4]])
    d = Matrix([[5, 6], [7, 8]])
    result = multiply(c, d)
    assert result.get(0, 0) == 19  # 1*5 + 2*7
    assert result.get(0, 1) == 22  # 1*6 + 2*8
    assert result.get(1, 0) == 43  # 3*5 + 4*7
    assert result.get(1, 1) == 50  # 3*6 + 4*8


def test_matrix_multiplication_different_sizes():
    """Test matrix multiplication with different dimensions."""
    from alumathpeergroup10.operations import multiply
    
    # Test 2x3 × 3x2 = 2x2
    a = Matrix([[1, 2, 3], [4, 5, 6]])
    b = Matrix([[7, 8], [9, 10], [11, 12]])
    result = multiply(a, b)
    assert result.shape == (2, 2)
    assert result.get(0, 0) == 58   # 1*7 + 2*9 + 3*11
    assert result.get(0, 1) == 64   # 1*8 + 2*10 + 3*12
    assert result.get(1, 0) == 139  # 4*7 + 5*9 + 6*11
    assert result.get(1, 1) == 154  # 4*8 + 5*10 + 6*12
    
    # Test 1x3 × 3x1 = 1x1
    c = Matrix([[1, 2, 3]])
    d = Matrix([[4], [5], [6]])
    result = multiply(c, d)
    assert result.shape == (1, 1)
    assert result.get(0, 0) == 32  # 1*4 + 2*5 + 3*6
    
    # Test 3x1 × 1x3 = 3x3
    e = Matrix([[1], [2], [3]])
    f = Matrix([[4, 5, 6]])
    result = multiply(e, f)
    assert result.shape == (3, 3)
    assert result.get(0, 0) == 4   # 1*4
    assert result.get(2, 2) == 18  # 3*6


def test_multiplication_error_handling():
    """Test error handling for invalid matrix multiplications."""
    from alumathpeergroup10.operations import multiply
    
    # Test incompatible dimensions (2x2 × 3x3)
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    with pytest.raises(ValueError) as excinfo:
        multiply(a, b)
    assert "Cannot multiply matrices with shapes (2, 2) and (3, 3)" in str(excinfo.value)
    assert "columns of first matrix (2) must equal rows of second matrix (3)" in str(excinfo.value)
    
    # Test empty matrices
    empty = Matrix([[]])
    with pytest.raises(ValueError, match="Matrix cannot be empty"):
        multiply(empty, a)
    with pytest.raises(ValueError, match="Matrix cannot be empty"):
        multiply(a, empty)
    
    # Test invalid types
    with pytest.raises(TypeError, match="must be a non-empty Matrix or 2D list"):
        multiply("not a matrix", a)
    with pytest.raises(TypeError, match="cannot be None"):
        multiply(None, a)
    
    # Test with non-numeric values
    invalid = Matrix([[1, 2], [3, "four"]])
    with pytest.raises(ValueError, match="Matrix elements must be numbers"):
        multiply(a, invalid)
