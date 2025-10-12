def curry_explicit(func, arity):
    if arity < 0:
        raise ValueError("Arity must be non-negative")

    def inner(*args):
        if len(args) > arity:
            raise ValueError("Arity not eq with args")

        if len(args) == arity:
            return func(*args)

        def next_curry(x):
            return inner(*(args + (x,)))

        return next_curry

    return inner


def uncurry_explicit(func, arity):
    if arity < 0:
        raise ValueError("Arity must be non-negative")

    def inner(*args):
        if len(args) != arity:
            raise ValueError("Arity not eq with args")

        new_func = func
        for arg in args:
            new_func = new_func(arg)
        return new_func

    return inner
