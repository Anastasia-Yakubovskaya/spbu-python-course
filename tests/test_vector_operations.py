"""
Test module for vector operations.

Contains unit tests for vector functions: scalar product, length calculation, angle between vectors.
"""

import sys
import os
import math

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "project"))

from vector import (
    calculate_scalar_product,
    calculate_vector_length,
    calculate_angle_between_vectors,
)


def test_calculate_scalar_product():
    """
    Test scalar product calculation with various cases.
    """
    # Test with positive numbers
    first_vector = [1.0, 2.0, 3.0]
    second_vector = [4.0, 5.0, 6.0]
    expected_result = 1.0 * 4.0 + 2.0 * 5.0 + 3.0 * 6.0
    assert calculate_scalar_product(first_vector, second_vector) == expected_result

    # Test with zero vector
    zero_vector = [0.0, 0.0, 0.0]
    normal_vector = [1.0, 2.0, 3.0]
    assert calculate_scalar_product(zero_vector, normal_vector) == 0.0

    # Test with negative numbers
    vector_with_negatives = [-1.0, 2.0, -3.0]
    mixed_sign_vector = [4.0, -5.0, 6.0]
    expected_negative_result = (-1.0) * 4.0 + 2.0 * (-5.0) + (-3.0) * 6.0
    assert (
        calculate_scalar_product(vector_with_negatives, mixed_sign_vector)
        == expected_negative_result
    )


def test_calculate_vector_length():
    """
    Test vector length calculation with various cases.
    """
    # Test with 2D vector
    two_dimensional_vector = [3.0, 4.0]
    expected_length = 5.0
    assert calculate_vector_length(two_dimensional_vector) == expected_length

    # Test with unit vector
    unit_vector = [1.0, 0.0, 0.0]
    assert calculate_vector_length(unit_vector) == 1.0

    # Test with single element vector
    single_element_vector = [5.0]
    assert calculate_vector_length(single_element_vector) == 5.0

    # Test with zero vector
    zero_vector = [0.0, 0.0, 0.0, 0.0]
    assert calculate_vector_length(zero_vector) == 0.0


def test_calculate_angle_between_vectors():
    """
    Test angle calculation between vectors with various cases.
    """
    # Test 45 degree angle
    forty_five_degree_vector = [1.0, 1.0]
    horizontal_vector = [1.0, 0.0]
    expected_forty_five_degrees = math.pi / 4.0
    assert math.isclose(
        calculate_angle_between_vectors(forty_five_degree_vector, horizontal_vector),
        expected_forty_five_degrees,
        abs_tol=0.0001,
    )

    # Test 60 degree angle
    sixty_degree_vector = [1.0, math.sqrt(3)]
    another_horizontal_vector = [2.0, 0.0]
    expected_sixty_degrees = math.pi / 3.0
    assert math.isclose(
        calculate_angle_between_vectors(sixty_degree_vector, another_horizontal_vector),
        expected_sixty_degrees,
        abs_tol=0.0001,
    )

    # Test perpendicular vectors
    first_perpendicular_vector = [1.0, 0.0]
    second_perpendicular_vector = [0.0, 1.0]
    expected_right_angle = math.pi / 2.0
    assert math.isclose(
        calculate_angle_between_vectors(
            first_perpendicular_vector, second_perpendicular_vector
        ),
        expected_right_angle,
        abs_tol=0.0001,
    )

    # Test parallel vectors
    original_vector = [1.0, 2.0]
    scaled_vector = [2.0, 4.0]
    assert math.isclose(
        calculate_angle_between_vectors(original_vector, scaled_vector),
        0.0,
        abs_tol=0.0001,
    )

    # Test opposite vectors
    forward_vector = [1.0, 0.0]
    backward_vector = [-1.0, 0.0]
    expected_straight_angle = math.pi
    assert math.isclose(
        calculate_angle_between_vectors(forward_vector, backward_vector),
        expected_straight_angle,
        abs_tol=0.0001,
    )
