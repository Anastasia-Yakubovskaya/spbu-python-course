import copy
import inspect
from typing import Callable, Any


def smart_args(enable_positional: bool = False):
    """
    Decorator that enhances default arguments with `isolated()` and `evaluated()` markers.
    By default, these markers work only with keyword-only arguments.

    Args:
        enable_positional (bool): Allow markers on positional arguments if True.

    Returns:
        Callable: Decorated function.

    Raises:
        AssertionError: On invalid marker usage (e.g., with positional args when disabled).
        ValueError: If an `isolated()` argument is not provided.
    """

    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)

        if not enable_positional:
            for name, param in sig.parameters.items():
                default = param.default
                if isinstance(default, tuple) and default[0] in (
                    "isolated",
                    "evaluated",
                ):
                    if param.kind != param.KEYWORD_ONLY:
                        raise AssertionError(
                            f"Cannot use {default[0]} for positional arguments"
                        )

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments_dict = dict(bound_args.arguments)

            for name, param in sig.parameters.items():
                default = param.default
                current_value = arguments_dict[name]

                is_isolated = isinstance(default, tuple) and default == ("isolated",)
                is_evaluated = (
                    isinstance(default, tuple)
                    and len(default) == 2
                    and default[0] == "evaluated"
                )

                if is_isolated and is_evaluated:
                    raise AssertionError(
                        f"Argument '{name}' cannot be both Isolated and Evaluated"
                    )

                if is_isolated:
                    if current_value == default:
                        raise ValueError(
                            f"Argument '{name}' with Isolated() must be provided"
                        )
                    arguments_dict[name] = copy.deepcopy(current_value)

                elif is_evaluated:
                    if current_value == default:
                        arguments_dict[name] = default[1]()

            return func(**arguments_dict)

        return wrapper

    return decorator


def evaluated(func: Callable) -> tuple:
    """Marks a default argument to be evaluated at call time via `func()`."""
    return ("evaluated", func)


def isolated() -> tuple:
    """Marks a required argument that will be deep-copied on use."""
    return ("isolated",)
