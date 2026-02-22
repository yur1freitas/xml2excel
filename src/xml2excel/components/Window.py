from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from xml2excel.utils.path import resource_path


class Window(QMainWindow):
    DEFAULT_TITLE = 'Conversor de XML para Excel'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon_path = str(resource_path('assets/xml2excel.png'))
        icon = QIcon(icon_path)

        self.setWindowTitle(self.DEFAULT_TITLE)
        self.setWindowIcon(icon)
