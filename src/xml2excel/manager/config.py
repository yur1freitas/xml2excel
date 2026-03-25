from typing import Callable

from xml2excel.utils.flatdict2excel import ColumnPrefixStyle
from xml2excel.utils.var import Variable


class Config:
    _merge: Variable[bool]
    _recursive: Variable[bool]
    _index_column: Variable[bool]
    _ignore_columns: Variable[set[str]]
    _column_prefix_style: Variable[ColumnPrefixStyle]

    def __init__(self):
        self._merge = Variable(True)
        self._recursive = Variable(False)
        self._index_column = Variable(False)
        self._ignore_columns = Variable(set())
        self._column_prefix_style = Variable(ColumnPrefixStyle.HIERARCHICAL)

    @property
    def merge(self) -> bool:
        return self._merge.get()

    @property
    def index_column(self) -> bool:
        return self._index_column.get()

    @property
    def recursive(self) -> bool:
        return self._recursive.get()

    @property
    def column_prefix_style(self) -> ColumnPrefixStyle:
        return self._column_prefix_style.get()

    @property
    def ignore_columns(self) -> set[str]:
        return self._ignore_columns.get()

    @merge.setter
    def merge(self, value: bool) -> None:
        self._merge.set(value)

    @index_column.setter
    def index_column(self, value: bool) -> None:
        self._index_column.set(value)

    @recursive.setter
    def recursive(self, value: bool) -> None:
        self._recursive.set(value)

    @column_prefix_style.setter
    def column_prefix_style(self, value: ColumnPrefixStyle) -> None:
        self._column_prefix_style.set(value)

    @ignore_columns.setter
    def ignore_columns(self, value: set[str]) -> None:
        self._ignore_columns.set(value)

    def trace(self, attr: str, callback: Callable) -> None:
        match attr:
            case 'merge':
                self._merge.trace(callback)
            case 'recursive':
                self._recursive.trace(callback)
            case 'index_column':
                self._index_column.trace(callback)
            case 'ignore_columns':
                self._ignore_columns.trace(callback)
            case 'column_prefix_style':
                self._column_prefix_style.trace(callback)
            case _:
                raise ValueError(f'Esse atributo não existe: {attr}')
