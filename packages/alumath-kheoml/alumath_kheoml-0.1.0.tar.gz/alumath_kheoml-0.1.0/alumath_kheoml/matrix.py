"""
Matrix operations module for the alumath_kheoml package.
"""

import numpy as np

def matrix_multiply(A, B):
    """
    Multiply two matrices of different dimensions.
    
    This function performs matrix multiplication of A and B, where
    A is of shape (m, n) and B is of shape (n, p). The result is a
    matrix of shape (m, p).
    
    Parameters
    ----------
    A : array-like
        First matrix of shape (m, n)
    B : array-like
        Second matrix of shape (n, p)
        
    Returns
    -------
    C : ndarray
        Result of matrix multiplication, shape (m, p)
        
    Raises
    ------
    ValueError
        If the matrices cannot be multiplied due to incompatible shapes
    """
    # Convert to numpy arrays if they aren't already
    A = np.asarray(A)
    B = np.asarray(B)
    
    # Check that the matrices can be multiplied
    if A.shape[1] != B.shape[0]:
        raise ValueError(f"Matrices cannot be multiplied: A has shape {A.shape} and B has shape {B.shape}")
    
    # Perform matrix multiplication
    return np.dot(A, B)

def is_valid_matrix(A):
    """
    Check if the input is a valid matrix.
    
    Parameters
    ----------
    A : array-like
        Input to check if it's a valid matrix
        
    Returns
    -------
    bool
        True if the input is a valid 2D array, False otherwise
    """
    try:
        # Convert to numpy array
        A = np.asarray(A)
        
        # Check if it's 2D
        if A.ndim != 2:
            return False
        
        return True
    except:
        return False

class Matrix:
    """
    A class for matrix operations.
    
    Attributes
    ----------
    data : ndarray
        The matrix data
    shape : tuple
        The shape of the matrix (rows, columns)
    """
    
    def __init__(self, data):
        """
        Initialize with matrix data.
        
        Parameters
        ----------
        data : array-like
            Data for the matrix
            
        Raises
        ------
        ValueError
            If the provided data is not a valid 2D array
        """
        if not is_valid_matrix(data):
            raise ValueError("Data must be a valid 2D array")
        
        self.data = np.asarray(data)
        self.shape = self.data.shape
    
    def __repr__(self):
        """
        String representation of the matrix.
        """
        return f"Matrix(shape={self.shape})"
    
    def __str__(self):
        """
        Print-friendly representation of the matrix.
        """
        return f"Matrix of shape {self.shape}:\n{self.data}"
    
    def multiply(self, other):
        """
        Multiply this matrix with another matrix.
        
        Parameters
        ----------
        other : Matrix or array-like
            The matrix to multiply with
            
        Returns
        -------
        Matrix
            The result of the multiplication
            
        Raises
        ------
        ValueError
            If the matrices cannot be multiplied
        """
        if isinstance(other, Matrix):
            other_data = other.data
        else:
            other_data = np.asarray(other)
        
        result = matrix_multiply(self.data, other_data)
        return Matrix(result)
    
    def __matmul__(self, other):
        """
        Implement the @ operator for matrix multiplication.
        
        Parameters
        ----------
        other : Matrix or array-like
            The matrix to multiply with
            
        Returns
        -------
        Matrix
            The result of the multiplication
        """
        return self.multiply(other)
    
    def transpose(self):
        """
        Get the transpose of the matrix.
        
        Returns
        -------
        Matrix
            The transposed matrix
        """
        return Matrix(self.data.T)
