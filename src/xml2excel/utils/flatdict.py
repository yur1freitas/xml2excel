from collections.abc import ItemsView, KeysView, MutableMapping, ValuesView
from typing import Any, Generic, Iterator, TypeVar, Union, cast

V = TypeVar('V')


class flatdict(MutableMapping, Generic[V]):
    """
    Inspirado por https://github.com/gmr/flatdict
    """

    __slots__ = ('_value', '_delimiter')

    def __init__(
        self,
        value: Union[dict, 'flatdict', None] = None,
        delimiter: str = ':',
    ) -> None:
        super().__init__()

        self._value: dict[str, V] = {}
        self._delimiter: str = delimiter

        if value:
            self._value.update(value)

    def __len__(self) -> int:
        return len(self.keys())

    def __iter__(self) -> Iterator[str]:
        yield from self.iterkeys()

    def __delitem__(self, key: str | list[str] | tuple[str]) -> None:
        path = key.split(self._delimiter) if isinstance(key, str) else key

        val = cast(Any, self._value)

        steps, last_key = path[:-1], path[-1]

        for step in steps:
            val = val[step]

        del val[last_key]

    def __getitem__(self, key: str | list[str] | tuple[str]) -> V:
        path = key.split(self._delimiter) if isinstance(key, str) else key

        val = cast(Any, self._value)

        for step in path:
            val = val[step]

        return val

    def __setitem__(self, key: str | list[str] | tuple[str], value: V) -> None:
        path = key.split(self._delimiter) if isinstance(key, str) else key

        val = cast(Any, self._value)

        steps, last_key = path[:-1], path[-1]

        for step in steps:
            val = val[step]

        val[last_key] = value

    def dict(self) -> dict[str, V]:
        return dict(self._value)

    def keys(self) -> KeysView[str]:
        return KeysView(list(self.iterkeys()))

    def values(self) -> ValuesView[V]:
        return ValuesView(list(self.itervalues()))

    def items(self) -> ItemsView[str, V]:
        return ItemsView(list(self.iteritems()))

    def iterkeys(self) -> Iterator[str]:
        for k in self._value:
            v = self._value[k]

            if isinstance(v, (dict, flatdict)):
                for subk in v:
                    yield f'{k}{self._delimiter}{subk}'
            else:
                yield k

    def itervalues(self) -> Iterator[V]:
        for k in self.iterkeys():
            yield self.__getitem__(k)

    def iteritems(self) -> Iterator[tuple[str, V]]:
        for k in self.iterkeys():
            yield k, self.__getitem__(k)

    def update(self, other: Any = None, **kwargs: Any) -> None:
        value = dict(other or kwargs)

        for k in value:
            self.__setitem__(k, value[k])
