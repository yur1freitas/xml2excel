from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from xml2excel.components import App
from xml2excel.components.tree.BaseColumnModel import BaseColumnModel
from xml2excel.components.tree.ColumnTree import ColumnTree
from xml2excel.components.tree.PropagationDirection import PropagationDirection
from xml2excel.components.tree.PropagationMode import PropagationMode


class ColumnTreeRoot(BaseColumnModel):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.app = App.instance()
        self.setObjectName(self.__class__.__name__)

        self._id = 'root'
        self._path = self._id
        self._root = None
        self._data = None
        self._propagation_mode = PropagationMode.ALL

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(12)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(text='Colunas Habilitadas: ')

        self._checkbox = QCheckBox('Raiz')
        self._checkbox.setChecked(True)
        self._checkbox.stateChanged.connect(self.__onCheckboxChanged)

        self._scrollarea = QScrollArea()
        self._scrollarea.setWidgetResizable(True)

        self._scrollarea_widget = QWidget()
        self._scrollarea.setWidget(self._scrollarea_widget)

        self._scrollarea_layout = QVBoxLayout(self._scrollarea_widget)
        self._scrollarea_layout.setSpacing(0)
        self._scrollarea_layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._checkbox)
        self._layout.addWidget(self._scrollarea)

        self.app.store.trace('pending', self.__onDataChange)

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
        if direction == PropagationDirection.DOWN:
            if self._propagation_mode != PropagationMode.ROOT:
                self.propagating.emit(direction, checked)

    @Slot(int)
    def __onCheckboxChanged(self, *args):
        if self.isChecked():
            self.propagate(PropagationDirection.DOWN, True)
        else:
            self.propagate(PropagationDirection.DOWN, False)

    @Slot(PropagationDirection, bool)
    def __onPropagating(
        self,
        direction: PropagationDirection,
        checked: bool,
    ) -> None:
        self.setChecked(checked)

    def __reset(self):
        self.app.config.ignore_columns = set()

        for tree in self._scrollarea_widget.children():
            if isinstance(tree, BaseColumnModel):
                tree.setParent(None)

    def __onDataChange(self, pending: bool) -> None:
        self.__reset()

        if pending:
            return

        data = self.app.store.data

        visited = set[str]()

        for item in data:
            for i, key in enumerate(item.dict().keys()):
                if key in visited:
                    continue

                idata = [source[key] for source in data if key in source]

                tree = ColumnTree(id=key, root=self, data=idata)

                self._scrollarea_layout.addWidget(
                    tree,
                    alignment=Qt.AlignmentFlag.AlignTop,
                )
                visited.add(key)
