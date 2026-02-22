from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QPushButton

from xml2excel.commands.import_files import ImportFilesInput, import_files
from xml2excel.manager.context import GlobalContext


class ImportFilesButton(QPushButton):
    DIALOG_TITLE = 'Importar XMLs'

    def __init__(self, ctx: GlobalContext, **kwargs):
        super().__init__(**kwargs)

        self._ctx = ctx

        self.clicked.connect(self._click)

    @Slot()
    def _click(self) -> None:
        store = self._ctx.store
        config = self._ctx.config

        dirpath = QFileDialog.getExistingDirectory(
            self,
            caption=self.DIALOG_TITLE,
        )

        if dirpath:
            output = import_files(
                ImportFilesInput(
                    path=dirpath,
                    recursive=config.recursive,
                    prefix_mode=config.prefix_mode,
                )
            )

            store.data = output.data
            store.filepaths = output.filepaths
