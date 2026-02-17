from typing import Callable, Generic, Self, TypeAlias, TypeVar

T = TypeVar('T')

Listener: TypeAlias = Callable[[T], None]


class Variable(Generic[T]):
    def __init__(self, value: T, *, max_listeners: int = 5):
        self._value: T = value
        self._listeners = set[Listener]()

        self._max_listeners: int = max_listeners
        self._notifications_enabled: bool = True

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value
        self._emit()

    def trace(self, callback: Listener) -> Self:
        self._check_capacity()
        self._listeners.add(callback)

        return self

    def untrace(self, callback: Callable) -> Self:
        self._listeners.remove(callback)

        return self

    def untrace_all(self) -> None:
        self._listeners.clear()

    def _emit(self):
        for listener in self._listeners:
            try:
                listener(self._value)
            except Exception as exc:
                print(f'[Variable] Um listener lançou uma exceção: {exc}')

    def _check_capacity(self) -> None:
        if len(self._listeners) >= self._max_listeners:
            raise ValueError(
                f'O número de ouvintes excedeu o limite máximo ({self._max_listeners}).'
            )

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f'<{cls_name} value={self._value!r} listeners={len(self._listeners)}>'
