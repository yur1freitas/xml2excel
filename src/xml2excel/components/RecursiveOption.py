from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from xml2excel.manager.context import GlobalContext


class RecursiveOption(QCheckBox):
    def __init__(self, ctx: GlobalContext, **kwargs):
        super().__init__(**kwargs)

        self._ctx = ctx

        self.setChecked(self._ctx.config.recursive)
        self.checkStateChanged.connect(self._on_check)

    @Slot()
    def _on_check(self):
        self._ctx.config.recursive = self.isChecked()
