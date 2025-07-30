class Matrix:
    """
    A class to represent a mathematical matrix.
    """
    
    def __init__(self, data):
        """
        Initialize a Matrix with the given 2D list of numbers.
        
        Args:
            data (list): A 2D list of numbers representing the matrix
            
        Raises:
            ValueError: If the matrix is empty, not rectangular, or contains invalid elements
            TypeError: If the input is not a list of lists
        """
        # Check if input is a list
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise TypeError("Matrix must be initialized with a 2D list")
        
        # Check for empty matrix
        if not data or not any(data):
            raise ValueError("Matrix cannot be empty")
        
        # Check if all rows have the same length and contain valid elements
        num_cols = len(data[0])
        for i, row in enumerate(data):
            if not isinstance(row, list):
                raise TypeError(f"Row {i} is not a list")
            if len(row) != num_cols:
                raise ValueError(f"All rows must have the same length. Row 0 has {num_cols} elements but row {i} has {len(row)}")
            if not all(isinstance(x, (int, float)) for x in row):
                raise ValueError(f"Matrix elements must be numbers. Invalid element found in row {i}")
        
        self._data = [row[:] for row in data]  # Create a deep copy of the data
        self._rows = len(data)
        self._cols = num_cols
    
    @property
    def rows(self):
        """Get the number of rows in the matrix."""
        return self._rows
    
    @property
    def cols(self):
        """Get the number of columns in the matrix."""
        return self._cols
    
    @property
    def shape(self):
        """Get the shape of the matrix as a tuple (rows, cols)."""
        return (self._rows, self._cols)
    
    def get(self, row, col):
        """
        Get the element at the specified position.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            
        Returns:
            The element at the specified position
            
        Raises:
            IndexError: If indices are out of bounds
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"Indices ({row}, {col}) out of bounds for matrix of shape {self.shape}")
        return self._data[row][col]
    
    def set(self, row, col, value):
        """
        Set the element at the specified position.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            value (int/float): New value to set
            
        Raises:
            IndexError: If indices are out of bounds
            TypeError: If value is not a number
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"Indices ({row}, {col}) out of bounds for matrix of shape {self.shape}")
        if not isinstance(value, (int, float)):
            raise TypeError("Matrix elements must be numbers")
        self._data[row][col] = value
    
    def __str__(self):
        """Return a string representation of the matrix."""
        return '\n'.join([' '.join(map(str, row)) for row in self._data])
    
    def __repr__(self):
        """Return a string representation that can be used to recreate the matrix."""
        return f"Matrix({self._data})"
    
    def __eq__(self, other):
        """Check if two matrices are equal."""
        if not isinstance(other, Matrix) or self.shape != other.shape:
            return False
        return all(self._data[i][j] == other._data[i][j] 
                  for i in range(self._rows) for j in range(self._cols))
