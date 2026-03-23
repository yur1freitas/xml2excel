from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QWidget

from xml2excel.components.tree.PropagationDirection import PropagationDirection
from xml2excel.components.tree.PropagationMode import PropagationMode


class BaseColumnModel(QFrame):
    propagating = Signal(PropagationDirection, bool)

    def __init__(
        self,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

    @property
    def id(self) -> str:
        raise NotImplementedError(
            'id() precisa ser implementando em uma subclasse'
        )

    @property
    def path(self) -> str:
        raise NotImplementedError(
            'path() precisa ser implementando em uma subclasse'
        )

    @property
    def root(self) -> Union['BaseColumnModel', None]:
        raise NotImplementedError(
            'root() precisa ser implementando em uma subclasse'
        )

    def isChecked(self) -> bool:
        raise NotImplementedError(
            'isChecked() precisa ser implementando em uma subclasse'
        )

    def setChecked(self, checked: bool) -> None:
        raise NotImplementedError(
            'isChecked() precisa ser implementando em uma subclasse'
        )

    @property
    def propagationMode(self) -> PropagationMode:
        raise NotImplementedError(
            'propagationMode() precisa ser implementando em uma subclasse'
        )

    def setPropagationMode(self, mode: PropagationMode):
        raise NotImplementedError(
            'setPropagationMode() precisa ser implementando em uma subclasse'
        )

    def resetPropagationMode(self) -> None:
        raise NotImplementedError(
            'resetPropagationMode() precisa ser implementando em uma subclasse'
        )

    def propagate(self, direction: PropagationDirection, checked: bool) -> None:
        raise NotImplementedError(
            'propagate() precisa ser implementando em uma subclasse'
        )
