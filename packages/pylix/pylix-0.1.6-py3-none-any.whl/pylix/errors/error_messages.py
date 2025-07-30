from typing import Iterable

from pylix.errors.enums import ArgumentCodes, MathCodes, BaseCodes, TypesTuple


ARGUMENT_ERROR_MESSAGES: dict = {
    ArgumentCodes.NONE:
        "There is no information regarding this error.",
    ArgumentCodes.ZERO:
        "The given argument is a zero despite expecting a non zero value.",
    ArgumentCodes.LIST_LAYER_NOT_NUMBER:
        f"The values within the list are not numbers {TypesTuple.NUMBER.value}.",
    ArgumentCodes.OUT_OF_RANGE:
        "The given value is not within the acceptable range.",
    ArgumentCodes.NOT_NUMBER:
        f"The given value is not a number {TypesTuple.NUMBER.value}.",
    ArgumentCodes.NOT_INT:
        f"The given value is a non integer {TypesTuple.INT.value} value.",
    ArgumentCodes.NOT_LISTS:
        f"The given variable is not of the expected lists types: {TypesTuple.LISTS.value}.",
    ArgumentCodes.NOT_POSITIV:
        f"The argument value was below zero (value < 0).",
    ArgumentCodes.LIST_LAYER_NOT_NUMBER_LISTS:
        f"The given value was neither a number nor a list as defined for: {(*TypesTuple.NUMBER.value, *TypesTuple.LISTS.value)}.",
    ArgumentCodes.NOT_MATRIX_NP_ARRAY:
        f"The argument was not an instance of pylix.algebra.Matrix or numpy.ndarray.",
    ArgumentCodes.NOT_EQUAL:
        f"The given value was not equal to some metric.",
    ArgumentCodes.MISMATCH_DIMENSION:
        f"The dimensions of the object did not fit a dimension criteria.",
    ArgumentCodes.NOT_TUPLE_LIST_ND_ARRAY:
        f"The given argument was not an instance of tuple, list, numpy.ndarray.",
    ArgumentCodes.NOT_FLOAT:
        f"The argument was not a float defined as {TypesTuple.FLOAT.TUPLE}.",
    ArgumentCodes.UNEXPECTED_TYPE:
        f"The given argument was of a not expected type.",
    ArgumentCodes.NOT_AXIS:
        f"The argument was expected to be a pylix.algebra.AXIS.",
    ArgumentCodes.NOT_VECTOR3D:
        f"For this operation only 3d vectors can be used. Given argument was not one.",
    ArgumentCodes.NOT_VECTOR:
        f"The given argument was not a pylix.algebra.Vector.",
    ArgumentCodes.NOT_MATRIX:
        f"The given argument was not a pylix.algebra.Matrix.",
    ArgumentCodes.NOT_LISTS_TUPLE:
        f"The given argument was expected to be of type {(*TypesTuple.TUPLE.value, *TypesTuple.LISTS.value)}.",
    ArgumentCodes.NOT_POLYNOMIAL:
        f"The given argument was not a pylix.algebra.Polynomial",
    ArgumentCodes.NOT_INT_BOOl:
        f"The given argument was not in {(*TypesTuple.INT.value, bool)}",
    ArgumentCodes.TOO_BIG:
        f"The given argument was bigger than a limit value.",
    ArgumentCodes.TOO_SMALL:
        f"The given argument was smaller than a limit value.",
    ArgumentCodes.NOT_ITERABLE:
        f"The given value is not an iterable.",
    ArgumentCodes.ITERABLE_LAYER_NOT_NUMBER_LISTS:
        f"The given value was neither a number nor an iterable as defined for: {(*TypesTuple.NUMBER.value, Iterable)}.",
}

MATH_ERROR_MESSAGES: dict = {
    MathCodes.NONE:
        f"There is no information regarding this error.",
    MathCodes.UNFIT_DIMENSIONS:
        f"For this mathematical operations the given argument does not have an acceptable dimension.",
    MathCodes.NOT_MATRIX:
        f"The given argument for the operation was not a pylix.algebra.Matrix.",
    MathCodes.NOT_MATRIX_NUMBER:
        f"The given argument for the operation was not a pylix.algebra.Matrix or {TypesTuple.NUMBER.value}.",
    MathCodes.NOT_NUMBER:
        f"The type of the argument is not in {TypesTuple.NUMBER.value}.",
    MathCodes.NOT_FALSE:
        f"The argument has to be False, but it was not.",
    MathCodes.NOT_POSITIV:
        f"The value should be positiv, but was negativ.",
    MathCodes.NOT_INT:
        f"The value was not an integer defined as {TypesTuple.INT.value}",
    MathCodes.NOT_VECTOR:
        f"The given value was not a pylix.algebra.Vector.",
    MathCodes.NOT_DEFINED:
        f"It was tried to execute an undefined operation (e.g. division by zero).",
    MathCodes.ZERO:
        f"The value is zero, but was not expected to be zero.",
    MathCodes.NOT_VECTOR_NUMBER:
        f"The given argument for the operation was not a pylix.algebra.Vector or {TypesTuple.NUMBER.value}.",
    MathCodes.VECTOR:
        f"The given value was a pylix.algebra.Vector. It was not expected to be one."
}

BASE_ERROR_MESSAGES: dict = {
    BaseCodes.NONE:
        f"There is no information regarding this error.",
    BaseCodes.TODO:
        f"The function or module or co. is yet to be done."
}
