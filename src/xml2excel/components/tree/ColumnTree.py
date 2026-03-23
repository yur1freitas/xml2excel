from typing import Iterable, cast

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox, QVBoxLayout

from xml2excel.components import App
from xml2excel.components.Collapsible import Collapsible
from xml2excel.components.tree.BaseColumnModel import BaseColumnModel
from xml2excel.components.tree.ColumnTreeLeaf import ColumnTreeLeaf
from xml2excel.components.tree.PropagationDirection import PropagationDirection
from xml2excel.components.tree.PropagationMode import PropagationMode
from xml2excel.utils.flatdict import flatdict
from xml2excel.utils.xml2flatdict import XMLData


class ColumnTree(BaseColumnModel):
    def __init__(
        self,
        parent=None,
        *,
        id: str,
        path: str | None = None,
        root: BaseColumnModel | None = None,
        data: Iterable[XMLData] | None = None,
        checked: bool = True,
    ):
        super().__init__(parent=parent)

        self.app = App.instance()
        self.setObjectName(self.__class__.__name__)

        self._id = id
        self._path = f'{path}:{id}' if path else id
        self._root = root
        self._data = data
        self._propagation_mode = PropagationMode.ALL

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(8, 8, 0, 8)

        self._checkbox = QCheckBox()
        self._checkbox.setChecked(checked)
        self._checkbox.setFixedSize(24, 24)
        self._checkbox.stateChanged.connect(self.__onCheckboxChanged)

        self._collapsible = Collapsible(label=id)
        self._collapsible.expanded.connect(self.__createChildrens)
        self._collapsible.trigger.addWidget(self._checkbox)

        self._layout.addWidget(self._collapsible)

        if self.root is not None:
            self.root.propagating.connect(self.__onPropagating)

        if not checked:
            self.app.config.ignore_columns.add(self._path)

    @property
    def id(self) -> str:
        return self._id

    @property
    def path(self) -> str:
        return self._path

    @property
    def root(self) -> BaseColumnModel | None:
        return self._root

    def isChecked(self) -> bool:
        return self._checkbox.isChecked()

    def setChecked(self, checked: bool) -> None:
        self._checkbox.setChecked(checked)

    @property
    def propagationMode(self) -> PropagationMode:
        return self._propagation_mode

    def setPropagationMode(self, mode: PropagationMode):
        self._propagation_mode = mode

    def resetPropagationMode(self) -> None:
        self._propagation_mode = PropagationMode.ALL

    def propagate(self, direction: PropagationDirection, checked: bool) -> None:
        match direction:
            case PropagationDirection.UP:
                if (
                    self.root is not None
                    and self._propagation_mode != PropagationMode.CHILDREN
                ):
                    self.root.setPropagationMode(PropagationMode.ROOT)
                    self.root.setChecked(checked)
                    self.root.resetPropagationMode()
            case PropagationDirection.DOWN:
                if self._propagation_mode != PropagationMode.ROOT:
                    self.propagating.emit(direction, checked)

    @Slot(int)
    def __onCheckboxChanged(self, *args):
        store = self.app.config.ignore_columns

        if self.isChecked():
            if self.path in store:
                store.remove(self.path)

            self.propagate(PropagationDirection.UP, True)
            self.propagate(PropagationDirection.DOWN, True)
        else:
            store.add(self.path)

            self.propagate(PropagationDirection.DOWN, False)

    @Slot(PropagationDirection, bool)
    def __onPropagating(
        self,
        direction: PropagationDirection,
        checked: bool,
    ) -> None:
        self.setChecked(checked)

    def __createChildrens(self) -> None:
        if self._data is None:
            return

        visited = set[str]()

        store = self.app.config.ignore_columns

        if store is not None and self.path in store:
            store.remove(self.path)

        for item in self._data:
            for key, value in item.dict().items():
                if key in visited:
                    continue

                if isinstance(value, flatdict):
                    data = [
                        source[key]
                        for source in cast(Iterable[XMLData], self._data)
                        if key in source
                    ]

                    subtree = ColumnTree(
                        id=key,
                        path=self.path,
                        root=self,
                        data=data,
                        checked=self.isChecked(),
                    )

                    self._collapsible.content.insertWidget(0, subtree)
                else:
                    leaf = ColumnTreeLeaf(
                        id=key,
                        path=self.path,
                        root=self,
                        checked=self.isChecked(),
                    )

                    self._collapsible.content.addWidget(leaf)

                visited.add(key)

            self._data = None
