"""
Test module for currying functions.
Contains unit tests for curry_explicit and uncurry_explicit functions.
"""

import sys
import os
import pytest

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_3")
sys.path.insert(0, os.path.abspath(project_path))

from curry import curry_explicit, uncurry_explicit


def test_curry_basic_functionality():
    """
    Test basic currying functionality.

    Test cases:
    - Simple binary function currying
    - Function with five arguments
    - Built-in function (max)
    """

    def add(x, y):
        return x + y

    curried_add = curry_explicit(add, 2)
    assert curried_add(2)(3) == 5

    def multiply_five(a, b, c, d, e):
        return a * b * c * d * e

    curried_mult = curry_explicit(multiply_five, 5)
    assert curried_mult(2)(2)(2)(2)(2) == 32

    curried_max = curry_explicit(max, 3)
    assert curried_max(1)(5)(3) == 5


def test_curry_arity_edge_cases():
    """
    Test currying with edge cases of arity.

    Test cases:
    - Arity = 0 (constant function)
    - Arity = 1 (single argument)
    - Negative arity (should raise ValueError)
    """

    def const():
        return "hello"

    curried_const = curry_explicit(const, 0)
    assert curried_const() == "hello"

    with pytest.raises(ValueError, match="Arity must be non-negative"):
        curry_explicit(const, -1)

    def square(x):
        return x * x

    curried_square = curry_explicit(square, 1)
    assert curried_square(5) == 25


def test_curry_argument_validation():
    """
    Test that curried functions enforce correct argument application.

    Test cases:
    - Passing too many arguments at once
    - Passing extra arguments to zero-arity function
    - Partial application followed by correct completion
    """

    def add_two(x, y):
        return x + y

    curried = curry_explicit(add_two, 2)

    intermediate = curried(10)
    assert intermediate(5) == 15

    with pytest.raises(TypeError):
        curried(1, 2)

    def zero():
        return 42

    curried_zero = curry_explicit(zero, 0)
    assert curried_zero() == 42

    with pytest.raises(ValueError, match="Arity not eq with args"):
        curried_zero(1)


def test_uncurry_basic_functionality():
    """
    Test basic uncurrying functionality.

    Test cases:
    - Uncurry a binary curried function
    - Uncurry a five-argument curried function
    - Round-trip: curry → uncurry → same result as original
    """

    def add(x, y):
        return x + y

    curried = curry_explicit(add, 2)
    uncurried = uncurry_explicit(curried, 2)
    assert uncurried(7, 3) == 10

    def prod(a, b, c, d, e):
        return a + b + c + d + e

    curried_prod = curry_explicit(prod, 5)
    uncurried_prod = uncurry_explicit(curried_prod, 5)
    assert uncurried_prod(1, 2, 3, 4, 5) == 15

    def original(a, b, c):
        return a * b - c

    curried_orig = curry_explicit(original, 3)
    uncurried_orig = uncurry_explicit(curried_orig, 3)
    assert original(4, 5, 6) == uncurried_orig(4, 5, 6) == 14


def test_uncurry_argument_validation():
    """
    Test that uncurried functions validate argument count.

    Test cases:
    - Too few arguments
    - Too many arguments
    - Negative arity during uncurry
    """

    def f(x, y):
        return x + y

    curried = curry_explicit(f, 2)
    uncurried = uncurry_explicit(curried, 2)

    with pytest.raises(ValueError, match="Arity not eq with args"):
        uncurried(1)

    with pytest.raises(ValueError, match="Arity not eq with args"):
        uncurried(1, 2, 3)

    with pytest.raises(ValueError, match="Arity must be non-negative"):
        uncurry_explicit(curried, -1)
