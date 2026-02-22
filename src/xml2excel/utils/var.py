from typing import Any, Callable, Generic, Self, TypeAlias, TypeVar

from PySide6.QtCore import QObject, Signal

T = TypeVar('T')

Listener: TypeAlias = Callable[[T], None]


class Variable(Generic[T], QObject):
    changed = Signal(Any)

    _listener_count: int = 0

    def __init__(self, value: T, *, max_listeners: int = 5):
        super().__init__()

        self._value: T = value
        self._max_listeners: int = max_listeners

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value
        self.changed.emit(value)

    def trace(self, listener: Listener) -> Self:
        if self._listener_count >= self._max_listeners:
            raise ValueError('O número máximo de ouvintes foi atingido')

        self.changed.connect(listener)
        self._listener_count += 1

        return self

    def untrace(self, listener: Listener) -> Self:
        self.changed.disconnect(listener)
        self._listener_count -= 1

        return self

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f'<{cls_name} value={self._value!r} listeners={self._listener_count}>'
