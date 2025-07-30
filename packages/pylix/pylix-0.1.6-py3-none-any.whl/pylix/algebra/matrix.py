import math
from typing import override, Optional, Self, Union, List, Iterable
from enum import Enum

import numpy as np

from pylix.errors import deprecated
from pylix.algebra.statics import rnd
from pylix.errors import ArgumentError, MathError, ArgumentCodes, assertion, MathCodes, TypesTuple
from pylix.types import Number, Int, Lists, AllLists

def add_matrix(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]

def sub_matrix(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

def strassen_multiply(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2
    A11 = [[A[i][j] for j in range(mid)] for i in range(mid)]
    A12 = [[A[i][j] for j in range(mid, n)] for i in range(mid)]
    A21 = [[A[i][j] for j in range(mid)] for i in range(mid, n)]
    A22 = [[A[i][j] for j in range(mid, n)] for i in range(mid, n)]

    B11 = [[B[i][j] for j in range(mid)] for i in range(mid)]
    B12 = [[B[i][j] for j in range(mid, n)] for i in range(mid)]
    B21 = [[B[i][j] for j in range(mid)] for i in range(mid, n)]
    B22 = [[B[i][j] for j in range(mid, n)] for i in range(mid, n)]

    M1 = strassen_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_multiply(add_matrix(A21, A22), B11)
    M3 = strassen_multiply(A11, sub_matrix(B12, B22))
    M4 = strassen_multiply(A22, sub_matrix(B21, B11))
    M5 = strassen_multiply(add_matrix(A11, A12), B22)
    M6 = strassen_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]

    return C

def matrix_multiply_opt(A, B):
    m, n = len(A), len(A[0])
    p = len(B[0])
    C = [[0] * p for _ in range(m)]

    for i in range(m):
        for k in range(n):  # Äußere Schleife über `k` verbessert den Cache-Zugriff
            for j in range(p):
                C[i][j] += A[i][k] * B[k][j]

    return C

class Axis(Enum):
    X: int = 0
    Y: int = 1
    Z: int = 2

class Matrix:
    """
    A class representing a mathematical matrix with various operations like addition, subtraction, multiplication,
    and more. The matrix can be created from a 2D list of numbers or initialized as a zero matrix. It supports
    operations with other matrices and scalar values, and provides methods for accessing and modifying matrix
    components. This matrix is iterable.

    Une classe qui représente une matrice mathématique. Elle a différentes méthodes comme l'addition, la soustraction,
    multiplication et plus encore. La matrice peut être créée à partir d'une liste de nombres en 2D ou initialisée en
    tant que matrice zéro. Elle prend en charge les opérations avec d'autres matrices et valeurs scalaires, et fournit
    des méthodes pour accéder aux composants de la matrice et les modifier. Cette matrice est itérable.

    Attributes:
        _data (np.ndarray): A NumPy array holding the matrix data.
        _rows (int): The number of rows in the matrix.
        _columns (int): The number of columns in the matrix.

    """
    def __init__(self, data: Iterable[Iterable[Number]] = None,
                 rows: Int = 2, columns: Int = 2,
                 default_value: Number = 0):
        """
        Creates a 2D Matrix.

        Crée une matrice 2D.

        Args:
            data (Iterable[Iterable[Number]]): A 2D array which holds the components
            columns (int): the number of columns (default 2; If none are given, columns = len(data[0]))
            rows (int): the number of rows (default 2; If none are given, rows = len(data))
            default_value (Number): If no data is given, this value will be used as placeholder. default = 0
        """
        default_data: bool = False
        if data is None:
            data: np.ndarray = np.full((2, 2), default_value)
            default_data = True
        assertion.assert_types(rows, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(columns, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(data, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
        assertion.assert_is_positiv(rows, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(columns, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_not_zero(columns, ArgumentError, code=ArgumentCodes.ZERO)
        assertion.assert_not_zero(rows, ArgumentError, code=ArgumentCodes.ZERO)
        if len(data) > 0:
            assertion.assert_layer_list(data, assertion.assert_types,
                                        {"types": (*TypesTuple.NUMBER.value, Iterable)}, ArgumentError,
                                        code=ArgumentCodes.ITERABLE_LAYER_NOT_NUMBER_LISTS)
        if len(data) > 0 and isinstance(data[0], TypesTuple.LISTS.value):
            for d in data:
                assertion.assert_type(d, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
                assertion.assert_layer_list(d, assertion.assert_types,
                                            {"types": TypesTuple.NUMBER.value}, ArgumentError,
                                            code=ArgumentCodes.LIST_LAYER_NOT_NUMBER)
        if len(data) > 0 and isinstance(data[0], TypesTuple.NUMBER.value):
            for d in data:
                assertion.assert_types(d, TypesTuple.NUMBER.value, ArgumentError,
                                       code=ArgumentCodes.NOT_NUMBER)
            copy_ = list()
            for d in data:
                copy_.append([d])
            data = copy_

        self._rows: int = int(rows)
        self._columns: int = int(columns)

        if not default_data and columns == 2:
            self._columns: int = len(data[0])
        elif not default_data and len(data) > 0 and rows != len(data[0]):
            self._columns: int = len(data[0])
        elif not default_data and len(data) == 0:
            self._columns: int = 0
        if not default_data and rows == 2:
            self._rows: int = len(data)
        elif not default_data and rows != len(data):
            self._rows: int = len(data)

        self._data = np.array(data)
        if default_data and (rows != 2 or columns != 2):
            self._data = np.full((self._rows, self._columns), default_value)

    def get_rows(self) -> int:
        return self._rows

    def get_columns(self) -> int:
        return self._columns

    def get_dimension(self) -> tuple:
        return self._rows, self._columns

    @deprecated("Use matrix[i][j] instead.")
    def get_component(self, row: Int, column: Int) -> float:
        assertion.assert_types(column, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(row, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)

        assertion.assert_range(row, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        assertion.assert_range(column, 0, len(self._data[row]) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        column = int(column)
        row = int(row)
        return float(self._data[row][column])

    @deprecated("Use matrix[i][j] = value instead.")
    def set_component(self, row: Int, column: Int, value: Number) -> None:
        assertion.assert_types(column, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(row, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(value, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)

        assertion.assert_range(row, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        assertion.assert_range(column, 0, len(self._data[row]) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        self._data[row][column] = value

    def get_components(self) -> np.ndarray:
        return self._data.copy()

    def set_components(self, data: Iterable[Iterable[Number]]) -> None:
        assertion.assert_type(data, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
        if len(data) > 0:
            assertion.assert_layer_list(data, assertion.assert_types,
                                        {"types": (*TypesTuple.NUMBER.value, Iterable)}, ArgumentError,
                                        code=ArgumentCodes.ITERABLE_LAYER_NOT_NUMBER_LISTS)
        if len(data) > 0 and isinstance(data[0], TypesTuple.LISTS.value):
            for d in data:
                assertion.assert_type(d, Iterable, ArgumentError, code=ArgumentCodes.NOT_ITERABLE)
                assertion.assert_layer_list(d, assertion.assert_types,
                                            {"types": TypesTuple.NUMBER.value}, ArgumentError,
                                            code=ArgumentCodes.LIST_LAYER_NOT_NUMBER)
        if len(data) > 0 and isinstance(data[0], TypesTuple.NUMBER.value):
            for d in data:
                assertion.assert_types(d, TypesTuple.NUMBER.value, ArgumentError,
                                       code=ArgumentCodes.NOT_NUMBER)
            copy_ = list()
            for d in data:
                copy_.append([d])
            data = copy_
        if len(data) != self._rows:
            self._rows = len(data)
        if len(data) > 0 and len(data[0]) != self._columns:
            self._columns = len(data[0])
        elif len(data[0]) == 0:
            self._columns = 0
        self._data = np.array(data)

    def copy(self) -> Self:
        return Matrix(data=list(self.get_components()))

    def where(self, m: Union[AllLists, Self], for_false: any = -1) -> Self:
        """
        Creates a matrix whose values are defined by the arg matrix / list, which allows the values from self at a position.

        Crée une matrice dont les valeurs sont définies par l'arg Matrix, qui autorise les valeurs de self à une position.

        Args:
            m (Union[AllLists, Self]): The matrix / list which allows
            for_false (any): default = -1. The value for non allowed values.

        Returns:
            Allowed matrix (Matrix): The matrix with only allowed values.

        Raises:
            ArgumentError: If m is not a matrix / list
            ArgumentError: If m has not the same dimensions as self.
            ArgumentError: If m has non number or boolean values.
        """
        assertion.assert_types(m, (*TypesTuple.LISTS.value, *TypesTuple.TUPLE.value, Matrix), ArgumentError,
                               code=ArgumentCodes.NOT_LISTS_TUPLE)
        if isinstance(m, Matrix):
            m = m.get_components()
        tester: list = list()
        for i, row in enumerate(m):
            assertion.assert_equals(len(row), self.get_columns(), ArgumentError, code=ArgumentCodes.NOT_EQUAL)
            assertion.assert_types(row, (*TypesTuple.LISTS.value, *TypesTuple.TUPLE.value, Matrix), ArgumentError,
                                   code=ArgumentCodes.NOT_LISTS_TUPLE)
            tester.append(list())
            for value in row:
                assertion.assert_types(value, (*TypesTuple.NUMBER.value, bool), ArgumentError,
                                       code=ArgumentCodes.NOT_INT_BOOl)
                if isinstance(value, (np.integer, np.floating)):
                    tester[i].append(value > 0)
                    continue
                tester[i].append(bool(value))

        result: Matrix = Matrix(rows=self.get_rows(), columns=self.get_columns())
        for i, rows in enumerate(self):
            for j, value in enumerate(self[i]):
                result[i][j] = value if tester[i][j] else for_false

        return result

    def max_in_column(self, column: Int) -> float:
        assertion.assert_types(column, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(column, 0, self.get_columns()-1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)

        max_: float = float(self[0][column])
        for i in range(self.get_rows()):
            max_: float = max(max_, float(self[i][column]))

        return float(max_)

    def min_in_column(self, column: Int) -> float:
        assertion.assert_types(column, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(column, 0, self.get_columns()-1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)

        min_: float = float(self[0][column])
        for i in range(self.get_rows()):
            min_: float = min(min_, float(self[i][column]))

        return float(min_)

    def sum_in_column(self, column: Int) -> float:
        assertion.assert_types(column, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(column, 0, self.get_columns() - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)

        sum_: float = 0
        for i in range(self.get_rows()):
            sum_ += float(self[i][column])

        return rnd(sum_)

    def max_in_row(self, row: Int) -> float:
        assertion.assert_types(row, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(row, 0, self.get_rows()-1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)

        max_: float = float(self[row][0])
        for i in range(self.get_columns()):
            max_: float = max(max_, float(self[row][i]))

        return float(max_)

    def min_in_row(self, row: Int) -> float:
        assertion.assert_types(row, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(row, 0, self.get_rows()-1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)

        min_: float = float(self[row][0])
        for i in range(self.get_columns()):
            min_: float = min(min_, float(self[row][i]))

        return float(min_)

    def sum_in_row(self, row: Int) -> float:
        assertion.assert_types(row, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(row, 0, self.get_rows()-1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)

        sum_: float = 0
        for i in range(self.get_columns()):
            sum_ += float(self[row][i])

        return rnd(sum_)

    def max(self) -> float:
        max_: float = float(self[0][0])

        for i in range(self.get_rows()):
            for j in range(self.get_columns()):
                max_: float = max(max_, float(self[i][j]))

        return float(max_)

    def min(self) -> float:
        min_: float = float(self[0][0])

        for i in range(self.get_rows()):
            for j in range(self.get_columns()):
                min_: float = min(min_, float(self[i][j]))

        return float(min_)

    def sum(self) -> float:
        sum_: float = 0

        for i in range(self.get_rows()):
            for j in range(self.get_columns()):
                sum_ += float(self[i][j])

        return rnd(sum_)

    @classmethod
    def create_identity_matrix(cls, n: int = 2) -> Self:
        """
        Creates an identity matrix of size n x n.

        Crée une matrice unité.

        Args:
            n (int): The size of the identity matrix. Default is 2.

        Returns:
            Identity matrix (Matrix): A new identity matrix of the specified size.

        Raises:
            ArgumentError: If n is not an integer.
            ArgumentError: If n is not positiv.
        """
        assertion.assert_types(n, TypesTuple.INT.value, ArgumentError,
                               code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(n, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        identity_matrix: np.ndarray = np.zeros(shape=(n, n))
        for i in range(len(identity_matrix)):
            identity_matrix[i][i] = 1
        return Matrix(data=list(identity_matrix))

    @classmethod
    def create_rotation_matrix_2D(cls, theta: Number) -> Self:
        """
        Creates a rotation matrix (counterclockwise) for a 2D vector.

        Crée une matrice de rotation (anti-horaire) pour un 2D vecteur.

        Args:
            theta (float): the angle of rotation in degree.

        Returns:
            A rotation matrix (Matrix): for the angle theta.

        Raises:
            ArgumentError: If theta is not a number (int, float).
            ArgumentError: If theta is smaller 0 or bigger 360.
        """
        assertion.assert_types(theta, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        assertion.assert_range(theta, 0, 360, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        return Matrix([
            [rnd(math.cos(math.radians(theta))), rnd((-1) * math.sin(math.radians(theta)))],
            [rnd(math.sin(math.radians(theta))), rnd(math.cos(math.radians(theta)))]
        ])

    @classmethod
    def create_rotation_matrix_3D(cls, theta: Number, axis: Axis) -> Self:
        """
        Creates a rotation matrix (counterclockwise) for a 3D vector.

        Crée une matrice de rotation (anti-horaire) pour un 3D vecteur.

        Args:
            theta (float): the angle of rotation in degree.
            axis (Axis): the axis for which the rotation matrix should be.

        Returns:
            A rotation matrix (Matrix): for the angle theta.

        Raises:
            ArgumentError: If theta is not a number (int, float).
            ArgumentError: If theta is smaller 0 or bigger 360.
            ArgumentError: If axis not of type Axis.
        """
        assertion.assert_types(theta, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        assertion.assert_range(theta, 0, 360, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        assertion.assert_type(axis, Axis, ArgumentError, code=ArgumentCodes.NOT_AXIS)
        matrix: list = list()
        if axis.value == Axis.X.value:
            matrix: list = [
                [1, 0, 0],
                [0, rnd(math.cos(math.radians(theta))), rnd((-1) * math.sin(math.radians(theta)))],
                [0, rnd(math.sin(math.radians(theta))), rnd(math.cos(math.radians(theta)))]
            ]
        elif axis.value == Axis.Y.value:
            matrix: list = [
                [rnd(math.cos(math.radians(theta))), 0, rnd(math.sin(math.radians(theta)))],
                [0, 1, 0],
                [rnd((-1) * math.sin(math.radians(theta))), 0, rnd(math.cos(math.radians(theta)))]
            ]
        else:
            matrix: list = [
                [rnd(math.cos(math.radians(theta))), rnd((-1) * math.sin(math.radians(theta))), 0],
                [rnd(math.sin(math.radians(theta))), rnd(math.cos(math.radians(theta))), 0],
                [0, 0, 1]
            ]
        return Matrix(matrix)

    def get_invers(self) -> Optional[Self]:
        """
        Creates the inverse matrix for the matrix.

        Crée une matrice inverse pour la matrice.

        Returns:
            An invers matrix (Matrix)

        Raises:
            MathError: if the matrix is not quadratic
        """
        assertion.assert_equals(self._columns, self._rows, MathError, code=MathCodes.UNFIT_DIMENSIONS)
        if np.linalg.det(self.get_components()) != 0:
            invers: np.ndarray = np.linalg.inv(self.get_components())
            return Matrix(data=list(invers))
        return None

    def __eq__(self, other: Union[AllLists, Self]) -> bool:
        if isinstance(other, Matrix):
            if self.get_rows() != other.get_rows() and self.get_columns() != other.get_columns():
                return False
            bools = self.get_components() == other.get_components()
            fin = list()
            for column in bools:
                fin.append(all(column))
            return all(fin)
        elif isinstance(other, np.ndarray):
            if self.get_components().shape != other.shape:
                return False
            bools = self.get_components() == other
            fin = list()
            for column in bools:
                fin.append(all(column))
            return all(fin)
        elif isinstance(other, (*TypesTuple.LISTS.value, *TypesTuple.TUPLE.value)):
            other = list(other)
            for i in other:
                if not isinstance(i, (*TypesTuple.LISTS.value, *TypesTuple.TUPLE.value)):
                    return False

            if len(other) != len(self._data) or len(other[0]) != len(other[0]):
                return False
            for i in other:
                if len(i) != len(other[0]):
                    return False
            for i in range(len(other)):
                for j in range(len(other[0])):
                    if other[i][j] != self._data[i][j]:
                        return False
            return True
        return False

    def __add__(self, other: Self) -> Self:
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX,
                              msg="Only a matrix can be added to a matrix.")
        if self.get_dimension() != other.get_dimension():
            raise MathError(MathCodes.UNFIT_DIMENSIONS, "The dimensions of the matrices do not fit!", other)
        matrixA = self.get_components()
        matrixB = other.get_components()
        return Matrix(data=list(matrixA + matrixB), rows=self._rows, columns=self._columns)

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __iadd__(self, other: Self) -> Self:
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX,
                              msg="Only a matrix can be added to a matrix.")
        if self.get_dimension() != other.get_dimension():
            raise MathError(MathCodes.UNFIT_DIMENSIONS, "The dimensions of the matrices do not fit!", other)
        temp: Matrix = self + other
        self.set_components(temp.get_components())
        return self

    def __sub__(self, other: Self) -> Self:
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX,
                              msg="Only a matrix can be subtracted to a matrix.")
        if self.get_dimension() != other.get_dimension():
            raise MathError(MathCodes.UNFIT_DIMENSIONS, "The dimensions of the matrices do not fit!", other)
        matrixA = self.get_components()
        matrixB = other.get_components()
        return Matrix(list(matrixA - matrixB), columns=self._columns, rows=self._rows)

    def __rsub__(self, other: Self) -> Self:
        assertion.assert_type(other, Matrix, MathError, code=MathCodes.NOT_MATRIX)
        return other - self

    def __isub__(self, other: Self) -> Self:
        temp: Matrix = self - other
        self.set_components(temp.get_components())
        return self

    def __mul__(self, other: Union[Self, *TypesTuple.NUMBER.value]) -> Self:
        assertion.assert_types(other, (Matrix, *TypesTuple.NUMBER.value), MathError, code=MathCodes.NOT_MATRIX_NUMBER,
                               msg="Only matrices, int, float can be multiplied to a matrix.")
        multiplied: Matrix = Matrix()

        if isinstance(other, Matrix):
            assertion.assert_equals(self.get_columns(), other.get_rows(), MathError,
                                    code=MathCodes.UNFIT_DIMENSIONS,
                                    msg="Columns of self do not equal rows of other.")

            a: list = list(self.get_components())
            b: list = list(other.get_components())
            c: list = list()
            if other.get_rows() == 1:
                a: np.ndarray = np.array(a)
                b: np.ndarray = np.array(b)
                c: list = list(np.dot(a, b))
            elif self._rows == self._columns:
                c: list = strassen_multiply(a, b)
            else:
                c: list = matrix_multiply_opt(a, b)
            c_: list = list()
            for ind, column in enumerate(c):
                c_.append(list())
                for row in column:
                    c_[ind].append(rnd(row))
            c = c_
            multiplied.set_components(c)

        if isinstance(other, TypesTuple.NUMBER.value):
            temp: list = list()
            if self._rows > 1:
                for column_index, column in enumerate(self._data):
                    temp.append(list())
                    for component in self._data[column_index]:
                        temp[column_index].append(component * other)
            else:
                for component in self._data:
                    temp.append([component * other])
            multiplied.set_components(temp)
        return multiplied

    def __rmul__(self, other: Union[Self, *TypesTuple.NUMBER.value]) -> Self:
        assertion.assert_types(other, (Matrix, *TypesTuple.NUMBER.value), MathError, code=MathCodes.NOT_MATRIX_NUMBER,
                               msg="Only matrices, int, float can be multiplied to a matrix.")
        multiplied: Matrix = Matrix()

        if isinstance(other, Matrix):
            assertion.assert_equals(other.get_columns(), self.get_rows(), MathError,
                                    code=MathCodes.UNFIT_DIMENSIONS,
                                    msg="Rows of self do not equal columns of other.")

            b: list = list(self.get_components())
            a: list = list(other.get_components())
            c: list = list()
            if self._rows == self._columns:
                c: list = strassen_multiply(a, b)
            else:
                c: list = matrix_multiply_opt(a, b)
            multiplied.set_components(c)

        if isinstance(other, TypesTuple.NUMBER.value):
            temp: list = list()
            if self._rows > 1:
                for column_index, column in enumerate(self._data):
                    temp.append(list())
                    for component in self._data[column_index]:
                        temp[column_index].append(component * other)
            else:
                for component in self._data:
                    temp.append([component * other])
            multiplied.set_components(temp)
        return multiplied

    def __imul__(self, other: Union[Self, *TypesTuple.NUMBER.value]) -> Self:
        assertion.assert_types(other, (Matrix, *TypesTuple.NUMBER.value), MathError, code=MathCodes.NOT_MATRIX_NUMBER,
                               msg="Only matrices, int, float can be multiplied to a matrix.")

        if isinstance(other, Matrix):
            multiplied: Matrix = self * other
            self.set_components(multiplied.get_components())

        if isinstance(other, TypesTuple.NUMBER.value):
            multiplied: Matrix = self * other
            self.set_components(multiplied.get_components())
        return self

    def __truediv__(self, other: Number) -> Self:
        assertion.assert_types(other, TypesTuple.NUMBER.value, MathError,
                               code=MathCodes.NOT_NUMBER)
        assertion.assert_not_zero(other, MathError, code=MathCodes.ZERO, msg="Division by Zero is not defined.")
        return self * (1/other)

    def __itruediv__(self, other: Number) -> Self:
        assertion.assert_types(other, TypesTuple.NUMBER.value, MathError,
                               code=MathCodes.NOT_NUMBER)
        dived: Matrix = self / other
        self.set_components(dived.get_components())
        return self

    def __pow__(self, power: Int, modulo=None) -> Self:
        assertion.assert_false(modulo, MathCodes, code=MathCodes.NOT_FALSE, msg="Modulo not defined.")
        assertion.assert_types(power, TypesTuple.INT.value, MathError, code=MathCodes.NOT_INT)
        assertion.assert_is_positiv(power, MathError, code=MathCodes.NOT_POSITIV)
        multiplied: Matrix = self.copy()
        for _ in range(power-1):
            multiplied *= self
        return multiplied

    def __ipow__(self, other: Int) -> Self:
        multiplied: Matrix = self ** other
        self.set_components(multiplied.get_components())
        return self

    def __str__(self) -> str:
        return f"{self._data}"

    def __repr__(self):
        return f"Matrix at {hex(id(self))} with:\n {self._data}"

    def __iter__(self) -> iter:
        return iter(list(self.get_components()))

    def __getitem__(self, item: Int) -> np.ndarray:
        assertion.assert_types(item, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        if item >= 0:
            assertion.assert_range(item, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
            return self._data[item]
        else:
            assertion.assert_range(len(self._data) + item, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
            return self._data[len(self._data) + item]

    def __len__(self):
        return self.get_rows()
