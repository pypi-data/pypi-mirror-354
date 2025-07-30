# AlumathGroup26 - Matrix Calculator Library

A simple and efficient matrix calculator library for Python.

## Features

- Create and manipulate matrices
- Matrix multiplication with dimension validation
- Matrix addition and subtraction
- Matrix transpose
- Easy-to-use API

## Installation

```bash
pip install alumathGroup26
from alumath import Matrix, multiply_matrices

# Create matrices
matrix1 = Matrix([[1, 2], [3, 4]])
matrix2 = Matrix([[5, 6], [7, 8]])

# Multiply matrices
result = multiply_matrices(matrix1, matrix2)
print(result)