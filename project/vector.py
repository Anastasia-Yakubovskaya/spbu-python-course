"""
Vector Operations Module

This module provides basic vector operations including:
- Scalar (dot) product calculation
- Vector length calculation
- Angle between vectors calculation

All functions work with vectors represented as lists of floats.
"""

from math import sqrt, acos
from typing import List, Optional


def calculate_scalar_product(
    vector1: List[float], vector2: List[float]
) -> Optional[float]:
    """
    Calculate scalar product of two vectors

    Parameters:
        vector1 (List[float]): First vector
        vector2 (List[float]): Second vector

    Returns:
        Optional[float]: Scalar product of vectors vector1 and vector2
    """
    if len(vector1) != len(vector2):
        return None

    if not vector1 or not vector2:
        return None

    return sum(vector1[i] * vector2[i] for i in range(len(vector1)))


def calculate_vector_length(vector: List[float]) -> float:
    """
    Calculate length of a vector

    Parameters:
        vector (List[float]): Input vector

    Returns:
        float: Length of vector
    """
    if not vector:
        return 0.0

    return sqrt(sum(x**2 for x in vector))


def calculate_angle_between_vectors(
    vector1: List[float], vector2: List[float]
) -> Optional[float]:
    """
    Calculate angle between two vectors

    Parameters:
        vector1 (List[float]): First vector
        vector2 (List[float]): Second vector

    Returns:
        Optional[float]: Angle between vectors in radians
    """

    if len(vector1) != len(vector2):
        return None

    scalar_result = calculate_scalar_product(vector1, vector2)
    if scalar_result is None:
        return None

    length1 = calculate_vector_length(vector1)
    length2 = calculate_vector_length(vector2)

    if length1 == 0 or length2 == 0:
        return None

    denominator = length1 * length2
    if denominator == 0:
        return None

    cos_angle = scalar_result / denominator
    if cos_angle < -1 or cos_angle > 1:
        return None

    return acos(cos_angle)
