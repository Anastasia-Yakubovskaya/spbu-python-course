from typing import List, Optional


def calculate_matrix_sum(
    matrix_a: List[List[float]], matrix_b: List[List[float]]
) -> Optional[List[List[float]]]:
    """
    Add two matrices

    Parameters:
        matrix_a (List[List[float]]): First matrix
        matrix_b (List[List[float]]): Second matrix

    Returns:
        Optional[List[List[float]]]: Sum of matrix a and matrix b
    """
    if not matrix_a or not matrix_b:
        return None

    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        return None

    return [
        [float(matrix_a[i][j] + matrix_b[i][j]) for j in range(len(matrix_a[0]))]
        for i in range(len(matrix_a))
    ]


def calculate_matrix_product(
    matrix_a: List[List[float]], matrix_b: List[List[float]]
) -> Optional[List[List[float]]]:
    """
    Multiplicate two matrices

    Parameters:
        matrix_a (List[List[float]]): First matrix
        matrix_b (List[List[float]]): Second matrix

    Returns:
        Optional[List[List[float]]]: Product of matrix a and matrix b
    """
    if not matrix_a or not matrix_b:
        return None

    if len(matrix_a[0]) != len(matrix_b):
        return None

    result = [[0.0 for _ in range(len(matrix_b[0]))] for _ in range(len(matrix_a))]
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            for k in range(len(matrix_b)):
                result[i][j] += float(matrix_a[i][k] * matrix_b[k][j])

    return result


def calculate_matrix_transpose(
    matrix: List[List[float]],
) -> Optional[List[List[float]]]:
    """
     Transpose a matrix

    Parameters:
        matrix (List[List[float]]): Matrix

    Returns:
        Optional[List[List[float]]]: Transposed matrix
    """
    if not matrix:
        return None

    return [
        [float(matrix[j][i]) for j in range(len(matrix))] for i in range(len(matrix[0]))
    ]
