from collections.abc import Callable
from typing import Iterable

from .tools import derivative
from .calculator import calculate
from .methods import runge_kutta
from .types import Func, Funcs, Data, Method


class Solver:
    funcs: Funcs
    initial_conditions: dict[str, float]

    def __init__(self, independent_var: str, initial: float):
        self.funcs = dict()
        self.initial_conditions = {independent_var: initial}

    def derivative(self, var: str, initial: float) -> Callable[[Func], Func]:
        def outer(func: Func) -> Func:
            func = derivative(func)
            if var not in [*self.funcs.keys(), *self.initial_conditions.keys()]:
                self.funcs.update({var: func})
                self.initial_conditions.update({var: initial})
            else:
                raise ValueError("Variable is assigned")
            return func

        return outer

    def calculate(
        self,
        step: float,
        end: float | None = None,
        _iter: Iterable | None = None,
        method: Method = runge_kutta,
    ) -> Data:
        return calculate(
            self.funcs, step, end, _iter, method, **self.initial_conditions
        )
