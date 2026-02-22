from typing import cast

from PySide6.QtWidgets import QApplication

from xml2excel.manager.config import Config
from xml2excel.manager.store import Store


class App(QApplication):
    config = Config()
    store = Store()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def instance() -> 'App':
        return cast(App, QApplication.instance())
