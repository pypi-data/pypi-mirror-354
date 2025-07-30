"""
Matrix class implementation
"""

class Matrix:
    def __init__(self, data):
        """
        Initialize a matrix with 2D list data
        
        Args:
            data: 2D list representing the matrix
        """
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise ValueError("Matrix data must be a 2D list")
        
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty")
        
        # Check if all rows have the same length
        row_length = len(data[0])
        if not all(len(row) == row_length for row in data):
            raise ValueError("All rows must have the same length")
        
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __str__(self):
        """String representation of the matrix"""
        return '\n'.join([' '.join(map(str, row)) for row in self.data])
    
    def __repr__(self):
        """Representation of the matrix"""
        return f"Matrix({self.data})"
    
    def get_element(self, row, col):
        """Get element at specific position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        raise IndexError("Matrix index out of range")
    
    def set_element(self, row, col, value):
        """Set element at specific position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = value
        else:
            raise IndexError("Matrix index out of range")
    
    def get_dimensions(self):
        """Return matrix dimensions as (rows, columns)"""
        return (self.rows, self.cols)
    
    def transpose(self):
        """Return the transpose of the matrix"""
        transposed_data = [[self.data[i][j] for i in range(self.rows)] 
                          for j in range(self.cols)]
        return Matrix(transposed_data)