"""
Test module for smart_args decorator.
Contains unit tests for Isolated and Evaluated argument markers.
"""

import pytest
import os
import sys

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_3")
sys.path.insert(0, os.path.abspath(project_path))

from smart_args import smart_args, isolated, evaluated


def test_isolated_creates_deep_copy():
    """
    Test that Isolated marker creates a deep copy of the provided argument.

    Test cases:
    - Mutating the argument inside the function does not affect the original object
    - Nested mutable structures are also protected from side effects
    """
    original_data = {"list": [1, 2, 3], "nested": {"key": "value"}}

    @smart_args()
    def test_func(*, data=isolated()):
        data["list"].append(4)
        data["nested"]["modified"] = True
        return data

    result = test_func(data=original_data)

    assert result["list"] == [1, 2, 3, 4]
    assert result["nested"]["modified"] is True

    assert original_data["list"] == [1, 2, 3]
    assert "modified" not in original_data["nested"]


def test_evaluated_calls_function_each_time():
    """
    Test that Evaluated marker calls the function on every invocation.

    Test cases:
    - The wrapped function is executed each time the decorated function is called
    - Different results are returned if the function has side effects
    """
    counter = 0

    def counting_func():
        nonlocal counter
        counter += 1
        return f"value_{counter}"

    @smart_args()
    def test_func(*, val=evaluated(counting_func)):
        return val

    result1 = test_func()
    assert result1 == "value_1"
    assert counter == 1

    result2 = test_func()
    assert result2 == "value_2"
    assert counter == 2


def test_only_keyword_args_by_default():
    """
    Test that Isolated and Evaluated markers are restricted to keyword-only arguments.

    Test cases:
    - Using Isolated with a positional argument raises AssertionError
    - Using Evaluated with a positional argument raises AssertionError
    """
    with pytest.raises(
        AssertionError, match="Cannot use isolated for positional arguments"
    ):

        @smart_args()
        def invalid_func(pos_arg=isolated()):
            pass

    with pytest.raises(
        AssertionError, match="Cannot use evaluated for positional arguments"
    ):

        @smart_args()
        def invalid_func(pos_arg=evaluated(lambda: "default")):
            pass


def test_isolated_requires_argument():
    """
    Test that Isolated marker requires the argument to be provided explicitly.

    Test cases:
    - Function call succeeds when the argument is passed
    - ValueError is raised when the argument is omitted
    """

    @smart_args()
    def test_func(*, req_arg=isolated()):
        return req_arg

    assert test_func(req_arg="test") == "test"

    with pytest.raises(
        ValueError, match="Argument 'req_arg' with Isolated\(\) must be provided"
    ):
        test_func()


def test_usage_examples_from_spec():
    """
    Test examples from the specification to ensure correct behavior.

    Test cases:
    - Isolated marker protects original mutable object from modification
    - Regular default (x=get_random_number()) is computed once at definition time
    - Evaluated marker (y=evaluated(...)) is recomputed on every function call
    - Explicitly passed argument overrides Evaluated default
    """

    @smart_args()
    def check_isolation(*, d=isolated()):
        d["a"] = 0
        return d

    no_mutable = {"a": 10}
    result = check_isolation(d=no_mutable)
    assert result == {"a": 0}
    assert no_mutable == {"a": 10}

    call_count = 0

    def get_random_number():
        nonlocal call_count
        call_count += 1
        return 42

    @smart_args()
    def check_evaluation(*, x=get_random_number(), y=evaluated(get_random_number)):
        return x, y

    x1, y1 = check_evaluation()
    x2, y2 = check_evaluation()

    x3, y3 = check_evaluation(y=150)

    assert x1 == x2 == x3
    assert y1 == y2 == 42
    assert y3 == 150
    assert call_count == 3


def test_isolated_and_evaluated_together():
    """
    Test simultaneous use of Isolated and Evaluated on different arguments.

    Test cases:
    - Isolated argument is deep-copied and does not affect original data
    - Evaluated argument is recomputed on each call
    - Results from different calls are independent
    - Original data remains unchanged across multiple calls
    """
    call_count = 0

    def generate_id():
        nonlocal call_count
        call_count += 1
        return f"id_{call_count}"

    original_data = {"items": [1, 2, 3]}

    @smart_args()
    def process_data(*, data=isolated(), uid=evaluated(generate_id)):
        data["items"].append(uid)
        return data, uid

    result1_data, result1_uid = process_data(data=original_data)
    assert result1_uid == "id_1"
    assert result1_data["items"] == [1, 2, 3, "id_1"]
    assert original_data["items"] == [1, 2, 3]

    result2_data, result2_uid = process_data(data=original_data)
    assert result2_uid == "id_2"
    assert result2_data["items"] == [1, 2, 3, "id_2"]
    assert original_data["items"] == [1, 2, 3]

    assert result1_data is not result2_data
    assert result1_data != result2_data

    assert call_count == 2
