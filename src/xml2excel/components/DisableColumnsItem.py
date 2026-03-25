from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from xml2excel.components import App


class DisableColumnsItem(QCheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.instance()

        self.setChecked(True)
        self.stateChanged.connect(self._on_check)

    @Slot()
    def _on_check(self):
        config = self.app.config
        column = self.text()

        if column in config.ignore_columns:
            config.ignore_columns.remove(column)
        else:
            config.ignore_columns.add(column)
