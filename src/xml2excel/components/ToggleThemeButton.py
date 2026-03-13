from PySide6.QtWidgets import QPushButton, QWidget

from xml2excel.components import App
from xml2excel.utils.path import resource_path


class ToggleThemeButton(QPushButton):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName(self.__class__.__name__)
        self.setFixedSize(32, 32)

        self.app = App.instance()

        self.clicked.connect(self._toggle_theme)

    def _toggle_theme(self):
        self.app.theme.toggle()

        self.app.load_stylesheet(resource_path('styles/global.qss'))
