from typing import Callable

from xml2excel.aliases import AnyPathTuple, DataFrameTuple
from xml2excel.utils.var import Variable


class Store:
    _data: Variable[DataFrameTuple | None]
    _filepaths: Variable[AnyPathTuple | None]
    _pending: Variable[bool]

    def __init__(self):
        self._data = Variable(value=None)
        self._filepaths = Variable(value=None)
        self._pending = Variable(False)

    @property
    def data(self) -> DataFrameTuple | None:
        return self._data.get()

    @property
    def pending(self) -> bool:
        return self._pending.get()

    @property
    def filepaths(self) -> AnyPathTuple | None:
        return self._filepaths.get()

    @data.setter
    def data(self, value: DataFrameTuple | None):
        self._data.set(value)

    @filepaths.setter
    def filepaths(self, value: AnyPathTuple | None):
        self._filepaths.set(value)

    @pending.setter
    def pending(self, value: bool):
        self._pending.set(value)

    def trace(self, attr: str, callback: Callable):
        match attr:
            case 'data':
                self._data.trace(callback)
            case 'filepaths':
                self._filepaths.trace(callback)
            case 'pending':
                self._pending.trace(callback)
            case _:
                raise ValueError(f'Esse atributo não existe: {attr}')
