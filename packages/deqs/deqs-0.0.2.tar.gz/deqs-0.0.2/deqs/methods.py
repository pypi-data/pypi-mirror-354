from copy import deepcopy

from .types import Data, Funcs
from .tools import independent_variable


def runge_kutta(
    data: Data, funcs: Funcs, step: float, inplace: bool = True
) -> Data | None:
    if not inplace:
        data = deepcopy(data)
    idp_var = independent_variable(data, funcs)
    variables = funcs.keys()

    k1_kw = {k: data[k][-1] for k in variables}
    k1_kw.update({idp_var: data[idp_var][-1]})
    k1 = {k: step * funcs[k](**k1_kw) for k in variables}

    k2_kw = {k: data[k][-1] + 0.5 * k1[k] for k in variables}
    k2_kw.update({idp_var: data[idp_var][-1] + 0.5 * step})
    k2 = {k: step * funcs[k](**k2_kw) for k in variables}

    k3_kw = {k: data[k][-1] + 0.5 * k2[k] for k in variables}
    k3_kw.update({idp_var: data[idp_var][-1] + 0.5 * step})
    k3 = {k: step * funcs[k](**k3_kw) for k in variables}

    k4_kw = {k: data[k][-1] + k3[k] for k in variables}
    k4_kw.update({idp_var: data[idp_var][-1] + step})
    k4 = {k: step * funcs[k](**k4_kw) for k in variables}

    for k in variables:
        p = (1 / 6) * (k1[k] + 2 * k2[k] + 2 * k3[k] + k4[k])
        data[k].append(data[k][-1] + p)

    data[idp_var].append(data[idp_var][-1] + step)

    if not inplace:
        return data


def straight_euler(
    data: Data, funcs: Funcs, step: float, inplace: bool = True
) -> Data | None:
    if not inplace:
        data = deepcopy(data)
    idp_var = independent_variable(data, funcs)
    variables = funcs.keys()

    var_kw = {k: data[k][-1] for k in variables}
    var_kw.update({idp_var: data[idp_var][-1]})

    for k in variables:
        data[k].append(data[k][-1] + step * funcs[k](**var_kw))
    data[idp_var].append(data[idp_var][-1] + step)

    if not inplace:
        return data


def modified_euler(
    data: Data, funcs: Funcs, step: float, inplace: bool = True
) -> Data | None:
    if not inplace:
        data = deepcopy(data)
    idp_var = independent_variable(data, funcs)
    variables = funcs.keys()

    last_kw = {k: data[k][-1] for k in variables}
    last_kw.update({idp_var: data[idp_var][-1]})

    demi_kw = {k: data[k][-1] + step * funcs[k](**last_kw) for k in variables}
    demi_kw.update({idp_var: data[idp_var][-1] + step / 2})

    for k in variables:
        data[k].append(data[k][-1] + step * funcs[k](**demi_kw))
    data[idp_var].append(data[idp_var][-1] + step)

    if not inplace:
        return data
