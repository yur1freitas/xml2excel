from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from xml2excel.components import App
from xml2excel.components.tree.BaseColumnModel import BaseColumnModel
from xml2excel.components.tree.PropagationDirection import PropagationDirection
from xml2excel.components.tree.PropagationMode import PropagationMode


class ColumnTreeLeaf(BaseColumnModel):
    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        id: str,
        path: str | None,
        root: BaseColumnModel | None,
        checked: bool = True,
    ):
        super().__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.app = App.instance()

        self._id = id
        self._path = f'{path}:{id}' if path else id
        self._root = root
        self._propagation_mode = PropagationMode.ALL

        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(8, 8, 0, 8)

        self._checkbox = QCheckBox()
        self._checkbox.setChecked(checked)
        self._checkbox.setFixedSize(24, 24)
        self._checkbox.stateChanged.connect(self.__onCheckboxChanged)

        self._label = QLabel(id)
        self._label.setMaximumHeight(24)
        self._label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        self._layout.addWidget(self._checkbox)
        self._layout.addWidget(self._label)

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
        if (
            direction == PropagationDirection.UP
            and checked
            and self.root is not None
            and self._propagation_mode != PropagationMode.CHILDREN
        ):
            self.root.setPropagationMode(PropagationMode.ROOT)
            self.root.setChecked(checked)
            self.root.resetPropagationMode()

    @Slot(int)
    def __onCheckboxChanged(self, checkState: Qt.CheckState):
        store = self.app.config.ignore_columns

        if self.isChecked():
            if self.path in store:
                store.remove(self.path)

            self.propagate(PropagationDirection.UP, True)
        else:
            store.add(self.path)

    @Slot(PropagationDirection, bool)
    def __onPropagating(
        self,
        direction: PropagationDirection,
        checked: bool,
    ) -> None:
        self.setChecked(checked)
