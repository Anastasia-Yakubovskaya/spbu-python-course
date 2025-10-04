"""
Test module for matrix operations.
Contains unit tests for matrix functions: addition, multiplication, transposition.
"""

import sys
import os

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_1")
sys.path.insert(0, os.path.abspath(project_path))

from matrices import (
    calculate_matrix_sum,
    calculate_matrix_product,
    calculate_matrix_transpose,
)


def test_calculate_matrix_sum():
    """
    Test matrix addition with various cases.

    Test cases:
    - Basic 2x2 matrices
    - 1x1 matrices
    - Matrices with negative numbers
    """
    # Test basic 2x2 matrices
    matrix_a = [[1.0, 2.0], [3.0, 4.0]]
    matrix_b = [[5.0, 6.0], [7.0, 8.0]]
    expected_result = [[6.0, 8.0], [10.0, 12.0]]
    assert calculate_matrix_sum(matrix_a, matrix_b) == expected_result

    # Test 1x1 matrices
    matrix_c = [[5.0]]
    matrix_d = [[3.0]]
    assert calculate_matrix_sum(matrix_c, matrix_d) == [[8.0]]

    # Test matrices with negative numbers
    matrix_e = [[-1.0, 2.0], [3.0, -4.0]]
    matrix_f = [[5.0, -6.0], [-7.0, 8.0]]
    expected_negative_result = [[4.0, -4.0], [-4.0, 4.0]]
    assert calculate_matrix_sum(matrix_e, matrix_f) == expected_negative_result


def test_calculate_matrix_product():
    """
    Test matrix multiplication with various cases.

    Test cases:
    - Square matrices multiplication
    - Rectangular matrices multiplication
    - Incompatible matrices (should return None)
    """
    # Test square matrices multiplication
    matrix_a = [[1.0, 2.0], [3.0, 4.0]]
    matrix_b = [[2.0, 0.0], [1.0, 3.0]]
    expected_result = [[4.0, 6.0], [10.0, 12.0]]
    assert calculate_matrix_product(matrix_a, matrix_b) == expected_result

    # Test rectangular matrices multiplication
    matrix_c = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    matrix_d = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
    expected_rectangular_result = [[58.0, 64.0], [139.0, 154.0]]
    assert calculate_matrix_product(matrix_c, matrix_d) == expected_rectangular_result

    # Test incompatible matrices
    matrix_e = [[1.0, 2.0]]
    matrix_f = [[1.0], [2.0], [3.0]]
    assert calculate_matrix_product(matrix_e, matrix_f) is None


def test_calculate_matrix_transpose():
    """
    Test matrix transposition with various cases.

    Test cases:
    - Rectangular matrix transposition
    - Row vector transposition
    - Square matrix transposition
    - Column vector transposition
    """
    # Test rectangular matrix transposition
    rectangular_matrix = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    expected_rectangular_transpose = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    assert (
        calculate_matrix_transpose(rectangular_matrix) == expected_rectangular_transpose
    )

    # Test row vector transposition
    row_vector = [[1.0, 2.0, 3.0]]
    expected_row_transpose = [[1.0], [2.0], [3.0]]
    assert calculate_matrix_transpose(row_vector) == expected_row_transpose

    # Test square matrix transposition
    square_matrix = [[1.0, 2.0], [3.0, 4.0]]
    expected_square_transpose = [[1.0, 3.0], [2.0, 4.0]]
    assert calculate_matrix_transpose(square_matrix) == expected_square_transpose

    # Test column vector transposition
    column_vector = [[1.0], [2.0], [3.0]]
    expected_column_transpose = [[1.0, 2.0, 3.0]]
    assert calculate_matrix_transpose(column_vector) == expected_column_transpose
