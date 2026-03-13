from typing import cast

from PySide6.QtWidgets import QApplication

from xml2excel.aliases import AnyPath
from xml2excel.manager.config import Config
from xml2excel.manager.store import Store
from xml2excel.theme import Theme


class App(QApplication):
    config = Config()
    store = Store()
    theme = Theme()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def instance() -> 'App':
        return cast(App, QApplication.instance())

    def load_stylesheet(self, path: AnyPath):
        stylesheet = self.theme.read_stylesheet(path)

        if stylesheet:
            self.setStyleSheet(stylesheet)
