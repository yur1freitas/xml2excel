from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from xml2excel.components import App


class RecursiveOption(QCheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.instance()

        self.setChecked(self.app.config.recursive)
        self.checkStateChanged.connect(self._on_check)

    @Slot()
    def _on_check(self):
        self.app.config.recursive = self.isChecked()
