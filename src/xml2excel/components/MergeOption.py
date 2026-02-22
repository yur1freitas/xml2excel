from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from xml2excel.components import App


class MergeOption(QCheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.instance()

        self.setChecked(self.app.config.merge)
        self.stateChanged.connect(self._on_check)

    @Slot()
    def _on_check(self):
        self.app.config.merge = self.isChecked()
