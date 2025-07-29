from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar, Union

__all__ = "Sampler", "DataLoader", "Dataset"

T_co = TypeVar("T_co", covariant=True)
U = TypeVar("U")
IdxT = TypeVar("IdxT")

Dataset = Union[Iterable[T_co], Sequence[T_co]]
DataLoader = Iterable[T_co]
Sampler = Iterable[IdxT]
CollateFn = Callable[[Sequence[T_co]], U]
