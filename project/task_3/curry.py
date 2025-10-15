from typing import Callable, Any, Union


def curry_explicit(func: Callable, arity: int) -> Callable:
    """
    Curry a function explicitly with a fixed arity.

    Transforms a function that takes `arity` arguments into a sequence
    of functions each taking a single argument.

    Parameters:
        func (Callable): The function to curry.
        arity (int): The number of arguments the original function expects.
                     Must be non-negative.

    Returns:
        Callable: A curried version of the input function. If arity is 0,
                  returns a function that calls `func()` with no arguments.
                  Otherwise, returns a chain of functions that collect arguments
                  one by one until `arity` arguments are provided.

    Raises:
        ValueError: If `arity` is negative or if more arguments than `arity`
                    are passed during currying.
    """
    if arity < 0:
        raise ValueError("Arity must be non-negative")

    if arity == 0:

        def zero_arity(*args: Any) -> Any:
            if len(args) > 0:
                raise ValueError("Arity not eq with args")
            return func()

        return zero_arity

    def curried_function(*accumulated_args: Any) -> Union[Any, Callable]:
        if len(accumulated_args) > arity:
            raise ValueError("Arity not eq with args")

        if len(accumulated_args) == arity:
            return func(*accumulated_args)

        def next_curried(next_arg: Any) -> Union[Any, Callable]:
            return curried_function(*accumulated_args, next_arg)

        return next_curried

    def starter() -> Callable:
        return curried_function()

    return starter()


def uncurry_explicit(func: Callable, arity: int) -> Callable:
    """
    Uncurry a curried function explicitly with a fixed arity.

    Transforms a curried function (that takes one argument at a time)
    into a function that takes all `arity` arguments at once.

    Parameters:
        func (Callable): The curried function to uncurry.
        arity (int): The number of arguments the original (uncurried) function
                     is expected to receive. Must be non-negative.

    Returns:
        Callable: A function that accepts `arity` arguments in one call
                  and applies them sequentially to the curried function.

    Raises:
        ValueError: If `arity` is negative or if the number of provided arguments
                    does not exactly match `arity`.
    """
    if arity < 0:
        raise ValueError("Arity must be non-negative")

    def uncurried(*args: Any) -> Any:
        if len(args) != arity:
            raise ValueError("Arity not eq with args")

        current_func = func
        for arg in args:
            current_func = current_func(arg)
        return current_func

    return uncurried
