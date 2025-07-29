from functools import wraps

from .types import Data, Funcs, Func


def independent_variable(data: Data, funcs: Funcs) -> str:
    conditions: list[bool] = []

    data_keys = data.keys()
    funcs_keys = funcs.keys()

    conditions.append(len(data_keys) == len(funcs_keys) + 1)

    data_keys_set = set(data_keys)
    funcs_keys_set = set(funcs_keys)

    conditions.append(len(data_keys) == len(data_keys_set))
    conditions.append(len(funcs_keys) == len(funcs_keys_set))

    dif = data_keys_set - funcs_keys_set

    conditions.append(len(dif) == 1)

    if all(conditions):
        return next(iter(dif))
    else:
        raise ValueError("Data should have exactly one independent variable name")


def derivative(func: Func) -> Func:
    @wraps(func)
    def wrapper(*args, **kwargs):
        expected_args = func.__code__.co_varnames[: func.__code__.co_argcount]
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in expected_args}
        return func(*args, **filtered_kwargs)

    return wrapper
