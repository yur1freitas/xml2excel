from PySide6.QtCore import Signal, SignalInstance
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class CollapsibleTrigger(QFrame):
    clicked = Signal()

    def __init__(self, parent=None, *, label: str):
        super().__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.setProperty('expanded', False)
        self.setMinimumHeight(32)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        self._icon = QFrame()
        self._icon.setObjectName('Icon')
        self._icon.setFixedSize(16, 16)

        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(label)
        self._label.setMaximumHeight(24)

        self._layout.addWidget(self._icon)
        self._layout.addWidget(self._label)

    @property
    def label(self) -> QLabel:
        return self._label

    def mousePressEvent(self, *args):
        self.clicked.emit()

    def addWidget(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)

    def insertWidget(self, index: int, widget: QWidget) -> None:
        self._layout.insertWidget(index, widget)

    def setExpandedProperty(self, value: bool) -> None:
        self.setProperty('expanded', value)
        self._update_icon_style()

    def _update_icon_style(self) -> None:
        self._icon.style().unpolish(self._icon)
        self._icon.style().polish(self._icon)
        self._icon.update()


class CollapsibleContent(QFrame):
    expanded = Signal()
    collapsed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.setHidden(True)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

    def expand(self) -> None:
        self.setVisible(True)
        self.expanded.emit()

    def collapse(self) -> None:
        self.setHidden(True)
        self.collapsed.emit()

    def toggle(self) -> None:
        self.expand() if self.isHidden() else self.collapse()

    def addWidget(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)

    def insertWidget(self, index: int, widget: QWidget) -> None:
        self._layout.insertWidget(index, widget)


class Collapsible(QWidget):
    def __init__(self, parent=None, *, label: str):
        super().__init__(parent)

        self.setObjectName(self.__class__.__name__)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._trigger = CollapsibleTrigger(label=label)
        self._content = CollapsibleContent()

        self._trigger.clicked.connect(self.toggle)

        self._layout.addWidget(self._trigger)
        self._layout.addWidget(self._content)

    @property
    def is_expanded(self) -> bool:
        return self._content.isHidden()

    @property
    def is_collapsed(self) -> bool:
        return self._content.isVisible()

    @property
    def label(self) -> str:
        return self._trigger._label.text()

    @property
    def trigger(self) -> CollapsibleTrigger:
        return self._trigger

    @property
    def content(self) -> CollapsibleContent:
        return self._content

    @property
    def expanded(self) -> SignalInstance:
        return self._content.expanded

    @property
    def collapsed(self) -> SignalInstance:
        return self._content.collapsed

    @property
    def expand(self) -> None:
        self._content.expand()

    def collapse(self) -> None:
        self._content.collapse()

    def toggle(self) -> None:
        self._trigger.setExpandedProperty(self.is_expanded)
        self._content.toggle()
