from typing import Any, Generator, Iterable, Callable
from functools import reduce


def create_data_stream(data_source: Iterable[Any]) -> Generator[Any, None, None]:
    """
    Create a lazy data stream from an iterable data source.

    Parameters:
        data_source (Iterable[Any]): Source iterable data (list, tuple, range, etc.)

    Yields:
        Generator[Any, None, None]: Generator yielding items from the source
    """
    for data_item in data_source:
        yield data_item


def apply_operations_pipeline(
    input_stream: Generator, *processing_operations: Callable
) -> Generator:
    """
    Apply a sequence of processing operations to a data stream in a lazy manner.

    Parameters:
        input_stream (Generator): Source data generator
        *processing_operations (Callable): Sequence of operations to apply

    Returns:
        Generator: Resulting generator after applying all operations
    """
    processed_stream = input_stream
    for operation in processing_operations:
        processed_stream = operation(processed_stream)
    return processed_stream


def create_mapping_operation(
    transform_function: Callable,
) -> Callable[[Generator], Generator]:
    """
    Create a mapping operation that applies a transformation to each element.

    Parameters:
        transform_function (Callable): Function to transform each element

    Returns:
        Callable[[Generator], Generator]: Operation function for pipeline
    """

    def apply_mapping(input_generator: Generator) -> Generator:
        for input_element in input_generator:
            transformed_element = transform_function(input_element)
            yield transformed_element

    return apply_mapping


def create_filtering_operation(
    filter_condition: Callable[[Any], bool]
) -> Callable[[Generator], Generator]:
    """
    Create a filtering operation that filters elements based on a condition.

    Parameters:
        filter_condition (Callable[[Any], bool]): Filter condition function

    Returns:
        Callable[[Generator], Generator]: Operation function for pipeline
    """

    def apply_filtering(input_generator: Generator) -> Generator:
        for input_element in input_generator:
            if filter_condition(input_element):
                yield input_element

    return apply_filtering


def create_zipping_operation(*additional_iterables) -> Callable[[Generator], Generator]:
    """
    Create a zipping operation that combines multiple iterables with the main generator.

    Parameters:
        *additional_iterables: Additional iterables to zip with the main generator

    Returns:
        Callable[[Generator], Generator]: Operation function for pipeline
    """
    additional_iterators = [iter(iterable) for iterable in additional_iterables]

    def apply_zipping(main_generator: Generator) -> Generator:
        for main_element in main_generator:
            try:
                additional_elements = [
                    next(iterator) for iterator in additional_iterators
                ]
                yield (main_element,) + tuple(additional_elements)
            except StopIteration:
                break

    return apply_zipping


def reduce_data_stream(
    data_stream: Generator, reduction_function: Callable, initial_value: Any = None
) -> Any:
    """
    Reduce a data stream to a single value using a reduction function.

    Parameters:
        data_stream (Generator): Source data generator
        reduction_function (Callable): Reduction function
        initial_value (Any, optional): Initial value for reduction

    Returns:
        Any: Result of the reduction

    Raises:
        TypeError: If data stream is empty and no initial value provided
    """
    materialized_data = list(data_stream)
    if not materialized_data and initial_value is None:
        raise TypeError("reduce() of empty sequence with no initial value")
    if initial_value is None:
        return reduce(reduction_function, materialized_data)
    else:
        return reduce(reduction_function, materialized_data, initial_value)


def create_custom_operation(
    custom_processing_function: Callable[[Generator], Generator]
) -> Callable:
    """
    Create a custom operation from a user-defined generator function.

    Parameters:
        custom_processing_function (Callable[[Generator], Generator]): User-defined operation function

    Returns:
        Callable: Wrapped operation function for pipeline
    """

    def apply_custom_processing(input_generator: Generator) -> Generator:
        return custom_processing_function(input_generator)

    return apply_custom_processing


def collect_results(
    result_stream: Generator,
    result_collector: Callable = list,
    *collector_args: Any,
    **collector_kwargs: Any
) -> Any:
    """
    Collect the results of a data stream into a specified collection type.

    Parameters:
        result_stream (Generator): Result data generator from pipeline
        result_collector (Callable): Collection type or function (list, set, tuple, dict, etc.)
        *collector_args: Positional arguments for the collector
        **collector_kwargs: Keyword arguments for the collector

    Returns:
        Any: Collected data in the specified format
    """
    return result_collector(result_stream, *collector_args, **collector_kwargs)
