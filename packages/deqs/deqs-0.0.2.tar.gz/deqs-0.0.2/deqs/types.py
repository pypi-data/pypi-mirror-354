from collections.abc import Callable

Func = Callable[[*tuple[float, ...]], float]

Data = dict[str, list[float]]
Funcs = dict[str, Func]

Method = Callable[[Data, Funcs, float, bool], Data | None]
