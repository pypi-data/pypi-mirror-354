import abc
from collections.abc import Callable, Iterable, Sequence
import contextlib
import functools
from typing import Generic, TypeVar

from . import _types

T_co = TypeVar("T_co", covariant=True)
U = TypeVar("U")
CollateFn = Callable[[Sequence[T_co]], U]


class _BaseFetcher(Generic[T_co, U]):
    def __init__(self, dataset: _types, collate_fn: CollateFn):
        """Init function."""
        self._dataset = dataset
        self._collate_fn = collate_fn

    @abc.abstractmethod
    def fetch(self, possibly_batched_index) -> U:
        """Fetch the batch."""
        raise NotImplementedError


class _IterableFetcher(_BaseFetcher, Generic[T_co, U]):
    def __init__(self, dataset: _types.Dataset[T_co], collate_fn: CollateFn):
        """Init function."""
        super().__init__(dataset, collate_fn)
        self._iter = iter(dataset)
        self._ended = False

    def fetch(self, possibly_batched_index) -> U:
        """Fetch function."""
        if self._ended:
            raise StopIteration

        data = []
        for _ in possibly_batched_index:
            try:
                data.append(next(self._iter))
            except StopIteration:
                self._ended = True
                break

        # If we didn't fetch any data, then we need to stop iteration
        if len(data) == 0:
            raise StopIteration

        return self._collate_fn(data)


class _MapFetcher(_BaseFetcher, Generic[T_co, U]):
    def fetch(self, possibly_batched_index) -> U:
        """Fetch function."""
        if hasattr(self._dataset, "__getitems__") and self._dataset.__getitems__:
            data = self._dataset.__getitems__(possibly_batched_index)
        else:
            data = [self._dataset[idx] for idx in possibly_batched_index]

        return self._collate_fn(data)


@functools.singledispatch
def create_fetcher(dataset: _types.Dataset[T_co], collate_fn: CollateFn) -> _BaseFetcher[T_co, U]:
    """Create fetcher."""
    raise TypeError(f"Unsupported type {type(dataset).__name__}")


with contextlib.suppress(ImportError):
    import torch.utils.data

    @create_fetcher.register(torch.utils.data.IterableDataset)
    def create_torch_iterable_dataset_fetcher(
        dataset: torch.utils.data.IterableDataset[T_co], collate_fn: CollateFn
    ):
        """Create torch iterable dataset fetcher."""
        return create_iterable_fetcher(dataset, collate_fn)

    @create_fetcher.register(torch.utils.data.Dataset)
    def create_torch_dataset_fetcher(
        dataset: torch.utils.data.Dataset[T_co], collate_fn: CollateFn
    ):
        """Create torch dataset fetcher."""
        return create_sequence_fetcher(dataset, collate_fn)


@create_fetcher.register(Sequence)
def create_sequence_fetcher(dataset: Sequence[T_co], collate_fn: CollateFn) -> _MapFetcher:
    """Create sequence fetcher."""
    return _MapFetcher(dataset, collate_fn)


@create_fetcher.register(Iterable)
def create_iterable_fetcher(
    dataset: Iterable[T_co], collate_fn: CollateFn
) -> _IterableFetcher[T_co, U]:
    """Create iterable fetcher."""
    return _IterableFetcher(dataset, collate_fn)
