def multiply_matrices(matrix_a, matrix_b):
    """
    Multiplies two matrices (lists of lists).

    Args:
        matrix_a (list of lists): First matrix.
        matrix_b (list of lists): Second matrix.

    Returns:
        list of lists: Result of matrix multiplication.

    Raises:
        ValueError: If matrix dimensions are incompatible.
    """
    # Validate matrix dimensions
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])

    if cols_a != rows_b:
        raise ValueError("Number of columns of Matrix A must equal number of rows of Matrix B.")

    # Create result matrix
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    # Perform multiplication
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]

    return result
