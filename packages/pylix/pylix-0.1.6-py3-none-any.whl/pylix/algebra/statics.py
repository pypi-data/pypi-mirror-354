from typing import Iterable

import numpy as np

from pylix.errors import TypesTuple, assertion, ArgumentError, ArgumentCodes
from pylix.types import Number, Int

def rnd(x: Number, decimals: Int = 9) -> float:
    """
    Returns the rounded value.

    Renvoie la valeur arrondie.

    :param x: any Number
    :param decimals: an Int which represents the willed decimals (standard is 8)
    :return:
    """
    assertion.assert_types(x, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
    assertion.assert_types(decimals, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
    return float(np.round(x, decimals))

def average(iterable: Iterable[Number]):
    """
    This function calculates the average value of an iterable.

    Ca fonction calcule l'intersection d'iterable.

    :param iterable: any iterable which is filled with numbers.
    :return:
    """
    assertion.assert_type(iterable, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
    total: Number = 0
    len_: int = 0
    for value in iterable:
        assertion.assert_types(value, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        total += value
        len_ += 1
    return rnd(total / len_)

def variance(iterable: Iterable[Number]):
    """
    This function calculates the variance of an iterable.

    Ca fonction calcule la variance d'iterable.

    :param iterable: any iterable which is filled with numbers
    :return:
    """
    assertion.assert_type(iterable, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
    av = average(iterable)
    total: Number = 0
    len_ = 0
    for value in iterable:
        total += (value - av) ** 2
        len_ += 1
    return rnd(total / len_)

def std(iterable: Iterable[Number]):
    """
    This function calculates the standard deviation of an iterable.

    Ca fonction calcule l'écart-type d'iterable.

    :param iterable: any iterable which is filled with numbers
    :return:
    """
    assertion.assert_type(iterable, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
    return rnd(variance(iterable) ** (1/2))
