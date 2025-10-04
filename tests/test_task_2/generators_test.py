"""
Test module for lazy stream processing system.
Contains unit tests for generator-based data processing functions.
"""

import pytest
import sys
import os
from functools import reduce

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_2")
sys.path.insert(0, os.path.abspath(project_path))

from generators import (
    create_data_stream,
    create_operation_adapter,
    apply_processing_pipeline,
    collect_processed_results,
)


@pytest.fixture
def sample_numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_strings():
    return ["a", "aa", "aaa", "aaaa"]


def test_create_data_stream():
    """Test data stream creation."""
    stream = create_data_stream([1, 2, 3])
    result = list(stream)
    assert result == [1, 2, 3]


def test_map_operation_adapter(sample_numbers):
    """Test map operation adapter."""
    operation = create_operation_adapter(map, lambda x: x * 2)
    data_stream = create_data_stream(sample_numbers)
    result_stream = operation(data_stream)
    result = list(result_stream)
    assert result == [2, 4, 6, 8, 10]


def test_filter_operation_adapter(sample_numbers):
    """Test filter operation adapter."""
    operation = create_operation_adapter(filter, lambda x: x > 2)
    data_stream = create_data_stream(sample_numbers)
    result_stream = operation(data_stream)
    result = list(result_stream)
    assert result == [3, 4, 5]


def test_reduce_operation_adapter():
    """Test reduce operation adapter."""
    operation = create_operation_adapter(reduce, lambda acc, x: acc + x)
    data_stream = create_data_stream([1, 2, 3, 4])
    result_stream = operation(data_stream)
    result = list(result_stream)
    assert result == [10]


def test_processing_pipeline(sample_numbers):
    """Test processing pipeline with multiple operations."""
    operations = [
        create_operation_adapter(filter, lambda x: x > 1),
        create_operation_adapter(map, lambda x: x * 3),
    ]

    data_stream = create_data_stream(sample_numbers)
    result_stream = apply_processing_pipeline(data_stream, *operations)
    result = list(result_stream)
    assert result == [6, 9, 12, 15]


def test_collect_results_list(sample_numbers):
    """Test result collection as list."""
    data_stream = create_data_stream(sample_numbers)
    result = collect_processed_results(data_stream, list)
    assert result == [1, 2, 3, 4, 5]


def test_collect_results_set():
    """Test result collection as set."""
    data_stream = create_data_stream([1, 2, 2, 3])
    result = collect_processed_results(data_stream, set)
    assert result == {1, 2, 3}


def test_map_operation_with_strings(sample_strings):
    """Test map operation with string data."""
    operation = create_operation_adapter(map, lambda s: s.upper())
    data_stream = create_data_stream(sample_strings)
    result_stream = operation(data_stream)
    result = list(result_stream)
    assert result == ["A", "AA", "AAA", "AAAA"]


def test_filter_operation_with_strings(sample_strings):
    """Test filter operation with string data."""
    operation = create_operation_adapter(filter, lambda s: len(s) > 2)
    data_stream = create_data_stream(sample_strings)
    result_stream = operation(data_stream)
    result = list(result_stream)
    assert result == ["aaa", "aaaa"]


def test_string_processing_pipeline(sample_strings):
    """Test processing pipeline with string operations."""
    operations = [
        create_operation_adapter(filter, lambda s: len(s) > 2),
        create_operation_adapter(map, lambda s: s.upper()),
    ]

    data_stream = create_data_stream(sample_strings)
    result_stream = apply_processing_pipeline(data_stream, *operations)
    result = list(result_stream)
    assert result == ["AAA", "AAAA"]
