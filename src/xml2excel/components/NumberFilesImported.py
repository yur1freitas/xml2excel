from PySide6.QtWidgets import QLabel

from xml2excel.aliases import AnyPathTuple
from xml2excel.manager.context import GlobalContext


class NumberFilesImported(QLabel):
    DEFAULT_MESSAGE = 'Nº de arquivos importados: 0'

    def __init__(self, ctx: GlobalContext, **kwargs):
        super().__init__(text=self.DEFAULT_MESSAGE, **kwargs)

        self._ctx = ctx
        self._ctx.store.trace('filepaths', self._update_text)

    def _update_text(self, filepaths: AnyPathTuple):
        if filepaths is not None:
            amount = len(filepaths)
            self.setText(f'Nº de arquivos importados: {amount}')
        else:
            self.setText(self.DEFAULT_MESSAGE)
