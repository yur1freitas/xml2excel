from tkinter.filedialog import askdirectory

from customtkinter import CTkBaseClass

from xml2excel.commands.import_files import ImportFilesInput, import_files
from xml2excel.manager.context import GlobalContext

from .Button import Button


class ImportFilesButton(Button):
    DIALOG_TITLE = 'Importar XMLs'

    def __init__(self, master: CTkBaseClass, ctx: GlobalContext, **kwargs):
        self._ctx = ctx

        super().__init__(master, command=self._command, **kwargs)

    def _command(self) -> None:
        store = self._ctx.store
        dirpath = askdirectory(title=self.DIALOG_TITLE)

        if dirpath:
            output = import_files(
                ImportFilesInput(
                    path=dirpath,
                    prefix_mode=self._ctx.config.prefix_mode,
                    recursive=self._ctx.config.recursive,
                )
            )

            store.data = output.data
            store.filepaths = output.filepaths
