from collections import OrderedDict
from typing import Any, Callable


def decorator_cache(size: int = 0) -> Callable:
    """
    Caching decorator that stores up to `size` most recent function call results.
    Disabled when `size` is 0 (default).

    Args:
        size (int): Maximum number of cached results. Must be >= 0.

    Returns:
        Callable: Decorated function with LRU caching enabled.

    """

    def decorator(func: Callable) -> Callable:
        if size == 0:
            return func

        cache: OrderedDict = OrderedDict()

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))

            if key in cache:
                cache.move_to_end(key)
                return cache[key]

            result = func(*args, **kwargs)
            cache[key] = result

            if len(cache) > size:
                cache.popitem(last=False)

            return result

        return wrapper

    return decorator
