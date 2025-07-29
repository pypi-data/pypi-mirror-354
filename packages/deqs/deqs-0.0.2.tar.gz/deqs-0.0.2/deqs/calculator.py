from typing import Iterable

from .methods import runge_kutta
from .tools import independent_variable
from .types import Data, Funcs, Method


def calculate(
    funcs: Funcs,
    step: float,
    end: float | None = None,
    _iter: Iterable | None = None,
    method: Method = runge_kutta,
    **initial_conditions: float,
) -> Data:
    data = {k: [v] for k, v in initial_conditions.items()}
    if not _iter:
        idp_var = independent_variable(data, funcs)
        start = data[idp_var][0]
        _iter = range(int((end - start) / step))
    for _ in _iter:
        method(data, funcs, step, True)
    return data
