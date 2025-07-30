"""
Matrix operations module for AlumathGroup13
Provides matrix multiplication for different dimensions using pure Python only
"""

def validate_matrices(A, B):
    """
    Validate that matrices can be multiplied using pure Python only
    
    Args:
        A: First matrix (list of lists only)
        B: Second matrix (list of lists only)
    
    Returns:
        tuple: (rows_A, cols_A, rows_B, cols_B)
    
    Raises:
        ValueError: If matrices cannot be multiplied
    """
    # Check if matrices are valid lists
    if not isinstance(A, list) or not isinstance(B, list):
        raise ValueError("Matrices must be lists of lists")
    
    if not A or not B:
        raise ValueError("Matrices cannot be empty")
    
    # Ensure all rows are lists
    if not all(isinstance(row, list) for row in A):
        raise ValueError("Matrix A must be a list of lists")
    if not all(isinstance(row, list) for row in B):
        raise ValueError("Matrix B must be a list of lists")
    
    rows_A = len(A)
    cols_A = len(A[0]) if A else 0
    rows_B = len(B)
    cols_B = len(B[0]) if B else 0
    
    # Validate that all rows have same length
    if not all(len(row) == cols_A for row in A):
        raise ValueError("All rows in matrix A must have the same length")
    if not all(len(row) == cols_B for row in B):
        raise ValueError("All rows in matrix B must have the same length")
    
    # Validate dimensions for multiplication
    if cols_A != rows_B:
        raise ValueError(f"Cannot multiply matrices: {rows_A}x{cols_A} and {rows_B}x{cols_B}. "
                        f"Number of columns in first matrix ({cols_A}) must equal "
                        f"number of rows in second matrix ({rows_B})")
    
    return rows_A, cols_A, rows_B, cols_B

def matrix_multiply(A, B):
    """
    Multiply two matrices using standard matrix multiplication (pure Python only)
    
    Args:
        A: First matrix (list of lists only)
        B: Second matrix (list of lists only)
    
    Returns:
        list: Resulting matrix as list of lists
    
    Examples:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> result = matrix_multiply(A, B)
        >>> print(result)
        [[19, 22], [43, 50]]
    """
    # Validate matrices (pure Python validation)
    rows_A, cols_A, rows_B, cols_B = validate_matrices(A, B)
    
    # Initialize result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    # Perform matrix multiplication using pure Python
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def matrix_info(matrix):
    """
    Get information about a matrix using pure Python only
    
    Args:
        matrix: Input matrix (list of lists only)
    
    Returns:
        dict: Matrix information including dimensions and properties
    """
    if not isinstance(matrix, list):
        raise ValueError("Matrix must be a list of lists")
    
    if not matrix:
        return {"rows": 0, "cols": 0, "is_square": False, "is_empty": True}
    
    rows = len(matrix)
    cols = len(matrix[0]) if matrix else 0
    is_square = rows == cols
    
    return {
        "rows": rows,
        "cols": cols,
        "is_square": is_square,
        "is_empty": False,
        "shape": f"{rows}x{cols}"
    }