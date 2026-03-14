from typing import Callable

from xml2excel.utils.flatdict2excel import ColumnPrefixStyle
from xml2excel.utils.var import Variable


class Config:
    _merge: Variable[bool]
    _index: Variable[bool]
    _recursive: Variable[bool]
    _prefix_mode: Variable[ColumnPrefixStyle]
    _ignore_columns: Variable[list[str] | None]

    def __init__(self):
        self._merge = Variable(True)
        self._index = Variable(False)
        self._recursive = Variable(False)
        self._prefix_mode = Variable(ColumnPrefixStyle.HIERARCHICAL)
        self._ignore_columns = Variable(None)

    @property
    def merge(self) -> bool:
        return self._merge.get()

    @property
    def index(self) -> bool:
        return self._index.get()

    @property
    def recursive(self) -> bool:
        return self._recursive.get()

    @property
    def prefix_mode(self) -> ColumnPrefixStyle:
        return self._prefix_mode.get()

    @property
    def ignore_columns(self) -> list[str] | None:
        return self._ignore_columns.get()

    @merge.setter
    def merge(self, value: bool) -> None:
        self._merge.set(value)

    @index.setter
    def index(self, value: bool) -> None:
        self._index.set(value)

    @recursive.setter
    def recursive(self, value: bool) -> None:
        self._recursive.set(value)

    @prefix_mode.setter
    def prefix_mode(self, value: ColumnPrefixStyle) -> None:
        self._prefix_mode.set(value)

    @ignore_columns.setter
    def ignore_columns(self, value: list[str] | None) -> None:
        self._ignore_columns.set(value)

    def trace(self, attr: str, callback: Callable) -> None:
        match attr:
            case 'merge':
                self._merge.trace(callback)
            case 'index':
                self._index.trace(callback)
            case 'recursive':
                self._recursive.trace(callback)
            case 'prefix_mode':
                self._merge.trace(callback)
            case 'ignore_columns':
                self._ignore_columns.trace(callback)
            case _:
                raise ValueError(f'Esse atributo não existe: {attr}')
