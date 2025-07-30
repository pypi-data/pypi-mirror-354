from typing import Union, TypeVar, Iterable
import numpy as np

T = TypeVar('T')

Int = Union[int, np.integer]
Float = Union[float, np.floating]
Number = Union[Int, Float]
List: type = Union[list[T]]
Tuple: type = Union[tuple[T]]
Itera: type = Union[Iterable[T]]
NdArray: type = Union[np.ndarray]
Lists = Union[list[T], np.ndarray]
AllLists = Union[list[T], tuple[T, ...], np.ndarray, Iterable[T]]
Lists_2D = Union[list[list[T]], np.ndarray, Iterable[Iterable[T]]]
