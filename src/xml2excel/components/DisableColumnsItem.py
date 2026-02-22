from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from xml2excel.manager.context import GlobalContext


class DisableColumnsItem(QCheckBox):
    def __init__(self, ctx: GlobalContext, **kwargs):
        super().__init__(**kwargs)

        self._ctx = ctx

        self.setChecked(True)
        self.stateChanged.connect(self._on_check)

    @Slot()
    def _on_check(self):
        config = self._ctx.config

        if config.ignore_columns is None:
            return

        column = self.text()

        if column in config.ignore_columns:
            config.ignore_columns.remove(column)
        else:
            config.ignore_columns.append(column)
