import copy
import inspect


def smart_args(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        has_isolated = False
        has_evaluated = False

        for name, param in sig.parameters.items():
            default = param.default
            if isinstance(default, tuple):
                if default[0] == "isolated":
                    has_isolated = True
                elif default[0] == "evaluated":
                    has_evaluated = True

        assert not (
            has_isolated and has_evaluated
        ), "Cannot use both Isolated and Evaluated"

        for name, value in bound.arguments.items():
            param = sig.parameters[name]
            default = param.default

            assert not (
                param.kind == param.POSITIONAL_ONLY
                and isinstance(default, tuple)
                and default[0] in ["isolated", "evaluated"]
            ), f"Cannot use {default[0]} for positional arguments"

            if isinstance(default, tuple) and default[0] == "isolated":
                bound.arguments[name] = copy.deepcopy(value)

            elif isinstance(default, tuple) and default[0] == "evaluated":
                if name not in kwargs and list(sig.parameters.keys()).index(
                    name
                ) >= len(args):
                    bound.arguments[name] = default[1]()
        return func(*bound.args, **bound.kwargs)

    return wrapper


def evaluated(func):
    return ("evaluated", func)


def isolated():
    return ("isolated",)
