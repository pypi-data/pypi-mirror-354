import random
import numpy as np

from typing import override, Self, Union, Optional, Iterable

from pylix.errors import ArgumentError, MathError, assertion
from pylix.errors import ArgumentCodes,  MathCodes, TODO, TypesTuple
from pylix.errors import deprecated
from pylix.algebra.matrix import Matrix
from pylix.algebra.statics import rnd
from pylix.types import Number, Int, Lists, AllLists


class Vector(Matrix):
    """
        The Vector-class inherits from the Matrix class. It is a simple n-dimensional vector.

        La classe Vecteur hérite de la classe Matrice. Il s'agit d'un simple vecteur à n dimensions.

    """
    def __init__(self, coordinates: Optional[Iterable] = None, dimension: Int = 2, default_value: Number = 0):
        """
        Creates a vector.

        Crée un vecteur.

        Args:
            coordinates (Optional[Iterable]): A list of the coordinates for the vector.
            dimension (int): The dimension of the vector. (default 2; or len(coordinates))
            default_value (Number): The value which will be used, if coordinates is None.
        """
        assertion.assert_types(dimension, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(dimension, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_not_zero(dimension, ArgumentError, code=ArgumentCodes.ZERO)
        d: list = list()
        if coordinates is None:
            coordinates: list = [default_value for _ in range(dimension)]
        if isinstance(coordinates, tuple):
            coordinates = list(coordinates)
        assertion.assert_types(coordinates, TypesTuple.LISTS.value, ArgumentError, code=ArgumentCodes.NOT_LISTS)
        for coord in coordinates:
            if isinstance(coord, TypesTuple.NUMBER.value):
                d.append([coord])
            elif isinstance(coord, TypesTuple.LISTS.value):
                d.append([coord[0]])
            else:
                raise ArgumentError(ArgumentCodes.UNEXPECTED_TYPE, wrong_argument=type(coord))
        super().__init__(data=d, rows=dimension, columns=1)

    def cross(self, vec: Self) -> Self:
        """
            Computes the cross product of the vector with another 3D vector.

            Calcule le produit vectoriel de 2 vecteurs.

            Args:
                vec (Vector): The vector to compute the cross product with.

            Raises:
                ArgumentError: If `vec` is not of type Vector.
                MathError: If either vector does not have a dimension of 3.

            Returns:
                Vector: The resulting vector from the cross product.
        """
        assertion.assert_type(vec, Vector, ArgumentError, code=ArgumentCodes.NOT_VECTOR)
        assertion.assert_equals(vec.get_dimension(), 3, MathError, code=MathCodes.UNFIT_DIMENSIONS)
        assertion.assert_equals(self.get_dimension(), 3, MathError, code=MathCodes.UNFIT_DIMENSIONS)
        a, b, c = vec.get_data()
        d, e, f = self.get_data()
        return Vector([
            e * c - f * b,
            f * a - d * c,
            d * b - e * a
        ])

    @classmethod
    def from_matrix(cls, matrix: Matrix) -> Self:
        """
        Transforms a matrix into a vector.

        Transforme une matrice en un vecteur.

        Args:
            matrix (Matrix): The Matrix to transform into a vector.

        Raises:
            ArgumentError: If `matrix` is not of type Matrix.
            ArgumentError: If either matrix does not have 1 row.

        Returns:
            Vector: The resulting vector from the transformation.
        """
        assertion.assert_type(matrix, Matrix, ArgumentError, code=ArgumentCodes.NOT_MATRIX)
        assertion.assert_equals(matrix.get_columns(), 1, ArgumentError,
                                code=ArgumentCodes.MISMATCH_DIMENSION)
        coordinates: list = list()
        for component in matrix.get_components():
            coordinates.append(component[0])
        return Vector(coordinates, len(coordinates))

    @classmethod
    def sample(cls, vec: Self, len_output: int) -> Self:
        """
        Creates a vector of the size n with random data from the input vector.

        Crée un vecteur de taille n avec des données aléatoires provenant du vecteur d'entrée.

        Args:
            vec (Vector): The vector from which you want a sample.
            len_output (int): The length of the sample.

        Raises:
            ArgumentError: If `vec` is not of type Vector.
            ArgumentError: If `len_output` is not inz.
            ArgumentError: If `len_output` is smaller 1.

        Returns:
            Vector: The resulting vector from the sample.
        """
        assertion.assert_type(vec, Vector, ArgumentError, code=ArgumentCodes.NOT_VECTOR)
        assertion.assert_types(len_output, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_above(len_output, 0, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        return Vector(random.sample(list(vec.get_data()), len_output))

    @override
    def get_dimension(self) -> int:
        return len(self._data)

    @deprecated("Use vector[i] instead.")
    def get_component(self, index: Int) -> float:
        assertion.assert_types(index, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(index, 0, self.get_dimension() - 1, ArgumentError,
                               code=ArgumentCodes.OUT_OF_RANGE)
        return float(self._data[index][0])

    @deprecated("Use vector[i] = value instead.")
    def set_component(self, index: Int, value: Number) -> None:
        super().set_component(index, 1, value)

    def set_data(self, new: Lists) -> None:
        assertion.assert_types(new, TypesTuple.LISTS.value, ArgumentError,
                               code=ArgumentCodes.NOT_LISTS)
        assertion.assert_types_list(new, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        new: list = list(new)
        to_data: list = list()
        for a in new:
            to_data.append([a])
        self._data = np.array(to_data)

    def get_data(self) -> np.ndarray:
        n: np.ndarray = self.get_components()
        n = n.reshape(self.get_dimension())
        return n

    def length(self) -> float:
        total: float = 0
        for entry in self._data:
            total += entry[0] * entry[0]
        return rnd(total ** (1/2))

    def rand_choice(self, heat: Number = 0) -> int:
        """
        Returns the index of a randomly chosen element of the list.

        Renvoie l'indice d'un élément de la liste choisi au hasard.

        - if heat = -1: Chooses nearly always the max
        - if heat =  0: Uses the probability.
        - if heat =  1: Randomises the choice even more.

        Args:
            heat (Number): Changes the selection procedure.

        Returns:
            index of choice (int): The chosen Elements index.

        Raises:
            ArgumentError: If heat is not a number.
            ArgumentError: If heat is not in [-1; 1].
        """
        assertion.assert_types(heat, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        assertion.assert_range(heat, -1, 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        heat = float(heat)
        heat = np.clip(heat, -1, 1)
        probs = self.get_data()

        normalise = False

        for value in probs:
            if value >= 1:
                normalise: bool = True
                break

        if normalise or sum(list(probs)) != 1:
            sum_ = sum(list(probs))
            for i in range(len(probs)):
                probs[i] = rnd(float(probs[i] / sum_))

        if heat == -1:
            return int(np.argmax(probs))
        elif heat == 0:
            return int(np.random.choice(len(probs), p=probs))

        temp = 1 / (1 - heat) if heat < 0 else 1 + 4 * heat

        scaled_probs = np.exp(np.log(probs + 1e-9) / temp)
        scaled_probs /= np.sum(scaled_probs)

        return int(np.random.choice(len(probs), p=scaled_probs))

    @override
    def max(self) -> float:
        max_: float = float(self[0])
        for val in self:
            max_ = max(max_, float(val))
        return float(max_)

    @override
    def min(self) -> float:
        min_: float = float(self[0])
        for val in self:
            min_ = min(min_, float(val))
        return float(min_)

    @override
    def sum(self) -> float:
        sum_: float = 0
        for val in self:
            sum_ += val
        return rnd(sum_)

    @override
    def where(self, m: Union[AllLists, Self], for_false: any = -1) -> Self:
        """
        Creates a vector whose values are defined by the arg vector / list, which allows the values from self at a position.

        Crée un vecteur dont les valeurs sont définies par l'arg Vecteur, qui autorise les valeurs de self à une position.

        Args:
            m (Union[AllLists, Self]): The vector / list which allows
            for_false (any): default = -1. The value for non allowed values.

        Returns:
            Allowed vector (Vector): The vector with only allowed values.

        Raises:
            ArgumentError: If m is not a vector / list
            ArgumentError: If m has not the same dimensions as self.
            ArgumentError: If m has non number or boolean values.
        """
        assertion.assert_types(m, (*TypesTuple.LISTS.value, *TypesTuple.TUPLE.value, Matrix), ArgumentError,
                               code=ArgumentCodes.NOT_LISTS_TUPLE)
        if isinstance(m, Matrix) and not isinstance(m, Vector):
            m = m.get_components()[0]
        if isinstance(m, Vector):
            m = m.get_data()
        assertion.assert_equals(len(m), self.get_dimension(), ArgumentError, code=ArgumentCodes.NOT_EQUAL)
        tester: list = list()
        for i, value in enumerate(m):
            assertion.assert_types(value, (*TypesTuple.NUMBER.value, bool), ArgumentError,
                                   code=ArgumentCodes.NOT_INT_BOOl)
            if isinstance(value, (np.integer, np.floating)):
                tester.append(value > 0)
                continue
            tester.append(bool(value))

        result: Vector = Vector(dimension=self.get_dimension())
        for i, value in enumerate(self):
            result[i] = value if tester[i] else for_false

        return result

    def randomise(self, amount_of_randomising: int = 1) -> None:
        """
        Randomises the data of the vector n=1 amount of times.

        Randomise les données du vecteur n=1 nombre de fois.

        Args:
            amount_of_randomising (int): The amount of times the randomise function should be applied.

        Raises:
            ArgumentError: If `amount_of_randomising` is not inz.
            ArgumentError: If `amount_of_randomising` is smaller 1.

        Returns:
            Vector: The resulting vector from the sample.
        """
        assertion.assert_types(amount_of_randomising, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_above(amount_of_randomising, 0, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        for _ in range(amount_of_randomising):
            self.set_data(random.sample(list(self.get_data()), len(self._data)))

    @override
    def __add__(self, other: Matrix) -> Self:
        added: Matrix = super().__add__(other)
        return Vector.from_matrix(added)

    @override
    def __radd__(self, other: Matrix) -> Self:
        added: Matrix = super().__radd__(other)
        return Vector.from_matrix(added)

    @override
    def __sub__(self, other: Matrix) -> Self:
        sub: Matrix = super().__sub__(other)
        return Vector.from_matrix(sub)

    @override
    def __rsub__(self, other: Matrix) -> Self:
        sub: Matrix = super().__rsub__(other)
        return Vector.from_matrix(sub)

    @override
    def __mul__(self, other: Union[Self, *TypesTuple.NUMBER.value]) -> Union[Self, float]:
        assertion.assert_types(other, (Vector, *TypesTuple.NUMBER.value), MathError, code=MathCodes.NOT_VECTOR_NUMBER)
        if isinstance(other, Vector):
            assertion.assert_equals(self.get_dimension(), other.get_dimension(), MathError,
                                    code=MathCodes.UNFIT_DIMENSIONS)
            a: np.ndarray = self.get_components()
            b: np.ndarray = other.get_components()
            c: np.ndarray = a * b
            d: float | int = 0
            if len(c) > 0 and isinstance(c[0], TypesTuple.LISTS.value):
                for sub in c:
                    d += sub[0]
            elif len(c) > 0 and isinstance(c[0], TypesTuple.NUMBER.value):
                print(c)
                for n in c:
                    d += n
            return rnd(d)
        vector: np.ndarray = self.get_data()
        return Vector(list(vector * other), self.get_dimension())

    @override
    def __rmul__(self, other: Union[Matrix, Self, *TypesTuple.NUMBER.value]) -> Self:
        if isinstance(other, (Vector, *TypesTuple.NUMBER.value)):
            return self * other
        multiple: Matrix = super().__rmul__(other)
        return Vector.from_matrix(multiple)

    @override
    def __imul__(self, other: Union[Matrix, *TypesTuple.NUMBER.value]) -> Self:
        if isinstance(other, Vector):
            raise MathError(MathCodes.VECTOR)
        return super().__imul__(other)

    @override
    def __truediv__(self, other: Number) -> Self:
        div: Matrix = super().__truediv__(other)
        return Vector.from_matrix(div)

    @override
    def __pow__(self, power, modulo=None):
        raise MathError(MathCodes.NOT_DEFINED, msg="This Action is not defined.")

    @override
    def __str__(self) -> str:
        return f"{self.get_data()}"

    @override
    def __repr__(self) -> str:
        return f"Vector at {hex(id(self))} with:\n {self.get_data()}"

    @override
    def copy(self) -> Self:
        return Vector.from_matrix(super().copy())

    @override
    def __iter__(self) -> iter:
        return iter(list(self.get_data()))

    @override
    def __getitem__(self, item: Int) -> Number:
        assertion.assert_types(item, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        if item >= 0:
            assertion.assert_range(item, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
            return float(self._data[item][0])
        else:
            assertion.assert_range(len(self._data) + item, 0, len(self._data) - 1, ArgumentError,
                                   code=ArgumentCodes.OUT_OF_RANGE)
            return float(self._data[len(self._data) + item][0])

    def __setitem__(self, index: Int, value: Number) -> None:
        assertion.assert_types(index, TypesTuple.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(value, TypesTuple.NUMBER.value, ArgumentError, code=ArgumentCodes.NOT_NUMBER)
        if index >= 0:
            assertion.assert_range(index, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
            self._data[index] = [value]
        else:
            assertion.assert_range(len(self._data) + index, 0, len(self._data) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
            self._data[len(self._data) + index] = [value]

    def __len__(self) -> int:
        return self.get_dimension()
