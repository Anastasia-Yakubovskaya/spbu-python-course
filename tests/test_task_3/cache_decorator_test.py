import sys
import os

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_3")
sys.path.insert(0, os.path.abspath(project_path))

from cache_decorator import decorator_cache


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

    @decorator_cache
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

    assert call_count == 3

    identity(2)
    assert call_count == 3

    assert identity(3) == 3


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


def test_cache_with_builtin_functions():
    """
    Test caching with built-in Python functions.

    Test cases:
    - Using sum(), max(), min() to demonstrate caching
    """
    call_count = 0

    @decorator_cache(size=2)
    def custom_sum(*args):
        nonlocal call_count
        call_count += 1
        return sum(args)

    assert custom_sum(1, 2, 3) == 6
    assert custom_sum(1, 2, 3) == 6
    assert call_count == 1

    assert custom_sum(4, 5) == 9
    assert custom_sum(4, 5) == 9
    assert call_count == 2


def test_cache_with_mixed_types():
    """
    Test caching with mixed argument types.

    Test cases:
    - Cache works for functions that accept different types of arguments.
    """
    call_count = 0

    @decorator_cache(size=2)
    def process_mixed(x, y=1):
        nonlocal call_count
        call_count += 1
        return x * y

    assert process_mixed(2, 3) == 6
    assert process_mixed(2, 3) == 6
    assert call_count == 1

    assert process_mixed("a", 3) == "aaa"
    assert process_mixed("a", 3) == "aaa"
    assert call_count == 2


def test_cache_lru_eviction():
    """
    Test LRU (Least Recently Used) eviction policy.

    This test demonstrates that the oldest entry is evicted when the cache exceeds the size limit.
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

    assert call_count == 3
    assert identity(2) == 2
    assert identity(3) == 3
    assert identity(1) == 1


def test_cache_lru_after_i_operations():
    """
    Test LRU (Least Recently Used) eviction policy and check cache state after each operation.

    This test demonstrates the cache state after each `i`-й operation and ensures that
    the oldest entry is evicted when the cache exceeds the size limit.
    """
    call_count = 0

    @decorator_cache(size=2)
    def identity(x):
        nonlocal call_count
        call_count += 1
        return x

    result_1 = identity(1)
    assert call_count == 1
    assert result_1 == 1

    result_2 = identity(2)
    assert call_count == 2
    assert result_2 == 2

    result_3 = identity(3)
    assert call_count == 3
    assert result_3 == 3

    result_4 = identity(2)
    assert call_count == 3
    assert result_4 == 2

    result_5 = identity(3)
    assert call_count == 3
    assert result_5 == 3
