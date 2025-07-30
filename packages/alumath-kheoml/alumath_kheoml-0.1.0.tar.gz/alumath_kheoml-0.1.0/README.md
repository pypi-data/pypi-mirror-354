# alumath_kheoml

A Python library for matrix operations developed at African Leadership University. This package provides efficient matrix operations and was created as part of a mathematics and machine learning course.

## Installation

You can install the package directly from PyPI:

```bash
pip install alumath_kheoml
```

## Usage

### Basic Matrix Operations

```python
import numpy as np
from alumath_kheoml import Matrix, matrix_multiply

# Create matrices
A = Matrix(np.array([[1, 2], [3, 4]]))
B = Matrix(np.array([[5, 6], [7, 8]]))

# Matrix multiplication using function
C = matrix_multiply(A.data, B.data)
print(C)

# Matrix multiplication using Matrix class method
D = A.multiply(B)
print(D)

# Matrix multiplication using @ operator
E = A @ B
print(E)

# Transpose
F = A.transpose()
print(F)
```

### Working with Different Matrix Dimensions

```python
import numpy as np
from alumath_kheoml import Matrix

# Create matrices of different dimensions
A = Matrix(np.array([[1, 2, 3], [4, 5, 6]]))  # 2x3
B = Matrix(np.array([[7, 8], [9, 10], [11, 12]]))  # 3x2

# Multiply them
C = A @ B  # Should result in a 2x2 matrix
print(C)

# This will fail due to incompatible dimensions
try:
    D = B @ A
except ValueError as e:
    print(f"Error: {e}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Group 4 - ALU Math and Machine Learning Course
