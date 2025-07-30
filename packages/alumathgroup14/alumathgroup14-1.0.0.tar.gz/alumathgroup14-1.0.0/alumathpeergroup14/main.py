class MatrixDimensionError(Exception):
    """Custom error for invalid matrix multiplication."""
    pass


def multiply_matrices(A, B):
    # Validate that both inputs are lists of lists
    if not (isinstance(A, list) and isinstance(B, list)):
        raise MatrixDimensionError("Sorry, peer group 14 does not allow multiplication of non-list objects: Inputs must be lists.")
    
    if not A or not B or not all(isinstance(row, list) for row in A + B):
        raise MatrixDimensionError(" Matrices must be 2D.")

    # Validate dimensions: columns of A == rows of B
    if len(A[0]) != len(B):
        raise MatrixDimensionError("Warning: Emmanuel, Jade, Phinah and Pretty are disappointed. Sorry comrade can't multiply these matrices.")

    # Matrix multiplication
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            value = sum(A[i][k] * B[k][j] for k in range(len(B)))
            row.append(value)
        result.append(row)
    return result
