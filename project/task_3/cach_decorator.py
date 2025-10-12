def decorator_cache(size=0):
    def decorator(func):
        if size == 0:
            return func
        cache_dict = {}

        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))

            if key in cache_dict:
                return cache_dict[key]

            result = func(*args, **kwargs)

            cache_dict[key] = result

            if len(cache_dict) > size:
                cache_dict.clear()
                cache_dict[key] = result

            return result

        return wrapper

    return decorator
