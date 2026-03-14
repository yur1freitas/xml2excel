from enum import StrEnum

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget

from xml2excel.components import App
from xml2excel.utils.flatdict2excel import ColumnPrefixStyle


class Values(StrEnum):
    NONE = 'Nenhum'
    PARENT = 'Uma Tag Pai'
    HIERARCHICAL = 'Todas as Tags Pai'


class PrefixOption(QWidget):
    VALUES: list[str] = [
        Values.NONE,
        Values.PARENT,
        Values.HIERARCHICAL,
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.instance()

        self._layout = QVBoxLayout(self)

        self._label = QLabel(self, text='Modo de Prefixo:')

        self._combobox = QComboBox(self)
        self._combobox.addItems(self.VALUES)
        self._combobox.setCurrentIndex(self.app.config.prefix_mode)
        self._combobox.currentTextChanged.connect(self._on_select)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._combobox)

    @Slot(str)
    def _on_select(self, value: str) -> None:
        config = self.app.config

        match value:
            case Values.NONE:
                config.prefix_mode = ColumnPrefixStyle.NONE
            case Values.PARENT:
                config.prefix_mode = ColumnPrefixStyle.PARENT
            case Values.HIERARCHICAL:
                config.prefix_mode = ColumnPrefixStyle.HIERARCHICAL
