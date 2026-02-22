from enum import StrEnum

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget

from xml2excel.manager.context import GlobalContext
from xml2excel.utils.flatten_xml import PrefixMode


class Values(StrEnum):
    NONE = 'Nenhum'
    CLOSEST = 'Uma Tag Pai'
    ALL = 'Todas as Tags Pai'


class PrefixOption(QWidget):
    VALUES: list[str] = [
        Values.NONE,
        Values.CLOSEST,
        Values.ALL,
    ]

    def __init__(self, ctx: GlobalContext, **kwargs):
        super().__init__(**kwargs)

        self._ctx = ctx

        self._layout = QVBoxLayout(self)

        self._label = QLabel(self, text='Modo de Prefixo:')

        self._combobox = QComboBox(self)
        self._combobox.addItems(self.VALUES)
        self._combobox.setCurrentIndex(self._ctx.config.prefix_mode)
        self._combobox.currentTextChanged.connect(self._on_select)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._combobox)

    @Slot(str)
    def _on_select(self, value: str) -> None:
        config = self._ctx.config

        match value:
            case Values.NONE:
                config.prefix_mode = PrefixMode.NONE
            case Values.CLOSEST:
                config.prefix_mode = PrefixMode.CLOSEST
            case Values.ALL:
                config.prefix_mode = PrefixMode.ALL
