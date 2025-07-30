# This module provides a function to multiply two matrices.

def multiply_matrices(A, B):
    # Validate matrix shapes
    if len(A[0]) != len(B):
        raise ValueError("Number of columns of A must equal number of rows of B.")
    
    # Result dimensions: rows of A x columns of B
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    # Multiply
    for i in range(len(A)):          
        for j in range(len(B[0])):  
            for k in range(len(B)):  
                result[i][j] += A[i][k] * B[k][j]

    return result
