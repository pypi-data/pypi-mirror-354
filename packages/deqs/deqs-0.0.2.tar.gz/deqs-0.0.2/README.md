# deqs
## Simple library for solving systems of differential equations

### Installation:

```shell
pip install deqs
```

### Usage styles:
- objective:

```python
from deqs import Solver

solver = Solver("t", 0)


@solver.derivative("x", 1)
def dxdt(y: float) -> float:
    return -y


@solver.derivative("y", 1)
def dydt(x: float, y: float) -> float:
    return 2 * x + 2 * y


if __name__ == "__main__":
    data = solver.calculate(step=10**-6, end=5)
    # data = {"t": [0, ...], "x": [1, ...], "y": [1, ...]}
```

- functional:

```python
from deqs import calculate, derivative


@derivative
def dxdt(y: float) -> float:
    return -y


@derivative
def dydt(x: float, y: float) -> float:
    return 2 * x + 2 * y


if __name__ == "__main__":
    data = calculate(
        funcs={"x": dxdt, "y": dydt},
        step=10**-6, end=5,
        t=0, x=1, y=1
    )
    # data = {"t": [0, ...], "x": [1, ...], "y": [1, ...]}
```

The MIT License Copyright @ 2025 belinmikh