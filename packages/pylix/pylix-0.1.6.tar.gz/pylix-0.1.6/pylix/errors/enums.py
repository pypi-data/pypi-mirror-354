import numpy as np

from enum import Enum

class TypesTuple(Enum):
    INT = (int, np.integer)
    FLOAT = (float, np.floating)
    NUMBER = (*INT, *FLOAT)
    LIST = (list,)
    TUPLE = (tuple,)
    ND_ARRAY = (np.ndarray,)
    LISTS = (*LIST, *ND_ARRAY)

class BaseCodes(Enum):
    NONE = 0
    TODO = 1

class ArgumentCodes(Enum):
    NONE = 0
    ZERO = 1
    LIST_LAYER_NOT_NUMBER = 2
    OUT_OF_RANGE = 3
    NOT_NUMBER = 4
    NOT_INT = 5
    NOT_LISTS = 6
    NOT_POSITIV = 7
    LIST_LAYER_NOT_NUMBER_LISTS = 8
    NOT_MATRIX_NP_ARRAY = 9
    NOT_EQUAL = 10
    MISMATCH_DIMENSION = 11
    NOT_TUPLE_LIST_ND_ARRAY = 12
    NOT_FLOAT = 13
    UNEXPECTED_TYPE = 14
    NOT_AXIS = 15
    NOT_VECTOR3D = 16
    NOT_VECTOR = 17
    NOT_MATRIX = 18
    NOT_LISTS_TUPLE = 19
    NOT_BOOl = 20
    NOT_POLYNOMIAL = 21
    NOT_INT_BOOl = 22
    TOO_BIG = 23
    TOO_SMALL = 24
    NOT_ITERABLE = 25
    ITERABLE_LAYER_NOT_NUMBER_LISTS = 26

class MathCodes(Enum):
    NONE = 0
    UNFIT_DIMENSIONS = 1
    NOT_MATRIX = 2
    NOT_MATRIX_NUMBER = 3
    NOT_NUMBER = 4
    NOT_FALSE = 5
    NOT_POSITIV = 6
    NOT_INT = 7
    NOT_VECTOR = 8
    NOT_DEFINED = 9
    ZERO = 10
    NOT_VECTOR_NUMBER = 11
    VECTOR = 12
