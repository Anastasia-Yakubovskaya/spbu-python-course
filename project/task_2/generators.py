"""
Lazy Stream Processing System

This module implements a system for lazy stream processing using Python generators.
The system includes:
- Data stream generation from various sources
- Pipeline for applying sequence of operations
- Support for built-in functions (map, filter, zip, reduce, etc.)
- Support for custom user-defined functions
- Result aggregation into different collection types

All operations are applied lazily, processing data on-demand without loading
entire datasets into memory.
"""

from typing import Callable, Generator, Any, Iterable
from functools import reduce


def create_data_stream(data_source: Iterable) -> Generator[Any, None, None]:
    """
    Create a lazy data stream from an iterable data source.

    Parameters:
        data_source (Iterable): Source iterable data (list, tuple, range, generator, etc.)

    Returns:
        Generator[Any, None, None]: Generator yielding items from the source
    """
    yield from data_source


def create_operation_adapter(
    func: Callable, *args, **kwargs
) -> Callable[[Generator], Generator]:
    """
    Create an adapter for any function to work with the processing pipeline.

    Parameters:
        func (Callable): Function to adapt (map, filter, zip, reduce, enumerate, or custom)
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Callable[[Generator], Generator]: Adapted function that takes a generator
                                        and returns a generator
    """

    def apply_adapted_operation(input_generator: Generator) -> Generator:
        """
        Apply the adapted operation to the input generator.

        Parameters:
            input_generator (Generator): Input data generator

        Yields:
            Any: Processed data items
        """
        if func.__name__ in ["map", "filter", "zip", "enumerate"]:
            yield from func(*args, input_generator, **kwargs)

        elif func.__name__ == "reduce":
            list_data = list(input_generator)
            if not list_data and not args:
                raise TypeError("Error")
            if args:
                reduction_func = args[0]
                initial = args[1] if len(args) > 1 else None
                if initial is None:
                    result = reduce(reduction_func, list_data)
                else:
                    result = reduce(reduction_func, list_data, initial)
            else:
                result = reduce(func, list_data, **kwargs)
            yield result
        else:
            yield from func(input_generator, *args, **kwargs)

    return apply_adapted_operation


def apply_processing_pipeline(
    input_generator: Generator, *operations: Callable
) -> Generator:
    """
    Apply a sequence of processing operations to a data stream in a lazy manner.

    Parameters:
        input_generator (Generator): Source data generator
        *operations (Callable): Sequence of operations to apply to the data stream

    Returns:
        Generator: Resulting generator after applying all operations
    """
    current_stream = input_generator
    for operation in operations:
        current_stream = operation(current_stream)

    return current_stream


def collect_processed_results(
    processed_stream: Generator,
    result_collector: Callable = list,
    *collection_args: Any,
    **collection_kwargs: Any
) -> Any:
    """
    Collect the results of a processed data stream into a specified collection type.

    Parameters:
        processed_stream (Generator): Processed data generator from pipeline
        result_collector (Callable): Collection type or function (list, set, tuple, dict, etc.)
        *collection_args: Positional arguments for the collector
        **collection_kwargs: Keyword arguments for the collector

    Returns:
        Any: Collected data in the specified format
    """
    return result_collector(processed_stream, *collection_args, **collection_kwargs)
