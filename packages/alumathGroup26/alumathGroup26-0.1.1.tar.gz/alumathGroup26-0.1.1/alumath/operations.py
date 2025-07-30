"""
Matrix operations implementation
"""

from .matrix import Matrix

def multiply_matrices(matrix1, matrix2):
    """
    Multiply two matrices
    
    Args:
        matrix1: First Matrix object
        matrix2: Second Matrix object
    
    Returns:
        Matrix: Result of matrix multiplication
    
    Raises:
        ValueError: If matrices cannot be multiplied
    """
    if not isinstance(matrix1, Matrix) or not isinstance(matrix2, Matrix):
        raise TypeError("Both arguments must be Matrix objects")
    
    if matrix1.cols != matrix2.rows:
        raise ValueError(f"Cannot multiply matrices: {matrix1.rows}x{matrix1.cols} and {matrix2.rows}x{matrix2.cols}")
    
    # Initialize result matrix with zeros
    result_data = [[0 for _ in range(matrix2.cols)] for _ in range(matrix1.rows)]
    
    # Perform matrix multiplication
    for i in range(matrix1.rows):
        for j in range(matrix2.cols):
            for k in range(matrix1.cols):
                result_data[i][j] += matrix1.data[i][k] * matrix2.data[k][j]
    
    return Matrix(result_data)

def add_matrices(matrix1, matrix2):
    """
    Add two matrices
    
    Args:
        matrix1: First Matrix object
        matrix2: Second Matrix object
    
    Returns:
        Matrix: Result of matrix addition
    """
    if not isinstance(matrix1, Matrix) or not isinstance(matrix2, Matrix):
        raise TypeError("Both arguments must be Matrix objects")
    
    if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
        raise ValueError("Matrices must have the same dimensions for addition")
    
    result_data = [[matrix1.data[i][j] + matrix2.data[i][j] 
                   for j in range(matrix1.cols)] 
                  for i in range(matrix1.rows)]
    
    return Matrix(result_data)

def subtract_matrices(matrix1, matrix2):
    """
    Subtract two matrices
    
    Args:
        matrix1: First Matrix object
        matrix2: Second Matrix object
    
    Returns:
        Matrix: Result of matrix subtraction
    """
    if not isinstance(matrix1, Matrix) or not isinstance(matrix2, Matrix):
        raise TypeError("Both arguments must be Matrix objects")
    
    if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
        raise ValueError("Matrices must have the same dimensions for subtraction")
    
    result_data = [[matrix1.data[i][j] - matrix2.data[i][j] 
                   for j in range(matrix1.cols)] 
                  for i in range(matrix1.rows)]
    
    return Matrix(result_data)