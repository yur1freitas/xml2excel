from customtkinter import CTkLabel

from xml2excel.aliases import AnyPathTuple
from xml2excel.manager.context import GlobalContext


class NumberFilesImported(CTkLabel):
    def __init__(self, master, ctx: GlobalContext, **kwargs):
        super().__init__(master, text='', **kwargs)

        self._ctx = ctx
        self._ctx.store.trace('filepaths', self._update_text)

    def _update_text(self, filepaths: AnyPathTuple):
        if filepaths is not None:
            amount = len(filepaths)
            self.configure(text=f'Nº de arquivos importados: {amount}')
