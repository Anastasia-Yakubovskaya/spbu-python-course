"""
Test module for caching decorator.
Contains unit tests for decorator_cache function with LRU behavior.
"""

import sys
import os

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_3")
sys.path.insert(0, os.path.abspath(project_path))

from cach_decorator import decorator_cache


def test_cache_basic_functionality():
    """
    Test basic caching behavior with repeated calls.

    Test cases:
    - Repeated call with same positional arguments returns cached result
    - Different argument sets are cached separately
    """
    call_count = 0

    @decorator_cache(size=2)
    def add(x, y):
        nonlocal call_count
        call_count += 1
        return x + y

    assert add(1, 2) == 3
    assert call_count == 1

    assert add(1, 2) == 3
    assert call_count == 1

    assert add(3, 4) == 7
    assert call_count == 2


def test_cache_disabled_when_size_zero():
    """
    Test that caching is disabled when size=0.

    Test cases:
    - Function is called every time even with identical arguments
    """
    call_count = 0

    @decorator_cache(size=0)
    def inc(x):
        nonlocal call_count
        call_count += 1
        return x + 1

    assert inc(5) == 6
    assert inc(5) == 6
    assert call_count == 2


def test_cache_with_keyword_arguments():
    """
    Test caching with keyword arguments.

    Test cases:
    - Repeated calls with same keyword arguments use cache
    - Positional and keyword calls are treated as different keys
    """
    call_count = 0

    @decorator_cache(size=2)
    def multiply(x, y=1):
        nonlocal call_count
        call_count += 1
        return x * y

    assert multiply(2, 3) == 6
    assert multiply(2, 3) == 6
    assert call_count == 1

    assert multiply(x=4, y=5) == 20
    assert multiply(x=4, y=5) == 20
    assert call_count == 2


def test_cache_lru_eviction_policy():
    """
    Test LRU (Least Recently Used) eviction behavior.

    Test cases:
    - Oldest entry is evicted when cache exceeds size limit
    - Recently used entries remain in cache
    """
    call_count = 0

    @decorator_cache(size=2)
    def identity(x):
        nonlocal call_count
        call_count += 1
        return x

    identity(1)
    identity(2)
    identity(3)
    identity(2)

    assert call_count == 3


def test_cache_with_special_values():
    """
    Test caching with special argument values.

    Test cases:
    - None as argument value
    - Default parameters with explicit None
    - Variable-length arguments (*args)
    """
    call_count = 0

    @decorator_cache(size=2)
    def process(x, y=None):
        nonlocal call_count
        call_count += 1
        return x if y is None else x + y

    process(5)
    process(5, None)
    process(5, y=None)

    assert call_count == 3

    call_count_var = 0

    @decorator_cache(size=2)
    def sum_args(*args):
        nonlocal call_count_var
        call_count_var += 1
        return sum(args)

    sum_args(1, 2, 3)
    sum_args(1, 2, 3)
    sum_args(4, 5)
    sum_args(1, 2, 3)

    assert call_count_var == 2
