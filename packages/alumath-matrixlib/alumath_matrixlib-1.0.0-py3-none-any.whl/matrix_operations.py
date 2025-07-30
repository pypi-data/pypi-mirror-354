def matrix_multiply(a, b):
    """Perform matrix multiplication on two matrices of any compatible dimensions."""
    if len(a[0]) != len(b):
        raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
    
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) 
             for j in range(len(b[0]))] 
             for i in range(len(a))]