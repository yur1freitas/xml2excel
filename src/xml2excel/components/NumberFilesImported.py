from PySide6.QtWidgets import QLabel

from xml2excel.aliases import AnyPathTuple
from xml2excel.components import App


class NumberFilesImported(QLabel):
    DEFAULT_MESSAGE = 'Nº de arquivos importados: 0'

    def __init__(self, **kwargs):
        super().__init__(text=self.DEFAULT_MESSAGE, **kwargs)

        self.app = App.instance()
        self.app.store.trace('filepaths', self._update_text)

    def _update_text(self, filepaths: AnyPathTuple):
        if filepaths is not None:
            amount = len(filepaths)
            self.setText(f'Nº de arquivos importados: {amount}')
        else:
            self.setText(self.DEFAULT_MESSAGE)
